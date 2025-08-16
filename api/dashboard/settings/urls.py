from django.urls import include, path

urlpatterns = [
    path("", include("home.settings.urls")),
    path("stock/", include("dashboard.stock.urls")),
    path("orders/", include("dashboard.orders.urls")),
]
