from abstra.messages import *
from abstra.workflows import *

recipient_email = get_data("recipient_email")
invoice_link = get_data("invoice_link")

print(f"Recipient email: {recipient_email}")

def send_email_with_invoice_link(invoice_link, recipient_email):
    send_email(
        title="Nota Fiscal de Serviço",
        message=f"Segue o link para download da sua nota fiscal de serviço: {invoice_link}",
        to=recipient_email
    )

if invoice_link and recipient_email:
    send_email_with_invoice_link(invoice_link, recipient_email)