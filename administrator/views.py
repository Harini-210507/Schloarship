from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.utils import timezone
from django.db.models import Q

from accounts.views import admin_required
from scholarships.models import Scholarship, RequiredDocument
from scholarships.forms import ScholarshipForm, RequiredDocumentForm
from applications.models import ScholarshipApplication, UploadedDocument


# ── Dashboard ─────────────────────────────────────────────────────────────────

@admin_required
def dashboard(request):
    applications = ScholarshipApplication.objects.select_related('student', 'scholarship').all()

    # Filters
    status_filter      = request.GET.get('status', '')
    scholarship_filter = request.GET.get('scholarship', '')
    date_filter        = request.GET.get('date', '')

    if status_filter:
        applications = applications.filter(status=status_filter)
    if scholarship_filter:
        applications = applications.filter(scholarship_id=scholarship_filter)
    if date_filter:
        applications = applications.filter(submitted_at__date=date_filter)

    scholarships = Scholarship.objects.all()

    context = {
        'applications':        applications,
        'scholarships':        scholarships,
        'total':               ScholarshipApplication.objects.count(),
        'submitted_count':     ScholarshipApplication.objects.filter(status='submitted').count(),
        'under_review_count':  ScholarshipApplication.objects.filter(status='under_review').count(),
        'approved_count':      ScholarshipApplication.objects.filter(status='approved').count(),
        'rejected_count':      ScholarshipApplication.objects.filter(status='rejected').count(),
        'status_filter':       status_filter,
        'scholarship_filter':  scholarship_filter,
        'date_filter':         date_filter,
    }
    return render(request, 'administrator/dashboard.html', context)


# ── Application Review ────────────────────────────────────────────────────────

@admin_required
def review_application(request, pk):
    application = get_object_or_404(
        ScholarshipApplication.objects.select_related('student', 'scholarship', 'reviewed_by'),
        pk=pk
    )
    uploads = application.uploaded_documents.select_related('required_document').all()

    if request.method == 'POST':
        action = request.POST.get('action')

        # ── Document status update ─────────────────────────────────────────
        if action == 'update_docs':
            for upload in uploads:
                new_status = request.POST.get(f'doc_status_{upload.pk}', upload.status)
                new_reason = request.POST.get(f'doc_reason_{upload.pk}', '').strip()
                upload.status           = new_status
                upload.rejection_reason = new_reason if new_status == 'rejected' else ''
                upload.reviewed_at      = timezone.now()
                upload.save()
            # Move application to under_review if it was only submitted
            if application.status == 'submitted':
                application.status = 'under_review'
                application.save()
            messages.success(request, 'Document statuses updated.')

        # ── Approve application ────────────────────────────────────────────
        elif action == 'approve':
            if not application.all_mandatory_docs_verified():
                messages.error(request, 'All mandatory documents must be verified before approving.')
            else:
                application.status      = 'approved'
                application.review_notes = request.POST.get('review_notes', '').strip()
                application.reviewed_at = timezone.now()
                application.reviewed_by = request.user
                application.save()
                messages.success(request, f'Application #{pk} approved.')
                return redirect('administrator:dashboard')

        # ── Reject application ─────────────────────────────────────────────
        elif action == 'reject':
            reason = request.POST.get('review_notes', '').strip()
            if not reason:
                messages.error(request, 'Please provide a reason for rejection.')
            else:
                application.status       = 'rejected'
                application.review_notes = reason
                application.reviewed_at  = timezone.now()
                application.reviewed_by  = request.user
                application.save()
                messages.success(request, f'Application #{pk} rejected.')
                return redirect('administrator:dashboard')

        return redirect('administrator:review_application', pk=pk)

    required_docs = application.scholarship.required_documents.all()
    upload_map    = {u.required_document_id: u for u in uploads}

    doc_review_list = []
    for rd in required_docs:
        doc_review_list.append({
            'required_doc': rd,
            'upload':       upload_map.get(rd.pk),
        })

    context = {
        'application':    application,
        'doc_review_list': doc_review_list,
        'can_approve':    application.all_mandatory_docs_verified(),
    }
    return render(request, 'administrator/review_application.html', context)


# ── Scholarship Management ────────────────────────────────────────────────────

@admin_required
def manage_scholarships(request):
    scholarships = Scholarship.objects.all()
    return render(request, 'administrator/manage_scholarships.html', {'scholarships': scholarships})


@admin_required
def create_scholarship(request):
    if request.method == 'POST':
        form = ScholarshipForm(request.POST)
        if form.is_valid():
            scholarship = form.save(commit=False)
            scholarship.created_by = request.user
            scholarship.save()
            messages.success(request, f'Scholarship "{scholarship.title}" created.')
            return redirect('administrator:edit_scholarship', pk=scholarship.pk)
        messages.error(request, 'Please fix the errors below.')
    else:
        form = ScholarshipForm()
    return render(request, 'administrator/scholarship_form.html', {'form': form, 'title': 'Create Scholarship'})


@admin_required
def edit_scholarship(request, pk):
    scholarship = get_object_or_404(Scholarship, pk=pk)
    required_docs = scholarship.required_documents.all()

    if request.method == 'POST':
        form = ScholarshipForm(request.POST, instance=scholarship)
        if form.is_valid():
            form.save()
            messages.success(request, 'Scholarship updated.')
            return redirect('administrator:edit_scholarship', pk=pk)
        messages.error(request, 'Please fix the errors below.')
    else:
        form = ScholarshipForm(instance=scholarship)

    doc_form = RequiredDocumentForm()
    return render(request, 'administrator/scholarship_form.html', {
        'form':         form,
        'scholarship':  scholarship,
        'required_docs': required_docs,
        'doc_form':     doc_form,
        'title':        'Edit Scholarship',
    })


@admin_required
def add_required_document(request, scholarship_pk):
    scholarship = get_object_or_404(Scholarship, pk=scholarship_pk)
    if request.method == 'POST':
        form = RequiredDocumentForm(request.POST)
        if form.is_valid():
            doc = form.save(commit=False)
            doc.scholarship = scholarship
            doc.save()
            messages.success(request, f'Document "{doc.name}" added.')
    return redirect('administrator:edit_scholarship', pk=scholarship_pk)


@admin_required
def delete_required_document(request, pk):
    doc = get_object_or_404(RequiredDocument, pk=pk)
    scholarship_pk = doc.scholarship_id
    if request.method == 'POST':
        doc.delete()
        messages.success(request, 'Document requirement removed.')
    return redirect('administrator:edit_scholarship', pk=scholarship_pk)


@admin_required
def toggle_scholarship(request, pk):
    scholarship = get_object_or_404(Scholarship, pk=pk)
    if request.method == 'POST':
        scholarship.is_active = not scholarship.is_active
        scholarship.save()
        state = 'activated' if scholarship.is_active else 'deactivated'
        messages.success(request, f'Scholarship "{scholarship.title}" {state}.')
    return redirect('administrator:manage_scholarships')
