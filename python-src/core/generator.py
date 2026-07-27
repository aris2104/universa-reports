"""Core package for report generation using WeasyPrint."""

import os
from datetime import datetime
from jinja2 import Environment, FileSystemLoader
from weasyprint import HTML, CSS

TYPE_FOLDERS = {
    "Rapport de Stage": "stage",
    "Internship Report": "stage",
    "Compte-Rendu de TP": "tp",
    "Lab Work (TP) Report": "tp",
    "Rapport de Projet": "project",
    "Project Report": "project",
}

DOMAIN_SLUGS = {
    "Cybersécurité": "cybersecurite",
    "Cybersecurity": "cybersecurite",
    "Développement Logiciel": "developpement",
    "Software Development": "developpement",
    "Général": "generique",
    "Generic": "generique",
}

TEMPLATE_FILE_SLUGS = {
    "Cybersécurité": "cybersecurity",
    "Cybersecurity": "cybersecurity",
    "Développement Logiciel": "development",
    "Software Development": "development",
    "Général": "generic",
    "Generic": "generic",
}


def resolve_template(templates_dir: str, doc_type: str, domain: str) -> str:
    """Trouve le template HTML approprié."""
    folder = TYPE_FOLDERS.get(doc_type, "stage")
    file_slug = TEMPLATE_FILE_SLUGS.get(domain, "generic")

    specific_rel = f"{folder}/{file_slug}.html"
    if os.path.exists(os.path.join(templates_dir, folder, f"{file_slug}.html")):
        return specific_rel

    generic_rel = f"{folder}/generic.html"
    if os.path.exists(os.path.join(templates_dir, folder, "generic.html")):
        return generic_rel

    return f"{folder}/generic.html"


def _parse_date(value: str):
    if not value:
        return None
    for fmt in ("%d/%m/%Y", "%Y-%m-%d"):
        try:
            return datetime.strptime(value, fmt)
        except (ValueError, TypeError):
            continue
    return None


def _fill_bridging_defaults(context: dict) -> dict:
    if not context.get("student_school") and context.get("institution"):
        context["student_school"] = context["institution"]
    if not context.get("institution") and context.get("student_school"):
        context["institution"] = context["student_school"]

    if not context.get("academic_tutor_name") and context.get("supervisor_name"):
        context["academic_tutor_name"] = context["supervisor_name"]

    if not context.get("duration_label"):
        start = _parse_date(context.get("period_start"))
        end = _parse_date(context.get("period_end"))
        if start and end and end >= start:
            days = (end - start).days
            weeks = max(1, round(days / 7))
            context["duration_label"] = f"{weeks} semaine{'s' if weeks > 1 else ''}"

    return context


def generate_pdf(
    doc_type: str = "Rapport de Stage",
    domain: str = "Cybersécurité",
    title: str = "",
    student_name: str = "",
    supervisor_name: str = "",
    institution: str = "",
    lang: str = "fr",
    output_path: str = "Rapport.pdf",
    **kwargs,
):
    """Génère le rapport PDF via WeasyPrint."""

    # core/ -> python-src/
    core_dir = os.path.dirname(os.path.abspath(__file__))
    python_src_dir = os.path.dirname(core_dir)

    # D'après ton VS Code : templates et assets sont sous python-src/
    templates_dir = os.path.join(python_src_dir, "templates")
    css_path = os.path.join(python_src_dir, "assets", "styles.css")

    template_rel_path = resolve_template(templates_dir, doc_type, domain)

    env = Environment(loader=FileSystemLoader(templates_dir))
    template = env.get_template(template_rel_path)

    domain_slug = DOMAIN_SLUGS.get(domain, "generique")

    context = {
        "doc_type": doc_type,
        "domain": domain,
        "domain_slug": domain_slug,
        "title": title,
        "student_name": student_name,
        "supervisor_name": supervisor_name,
        "institution": institution,
        "lang": lang,
        **kwargs,
    }

    context = _fill_bridging_defaults(context)

    if "toc_entries" not in context:
        context["toc_entries"] = [
            ("01", "Présentation de la structure d'accueil"),
            ("02", "Objectifs du stage"),
            ("03", "Missions réalisées"),
            ("04", "Outils et méthodes utilisés"),
            ("05", "Compétences développées"),
            ("06", "Difficultés rencontrées et solutions apportées"),
            ("07", "Conclusion"),
        ]

    rendered_html = template.render(**context)

    stylesheets = []
    if os.path.exists(css_path):
        stylesheets.append(CSS(filename=css_path))

    html_obj = HTML(string=rendered_html, base_url=templates_dir)
    html_obj.write_pdf(target=output_path, stylesheets=stylesheets)

    return output_path