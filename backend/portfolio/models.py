from django.db import models


class Profile(models.Model):
    """Singleton-style profile / bio-data. Only one row is meant to exist."""
    full_name = models.CharField(max_length=150)
    title = models.CharField(max_length=200, help_text="e.g. Full Stack Web Developer")
    tagline = models.CharField(max_length=250, blank=True, help_text="Short one-liner shown under your name")
    bio = models.TextField(help_text="A short paragraph about yourself")
    email = models.EmailField()
    phone = models.CharField(max_length=30, blank=True)
    address = models.CharField(max_length=200, blank=True)
    photo = models.ImageField(upload_to='profile/', blank=True, null=True)
    cv_file = models.FileField(
        upload_to='cv/', blank=True, null=True,
        help_text=(
            "Optional. Upload your own designed CV PDF here if you want it served "
            "as-is. If left empty, the Download CV button automatically serves a "
            "standard CV generated from the information below (education, "
            "experience, skills, projects) — no upload required."
        ),
    )

    github_url = models.URLField(blank=True)
    linkedin_url = models.URLField(blank=True)
    facebook_url = models.URLField(blank=True)
    twitter_url = models.URLField(blank=True)
    website_url = models.URLField(blank=True)

    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.full_name


class Education(models.Model):
    profile = models.ForeignKey(Profile, related_name='education', on_delete=models.CASCADE)
    institution = models.CharField(max_length=200)
    degree = models.CharField(max_length=200, help_text="e.g. B.Sc. in Computer Science")
    field_of_study = models.CharField(max_length=200, blank=True)
    start_year = models.CharField(max_length=10)
    end_year = models.CharField(max_length=10, blank=True, help_text="Leave blank if ongoing")
    result = models.CharField(max_length=50, blank=True, help_text="e.g. CGPA 3.80/4.00")
    description = models.TextField(blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order', '-start_year']

    def __str__(self):
        return f"{self.degree} - {self.institution}"


class Experience(models.Model):
    profile = models.ForeignKey(Profile, related_name='experience', on_delete=models.CASCADE)
    company = models.CharField(max_length=200)
    role = models.CharField(max_length=200)
    location = models.CharField(max_length=150, blank=True)
    start_date = models.CharField(max_length=20, help_text="e.g. Jan 2024")
    end_date = models.CharField(max_length=20, blank=True, help_text="Leave blank if 'Present'")
    description = models.TextField(blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order', '-start_date']

    def __str__(self):
        return f"{self.role} @ {self.company}"


class SkillCategory(models.Model):
    profile = models.ForeignKey(Profile, related_name='skill_categories', on_delete=models.CASCADE)
    name = models.CharField(max_length=100, help_text="e.g. Languages, Frameworks, Tools")
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.name


class Skill(models.Model):
    category = models.ForeignKey(SkillCategory, related_name='skills', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    proficiency = models.PositiveSmallIntegerField(default=80, help_text="0-100, used for the skill bar")
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order', 'name']

    def __str__(self):
        return self.name


class Project(models.Model):
    profile = models.ForeignKey(Profile, related_name='projects', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()
    tech_stack = models.CharField(max_length=300, help_text="Comma separated, e.g. Django, React, PostgreSQL")
    image = models.ImageField(upload_to='projects/', blank=True, null=True)
    live_url = models.URLField(blank=True)
    repo_url = models.URLField(blank=True)
    featured = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order', '-id']

    def __str__(self):
        return self.title

    def tech_list(self):
        return [t.strip() for t in self.tech_stack.split(',') if t.strip()]


class ContactMessage(models.Model):
    """Messages submitted through the site's contact form."""
    name = models.CharField(max_length=150)
    email = models.EmailField()
    subject = models.CharField(max_length=200, blank=True)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} <{self.email}> - {self.subject or 'No subject'}"
