from django.db.models import QuerySet
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render

from .forms import DocumentFileForm
from .models import (
    DocumentFile,
    DocumentType,
    Request,
    RequestRequirement,
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


def issuable_document_detail_view(request: HttpRequest, document_code: str):
    issuable_document = DocumentType.objects.get(code=document_code)
    requirements: QuerySet[RequestRequirement] = issuable_document.requirements.all()
    user_documents = DocumentFile.objects.filter(user=request.user)
    is_valid: bool = False
    errors: list[str] = []

    # Loop through requirements
    for requirement in requirements:
        # For requirements with document_category,
        #   count the user's documents with a distinct document_type
        #   matching the requirement's document_category
        # If it is less than the required quantity, add error
        # Continue to next loop
        if requirement.document_category:
            user_document_count_in_category = (
                user_documents.distinct("document_type")
                .filter(document_type__category=requirement.document_category)
                .count()
            )
            if user_document_count_in_category < requirement.quantity:
                missing_document_count = requirement.quantity - user_document_count_in_category
                errors.append(f"Missing {missing_document_count} {requirement.document_category.name}")
            continue

        # For requirements with document_type,
        #   check if the user has a document with the required document_type
        # If not, add error
        # Continue to next loop
        user_documents_with_required_type_exists = user_documents.filter(
            document_type=requirement.document_type,
        ).exists()
        if not user_documents_with_required_type_exists:
            errors.append(f"Missing {requirement.document_type.name}")
        continue

    is_valid = len(errors) == 0
    context = {
        "issuable_document": issuable_document,
        "requirements": requirements,
        "requirements_count": requirements.count(),
        "is_valid": is_valid,
        "errors": errors,
        "errors_count": len(errors),
    }
    return render(request, "document/issuable_document_detail.html", context)
