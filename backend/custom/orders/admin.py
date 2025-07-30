from core.globals.adminsite import admin_site
from django.contrib import admin

from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ("price_at_time", "total_price")


@admin.register(Order, site=admin_site)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "creator",
        "staff_orders_handler",
        "is_assigned",
        "status",
        "assigned_at",
        "created_at",
    )
    list_filter = ("status", "assigned_at", "created_at")
    search_fields = ("creator__username", "staff_orders_handler__username")
    readonly_fields = ("creator", "status", "assigned_at", "is_assigned")
    inlines = [OrderItemInline]

    def save_model(self, request, obj, form, change):
        if not change and not obj.creator:
            obj.creator = request.user
        super().save_model(request, obj, form, change)

    def get_queryset(self, request):
        qs = super().get_queryset(request)

        # Superusers see everything
        if request.user.is_superuser:
            return qs

        if request.user.groups.filter(name="ORDERS_MANAGER").exists():
            return qs

        if request.user.groups.filter(name="ORDERS_HANDLER").exists():
            return qs.filter(staff_orders_handler=request.user)

        # Not in any allowed group
        return qs.none()

    def has_change_permission(self, request, obj=None):
        # Optionally restrict change permission to managers/superusers
        return (
            request.user.is_superuser
            or request.user.groups.filter(name="ORDERS_MANAGER").exists()
        )

    def has_delete_permission(self, request, obj=None):
        return self.has_change_permission(request)

    def has_add_permission(self, request):
        # Orders may not be created manually from admin except if superuser
        return request.user.is_superuser


# @admin.register(AssignedOrder)
# class AssignedOrderAdmin(admin.ModelAdmin):
#     list_display = (
#         "id",
#         "creator",
#         "staff_orders_handler",
#         "status",
#         "assigned_at",
#         "created_at",
#     )
#     list_filter = ("status", "assigned_at", "created_at")
#     search_fields = ("creator__username", "staff_orders_handler__username")
#     readonly_fields = ("status", "assigned_at")
#     inlines = [OrderItemInline]
#     actions = ["assign_to_me", "unassign_order"]

#     def get_queryset(self, request):
#         """Filter assigned orders to show only those assigned to the current user."""
#         qs = super().get_queryset(request)

#         # If user is superuser, show all assigned orders
#         if request.user.is_superuser:
#             return qs

#         # Filter to show only orders assigned to the current user
#         # Only show if user has the ORDERS_HANDLER group
#         if request.user.groups.filter(name="ORDERS_HANDLER").exists():
#             return qs.filter(staff_orders_handler=request.user)

#         # If user doesn't have the required group, show empty queryset
#         return qs.none()

#     def has_change_permission(self, request, obj=None):
#         """Allow changing only if user is assigned to the order or is superuser."""
#         if request.user.is_superuser:
#             return True

#         if obj is None:
#             return True  # Allow access to change list

#         # Allow change only if the order is assigned to the current user
#         return obj.staff_orders_handler == request.user

#     def has_delete_permission(self, request, obj=None):
#         """Restrict delete permissions."""
#         if request.user.is_superuser:
#             return True

#         if obj is None:
#             return False

#         # Allow delete only if assigned to current user (optional - you might want to restrict this)
#         return obj.staff_orders_handler == request.user

#     def assign_to_me(self, request, queryset):
#         """Admin action to assign selected orders to the current user."""
#         if not request.user.groups.filter(name="ORDERS_HANDLER").exists():
#             self.message_user(
#                 request, "You don't have permission to handle orders.", level="ERROR"
#             )
#             return

#         assigned_count = 0
#         for order in queryset:
#             try:
#                 if order.is_available_for_assignment:
#                     order.assign_to_staff_orders_handler(request.user)
#                     assigned_count += 1
#             except Exception as e:
#                 self.message_user(
#                     request, f"Error assigning order {order.id}: {e}", level="ERROR"
#                 )

#         if assigned_count:
#             self.message_user(
#                 request, f"Successfully assigned {assigned_count} orders to you."
#             )

#     assign_to_me.short_description = "Assign selected orders to me"

#     def unassign_order(self, request, queryset):
#         """Admin action to unassign orders."""
#         unassigned_count = 0
#         for order in queryset:
#             if order.staff_orders_handler == request.user or request.user.is_superuser:
#                 order.unassign_order()
#                 unassigned_count += 1

#         if unassigned_count:
#             self.message_user(
#                 request, f"Successfully unassigned {unassigned_count} orders."
#             )

#     unassign_order.short_description = "Unassign selected orders"


# @admin.register(UnassignedOrder)
# class UnassignedOrderAdmin(admin.ModelAdmin):
#     list_display = ("id", "creator", "status", "created_at")
#     list_filter = ("created_at",)
#     search_fields = ("creator__username",)
#     readonly_fields = ("status", "assigned_at")
#     inlines = [OrderItemInline]

#     def get_queryset(self, request):
#         """Show unassigned orders that can be picked up by staff."""
#         qs = super().get_queryset(request)

#         # If user is superuser, show all unassigned orders
#         if request.user.is_superuser:
#             return qs

#         # Only show unassigned orders if user has the ORDERS_HANDLER group
#         if request.user.groups.filter(name="ORDERS_HANDLER").exists():
#             return qs

#         # If user doesn't have the required group, show empty queryset
#         return qs.none()
