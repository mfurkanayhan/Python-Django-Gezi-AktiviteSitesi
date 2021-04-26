from django.contrib import admin

# Register your models here.
from product.models import Category, Content, Images

class ContentImageInline(admin.TabularInline):
    model = Images
    extra = 5


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['title', 'status', 'image_tag']
    list_filter = ['status']
    readonly_fields = ('image_tag',)

class ContentAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'city', 'country', 'konum', 'image_tag', 'status']
    readonly_fields = ('image_tag',)
    list_filter = ['status', 'category']
    inlines = [ContentImageInline]


class ImagesAdmin(admin.ModelAdmin):
    list_display = ['title', 'image_tag']
    readonly_fields = ('image_tag',)

admin.site.register(Category,CategoryAdmin)
admin.site.register(Content,ContentAdmin)
admin.site.register(Images,ImagesAdmin)