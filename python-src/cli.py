#!/usr/bin/env python3
"""
Universa Reports — CLI interactif
----------------------------------
Philosophie : on ne demande à l'utilisateur QUE ce qui est réellement
indispensable pour identifier son document (dates, entreprise, module,
groupe...). Tout le reste possède déjà des valeurs par défaut pertinentes.
"""

import os
import sys
from datetime import datetime
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from rich.text import Text

console = Console()

# ------------------------------------------------------------------ #
# Correspondances
# ------------------------------------------------------------------ #

DOMAIN_SLUGS = {
    "Cybersécurité": "cybersecurite",
    "Cybersecurity": "cybersecurite",
    "Développement Logiciel": "developpement",
    "Software Development": "developpement",
    "Général": "generique",
    "Generic": "generique",
}

TYPE_KEY_MAP = {
    "Compte-Rendu de TP": "tp",
    "Lab Work (TP) Report": "tp",
    "Rapport de Stage": "stage",
    "Internship Report": "stage",
    "Rapport de Projet": "project",
    "Project Report": "project",
}

MESSAGES = {
    'fr': {
        'title': "UNIVERSA REPORTS",
        'subtitle': "Le générateur de rapports académiques professionnels",
        'author': "Développé par PEREIRA ARISTIDE BIMAM KPESS",
        'select_type': "Quel type de document souhaitez-vous générer ?",
        'types': ["Compte-Rendu de TP", "Rapport de Stage", "Rapport de Projet", "Quitter"],
        'select_domain': "Sélectionnez votre domaine d'études :",
        'domains': ["Cybersécurité", "Développement Logiciel", "Général"],
        'step1': "Étape 1 : Type de document",
        'step2': "Étape 2 : Domaine d'études",
        'step3': "Étape 3 : Identification",
        'step4': "Étape 4 : Informations essentielles",
        'step5': "Étape 5 : Informations complémentaires (Optionnel)",
        'enter_title': "Titre du rapport",
        'enter_student': "Nom complet de l'étudiant",
        'enter_supervisor': "Nom de l'encadrant / professeur",
        'enter_institution': "Nom de l'établissement / université",
        'summary': "Récapitulatif",
        'generating': "Génération du rapport PDF en cours...",
        'success': "Rapport généré avec succès !",
        'cancel': "Opération annulée. À bientôt !",
        'choice': "Votre choix",
        'default_note': "Astuce : tout ce qui n'est pas demandé ici est pré-rempli "
                         "avec un contenu type dans le PDF. Il vous suffira de "
                         "l'éditer.",
    },
    'en': {
        'title': "UNIVERSA REPORTS",
        'subtitle': "The Ultimate Academic Report Generator",
        'author': "Created by PEREIRA ARISTIDE BIMAM KPESS",
        'select_type': "What type of document do you want to generate?",
        'types': ["Lab Work (TP) Report", "Internship Report", "Project Report", "Quit"],
        'select_domain': "Select your study domain:",
        'domains': ["Cybersecurity", "Software Development", "Generic"],
        'step1': "Step 1: Document Type",
        'step2': "Step 2: Study Domain",
        'step3': "Step 3: Identification",
        'step4': "Step 4: Essential Information",
        'step5': "Step 5: Additional Information (Optional)",
        'enter_title': "Report title",
        'enter_student': "Student's full name",
        'enter_supervisor': "Supervisor / Professor name",
        'enter_institution': "Institution / University name",
        'summary': "Summary",
        'generating': "Generating PDF report...",
        'success': "Report generated successfully!",
        'cancel': "Operation cancelled. See you soon!",
        'choice': "Your choice",
        'default_note': "Tip: anything not asked here is already pre-filled "
                         "with sensible placeholder content in the PDF. Just edit it.",
    }
}

ESSENTIAL_FIELDS = {
    'fr': {
        "tp": [
            ("module_name", "Module / UE concerné", None),
            ("tp_title", "Titre du TP", None),
            ("group_name", "Groupe / binôme", "Individuel"),
            ("session_date", "Date de la séance (JJ/MM/AAAA)", None),
        ],
        "stage": [
            ("company_name", "Entreprise / structure d'accueil", None),
            ("tutor_name", "Tuteur en entreprise", None),
            ("period_start", "Date de début de stage (JJ/MM/AAAA)", None),
            ("period_end", "Date de fin de stage (JJ/MM/AAAA)", None),
        ],
        "project": [
            ("report_title", "Titre du projet", None),
            ("company_name", "Client / commanditaire (si applicable)", "N/A"),
            ("period_start", "Date de début du projet (JJ/MM/AAAA)", None),
            ("period_end", "Date de fin du projet (JJ/MM/AAAA)", None),
        ],
    },
    'en': {
        "tp": [
            ("module_name", "Related module / course", None),
            ("tp_title", "Lab work title", None),
            ("group_name", "Group / pair", "Individual"),
            ("session_date", "Session date (DD/MM/YYYY)", None),
        ],
        "stage": [
            ("company_name", "Host company / organization", None),
            ("tutor_name", "Company supervisor", None),
            ("period_start", "Internship start date (DD/MM/YYYY)", None),
            ("period_end", "Internship end date (DD/MM/YYYY)", None),
        ],
        "project": [
            ("report_title", "Project title", None),
            ("company_name", "Client / sponsor (if applicable)", "N/A"),
            ("period_start", "Project start date (DD/MM/YYYY)", None),
            ("period_end", "Project end date (DD/MM/YYYY)", None),
        ],
    },
}


def display_banner(lang_code='fr'):
    msg = MESSAGES[lang_code]
    banner_text = Text()
    banner_text.append(f"{msg['title']}\n", style="bold cyan")
    banner_text.append(f"{msg['subtitle']}\n", style="italic white")
    banner_text.append(f"{msg['author']}", style="dim yellow")

    console.print(
        Panel(
            banner_text,
            border_style="bright_blue",
            padding=(1, 4),
            expand=False
        )
    )


def ask_essential_fields(lang: str, type_key: str) -> dict:
    msg = MESSAGES[lang]
    fields = ESSENTIAL_FIELDS[lang].get(type_key, [])

    console.print(f"\n[bold green]🎯 {msg['step4']}[/bold green]")
    console.print(f"[dim italic]{msg['default_note']}[/dim italic]\n")

    collected = {}
    for key, label, default in fields:
        value = Prompt.ask(f" • {label}", default=default) if default is not None \
            else Prompt.ask(f" • {label}")
        collected[key] = value
    return collected


def main():
    console.clear()

    # 1. Langue
    console.print(
        Panel(
            "[bold cyan]🌐 Langue / Language[/bold cyan]\n\n"
            "  [bold green]1.[/bold green] Français\n"
            "  [bold green]2.[/bold green] English",
            border_style="magenta",
            expand=False
        )
    )

    lang_choice = Prompt.ask("Votre choix / Your choice", choices=["1", "2"], default="1")
    lang = 'fr' if lang_choice == "1" else 'en'
    msg = MESSAGES[lang]

    console.clear()
    display_banner(lang)

    # 2. Type de rapport
    console.print(f"\n[bold green]📋 {msg['step1']}[/bold green]")
    console.print(f"[italic]{msg['select_type']}[/italic]\n")

    types_list = msg['types']
    for idx, t in enumerate(types_list, 1):
        console.print(f"  [bold cyan]{idx}.[/bold cyan] {t}")

    type_choice = Prompt.ask(
        f"\n{msg['choice']}",
        choices=[str(i) for i in range(1, len(types_list) + 1)],
        default="1"
    )
    doc_type = types_list[int(type_choice) - 1]

    if doc_type in ["Quitter", "Quit"]:
        console.print(f"\n[yellow]{msg['cancel']}[/yellow]\n")
        sys.exit(0)

    type_key = TYPE_KEY_MAP.get(doc_type, "stage")

    # 3. Domaine
    console.print(f"\n[bold green]📌 {msg['step2']}[/bold green]")
    console.print(f"[italic]{msg['select_domain']}[/italic]\n")

    domains_list = msg['domains']
    for idx, d in enumerate(domains_list, 1):
        console.print(f"  [bold cyan]{idx}.[/bold cyan] {d}")

    domain_choice = Prompt.ask(
        f"\n{msg['choice']}",
        choices=[str(i) for i in range(1, len(domains_list) + 1)],
        default="1"
    )
    domain = domains_list[int(domain_choice) - 1]
    domain_slug = DOMAIN_SLUGS.get(domain, "generique")

    # 4. Identification minimale
    console.print(f"\n[bold green]✍️  {msg['step3']}[/bold green]\n")
    student_name = Prompt.ask(f" • {msg['enter_student']}")
    institution = Prompt.ask(f" • {msg['enter_institution']}")
    supervisor_name = Prompt.ask(f" • {msg['enter_supervisor']}")

    title = ""
    if type_key != "project":
        title = Prompt.ask(f" • {msg['enter_title']}", default="")

    # 5. Champs essentiels spécifiques
    essential = ask_essential_fields(lang, type_key)

    # 6. Champs optionnels (SAISIS AVANT LA GÉNÉRATION DU PDF)
    console.print(f"\n[bold green]⚙️  {msg['step5']}[/bold green]\n")
    student_number = Prompt.ask(" • Numéro étudiant", default="")
    submission_date = Prompt.ask(" • Date de soumission (JJ/MM/AAAA)", default=datetime.now().strftime("%d/%m/%Y"))
    abstract = Prompt.ask(" • Résumé (150-300 mots) — laissez vide pour le texte par défaut", default="")
    keywords = Prompt.ask(" • Mots-clés (séparés par des virgules)", default="")
    logo_path = Prompt.ask(" • Chemin vers le logo (optionnel)", default="")

    # 7. Récapitulatif
    console.print(f"\n[bold cyan]⚡ {msg['summary']}[/bold cyan]")
    console.print(f"  • Type : [bold]{doc_type}[/bold]")
    console.print(f"  • Domaine : [bold]{domain}[/bold] (Thème CSS: [italic]domain-{domain_slug}[/italic])")
    console.print(f"  • Étudiant(e) : {student_name}")
    for key, value in essential.items():
        console.print(f"  • {key} : {value}")

    # 8. Préparation des données
    clean_name = student_name.replace(' ', '_').strip() or "Etudiant"
    pdf_filename = f"Rapport_{clean_name}.pdf"
    output_path = os.path.join(os.getcwd(), pdf_filename)

    keywords_list = [k.strip() for k in keywords.split(",") if k.strip()] if keywords else []

    context_data = {
        "doc_type": doc_type,
        "domain": domain,
        "domain_slug": domain_slug,
        "title": title,
        "student_name": student_name,
        "student_number": student_number,
        "supervisor_name": supervisor_name,
        "institution": institution,
        "submission_date": submission_date,
        "abstract": abstract,
        "keywords": keywords,
        "keywords_list": keywords_list,
        "logo_path": logo_path,
        "lang": lang,
        **essential,
    }

    context_data.setdefault("generated_date", submission_date or datetime.now().strftime("%d/%m/%Y"))

    # 9. Génération du PDF (Génération pure dans le spinner)
    console.print()
    with console.status(f"[bold green]{msg['generating']}[/bold green]", spinner="dots"):
        try:
            from core.generator import generate_pdf

            generate_pdf(
                **context_data,
                output_path=output_path
            )
        except Exception as e:
            console.print(f"\n[bold red]✘ Erreur lors de la génération du PDF :[/bold red] {e}\n")
            sys.exit(1)

    console.print(f"\n[bold green]✨ {msg['success']}[/bold green]")
    console.print(f"[bold cyan]📄 Fichier disponible ici :[/bold cyan] [underline]{output_path}[/underline]\n")


if __name__ == "__main__":
    main()