from django.db.models import QuerySet
from django.http import HttpResponse
from django.shortcuts import redirect, render

from .models import DocumentFile


def index(request: HttpResponse):
    if not request.user.is_authenticated:
        return redirect(request, "404")

    documents: QuerySet[DocumentFile] = DocumentFile.objects.all()

    context = {
        "documents": documents,
        "documents_count": documents.count(),
    }
    return render(request, "document/index.html", context)
