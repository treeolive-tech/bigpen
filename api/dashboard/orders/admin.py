from django.contrib import admin, messages

from home.globals.adminsite import admin_site

from .forms import OrderItemFormSet
from .models import Order, OrderItem

# TODO: Have the is_completed be done by the staff member assigned to the order

# TODO: If the order was already marked as completed and the status says Completed, if any item is marked as incompleted it should go back to the right status.


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    formset = OrderItemFormSet
    extra = 0
    readonly_fields = ("price_at_time", "total_price")

    def get_fields(self, request, obj=None):
        if obj is None or not obj.is_assigned:  # New order or unassigned
            return ("item", "quantity", "price_at_time", "total_price")
        return ("item", "quantity", "price_at_time", "total_price", "is_completed")

    def get_readonly_fields(self, request, obj=None):
        readonly = list(super().get_readonly_fields(request, obj))
        if obj is None or not obj.is_assigned:  # New order or unassigned
            readonly.append("is_completed")
        return readonly

    def get_min_num(self, request, obj=None, **kwargs):
        if obj is None:  # New order
            return 1
        return 0

    def get_formset(self, request, obj=None, **kwargs):
        formset = super().get_formset(request, obj, **kwargs)
        formset.request = request
        return formset


@admin.register(Order, site=admin_site)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        "short_id",
        "creator",
        "staff_orders_handler",
        "is_assigned",
        "status",
        "assigned_at",
        "created_at",
        "completion_status",
    )
    list_filter = ("status", "assigned_at", "created_at")
    search_fields = (
        "id__icontains",
        "creator__username",
        "staff_orders_handler__username",
    )
    readonly_fields = (
        "creator",
        "status",
        "assigned_at",
        "is_assigned",
        "assigned_staff_info",
        "created_at",
        "completion_progress",
    )
    inlines = [OrderItemInline]
    base_fieldsets = (
        ("Basic Information", {"fields": ("creator", "status")}),
        (
            "Assignment Information",
            {"fields": ("staff_orders_handler", "is_assigned", "assigned_at")},
        ),
        (
            "Completion Progress",
            {"fields": ("completion_progress",), "classes": ("collapse",)},
        ),
        (
            "Additional Information",
            {"fields": ("notes",), "classes": ("collapse",)},
        ),
        (
            "Timestamps",
            {
                "fields": ("created_at",),
                "classes": ("collapse",),
            },
        ),
    )

    def completion_status(self, obj):
        """Display completion status in list view."""
        total_items = obj.items.count()
        completed_items = obj.items.filter(is_completed=True).count()
        if total_items == 0:
            return "No items"
        return f"{completed_items}/{total_items} items completed"

    completion_status.short_description = "Completion"

    def completion_progress(self, obj):
        """Display detailed completion progress."""
        total_items = obj.items.count()
        completed_items = obj.items.filter(is_completed=True).count()

        if total_items == 0:
            return "No items in this order"

        progress = f"{completed_items} of {total_items} items completed"
        if completed_items == total_items:
            progress += " ✓ (All items completed)"
        elif completed_items > 0:
            percentage = (completed_items / total_items) * 100
            progress += f" ({percentage:.1f}%)"

        return progress

    completion_progress.short_description = "Completion Progress"

    def assigned_staff_info(self, obj):
        if obj.staff_orders_handler:
            return f"Assigned to: {obj.staff_orders_handler.get_full_name() or obj.staff_orders_handler.username}"
        return "Not assigned"

    assigned_staff_info.short_description = "Assignment Info"

    def get_fieldsets(self, request, obj=None):
        if obj is None:  # New order - show no fieldsets, only inlines
            return ()

        # Existing order - show all fieldsets
        fieldsets = list(self.base_fieldsets)

        # Determine assignment fields based on user type and assignment status
        assignment_fields = ["is_assigned", "assigned_at"]
        if not request.user.groups.filter(name="ORDERS_OPERATOR").exists():
            assignment_fields.insert(0, "staff_orders_handler")
        if obj and obj.is_assigned:
            assignment_fields.append("assigned_staff_info")

        fieldsets[1] = (
            "Assignment Information",
            {"fields": tuple(assignment_fields)},
        )
        return fieldsets

    def save_model(self, request, obj, form, change):
        # Set the creator to the current user if not changing an existing object
        # of course this is when testing adding a new order via the admin
        # since adding new orders is typically done via the frontend
        # and not via the admin interface
        if not change and not obj.creator:
            obj.creator = request.user
        super().save_model(request, obj, form, change)

    def save_formset(self, request, form, formset, change):
        """Override to update order status after saving order items."""
        instances = formset.save(commit=False)

        # Save the instances
        for instance in instances:
            instance.save()

        # Delete any objects marked for deletion
        for obj in formset.deleted_objects:
            obj.delete()

        # Update the order status based on item completion
        if form.instance.pk:
            form.instance.save()  # This will trigger the status update logic

    def get_queryset(self, request):
        qs = super().get_queryset(request)

        # Superusers sees all orders
        if request.user.is_superuser:
            return qs

        # ORDERS_MANAGER group sees all orders as well
        if request.user.groups.filter(name="ORDERS_MANAGER").exists():
            return qs

        # ORDERS_OPERATOR group sees only orders assigned to them
        if request.user.groups.filter(name="ORDERS_OPERATOR").exists():
            return qs.filter(staff_orders_handler=request.user)

        # Not in any allowed group
        return qs.none()


@admin.register(OrderItem, site=admin_site)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = (
        "item",
        "order",
        "quantity",
        "price_at_time",
        "total_price",
        "is_completed",
        "order__created_at",
    )
    list_filter = ("is_completed", "order__status", "order__created_at", "item__name")
    search_fields = ("order__id__icontains", "order__short_id", "item__name")
    readonly_fields = ("price_at_time", "total_price")
    list_editable = ("is_completed",)  # Allow quick editing of completion status

    fieldsets = (
        ("Order Information", {"fields": ("order",)}),
        (
            "Item Details",
            {"fields": ("item", "quantity", "price_at_time", "total_price")},
        ),
        (
            "Completion Status",
            {"fields": ("is_completed",)},
        ),
    )

    def get_fields(self, request, obj=None):
        base_fields = ["order", "item", "quantity", "price_at_time", "total_price"]
        if obj and obj.order.is_assigned:  # Existing and assigned order
            base_fields.append("is_completed")
        return base_fields

    def get_fieldsets(self, request, obj=None):
        if obj is None or not obj.order.is_assigned:  # New item or unassigned order
            return (
                ("Order Information", {"fields": ("order",)}),
                (
                    "Item Details",
                    {"fields": ("item", "quantity", "price_at_time", "total_price")},
                ),
            )
        return self.fieldsets

    def get_readonly_fields(self, request, obj=None):
        readonly_fields = list(self.readonly_fields)

        # Hide completion field for new objects or unassigned orders
        if obj is None or (obj and not obj.order.is_assigned):
            readonly_fields.append("is_completed")

        if obj:
            readonly_fields.extend(["order", "item"])

        return readonly_fields

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.request = request
        return form

    def save_model(self, request, obj, form, change):
        """Override to show message when order is automatically completed."""
        old_order_status = None
        if change and obj.pk:
            old_order_status = obj.order.status

        super().save_model(request, obj, form, change)

        # Check if the order status changed to completed
        if (
            old_order_status
            and old_order_status != "completed"
            and obj.order.status == "completed"
        ):
            messages.success(
                request,
                f"Order #{obj.order.id} has been automatically marked as completed "
                "because all items are now fulfilled.",
            )

    def delete_model(self, request, obj):
        """Override delete to check if this would leave the order empty."""
        order = obj.order

        # Check if this is the last item in the order
        if order.items.count() == 1:
            messages.error(
                request,
                "Cannot delete the last item from an order. If you want to remove all items, please delete the order instead.",
            )
            return

        # Safe to delete
        super().delete_model(request, obj)

        # Update order status after deletion
        order.save()

    def delete_queryset(self, request, queryset):
        """Override bulk delete to prevent deletion that would leave orders empty."""
        orders_to_check = {}
        orders_to_update = set()

        # Count items per order that would be deleted
        for item in queryset:
            order_id = item.order.id
            orders_to_update.add(item.order)
            if order_id not in orders_to_check:
                orders_to_check[order_id] = {
                    "order": item.order,
                    "total_items": item.order.items.count(),
                    "items_to_delete": 0,
                }
            orders_to_check[order_id]["items_to_delete"] += 1

        # Check if any order would be left empty
        problem_orders = []
        for order_info in orders_to_check.values():
            if order_info["total_items"] == order_info["items_to_delete"]:
                problem_orders.append(order_info["order"].id)

        if problem_orders:
            messages.error(
                request,
                f"Cannot delete items from Order(s) #{', #'.join(map(str, problem_orders))} as it would leave them empty. "
                "If you want to remove all items, please delete the order(s) instead.",
            )
            return

        # Safe to delete
        super().delete_queryset(request, queryset)

        # Update order statuses after bulk deletion
        for order in orders_to_update:
            order.save()
