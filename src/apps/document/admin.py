from django.contrib import admin

from .models import DocumentCategory, DocumentFile, DocumentType


class DocumentCategoryAdmin(admin.ModelAdmin):
    pass


class DocumentTypeAdmin(admin.ModelAdmin):
    pass


class DocumentFileAdmin(admin.ModelAdmin):
    pass


admin.site.register(DocumentCategory, DocumentCategoryAdmin)
admin.site.register(DocumentType, DocumentTypeAdmin)
admin.site.register(DocumentFile, DocumentFileAdmin)
