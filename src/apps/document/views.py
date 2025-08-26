from django.db.models import QuerySet
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render

from .forms import DocumentFileForm
from .models import (
    DocumentFile,
    DocumentType,
    Request,
)


def index(request: HttpResponse):
    if not request.user.is_authenticated:
        return redirect(request, "404")

    documents: QuerySet[DocumentFile] = DocumentFile.objects.filter(user=request.user)

    context = {
        "documents": documents,
        "documents_count": documents.count(),
    }
    return render(request, "document/index.html", context)


def create_view(request: HttpRequest):
    form = DocumentFileForm()
    if request.method == "POST":
        form = DocumentFileForm(request.POST, request.FILES)

    context = {
        "form": form,
    }

    if form.is_valid():
        document_file = form.save(commit=False)
        document_file.user = request.user
        document_file.save()
        return redirect("document:index")

    return render(request, "document/form.html", context)


def request_list_view(request: HttpRequest):
    requests = Request.objects.select_related("document_type").filter(user=request.user)
    context = {
        "requests": requests,
        "requests_count": requests.count(),
    }
    return render(request, "document/request_list.html", context)


def issuable_document_list_view(request: HttpRequest):
    issuable_documents = DocumentType.objects.filter(is_issuable=True)
    context = {
        "issuable_documents": issuable_documents,
        "issuable_documents_count": issuable_documents.count(),
    }
    return render(request, "document/issuable_document_list.html", context)
