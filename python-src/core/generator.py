import os
import unicodedata
from jinja2 import Environment, FileSystemLoader
from weasyprint import HTML

def clean_str(text):
    """Enlève les accents et met en minuscules pour comparer facilement."""
    if not text:
        return ""
    text = text.lower().strip()
    text = unicodedata.normalize('NFD', text)
    return ''.join(c for c in text if unicodedata.category(c) != 'Mn')

def generate_pdf(doc_type, domain, title, student_name, supervisor_name, institution, lang, output_path):
    """
    Génère le PDF en sélectionnant le template exact selon le type et le domaine.
    """
    # 1. Chemin vers le dossier templates (python-src/templates)
    current_dir = os.path.dirname(os.path.abspath(__file__))  # core
    base_dir = os.path.dirname(current_dir)                  # python-src
    templates_dir = os.path.join(base_dir, 'templates')

    # 2. Choix du sous-dossier (stage ou tp)
    doc_clean = clean_str(doc_type)
    if "tp" in doc_clean or "lab" in doc_clean:
        sub_folder = "tp"
    else:
        sub_folder = "stage"

    target_dir = os.path.join(templates_dir, sub_folder)

    # 3. Choix du fichier HTML selon le domaine
    domain_clean = clean_str(domain)
    
    if "cyber" in domain_clean or "securite" in domain_clean:
        template_filename = "cybersecurity.html"
    elif "dev" in domain_clean or "program" in domain_clean or "code" in domain_clean:
        template_filename = "development.html"
    else:
        template_filename = "generic.html"

    # Vérification de sécurité : si le fichier spécifique n'existe pas, fallback sur generic.html
    full_template_path = os.path.join(target_dir, template_filename)
    if not os.path.exists(full_template_path):
        template_filename = "generic.html"

    # 4. Rendu Jinja2
    env = Environment(loader=FileSystemLoader(target_dir))
    template = env.get_template(template_filename)

    rendered_html = template.render(
        doc_type=doc_type,
        domain=domain,
        title=title,
        student_name=student_name,
        supervisor_name=supervisor_name,
        institution=institution,
        lang=lang
    )

    # 5. Écriture du PDF avec WeasyPrint
    html_obj = HTML(string=rendered_html, base_url=target_dir)
    with open(output_path, 'wb') as f:
        html_obj.write_pdf(f)