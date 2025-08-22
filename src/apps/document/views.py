from django.http import HttpResponse
from django.shortcuts import redirect, render

from .models import DocumentFile


def index(request: HttpResponse):
    if not request.user.is_authenticated:
        return redirect(request, "404")

    documents: DocumentFile = DocumentFile.objects.all()

    context = {
        "documents": documents,
    }
    return render(request, "document/index.html", context)
