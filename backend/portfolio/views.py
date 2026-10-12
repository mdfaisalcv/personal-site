from django.http import HttpResponse, FileResponse, Http404
from django.utils.text import slugify
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Profile, Project, ContactMessage
from .serializers import ProfileSerializer, ProjectSerializer, ContactMessageSerializer
from .pdf import generate_cv_pdf


class ProfileDetailView(APIView):
    """
    Returns the single profile (bio-data / CV) with all nested
    education, experience, skills and projects in one call.
    GET /api/profile/
    """

    def get(self, request):
        profile = Profile.objects.first()
        if not profile:
            return Response({'detail': 'Profile not set up yet.'}, status=404)
        serializer = ProfileSerializer(profile, context={'request': request})
        return Response(serializer.data)


class ProjectListView(generics.ListAPIView):
    """GET /api/projects/  (optionally ?featured=true)"""
    serializer_class = ProjectSerializer

    def get_queryset(self):
        qs = Project.objects.all()
        if self.request.query_params.get('featured') == 'true':
            qs = qs.filter(featured=True)
        return qs


class CVDownloadView(APIView):
    """
    GET /api/cv/download/

    Serves a downloadable CV PDF:
    - If the admin has uploaded a custom-designed CV file (Profile.cv_file),
      that file is served as-is.
    - Otherwise, a standard, ATS-friendly CV is generated on the fly from
      the Profile/Education/Experience/Skills/Projects data already in the
      database, so a downloadable CV is always available even before any
      file has been uploaded.
    """

    def get(self, request):
        profile = Profile.objects.first()
        if not profile:
            raise Http404('Profile not set up yet.')

        filename = f"{slugify(profile.full_name) or 'cv'}-CV.pdf"

        if profile.cv_file:
            try:
                return FileResponse(
                    profile.cv_file.open('rb'),
                    as_attachment=True,
                    filename=filename,
                    content_type='application/pdf',
                )
            except (FileNotFoundError, ValueError):
                pass  # fall through to the generated PDF below

        pdf_bytes = generate_cv_pdf(profile)
        response = HttpResponse(pdf_bytes, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        return response


class ContactMessageCreateView(generics.CreateAPIView):
    """POST /api/contact/  -- receives messages from the contact form"""
    queryset = ContactMessage.objects.all()
    serializer_class = ContactMessageSerializer
