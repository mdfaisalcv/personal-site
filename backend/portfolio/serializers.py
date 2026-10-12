from rest_framework import serializers
from .models import (
    Profile, Education, Experience, SkillCategory, Skill, Project, ContactMessage,
)


class EducationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Education
        fields = [
            'id', 'institution', 'degree', 'field_of_study',
            'start_year', 'end_year', 'result', 'description',
        ]


class ExperienceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Experience
        fields = [
            'id', 'company', 'role', 'location',
            'start_date', 'end_date', 'description',
        ]


class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = ['id', 'name', 'proficiency']


class SkillCategorySerializer(serializers.ModelSerializer):
    skills = SkillSerializer(many=True, read_only=True)

    class Meta:
        model = SkillCategory
        fields = ['id', 'name', 'skills']


class ProjectSerializer(serializers.ModelSerializer):
    tech_list = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = [
            'id', 'title', 'description', 'tech_stack', 'tech_list',
            'image', 'live_url', 'repo_url', 'featured',
        ]

    def get_tech_list(self, obj):
        return obj.tech_list()


class ProfileSerializer(serializers.ModelSerializer):
    education = EducationSerializer(many=True, read_only=True)
    experience = ExperienceSerializer(many=True, read_only=True)
    skill_categories = SkillCategorySerializer(many=True, read_only=True)
    projects = ProjectSerializer(many=True, read_only=True)

    class Meta:
        model = Profile
        fields = [
            'id', 'full_name', 'title', 'tagline', 'bio',
            'email', 'phone', 'address', 'photo', 'cv_file',
            'github_url', 'linkedin_url', 'facebook_url', 'twitter_url', 'website_url',
            'education', 'experience', 'skill_categories', 'projects',
        ]


class ContactMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactMessage
        fields = ['id', 'name', 'email', 'subject', 'message', 'created_at']
        read_only_fields = ['id', 'created_at']
