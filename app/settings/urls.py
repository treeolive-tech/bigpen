from django.urls import include, path

urlpatterns = [
    path("", include("olyv.settings.urls")),
    path("", include("app.home.urls")),
    path("stock/", include("app.stock.urls")),
    path("orders/", include("app.orders.urls")),
]
