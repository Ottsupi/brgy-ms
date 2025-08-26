from django.contrib import admin

from .models import (
    DocumentCategory,
    DocumentFile,
    DocumentType,
    Request,
    RequestRequirement,
)


class DocumentCategoryAdmin(admin.ModelAdmin):
    pass


class DocumentTypeAdmin(admin.ModelAdmin):
    pass


class DocumentFileAdmin(admin.ModelAdmin):
    pass


class RequestAdmin(admin.ModelAdmin):
    pass


class RequestRequirementAdmin(admin.ModelAdmin):
    pass


admin.site.register(DocumentCategory, DocumentCategoryAdmin)
admin.site.register(DocumentType, DocumentTypeAdmin)
admin.site.register(DocumentFile, DocumentFileAdmin)
admin.site.register(Request, DocumentFileAdmin)
admin.site.register(RequestRequirement, DocumentFileAdmin)
