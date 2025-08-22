from django import forms

from apps.document.models import DocumentFile


class DocumentFileForm(forms.ModelForm):
    class Meta:
        model = DocumentFile
        fields = (
            "document_type",
            "file_name",
            "file",
        )
