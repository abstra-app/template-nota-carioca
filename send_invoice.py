from abstra.forms import *
from abstra.tables import *
from abstra.tasks import send_task
from abstra.common import get_persistent_dir

import requests
import os
import json
from decimal import Decimal
from datetime import datetime, date

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.serialization.pkcs12 import load_key_and_certificates
from lxml import etree
from jinja2 import Template
import xmlschema
from dotenv import load_dotenv

import flags
from templates import gerar, consultar, cancelar
from nota_carioca import NotaCarioca


load_dotenv()

env = 'sandbox' # Change to 'production' to send the invoice to the production environment

try:
    original_city_list = requests.get(
        'https://servicodados.ibge.gov.br/api/v1/localidades/municipios').json()
except:
    with open('arquivos/cities_code.json') as json_file:
        original_city_list = json.load(json_file)


with open('arquivos/countries_bacen_code.json') as json_file:
    original_country_list = json.load(json_file)

operation_nature_options = [
    {"label": "Tributação no município", "value": 1},
    {"label": "Tributação fora do município", "value": 2},
    {"label": "Isenção", "value": 3},
    {"label": "Imune", "value": 4},
    {"label": "Exigibilidade suspensa por decisão judicial", "value": 5},
    {"label": "Exigibilidade suspensa por procedimento Administrativo", "value": 6}
]

tax_regime_options = [
    {"label": "Microempresa Municipal", "value": 1},
    {"label": "Estimativa", "value": 2},
    {"label": "Sociedade Professional", "value": 3},
    {"label": "Cooperativa", "value": 4},
    {"label": "MEI - Microempresário Individual", "value": 5},
    {"label": "ME EPP - Microempresário e Empresa de Pequeno Porte", "value": 6}
]

rps_type_options = [
    {"label": "RPS", "value": 1},
    {"label": "Nota Conjugada", "value": 2},
    {"label": "Cupom", "value": 3}
]

def load_public_key(pfx_path: str, pfx_password: str) -> tuple:
    '''Read the public key from a PFX file and return as PEM encoded'''

    try:
        with open(pfx_path, 'rb') as f:
            pfx_data = f.read()

        private_key, certificate, _ = load_key_and_certificates(
            pfx_data, pfx_password.encode(), backend=default_backend()
        )

        private_key_pem = private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        )

        cert_pem = certificate.public_bytes(serialization.Encoding.PEM)

        return cert_pem, private_key_pem

    except Exception as e:
        display(f"Erro ao carregar a chave pública: {e}", end_program=True)
        return None, None

def convert_none_to_zero(value) -> Decimal:
    return Decimal("0.00") if value is None else Decimal(f"{value:.2f}")


def processing_date(date_str: str):
    return None if date_str is None else datetime.strptime(date_str, '%Y-%m-%dT%H:%M:%S.%f')

def convert_city_code_to_dropdown_format(original_city_list) -> list:
    return [{'value': item['id'], 'label': item['nome']} for item in original_city_list]


def convert_country_code_to_dropdown_format(original_country_list) -> list:
    return [{'value': str(int(item['id'])), 'label': item['name']} for item in original_country_list]

def get_city_name_by_id(city_list: list, id: int) -> str:
    return next((item['nome'] for item in city_list if item['id'] == id), None)

def get_brazilian_states():
    return ['RO', 'AC', 'AM', 'RR', 'PA', 'AP', 'TO',
            'MA', 'PI', 'CE', 'RN', 'PB', 'PE', 'AL',
            'SE', 'BA', 'MG', 'ES', 'RJ', 'SP', 'PR',
            'SC', 'RS', 'MS', 'MT', 'GO', 'DF']


def tax_calculator(value, cofins, csll, irpj, pis):
    total_tax = 100 - (cofins + csll + irpj + pis)

    if irpj * (value / total_tax) < 10:
        tax = 100 - (cofins + csll + pis)
        irpj_brl = 0
    else:
        tax = total_tax
        irpj_brl = round(irpj * (value / tax), 2)

    cofins_brl = round(cofins * (value / tax), 2)
    csll_brl = round(csll * (value / tax), 2)
    pis_brl = round(pis * (value / tax), 2)
    invoice_value = round(value / (tax / 100), 2)

    if (cofins_brl + csll_brl+pis_brl) < 10:
        cofins_brl = 0
        csll_brl = 0
        pis_brl = 0
        invoice_value = value

    # compare the difference between invoice value and value
    difference = (invoice_value - (cofins_brl +
                  csll_brl + pis_brl + irpj_brl)) - value
    abs_diff = abs(round(difference, 2))
    epsilon = Decimal('1e-9')
    if abs_diff - Decimal('0.01') < epsilon:
        cofins_brl = cofins_brl + difference
    elif abs_diff < epsilon:
        pass
    else:
        display(
            f"Atenção: Há uma diferença de R$ {round(difference, 2)} no cálculo dos impostos.")
    return cofins_brl, csll_brl, irpj_brl, pis_brl, invoice_value


def initialize_rps_data(rps):
    if len(rps) != 0:
        rps_info = rps[0]
        return rps_info['batch_number'], rps_info['number_rps'] + 1, rps_info['serie_rps'], 'R' + str(rps_info['number_rps'] + 1)
    return 1, 1, 1, 'R1'

def calculate_tax_amount(tax_rate, amount):
    return Decimal(tax_rate * float(amount)).quantize(Decimal('0.00'))

def calculate_rps_amount_with_taxes(rps_amount, cofins, csll, irpj, pis):
    return tax_calculator(Decimal(rps_amount), Decimal(cofins), Decimal(csll), Decimal(irpj), Decimal(pis))

def handle_substitute_rps():
    substitute_rps_data = Page().display("Informações do RPS Substituto", size="large")\
                                .read_number("Número do RPS Substituto")\
                                .read("Série do RPS Substituto")\
                                .read("Tipo do RPS Substituto")\
                                .run()
    return substitute_rps_data.values()

def handle_foreign_taker(taker):
    taker.update({
        'cnpj': None,
        'cpf': None,
        'number_address': None,
        'complement_address': None,
        'district': None,
        'state': 'EX',
        'city_code': 9999999,
    })
    return taker

def complete_invoice_description(description, rps_date):
    if not description:
        month_names = ['Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho',
                       'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro']
        description = f"Nota referente a prestações de serviços realizados no mês de {month_names[rps_date.month - 1]}/{rps_date.year}."
    return description


def get_rps_data():
    customer_data = Page().display("Informações de Clientes", size='large')\
        .read("Razão Social")\
        .read_email("Email")\
        .read("CNPJ/CPF", required=False)\
        .read("Endereço")\
        .read("Endereço (Número)", required=False)\
        .read("Endereço (Complemento)", required=False)\
        .read("Bairro", required=False)\
        .read_dropdown("Cidade", convert_city_code_to_dropdown_format(original_city_list), required=False)\
        .read_dropdown("País", convert_country_code_to_dropdown_format(original_country_list), initial_value='1058',  required=False)\
        .read_dropdown("Estado", get_brazilian_states(), required=False)\
        .read("CEP", required=False)\
        .read("Número de Telefone", required=False)\
        .read_checkbox("Pessoa Jurídica?", required=False)\
    

    rps_data = Page().display("Informações do RPS", size="large")\
                     .read("Item de Serviço Prestado", initial_value='0101')\
                     .read("Código do Município do Prestador ", initial_value='3304557')\
                     .read("Código do Tributo Municipal", initial_value='010102')\
                     .read("CNPJ do Prestador").read("Inscrição Municipal do Prestador")\
                     .read_dropdown("Natureza da Operacao", operation_nature_options)\
                     .read_dropdown("Tipo de RPS", rps_type_options)\
                     .read_multiple_choice("Simples Nacional", [{"label": "Sim", "value": 1}, {"label": "Não", "value": 2}])\
                     .read_multiple_choice("Incentivador Cultural", [{"label": "Sim", "value": 1}, {"label": "Não", "value": 2}])


    invoice_data = Page().display("Informações da Nota", size="large")\
        .read_number("Cofins (%)", initial_value=3)\
        .read_number("Csll (%)", initial_value=1)\
        .read_number("Irpj (%)", initial_value=1.5)\
        .read_number("Pis (%)", initial_value=0.65)\
        .read_number("ISS (%)", initial_value=5)\
        .read_number("INSS (%)", initial_value=0)\
        .read_number("Valor da Nota (sem impostos)")\
        .read_date("Data de Emissão do RPS")\
        .read("Descrição da Nota", required=False)\
        .read_number("Deduções", required=False)\
        .read_number("Outras retenções", required=False)\
        .read_checkbox("ISS retido?", required=False)\
        .read_checkbox("RPS substituido?", required=False)\
        
    invoice_page = run_steps([customer_data, rps_data, invoice_data])

    # Customers
    taker_name, taker_email, taker_id_number, taker_address, taker_number_address, \
    taker_complement_address, taker_district, taker_city_code, taker_country_code, taker_state, \
    taker_zip_code, taker_phone_number, taker_is_juridical = invoice_page[0].values()

    # RPS
    service_item_list, city_code, city_tax_code, emitter_cnpj, emitter_city_inscription, \
    rps_operation_nature, rps_type, is_simplesnacional, cultural_promoter = invoice_page[1].values()

    # Invoice
    cofins, csll, irpj, pis, rps_tax_rate_iss, \
    rps_inss, rps_amount, rps_issuance_date, description, rps_deductions, rps_other_retentions, \
    retained_iss, substitute_rps = invoice_page[2].values()
        
    rps = select("invoices", order_by="created_at", order_desc=True, limit=1)
    batch_number, rps_number, rps_serie, nfse_id = initialize_rps_data(rps)


    rps_status = 1
    uf_invoice = 'RJ'
    dt_format = '%Y-%m-%dT%H:%M:%I'

    rps_amount = round(rps_amount, 2)
    rps_tax_rate_iss = round(float(rps_tax_rate_iss)/100, 2)

    if retained_iss:
        retained_iss_amount = calculate_tax_amount(rps_tax_rate_iss, rps_amount)
        rps_iss_amount = Decimal('0.00')
        rps_retained_iss = 1
    else:
        retained_iss_amount = Decimal('0.00')
        rps_iss_amount = calculate_tax_amount(rps_tax_rate_iss, rps_amount)
        rps_retained_iss = 2


    # convert results of tax_calculator in Decimal(rps.quantize(Decimal('0.00'))
    rps_cofins, rps_csll, rps_irpj, rps_pis, rps_invoice_value = calculate_rps_amount_with_taxes(
        rps_amount, cofins, csll, irpj, pis)

    conditioning_discount = Decimal('0.00')
    unconditioned_discount = Decimal('0.00')

    description = complete_invoice_description(description, rps_issuance_date)

    # Substitute rps:
    if substitute_rps:
        substitute_rps_data = Page().display("Informações do RPS Substituto", size="large")\
                                    .read_number("Número do RPS Substituto")\
                                    .read("Série do RPS Substituto")\
                                    .read("Tipo do RPS Substituto")\
                                    .run()

        substitute_rps_number, substitute_rps_serie, \
            substitute_rps_type = substitute_rps_data.values()
    else:
        substitute_rps_number = None
        substitute_rps_serie = None
        substitute_rps_type = None

    if taker_is_juridical:
        taker_cnpj = taker_id_number
        taker_cpf = None
    else:
        taker_cpf = taker_id_number
        taker_cnpj = None
        rps_pis = rps_cofins = rps_csll = rps_irpj = rps_inss = Decimal('0.00')
        rps_invoice_value = Decimal(rps_amount).quantize(Decimal('0.00'))

    taker_is_foreign = False
    if taker_country_code != '1058':
        taker_is_foreign = True
        foreign_taker_data = handle_foreign_taker({
            "cnpj": taker_cnpj,
            "cpf": taker_cpf,
            "number_address": taker_number_address,
            "complement_address": taker_complement_address,
            "district": taker_district,
            "state": taker_state,
            "city_code": taker_city_code
        })
        taker_cnpj, taker_cpf, taker_number_address, taker_complement_address, taker_district, taker_state, taker_city_code = foreign_taker_data.values()
        rps_pis = rps_cofins = rps_csll = rps_irpj = rps_inss = Decimal('0.00')
        rps_invoice_value = Decimal(rps_amount).quantize(Decimal('0.00'))

    rps_cofins = Decimal(rps_cofins).quantize(Decimal('0.00'))
    rps_csll = Decimal(rps_csll).quantize(Decimal('0.00'))
    rps_irpj = Decimal(rps_irpj).quantize(Decimal('0.00'))
    rps_pis = Decimal(rps_pis).quantize(Decimal('0.00'))
    rps_invoice_value = Decimal(rps_invoice_value).quantize(Decimal('0.00'))

    rps = {
        'nfse':
        {
            'id': nfse_id,
            'numero_lote': batch_number,
            'numero': rps_number,
            'serie': rps_serie,
            'tipo_rps': rps_type,
            'data_emissao': date(rps_issuance_date.year, rps_issuance_date.month, rps_issuance_date.day).strftime(dt_format),
            'natureza_operacao': rps_operation_nature,
            'status': rps_status,
            'pessoa_juridica': taker_is_juridical,
            'codigo_municipio': city_code,
            'UF': uf_invoice,
            'cliente_estrangeiro': taker_is_foreign,
            'rps_substituto': substitute_rps,
            'rps_substituido': {
                'numero': substitute_rps_number,
                'serie': substitute_rps_serie,
                'tipo_rps': substitute_rps_type
            },
            'emissor': {
                'optante_simples_nacional': is_simplesnacional,
                'incentivador_cultural': cultural_promoter,
                'cnpj': emitter_cnpj,
                'inscricao_municipal': emitter_city_inscription
            },
            'servico': {
                'valor': {
                    'valor_servicos': rps_invoice_value,
                    'valor_deducoes': convert_none_to_zero(rps_deductions),
                    'valor_pis': rps_pis,
                    'valor_cofins': rps_cofins,
                    'valor_inss': convert_none_to_zero(rps_inss),
                    'valor_ir': convert_none_to_zero(rps_irpj),
                    'valor_csll': rps_csll,
                    'iss_retido': rps_retained_iss,
                    'valor_iss': convert_none_to_zero(rps_iss_amount),
                    'valor_iss_retido': convert_none_to_zero(retained_iss_amount),
                    'outras_retencoes': convert_none_to_zero(rps_other_retentions),
                    'aliquota': rps_tax_rate_iss,
                    'valor_liquido': rps_amount,
                    'desconto_incondicionado': unconditioned_discount,
                    'desconto_condicionado': conditioning_discount
                },
                'item_lista_servicos': service_item_list,
                'codigo_tributacao_municipio': city_tax_code,
                'discriminacao': description,
                'codigo_municipio': city_code
            },
            'tomador': {
                'cnpj': taker_cnpj,
                'cpf': taker_cpf,
                'razao_social': taker_name,
                'endereco': {
                    'endereco': taker_address,
                    'numero': taker_number_address,
                    'complemento': taker_complement_address,
                    'bairro': taker_district,
                    'codigo_municipio': taker_city_code,
                    'uf': taker_state,
                    'cep': taker_zip_code,
                    'codigo_pais': taker_country_code,
                    'endereco_exterior': taker_address
                },
                'endereco_exterior': {
                    'codigo_pais': taker_country_code,
                    'endereco': taker_address
                },
                'telefone': taker_phone_number,
                'email': taker_email
            }}
    }

    return rps

def get_rps_status():
    dt_format = '%Y-%m-%d'

    emitter_info = Page().display('Notas Fiscais - Status', size='large')\
                         .read('CNPJ do Emissor')\
                         .read('Inscrição Municipal do Emissor')\
                         .read_date('Data Inicial')\
                         .read_date('Data Final')\
                         .run("Obter Notas Fiscais")
    
    emitter_cnpj, emitter_city_inscription, start_date, end_date = emitter_info.values()

    rps = {
        'nfse':
        {
            'data_inicial': datetime(start_date.year, start_date.month, start_date.day).strftime(dt_format),
            'data_final': date(end_date.year, end_date.month, end_date.day).strftime(dt_format),
            'emissor': {
                'cnpj': emitter_cnpj,
                'inscricao_municipal': emitter_city_inscription
            }}
    }
    return rps


def get_rps_cancel():
    city_code=str(3304557)
    cancel_codes = flags.CANCEL_CODE["codes"]
    
    rps_cancel = Page().display('Please fill in the information for the RPS to be cancelled.')\
                       .read('CNPJ do Emissor')\
                       .read('Inscrição Municipal do Emissor')\
                       .read('Código do Município do Prestador', initial_value=city_code)\
                       .read('NFSe Number')\
                       .read_dropdown('Reason to cancel code', cancel_codes)\
                       .run('Cancel RPS')

    emitter_cnpj, emitter_city_inscription, city_code, nfse_number, cancel_code = rps_cancel.values()

    rps = {
        'nfse':
        {
            'numero': nfse_number,
            'codigo_cancelamento': cancel_code,
            'emissor': {
                'cnpj': emitter_cnpj,
                'inscricao_municipal': emitter_city_inscription
            },
            'servico': {
                'codigo_municipio': city_code,
            }}
    }
    return rps


def verify_schema(xml, xml_schema):
    my_schema = xmlschema.XMLSchema(xml_schema)
    return my_schema.is_valid(xml)

def get_xml(nfse, temp):
    template = Template(temp)
    xml = template.render(nfse)
    parser = etree.XMLParser(ns_clean=True, recover=True,
                             remove_blank_text=False, encoding='UTF-8')
    output = etree.fromstring(xml, parser=parser)
    out = etree.tostring(output, encoding='unicode', method='xml')
    with open('./arquivos/test.xml', 'w') as f:
        f.write(out)

    xml_schema = './arquivos/nfse_pcrj_v01.xsd'
    verify_schema(out, xml_schema)
    return out


def send_invoice(env, certificate_path, pfx_password):
    nfse = get_rps_data()
    rps_batch_number = nfse['nfse']['numero_lote']
    rps_number = nfse['nfse']['numero']
    rps_serie = nfse['nfse']['serie']
    amount = float(nfse['nfse']['servico']['valor']['valor_liquido'])
    cnpj_emitter=nfse['nfse']['emissor']['cnpj']
    recipient_email = nfse['nfse']['tomador']['email']


    additional_data = {"rps_number": rps_number, "rps_batch_number": rps_batch_number,
                       "rps_serie": rps_serie, "amount": amount}
    xml = get_xml(nfse, gerar)
    certificate, key = load_public_key(certificate_path, pfx_password)

    nota = NotaCarioca(key=key, certificate=certificate,
                       city_code=3304557, env=env, cnpj_emitter=cnpj_emitter, xml=xml, recipient_email=recipient_email)

    nota.send(additional_data_to_send=additional_data)


def get_invoice(env, certificate_path, pfx_password):

    nfse = get_rps_status()
    xml = get_xml(nfse, consultar)
    certificate, key = load_public_key(certificate_path, pfx_password)
    cnpj_emitter=(nfse['nfse']['emissor']['cnpj']).replace(".", "").replace("/", "").replace("-", "")
    

    nota = NotaCarioca(key=key, certificate=certificate,
                       city_code=3304557, env=env, cnpj_emitter=cnpj_emitter, xml=xml, recipient_email=None)
    nota.status()


def cancel_invoice(env, certificate_path, pfx_password):
    nfse = get_rps_cancel()
    xml = get_xml(nfse, cancelar)
    certificate, key = load_public_key(certificate_path, pfx_password)

    nota = NotaCarioca(key=key, certificate=certificate,
                       city_code=3304557, env=env, cnpj_emitter=nfse['nfse']['emissor']['cnpj'], xml=xml, recipient_email=None)
    nota.cancel()



def invoice():
    pfx_password = os.environ.get('INVOICE_CERT_PASSWORD')
    pfx_name = os.environ.get('INVOICE_CERT_NAME')
    
    persistent_dir = get_persistent_dir()
    certificate_path = os.path.join(
        persistent_dir, pfx_name)
    nfse_reason = Page().display("Gestão de Notas Fiscais - Nota Carioca", size="large")\
                        .read_dropdown("Selecione a opção desejada para continuar:", [{"label": "Consultar notas existentes por período", "value": "status"}, {
                                "label": "Emitir Nota Fiscal Única", "value": "issue"}, {"label": "Cancelar Notas", "value": "cancel"}], key="invoice_selection")\
                        .run("Prosseguir")
    if nfse_reason["invoice_selection"] == "status":
        get_invoice(env, certificate_path, pfx_password)
    elif nfse_reason["invoice_selection"] == "issue":
        send_invoice(env, certificate_path, pfx_password)
    elif nfse_reason["invoice_selection"] == "cancel":
        cancel_invoice(env, certificate_path, pfx_password)

invoice()