from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import FileResponse, Http404
from django.db.models import Q
import os
from .models import Document
from .forms import DocumentUploadForm


def user_can_view(user, document):
    """Check if a user has permission to view a document."""
    if user.is_admin:
        return True
    if document.access_level == 'admin':
        return False
    if document.access_level == 'global':
        return True
    if document.access_level == 'affiliate':
        return document.affiliate == user.affiliate
    return False


@login_required
def document_list(request):
    user = request.user

    if user.is_admin:
        documents = Document.objects.all().select_related('uploaded_by', 'affiliate')
    else:
        documents = Document.objects.filter(
            Q(access_level='global') |
            Q(access_level='affiliate', affiliate=user.affiliate)
        ).select_related('uploaded_by', 'affiliate')

    # Search
    query = request.GET.get('q', '')
    if query:
        documents = documents.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query)
        )

    # Filter by category
    category_filter = request.GET.get('category', '')
    if category_filter:
        documents = documents.filter(category=category_filter)

    context = {
        'documents': documents,
        'query': query,
        'category_filter': category_filter,
        'category_choices': Document.CATEGORY_CHOICES,
    }
    return render(request, 'documents/list.html', context)


@login_required
def document_upload(request):
    if not request.user.is_staff_member:
        messages.error(request, "You do not have permission to upload documents.")
        return redirect('documents:list')

    if request.method == 'POST':
        form = DocumentUploadForm(request.POST, request.FILES)
        if form.is_valid():
            doc = form.save(commit=False)
            doc.uploaded_by = request.user
            doc.save()
            messages.success(request, f"'{doc.title}' uploaded successfully.")
            return redirect('documents:list')
    else:
        form = DocumentUploadForm()

    return render(request, 'documents/upload.html', {'form': form})


@login_required
def document_download(request, pk):
    document = get_object_or_404(Document, pk=pk)

    if not user_can_view(request.user, document):
        messages.error(request, "You do not have permission to access this document.")
        return redirect('documents:list')

    try:
        response = FileResponse(document.file.open('rb'))
        filename = os.path.basename(document.file.name)
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        return response
    except Exception:
        raise Http404("File not found.")


@login_required
def document_delete(request, pk):
    document = get_object_or_404(Document, pk=pk)
    if not request.user.is_admin:
        messages.error(request, "Only administrators can delete documents.")
        return redirect('documents:list')
    if request.method == 'POST':
        title = document.title
        document.file.delete(save=False)
        document.delete()
        messages.success(request, f"'{title}' has been deleted.")
    return redirect('documents:list')
