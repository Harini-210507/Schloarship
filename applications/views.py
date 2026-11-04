from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.utils import timezone

from accounts.views import student_required
from scholarships.models import Scholarship
from .models import ScholarshipApplication, UploadedDocument
from .forms import DocumentUploadForm


@student_required
def apply(request, scholarship_pk):
    """Start a new application for a scholarship."""
    scholarship = get_object_or_404(Scholarship, pk=scholarship_pk, is_active=True)

    # Prevent duplicate applications
    if ScholarshipApplication.objects.filter(
        student=request.user, scholarship=scholarship
    ).exists():
        messages.warning(request, 'You have already applied for this scholarship.')
        return redirect('applications:my_application', scholarship_pk=scholarship_pk)

    if not scholarship.is_open():
        messages.error(request, 'This scholarship is no longer accepting applications.')
        return redirect('scholarships:detail', pk=scholarship_pk)

    if request.method == 'POST':
        application = ScholarshipApplication.objects.create(
            student=request.user,
            scholarship=scholarship,
            status='submitted',
        )
        messages.success(request, 'Application submitted! Please upload your documents.')
        return redirect('applications:upload_documents', pk=application.pk)

    return render(request, 'applications/apply_confirm.html', {'scholarship': scholarship})


@student_required
def upload_documents(request, pk):
    """Upload required documents for an existing application."""
    application = get_object_or_404(ScholarshipApplication, pk=pk, student=request.user)
    required_docs = application.scholarship.required_documents.all()

    # Build a map: required_doc.pk → existing upload (if any)
    existing_uploads = {
        u.required_document_id: u
        for u in application.uploaded_documents.all()
    }

    if request.method == 'POST':
        any_saved = False
        for req_doc in required_docs:
            file_key = f'doc_{req_doc.pk}'
            if file_key in request.FILES:
                form = DocumentUploadForm({'file': None}, request.FILES, prefix=str(req_doc.pk))
                form.data = {}
                # Validate single file
                single_form = DocumentUploadForm(files={'file': request.FILES[file_key]})
                if single_form.is_valid():
                    existing = existing_uploads.get(req_doc.pk)
                    if existing:
                        # Replace the file
                        existing.file   = single_form.cleaned_data['file']
                        existing.status = 'pending'
                        existing.rejection_reason = ''
                        existing.save()
                    else:
                        UploadedDocument.objects.create(
                            application=application,
                            required_document=req_doc,
                            file=single_form.cleaned_data['file'],
                        )
                    any_saved = True
                    existing_uploads[req_doc.pk] = UploadedDocument.objects.filter(
                        application=application, required_document=req_doc
                    ).first()
                else:
                    for err in single_form.errors.get('file', []):
                        messages.error(request, f'{req_doc.name}: {err}')

        if any_saved:
            messages.success(request, 'Documents uploaded successfully.')

        if 'submit_final' in request.POST:
            return redirect('applications:status', pk=application.pk)

        return redirect('applications:upload_documents', pk=application.pk)

    # Re-fetch after possible save
    existing_uploads = {
        u.required_document_id: u
        for u in application.uploaded_documents.all()
    }

    doc_forms = []
    for req_doc in required_docs:
        doc_forms.append({
            'required_doc': req_doc,
            'upload':       existing_uploads.get(req_doc.pk),
            'form':         DocumentUploadForm(),
        })

    return render(request, 'applications/upload_documents.html', {
        'application': application,
        'doc_forms':   doc_forms,
    })


@student_required
def application_status(request, pk):
    """Show application status and per-document feedback to the student."""
    application = get_object_or_404(ScholarshipApplication, pk=pk, student=request.user)
    uploads     = application.uploaded_documents.select_related('required_document').all()
    return render(request, 'applications/status.html', {
        'application': application,
        'uploads':     uploads,
    })


@student_required
def my_application(request, scholarship_pk):
    """Redirect to status page for an application by scholarship pk."""
    scholarship = get_object_or_404(Scholarship, pk=scholarship_pk)
    application = get_object_or_404(
        ScholarshipApplication, student=request.user, scholarship=scholarship
    )
    return redirect('applications:status', pk=application.pk)
