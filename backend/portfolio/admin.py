from django.contrib import admin
from .models import (
    Profile, Education, Experience, SkillCategory, Skill, Project, ContactMessage,
)


class EducationInline(admin.TabularInline):
    model = Education
    extra = 1


class ExperienceInline(admin.TabularInline):
    model = Experience
    extra = 1


class ProjectInline(admin.TabularInline):
    model = Project
    extra = 1


class SkillCategoryInline(admin.TabularInline):
    model = SkillCategory
    extra = 1


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'title', 'email', 'updated_at')
    inlines = [EducationInline, ExperienceInline, SkillCategoryInline, ProjectInline]


@admin.register(SkillCategory)
class SkillCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'profile')


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'proficiency')


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'featured', 'profile')
    list_filter = ('featured',)


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'created_at', 'is_read')
    list_filter = ('is_read',)
    readonly_fields = ('name', 'email', 'subject', 'message', 'created_at')
