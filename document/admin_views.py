from pathlib import Path

import markdown

from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required

from .models import Document, DocumentFile

"""
Logging:
-------
import logging

logger = logging.getLogger(__name__)

logger.info("Application started")

logger.info(
    "User '%s' viewed document '%s'",
    request.user.username,
    selected_document.name,
)

logger.warning("Unsupported file type: %s", ext)

try:
    ...
except Exception:
    logger.exception("Failed to render markdown")

"""


@staff_member_required
def document_viewer(request):
    documents = Document.objects.all()

    selected_document = None
    selected_file = None

    file_type = None
    markdown_html = None

    document_id = request.GET.get("document")
    file_id = request.GET.get("file")

    if document_id:
        selected_document = Document.objects.filter(pk=document_id).first()

    if file_id:
        selected_file = DocumentFile.objects.filter(pk=file_id).first()
    elif selected_document:
        selected_file = selected_document.files.first()

    if selected_file:
        ext = Path(selected_file.file.name).suffix.lower()

        if ext in [".png", ".jpg", ".jpeg", ".gif", ".webp"]:
            file_type = "image"

        elif ext == ".pdf":
            file_type = "pdf"

        elif ext == ".md":
            file_type = "markdown"

            with open(selected_file.file.path, encoding="utf-8") as f:
                markdown_html = markdown.markdown(
                    f.read(),
                    extensions=["tables", "fenced_code"]
                )

    return render(
        request,
        "admin/document/document_viewer.html",
        {
            "documents": documents,
            "selected_document": selected_document,
            "selected_file": selected_file,
            "file_type": file_type,
            "markdown_html": markdown_html,
        },
    )
