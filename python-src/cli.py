import os
import sys
import time
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from rich.text import Text

console = Console()

# ==========================================
# 🌐 DICTIONNAIRE DES TRADUCTIONS (I18N)
# ==========================================
MESSAGES = {
    'fr': {
        'title': "UNIVERSA REPORTS",
        'subtitle': "Le générateur de rapports académiques professionnels",
        'author': "Développé par PEREIRA ARISTIDE BIMAM KPESS",
        'select_type': "Quel type de document souhaitez-vous générer ?",
        'types': ["Rapport de Stage", "Compte-Rendu de TP", "Rapport de Projet", "Quitter"],
        'select_domain': "Sélectionnez votre domaine d'études :",
        'domains': ["Cybersécurité", "Développement Logiciel", "Général"],
        'step1': "Étape 1 : Type de document",
        'step2': "Étape 2 : Domaine d'études",
        'step3': "Étape 3 : Informations générales",
        'enter_title': "Titre du rapport",
        'enter_student': "Nom complet de l'étudiant",
        'enter_supervisor': "Nom de l'encadrant / professeur",
        'enter_institution': "Nom de l'établissement / université",
        'summary': "Récapitulatif",
        'generating': "Génération du rapport PDF en cours...",
        'success': "Rapport généré avec succès !",
        'cancel': "Opération annulée. À bientôt !",
        'choice': "Votre choix"
    },
    'en': {
        'title': "UNIVERSA REPORTS",
        'subtitle': "The Ultimate Academic Report Generator",
        'author': "Created by PEREIRA ARISTIDE BIMAM KPESS",
        'select_type': "What type of document do you want to generate?",
        'types': ["Internship Report", "Lab Work (TP) Report", "Project Report", "Quit"],
        'select_domain': "Select your study domain:",
        'domains': ["Cybersecurity", "Software Development", "Generic"],
        'step1': "Step 1: Document Type",
        'step2': "Step 2: Study Domain",
        'step3': "Step 3: General Information",
        'enter_title': "Report title",
        'enter_student': "Student's full name",
        'enter_supervisor': "Supervisor / Professor name",
        'enter_institution': "Institution / University name",
        'summary': "Summary",
        'generating': "Generating PDF report...",
        'success': "Report generated successfully!",
        'cancel': "Operation cancelled. See you soon!",
        'choice': "Your choice"
    }
}

def display_banner(lang_code='fr'):
    """Affiche la bannière d'accueil"""
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

def main():
    console.clear()

    # 1. Choix de la langue
    console.print(
        Panel(
            "[bold cyan]🌐 Langue / Language[/bold cyan]\n\n"
            "  [bold green]1.[/bold green] Français\n"
            "  [bold green]2.[/bold green] English",
            border_style="magenta",
            expand=False
        )
    )
    
    lang_choice = Prompt.ask(
        "Votre choix / Your choice",
        choices=["1", "2"],
        default="1"
    )

    lang = 'fr' if lang_choice == "1" else 'en'
    msg = MESSAGES[lang]

    console.clear()
    display_banner(lang)

    # 2. Choix du type de rapport
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

    # 3. Choix du domaine
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

    # 4. Saisie des informations
    console.print(f"\n[bold green]✍️ {msg['step3']}[/bold green]\n")
    
    title = Prompt.ask(f" • {msg['enter_title']}")
    student_name = Prompt.ask(f" • {msg['enter_student']}")
    supervisor_name = Prompt.ask(f" • {msg['enter_supervisor']}")
    institution = Prompt.ask(f" • {msg['enter_institution']}")

    # 5. Récapitulatif
    console.print(f"\n[bold cyan]⚡ {msg['summary']}[/bold cyan]")
    console.print(f"  • Type : [bold]{doc_type}[/bold]")
    console.print(f"  • Domaine : [bold]{domain}[/bold]")
    console.print(f"  • Titre : {title}")
    console.print(f"  • Auteur : {student_name}")
    console.print(f"  • Établissement : {institution}")

    # 6. Génération réelle du PDF
    console.print()
    with console.status(f"[bold green]{msg['generating']}[/bold green]", spinner="dots"):
        try:
            from core.generator import generate_pdf
            
            clean_name = student_name.replace(' ', '_').strip() or "Etudiant"
            pdf_filename = f"Rapport_{clean_name}.pdf"
            output_path = os.path.join(os.getcwd(), pdf_filename)

            generate_pdf(
                doc_type=doc_type,
                domain=domain,
                title=title,
                student_name=student_name,
                supervisor_name=supervisor_name,
                institution=institution,
                lang=lang,
                output_path=output_path
            )

            console.print(f"\n[bold green]✨ {msg['success']}[/bold green]")
            console.print(f"[bold cyan]📄 Fichier disponible ici :[/bold cyan] [underline]{output_path}[/underline]\n")

        except Exception as e:
            console.print(f"\n[bold red]✘ Erreur lors de la génération du PDF :[/bold red] {e}\n")
            sys.exit(1)

if __name__ == "__main__":
    main()