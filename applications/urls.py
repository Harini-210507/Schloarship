from django.urls import path
from . import views

app_name = 'applications'

urlpatterns = [
    path('apply/<int:scholarship_pk>/',       views.apply,              name='apply'),
    path('<int:pk>/upload/',                  views.upload_documents,   name='upload_documents'),
    path('<int:pk>/status/',                  views.application_status, name='status'),
    path('my/<int:scholarship_pk>/',          views.my_application,     name='my_application'),
]

