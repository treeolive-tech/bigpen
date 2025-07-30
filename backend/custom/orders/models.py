from core.globals.models import AbstractCreatedAtUpdatedAt
from custom.stock.models import StockItem
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone

User = get_user_model()


class Order(AbstractCreatedAtUpdatedAt):
    """Order model with staff assignment functionality."""

    class Meta:
        ordering = ["-updated_at", "-created_at"]

    ORDER_STATUS_CHOICES = [
        ("pending", "Pending"),
        ("in_progress", "In Progress"),
        ("completed", "Completed"),
        ("cancelled", "Cancelled"),
    ]

    creator = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="orders",
        help_text="User who placed the order",
        null=True,
        blank=True,
    )
    staff_orders_handler = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="assigned_orders",
        help_text="Staff member assigned to work on this order. Only users with the 'ORDERS_HANDLER' group can be assigned orders to handle.",
    )
    status = models.CharField(
        max_length=20,
        choices=ORDER_STATUS_CHOICES,
        default="pending",
        help_text="Current status of the order",
    )

    is_assigned = models.BooleanField(
        default=False,
        help_text="Whether the order is currently assigned to a staff member",
    )

    assigned_at = models.DateTimeField(
        null=True,
        blank=True,
        help_text="When the order was assigned to staff",
    )
    notes = models.TextField(blank=True, help_text="Internal notes about the order")

    @property
    def is_available_for_assignment(self):
        """Check if order is available for staff to pick up."""
        return self.staff_orders_handler is None and self.status == "pending"

    def __str__(self):
        return (
            f"Order #{self.id} by {self.creator.username} - {self.get_status_display()}"
        )

    def clean(self):
        super().clean()

        if self.staff_orders_handler:
            if not (
                self.staff_orders_handler.is_superuser
                or self.staff_orders_handler.groups.filter(
                    name="ORDERS_HANDLER"
                ).exists()
            ):
                raise ValidationError(
                    {"staff_orders_handler": "User must be in the ORDERS_HANDLER group"}
                )

    def save(self, *args, **kwargs):
        self.is_assigned = True if self.staff_orders_handler else False

        if self.staff_orders_handler and not self.assigned_at:
            self.assigned_at = timezone.now()

        if not self.staff_orders_handler and self.assigned_at:
            self.assigned_at = None

        super().save(*args, **kwargs)

    def assign_to_staff_orders_handler(self, staff_user):
        """Assign order to a staff member with the 'ORDERS_HANDLER' group, set assigned_at and set status to in_progress."""
        # Validate the staff user
        if not self.can_be_assigned_to(staff_user):
            raise ValidationError(
                "User must be in the ORDERS_HANDLER group to handle orders."
            )

        if self.staff_orders_handler is not None:
            raise ValidationError("Order is already assigned to someone else")

        self.staff_orders_handler = staff_user
        self.status = "in_progress"
        self.assigned_at = timezone.now()
        self.save()

    def unassign_order(self):
        """Remove assignment from order."""
        self.staff_orders_handler = None
        self.status = "pending"
        self.assigned_at = None
        self.save()

    def can_be_assigned_to(self, staff_user):
        return (
            staff_user.is_superuser
            or staff_user.groups.filter(name="ORDERS_HANDLER").exists()
        )

    def get_total_items(self):
        """Get total number of items in the order."""
        return sum(item.quantity for item in self.items.all())

    def get_total_price(self):
        """Calculate total price of the order."""
        total = 0
        for order_item in self.items.all():
            total += order_item.total_price
        return total


class OrderItem(models.Model):
    """Individual items within an order."""

    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name="items",
    )
    item = models.ForeignKey(
        StockItem,
        on_delete=models.CASCADE,
        help_text="The item being ordered",
    )
    quantity = models.PositiveIntegerField(
        default=1,
        help_text="Quantity of this item in the order",
    )
    price_at_time = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Price of the item when the order was placed (for historical accuracy)",
    )

    class Meta:
        unique_together = ["order", "item"]

    def __str__(self):
        return f"{self.quantity} x {self.item.name}"

    def save(self, *args, **kwargs):
        """Save the current price when creating the order item."""
        if not self.price_at_time and self.item.current_price:
            self.price_at_time = self.item.current_price
        super().save(*args, **kwargs)

    @property
    def total_price(self):
        """Get total price for this order item."""
        price = self.price_at_time or self.item.current_price or 0
        return price * self.quantity
