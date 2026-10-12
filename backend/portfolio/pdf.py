"""
Generates a standard, ATS-friendly single/multi-page CV (resume) PDF
directly from the Profile data stored in the database — no manual
upload required. Built with reportlab (pure Python, no system
dependencies), so it works the same in Docker as on a plain server.
"""
import io

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.lib.enums import TA_LEFT
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, HRFlowable, ListFlowable, ListItem,
)

# --- Brand colour (matches the site's accent) used sparingly for headings ---
ACCENT = colors.HexColor('#3730A3')   # indigo-800 — reads fine in B&W print too
INK = colors.HexColor('#111827')      # near-black body text
MUTED = colors.HexColor('#4B5563')    # grey for meta text (dates, location)


def _styles():
    base = getSampleStyleSheet()
    styles = {
        'name': ParagraphStyle(
            'CVName', parent=base['Title'], fontName='Helvetica-Bold',
            fontSize=22, leading=26, textColor=INK, spaceAfter=2,
        ),
        'title': ParagraphStyle(
            'CVTitle', parent=base['Normal'], fontName='Helvetica',
            fontSize=12.5, leading=16, textColor=ACCENT, spaceAfter=6,
        ),
        'contact': ParagraphStyle(
            'CVContact', parent=base['Normal'], fontName='Helvetica',
            fontSize=9.5, leading=13, textColor=MUTED, spaceAfter=0,
        ),
        'section': ParagraphStyle(
            'CVSection', parent=base['Heading2'], fontName='Helvetica-Bold',
            fontSize=11.5, leading=14, textColor=ACCENT, spaceBefore=14,
            spaceAfter=4, letterSpacing=0.6,
        ),
        'body': ParagraphStyle(
            'CVBody', parent=base['Normal'], fontName='Helvetica',
            fontSize=10, leading=14, textColor=INK, alignment=TA_LEFT,
        ),
        'itemTitle': ParagraphStyle(
            'CVItemTitle', parent=base['Normal'], fontName='Helvetica-Bold',
            fontSize=10.5, leading=13, textColor=INK,
        ),
        'itemMeta': ParagraphStyle(
            'CVItemMeta', parent=base['Normal'], fontName='Helvetica-Oblique',
            fontSize=9.5, leading=13, textColor=MUTED,
        ),
        'bullet': ParagraphStyle(
            'CVBullet', parent=base['Normal'], fontName='Helvetica',
            fontSize=9.5, leading=13.5, textColor=INK,
        ),
    }
    return styles


def _rule():
    return HRFlowable(width='100%', thickness=0.8, color=colors.HexColor('#D1D5DB'),
                       spaceBefore=2, spaceAfter=8)


def _escape(text):
    """Minimal XML-escaping so user-entered text can't break ReportLab's markup parser."""
    if not text:
        return ''
    return (
        str(text)
        .replace('&', '&amp;')
        .replace('<', '&lt;')
        .replace('>', '&gt;')
    )


def _bullets_from_description(description, styles):
    """
    Experience/Project descriptions are stored as free text, often with
    '- ' prefixed lines. Render each non-empty line as its own bullet;
    if there are no '- ' lines, fall back to one paragraph.
    """
    if not description:
        return []
    lines = [l.strip(' -') for l in description.split('\n') if l.strip()]
    if not lines:
        return []
    items = [
        ListItem(Paragraph(_escape(line), styles['bullet']), leftIndent=0, spaceAfter=2)
        for line in lines
    ]
    return [ListFlowable(items, bulletType='bullet', start='•',
                          leftIndent=14, bulletFontSize=8, spaceAfter=4)]


def generate_cv_pdf(profile):
    """Builds the CV PDF for the given Profile instance and returns raw PDF bytes."""
    buf = io.BytesIO()
    doc = SimpleDocTemplate(
        buf, pagesize=A4,
        topMargin=18 * mm, bottomMargin=16 * mm,
        leftMargin=18 * mm, rightMargin=18 * mm,
        title=f"{profile.full_name} - CV",
        author=profile.full_name,
    )
    styles = _styles()
    story = []

    # --- Header: name, title, contact line ---
    story.append(Paragraph(_escape(profile.full_name), styles['name']))
    if profile.title:
        story.append(Paragraph(_escape(profile.title), styles['title']))

    contact_bits = []
    if profile.email:
        contact_bits.append(profile.email)
    if profile.phone:
        contact_bits.append(profile.phone)
    if profile.address:
        contact_bits.append(profile.address)
    for url in [profile.website_url, profile.linkedin_url, profile.github_url]:
        if url:
            contact_bits.append(url.replace('https://', '').replace('http://', ''))
    if contact_bits:
        story.append(Paragraph(_escape('   |   '.join(contact_bits)), styles['contact']))

    story.append(Spacer(1, 10))
    story.append(_rule())

    # --- Summary ---
    if profile.bio:
        story.append(Paragraph('SUMMARY', styles['section']))
        story.append(Paragraph(_escape(profile.bio), styles['body']))

    # --- Experience ---
    experience = list(profile.experience.all())
    if experience:
        story.append(Paragraph('EXPERIENCE', styles['section']))
        story.append(_rule())
        for exp in experience:
            left = f"{_escape(exp.role)} — {_escape(exp.company)}"
            right = f"{_escape(exp.start_date)} – {_escape(exp.end_date) or 'Present'}"
            story.append(Paragraph(left, styles['itemTitle']))
            meta_line = right if not exp.location else f"{right}   |   {_escape(exp.location)}"
            story.append(Paragraph(meta_line, styles['itemMeta']))
            story.extend(_bullets_from_description(exp.description, styles))
            story.append(Spacer(1, 6))

    # --- Education ---
    education = list(profile.education.all())
    if education:
        story.append(Paragraph('EDUCATION', styles['section']))
        story.append(_rule())
        for edu in education:
            degree_line = _escape(edu.degree)
            if edu.field_of_study:
                degree_line += f" — {_escape(edu.field_of_study)}"
            story.append(Paragraph(degree_line, styles['itemTitle']))
            years = f"{_escape(edu.start_year)} – {_escape(edu.end_year) or 'Present'}"
            inst_line = f"{_escape(edu.institution)}   |   {years}"
            if edu.result:
                inst_line += f"   |   {_escape(edu.result)}"
            story.append(Paragraph(inst_line, styles['itemMeta']))
            if edu.description:
                story.append(Paragraph(_escape(edu.description), styles['body']))
            story.append(Spacer(1, 6))

    # --- Skills ---
    categories = list(profile.skill_categories.all())
    if categories:
        story.append(Paragraph('SKILLS', styles['section']))
        story.append(_rule())
        for cat in categories:
            skill_names = [s.name for s in cat.skills.all()]
            if not skill_names:
                continue
            line = f"<b>{_escape(cat.name)}:</b> {_escape(', '.join(skill_names))}"
            story.append(Paragraph(line, styles['body']))
            story.append(Spacer(1, 3))

    # --- Projects (featured first, capped so the CV stays concise) ---
    projects = list(profile.projects.all())
    if projects:
        projects = sorted(projects, key=lambda p: (not p.featured, p.order))[:5]
        story.append(Paragraph('PROJECTS', styles['section']))
        story.append(_rule())
        for proj in projects:
            story.append(Paragraph(_escape(proj.title), styles['itemTitle']))
            if proj.tech_stack:
                story.append(Paragraph(_escape(proj.tech_stack), styles['itemMeta']))
            if proj.description:
                story.append(Paragraph(_escape(proj.description), styles['body']))
            link = proj.live_url or proj.repo_url
            if link:
                story.append(Paragraph(_escape(link), styles['itemMeta']))
            story.append(Spacer(1, 6))

    doc.build(story)
    return buf.getvalue()
