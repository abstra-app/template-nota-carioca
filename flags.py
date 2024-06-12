operation_nature = [
    {"label": "Tributação no município", "value": 1},
    {"label": "Tributação fora do município", "value": 2},
    {"label": "Isenção", "value": 3},
    {"label": "Imune", "value": 4},
    {"label": "Exigibilidade suspensa por decisão judicial", "value": 5},
    {"label": "Exigibilidade suspensa por procedimento Administrativo", "value": 6}
]

tax_regime = [
    {"label": "Microempresa Municipal", "value": 1},
    {"label": "Estimativa", "value": 2},
    {"label": "Sociedade Professional", "value": 3},
    {"label": "Cooperativa", "value": 4},
    {"label": "MEI - Microempresário Individual", "value": 5},
    {"label": "ME EPP - Microempresário e Empresa de Pequeno Porte", "value": 6}
]

rps_type = [
    {"label": "RPS", "value": 1},
    {"label": "Nota Conjugada", "value": 2},
    {"label": "Cupom", "value": 3}
]

NFSE_PROCESS = {
    'processing': 'processing',
    'accepted': 'accepted',
    'rejected': 'rejected',
    'cancelled': 'cancelled'
}

URL = {
    3304557: {
        "production": "https://notacarioca.rio.gov.br/WSNacional/nfse.asmx?wsdl",
        "sandbox": "https://notacariocahom.rio.gov.br/WSNacional/nfse.asmx?wsdl"
    }
}


CANCEL_CODE = {
    "codes": [
        {"value": 1, "label": "Erro na emissão"},
        {"value": 2, "label": "Serviço não prestado"},
        {"value": 3, "label": "Duplicidade da nota"},
        {"value": 9, "label": "Outros"}]
}