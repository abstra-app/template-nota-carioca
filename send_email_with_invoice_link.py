from abstra.messages import *
from abstra.workflows import *
from abstra.tasks import get_trigger_task

task = get_trigger_task()
invoice_data = task.get_payload()

recipient_email = invoice_data.get("recipient_email")
invoice_link = invoice_data.get("invoice_link")

def send_email_with_invoice_link(invoice_link, recipient_email):
    send_email(
        title="Nota Fiscal de Serviço",
        message=f"Segue o link para download da sua nota fiscal de serviço: {invoice_link}",
        to=recipient_email
    )

if invoice_link and recipient_email:
    print('Send Email')
    send_email_with_invoice_link(invoice_link, recipient_email)
    task.complete()