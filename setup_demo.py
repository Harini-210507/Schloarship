"""
Setup script — creates sample scholarships and demonstration accounts.

Run with:   python setup_demo.py

Accounts created:
  Admin   → username: admin      password: Admin@1234
  Student → username: student1   password: Student@1234

These are for local demonstration only. Change passwords before any deployment.
"""

import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'scholarship_system.settings')
django.setup()

from django.contrib.auth.models import User
from django.utils import timezone
from datetime import date, timedelta
from accounts.models import StudentProfile
from scholarships.models import Scholarship, RequiredDocument

print("=== Scholarship Application System - Demo Setup ===\n")

# -- Admin account -------------------------------------------------------
if not User.objects.filter(username='admin').exists():
    admin = User.objects.create_superuser(
        username='admin',
        email='admin@scholarshipsystem.local',
        password='Admin@1234',
        first_name='Admin',
        last_name='User',
    )
    print("[OK] Admin account created  ->  username: admin  /  password: Admin@1234")
else:
    admin = User.objects.get(username='admin')
    print("[INFO] Admin account already exists.")

# -- Student account -----------------------------------------------------
if not User.objects.filter(username='student1').exists():
    student = User.objects.create_user(
        username='student1',
        email='student1@example.local',
        password='Student@1234',
        first_name='Priya',
        last_name='Sharma',
    )
    StudentProfile.objects.create(
        user=student,
        phone='9876543210',
        date_of_birth=date(2002, 5, 15),
        address='123 Main Street, Chennai, Tamil Nadu 600001',
    )
    print("[OK] Student account created ->  username: student1  /  password: Student@1234")
else:
    print("[INFO] Student account already exists.")

# ── Sample Scholarships ──────────────────────────────────────────────────────
scholarships = [
    {
        'title':       'Merit Excellence Award',
        'description': 'Awarded to students who have demonstrated outstanding academic performance '
                       'throughout their studies. This scholarship supports bright minds in pursuing '
                       'higher education without financial barriers.',
        'eligibility': '• Minimum 80% aggregate marks in the previous academic year\n'
                       '• Enrolled in a recognized college or university\n'
                       '• Indian national\n'
                       '• Family annual income below ₹5,00,000',
        'amount':      50000.00,
        'deadline':    date.today() + timedelta(days=60),
    },
    {
        'title':       'Need-Based Financial Support Grant',
        'description': 'Designed to help students from economically disadvantaged backgrounds '
                       'continue their education. The grant covers tuition fees and basic educational expenses.',
        'eligibility': '• Family annual income below ₹2,00,000\n'
                       '• Enrolled in an undergraduate program\n'
                       '• Minimum 60% marks in the previous examination\n'
                       '• Valid income certificate from competent authority',
        'amount':      30000.00,
        'deadline':    date.today() + timedelta(days=45),
    },
    {
        'title':       'Women in Technology Scholarship',
        'description': 'Encouraging women to pursue careers in technology, engineering, and sciences. '
                       'This scholarship covers tuition and provides a monthly stipend for living expenses.',
        'eligibility': '• Female student\n'
                       '• Enrolled in B.Tech, B.Sc (CS/IT/Electronics), or related STEM program\n'
                       '• Minimum 70% marks\n'
                       '• Age between 18–25 years',
        'amount':      75000.00,
        'deadline':    date.today() + timedelta(days=90),
    },
]

doc_sets = [
    # Merit Excellence Award
    [
        {'name': 'Identity Document',      'description': 'Aadhaar card, PAN card, or passport (clear scan)', 'is_mandatory': True,  'order': 1},
        {'name': 'Academic Transcript',    'description': 'Official marksheet of the previous academic year',  'is_mandatory': True,  'order': 2},
        {'name': 'Income Certificate',     'description': 'Family income certificate issued by competent authority', 'is_mandatory': True, 'order': 3},
        {'name': 'Proof of Enrollment',    'description': 'Bonafide certificate or college ID card',            'is_mandatory': True,  'order': 4},
        {'name': 'Recommendation Letter',  'description': 'From a faculty member or HOD',                      'is_mandatory': False, 'order': 5},
    ],
    # Need-Based Grant
    [
        {'name': 'Identity Document',   'description': 'Any government-issued photo ID',                     'is_mandatory': True,  'order': 1},
        {'name': 'Income Certificate',  'description': 'Issued by a revenue officer (Tehsildar or above)',   'is_mandatory': True,  'order': 2},
        {'name': 'Proof of Enrollment', 'description': 'Bonafide certificate from your institution',         'is_mandatory': True,  'order': 3},
        {'name': 'Academic Transcript', 'description': 'Latest marksheet',                                   'is_mandatory': True,  'order': 4},
        {'name': 'Bank Passbook Copy',  'description': 'First page showing account details (optional)',      'is_mandatory': False, 'order': 5},
    ],
    # Women in Technology
    [
        {'name': 'Identity Document',   'description': 'Aadhaar or passport',                                'is_mandatory': True,  'order': 1},
        {'name': 'Academic Transcript', 'description': 'Previous year marksheet',                            'is_mandatory': True,  'order': 2},
        {'name': 'Proof of Enrollment', 'description': 'Bonafide certificate with course name',              'is_mandatory': True,  'order': 3},
        {'name': 'Income Certificate',  'description': 'Family income certificate (optional)',               'is_mandatory': False, 'order': 4},
        {'name': 'Statement of Purpose','description': '500-word essay on career goals (PDF)',               'is_mandatory': True,  'order': 5},
    ],
]

for i, s_data in enumerate(scholarships):
    scholarship, created = Scholarship.objects.get_or_create(
        title=s_data['title'],
        defaults={**s_data, 'created_by': admin, 'is_active': True}
    )
    if created:
        print(f"[OK] Scholarship created: {scholarship.title}")
        for doc_data in doc_sets[i]:
            RequiredDocument.objects.create(scholarship=scholarship, **doc_data)
        print(f"     -> {len(doc_sets[i])} required documents added.")
    else:
        print(f"[INFO] Scholarship already exists: {scholarship.title}")

print("\n=== Setup Complete ===")
print("\nRun the server:  python manage.py runserver")
print("Visit:           http://127.0.0.1:8000/")
print("\nDemo accounts (local development only):")
print("  Admin   -> username: admin     / password: Admin@1234")
print("  Student -> username: student1  / password: Student@1234")
print("\nWARNING: Change these passwords before any public or production deployment.")
