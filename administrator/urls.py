from django.urls import path
from . import views

app_name = 'administrator'

urlpatterns = [
    path('',                                    views.dashboard,             name='dashboard'),
    path('applications/<int:pk>/review/',       views.review_application,    name='review_application'),
    path('scholarships/',                       views.manage_scholarships,   name='manage_scholarships'),
    path('scholarships/create/',                views.create_scholarship,    name='create_scholarship'),
    path('scholarships/<int:pk>/edit/',         views.edit_scholarship,      name='edit_scholarship'),
    path('scholarships/<int:pk>/toggle/',       views.toggle_scholarship,    name='toggle_scholarship'),
    path('scholarships/<int:scholarship_pk>/add-document/', views.add_required_document, name='add_required_document'),
    path('documents/<int:pk>/delete/',          views.delete_required_document, name='delete_required_document'),
]

