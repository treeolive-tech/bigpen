import uuid

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone

from app.stock.models import StockItem
from olyv.base.models import AbstractCreatedAtUpdatedAt

User = get_user_model()


class Order(AbstractCreatedAtUpdatedAt):
    # Custom UUID primary key
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        help_text="Unique order identifier",
    )

    class Meta:
        ordering = [
            "created_at",
            "updated_at",
        ]

    ORDER_STATUS_CHOICES = [
        ("pending", "Pending (Unassigned)"),
        ("in_progress", "In Progress (Assigned)"),
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
        help_text="Staff member assigned to work on this order. Only users with the 'ORDERS_OPERATOR' group can be assigned orders to handle.",
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

    def __str__(self):
        return f"Order #{str(self.id)[:8]} by {self.creator.username} - {self.get_status_display()}"

    def clean(self):
        super().clean()

        if self.staff_orders_handler:
            if not (
                self.staff_orders_handler.is_superuser
                or self.staff_orders_handler.groups.filter(name="ORDERS_OPERATOR").exists()
            ):
                raise ValidationError(
                    {"staff_orders_handler": "User must be in the ORDERS_OPERATOR group"}
                )

    def are_all_items_completed(self):
        """Check if all order items are completed."""
        if not self.items.exists():
            return False
        return self.items.filter(is_completed=False).count() == 0

    def update_status_based_on_items(self):
        """Update order status based on item completion."""
        if self.are_all_items_completed() and self.status != "cancelled":
            self.status = "completed"
        elif self.is_assigned and self.status not in ["completed", "cancelled"]:
            self.status = "in_progress"
        elif not self.is_assigned and self.status not in ["completed", "cancelled"]:
            self.status = "pending"

    def save(self, *args, **kwargs):
        # Automatically set is_assigned based on staff handler
        self.is_assigned = True if self.staff_orders_handler else False

        # Automatically set assigned_at if staff handler is set
        if self.staff_orders_handler and not self.assigned_at:
            self.assigned_at = timezone.now()

        # Clear assigned_at if unassigned
        if not self.staff_orders_handler and self.assigned_at:
            self.assigned_at = None

        # Call super().save() first to ensure self.pk exists before accessing reverse relationships
        is_new = self.pk is None
        super().save(*args, **kwargs)

        # After initial save, update status based on item completion
        if not is_new:
            self.update_status_based_on_items()
            # Save again if status was modified
            super().save(update_fields=["status"])

    def get_total_items(self):
        """Get total number of items in the order."""
        return sum(item.quantity for item in self.items.all())

    def get_total_price(self):
        """Calculate total price of the order."""
        total = 0
        for order_item in self.items.all():
            total += order_item.total_price
        return total

    @property
    def short_id(self):
        """Return a shortened version of the UUID for display purposes."""
        return str(self.id)[:8].upper()


class OrderItem(models.Model):
    """Individual items within an order."""

    # Custom UUID primary key
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        help_text="Unique order item identifier",
    )

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
    is_completed = models.BooleanField(
        default=False,
        help_text="Whether this item has been completed or fulfilled",
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

        # Update the order status after saving the item
        self.order.save()

    @property
    def total_price(self):
        """Get total price for this order item."""
        price = self.price_at_time or self.item.current_price or 0
        return price * self.quantity
