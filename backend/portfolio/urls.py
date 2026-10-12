from django.urls import path
from .views import (
    ProfileDetailView, ProjectListView, ContactMessageCreateView, CVDownloadView,
)

urlpatterns = [
    path('profile/', ProfileDetailView.as_view(), name='profile-detail'),
    path('projects/', ProjectListView.as_view(), name='project-list'),
    path('contact/', ContactMessageCreateView.as_view(), name='contact-create'),
    path('cv/download/', CVDownloadView.as_view(), name='cv-download'),
]
