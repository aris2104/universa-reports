import sys, os
repo = r"C:\160WiFi Files\Automatisation_rapport\universa-reports\python-src"
if repo not in sys.path:
    sys.path.insert(0, repo)

from core.generator import generate_pdf

print('Calling generate_pdf...')
try:
    out_path = os.path.join(os.getcwd(), 'Rapport_Test_User.pdf')
    generate_pdf(
        doc_type='Rapport de Stage',
        domain='Cybersécurité',
        title='Test Report',
        student_name='Test User',
        supervisor_name='Tuteur Test',
        institution='Université Test',
        company_name='ACME SARL',
        period_start='01/06/2026',
        period_end='30/06/2026',
        generated_date='27/07/2026',
        output_path=out_path
    )
    print('generate_pdf completed, output:', out_path)
except Exception as e:
    import traceback
    print('ERROR:', e)
    traceback.print_exc()
    raise
