from django.urls import include, path

urlpatterns = [
    path("", include("core.settings.urls")),
    path("stock/", include("dashboard.stock.urls")),
    path("orders/", include("dashboard.orders.urls")),
]
