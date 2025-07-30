from django.contrib import admin

from core.globals.adminsite import admin_site

from .forms import ArticleForm
from .models import Article, ArticleCategory, ArticleTag


@admin.register(Article, site=admin_site)
class ArticleAdmin(admin.ModelAdmin):
    # Hide author field from the admin form
    exclude = ("author",)

    # Optional: Display author in the list view
    list_display = ("title", "author", "category", "date_created")
    list_filter = ("category", "date_created", "author")
    search_fields = ("title", "content")
    form = ArticleForm

    def save_model(self, request, obj, form, change):
        # Set the author to the current user if not already set
        if not obj.author_id:
            obj.author = request.user
        super().save_model(request, obj, form, change)

    # Optional: Filter queryset to show only user's own articles for non-superusers
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(author=request.user)

    # Optional: Show author field as readonly if you want to display it
    # readonly_fields = ('author',)

    # Optional: Custom form layout
    fieldsets = (
        ("Basic Information", {"fields": ("title", "content", "image")}),
        ("Categorization", {"fields": ("category", "tags"), "classes": ("collapse",)}),
    )


admin_site.register(ArticleCategory)
admin_site.register(ArticleTag)
