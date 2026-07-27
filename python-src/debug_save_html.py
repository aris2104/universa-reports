import sys, os
repo = r"C:\160WiFi Files\Automatisation_rapport\universa-reports\python-src"
if repo not in sys.path:
    sys.path.insert(0, repo)

from jinja2 import Environment, FileSystemLoader
from core import generator

# base_dir should point to the python-src directory (repo)
base_dir = repo
templates_dir = os.path.join(base_dir, "templates")

# Choose the same type/domain the user selected in the CLI run
doc_type = "Rapport de Stage"
domain = "Développement Logiciel"

# Resolve template path
template_rel_path = generator.resolve_template(templates_dir, doc_type, domain)
env = Environment(loader=FileSystemLoader(templates_dir))
template = env.get_template(template_rel_path)

# Construct a safe context (use reasonable defaults rather than the RRRR placeholder garbage)
context = {
    "doc_type": doc_type,
    "domain": domain,
    "domain_slug": "developpement",
    "title": "Titre de test",
    "student_name": "TER",
    "student_number": "",
    "supervisor_name": "RRRRR",
    "institution": "RRRR",
    "submission_date": "27/07/2026",
    "abstract": "Résumé de test : ceci est un texte servant à vérifier le rendu du résumé dans le template.",
    "keywords": "cybersécurité, test",
    "keywords_list": ["cybersécurité", "test"],
    "logo_path": "",
    "lang": "fr",
    # essential fields for stage
    "company_name": "RRRRR",
    "tutor_name": "RRRRRRRR",
    "period_start": "01/06/2026",
    "period_end": "30/06/2026",
}

# Inline CSS like generator does
css_path = os.path.join(base_dir, "assets", "styles.css")
styles_inline = ""
if os.path.exists(css_path):
    try:
        with open(css_path, "r", encoding="utf-8") as f:
            styles_inline = f.read()
    except Exception:
        styles_inline = ""
context["styles_inline"] = styles_inline

rendered = template.render(**context)

out_path = r"C:\160WiFi Files\Automatisation_rapport\rendered_debug.html"
with open(out_path, "w", encoding="utf-8") as f:
    f.write(rendered)

print('Rendered HTML saved to:', out_path)
