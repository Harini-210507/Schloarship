from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Scholarship, RequiredDocument


def scholarship_list(request):
    scholarships = Scholarship.objects.filter(is_active=True).order_by('-created_at')
    return render(request, 'scholarships/list.html', {'scholarships': scholarships})


def scholarship_detail(request, pk):
    scholarship = get_object_or_404(Scholarship, pk=pk)
    required_docs = scholarship.required_documents.all()

    # Check if the student already applied
    already_applied = False
    if request.user.is_authenticated and not request.user.is_staff:
        from applications.models import ScholarshipApplication
        already_applied = ScholarshipApplication.objects.filter(
            student=request.user, scholarship=scholarship
        ).exists()

    context = {
        'scholarship':   scholarship,
        'required_docs': required_docs,
        'already_applied': already_applied,
    }
    return render(request, 'scholarships/detail.html', context)
