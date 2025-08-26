import uuid

from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _


class DocumentCategory(models.Model):
    name = models.CharField(_("document category"), max_length=50)
    code = models.CharField(_("document category code"), max_length=50)

    class Meta:
        verbose_name = _("document category")
        verbose_name_plural = _("document categories")

    def __str__(self):
        return self.name


class DocumentType(models.Model):
    name = models.CharField(_("document type"), max_length=50)
    code = models.CharField(_("document type code"), max_length=50)
    category = models.ForeignKey(DocumentCategory, verbose_name=_("document category"), on_delete=models.CASCADE)
    is_issuable = models.BooleanField(_("issuable"), default=False)

    class Meta:
        verbose_name = _("document type")
        verbose_name_plural = _("document types")

    def __str__(self):
        return self.name


# TODO (ottsupi): Add limitations for file types


class DocumentFile(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_("user"), on_delete=models.CASCADE)
    document_type = models.ForeignKey(DocumentType, verbose_name=_("document type"), on_delete=models.CASCADE)
    file_name = models.CharField(_("file name"), max_length=50)
    file = models.FileField(_("file"), upload_to="documents/", max_length=100)
    date_added = models.DateTimeField(_("date added"), auto_now_add=True)

    class Meta:
        verbose_name = _("document")
        verbose_name_plural = _("documents")

    def __str__(self):
        return self.file_name


class Request(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_("user"), on_delete=models.CASCADE)
    document_type = models.ForeignKey(
        DocumentType,
        verbose_name=_("document type"),
        on_delete=models.CASCADE,
        limit_choices_to={"is_issuable": True},
    )
    date_requested = models.DateField(_("date requested"), auto_now_add=True)
    date_issued = models.DateField(_("date issued"), null=True)

    class Meta:
        verbose_name = _("request")
        verbose_name_plural = _("requests")

    def __str__(self):
        return f"{self.document_type.name} Request"

    @property
    def is_issued(self):
        return bool(self.date_issued)


class RequestRequirement(models.Model):
    requested_document = models.ForeignKey(
        DocumentType,
        verbose_name=_("requested document"),
        on_delete=models.CASCADE,
        related_name="requirements",
        limit_choices_to={"is_issuable": True},
    )
    document_category = models.ForeignKey(
        DocumentCategory,
        verbose_name=_("document category"),
        null=True,
        blank=True,
        on_delete=models.CASCADE,
    )
    document_type = models.ForeignKey(
        DocumentType,
        verbose_name=_("document type"),
        null=True,
        blank=True,
        on_delete=models.CASCADE,
    )
    quantity = models.IntegerField(_("quantity"))

    class Meta:
        verbose_name = _("requirement")
        verbose_name_plural = _("requirements")

    def __str__(self):
        if self.document_category:
            return f"{self.requested_document.name} Requirement | {self.quantity} {self.document_category}"
        return f"{self.requested_document.name} Requirement | {self.document_type}"
