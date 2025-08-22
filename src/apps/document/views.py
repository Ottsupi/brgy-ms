from django.db.models import QuerySet
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render

from .forms import DocumentFileForm
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


def create_view(request: HttpRequest):
    form = DocumentFileForm()
    if request.method == "POST":
        form = DocumentFileForm(request.POST, request.FILES)
        print(request.FILES)

    context = {
        "form": form,
    }

    if form.is_valid():
        document_file = form.save(commit=False)
        document_file.user = request.user
        document_file.save()
        return redirect("document:index")

    return render(request, "document/form.html", context)
