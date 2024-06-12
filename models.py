# -*- coding: utf-8 -*-

from abstra.forms import *
from abstra.tables import *
from abstra.workflows import *
import flags
from datetime import datetime
import xmltodict

import pandas as pd


class ErrorMixin(object):
    def _build_errors(self, response):
        self.status = flags.NFSE_PROCESS["rejected"]
        message = response["ListaMensagemRetorno"]["MensagemRetorno"]

        if isinstance(message, dict):
            self.errors.append(Error(**message))
        else:
            for error in message:
                self.errors.append(Error(**error))

        display(self.errors[0].__str__())


class ResponseRPS(ErrorMixin):
    def __init__(self, response=None, additional_data=[], in_process=False, multiple=False, env="sandbox", **kwargs):
        self.response = response
        self.nfse = None
        self.status = flags.NFSE_PROCESS["processing"]
        self.errors = []
        self.multiple = multiple
        self.env = env
        self.additional_data = additional_data

        if not in_process:
            self._process_response()

    def _build_nfse(self, response, list_index=None):
        if list_index != None:
            nfse_inf = response["ListaNfse"]["CompNfse"][list_index]["Nfse"]["InfNfse"]
        else:
            nfse_inf = response["ListaNfse"]["CompNfse"]["Nfse"]["InfNfse"]
        self.nfse = NFSe(**nfse_inf)

    def _process_response(self):
        response = xmltodict.parse(self.response)

        if response.get("GerarNfseResposta"):
            response = response["GerarNfseResposta"]

            if "ListaMensagemRetorno" in response.keys():
                self._build_errors(response)

                return None

            self.status = flags.NFSE_PROCESS["accepted"]
            if self.status == 'accepted':
                display(f'Status: {self.status} - Nota enviada com sucesso.')

                if self.multiple:
                    for rps in self.additional_data:
                        rps_params = {"batch_number": rps['rps_batch_number'], "number_rps": rps['rps_number'], "serie_rps": rps['rps_serie']}
                        insert("invoices", rps_params)
                else:
                    rps = self.additional_data
                    rps_params = {"batch_number": rps['rps_batch_number'], "number_rps": rps['rps_number'], "serie_rps": rps['rps_serie']}
                    insert("invoices", rps_params)

                xml_dict = {"ConsultarNfseResposta": response}
                response_xml = xmltodict.unparse(xml_dict)
                NFSeLink(response_xml, self.env)

        if response.get("ConsultarNfseResposta"):
            response = response["ConsultarNfseResposta"]
            print(response)
            if response["ListaNfse"] == None:
                display("NFSe não encontrada para este período.", end_program=True)

            if type(response["ListaNfse"]["CompNfse"]) == list:
                invoices = []
                for i, r in enumerate(response["ListaNfse"]["CompNfse"]):
                    self.status = flags.NFSE_PROCESS["accepted"]
                    if r.get("NfseCancelamento"):
                        self.status = flags.NFSE_PROCESS["cancelled"]
                    status = self.status
                    invoice_number = r["Nfse"]["InfNfse"]["Numero"]
                    invoice_amount = r["Nfse"]["InfNfse"]["Servico"]["Valores"]["ValorLiquidoNfse"]
                    verification_code = r["Nfse"]["InfNfse"]["CodigoVerificacao"]
                    emission_data = r["Nfse"]["InfNfse"]["DataEmissao"]

                    invoices.append(
                        {"Invoice Number": invoice_number, "Status": status, "Invoice Amount": invoice_amount,
                         "RPS Verification Code": verification_code, "Emission Date": emission_data})
                    
                df_invoices = pd.DataFrame(invoices)
                selected_invoices = Page().display('Há mais de uma nota fiscal para este período. Por favor, selecione a nota para ver com mais detalhes')\
                    .read_pandas_row_selection(df_invoices, full_width=True,  multiple=True)\
                    .run(["Finalizar", "Ver mais detalhes"])
                if selected_invoices.action == "Finalizar":
                    display("Obrigado", end_program=True)
                else:
                    for i in range(len(selected_invoices["result"])):
                        index = selected_invoices["result"][i]["index"]
                        invoice_response = xmltodict.parse(self.response)
                        invoice_response["ConsultarNfseResposta"]["ListaNfse"]["CompNfse"] = invoice_response[
                            "ConsultarNfseResposta"]["ListaNfse"]["CompNfse"][index]
                        xml_response = xmltodict.unparse(invoice_response)
                        NFSeLink(xml_response, self.env)

            else:
                invoice_response = xmltodict.parse(self.response)
                invoice_response["ConsultarNfseResposta"]["ListaNfse"]["CompNfse"] = invoice_response[
                    "ConsultarNfseResposta"]["ListaNfse"]["CompNfse"]
                xml_response = xmltodict.unparse(invoice_response)
                NFSeLink(xml_response, self.env)

                if response["ListaNfse"]["CompNfse"].get("NfseCancelamento"):
                    self.status = flags.NFSE_PROCESS["cancelled"]

        return (self.nfse)


class ResponseCancel(ErrorMixin):
    def __init__(self, response):
        self.response = response
        self.status = flags.NFSE_PROCESS["cancelled"]
        self.errors = []

        self._process_response()

    def _process_response(self):
        response = xmltodict.parse(self.response)["CancelarNfseResposta"]

        if "ListaMensagemRetorno" in response.keys():
            self._build_errors(response)


class Error(object):

    def __init__(self, **kwargs):

        self.description = kwargs.pop("Mensagem")
        self.code = kwargs.pop("Codigo")
        self.tip = kwargs.pop("Correcao", None)

    def __str__(self):
        return f"Erro: Código {self.code} - {self.description} {self.tip}"


class NFSe(object):
    def _format_datetime(self, date):
        if date:
            date = datetime.strptime(date, "%Y-%m-%dT%H:%M:%S")

        return date

    def __init__(self, **kwargs):
        self.key = kwargs["CodigoVerificacao"] or None
        self.number = int(kwargs["Numero"]) or None
        self.emission_date_nfse = self._format_datetime(
            kwargs.get("DataEmissao"))
        self.mirror = None
        self.xml = None


class NFSeXML(object):
    def __init__(self, response, **kwargs):
        self.response = response
        self.xml = None

        self._process_xml()

    def _process_xml(self):
        self.xml = self.response.encode("utf-8")
        # display(self.xml)


class NFSeLink(object):
    def __init__(self, response, env, **kwargs):
        self.response = response
        self.xml = None
        self.env = env

        self._get_link()

    def _get_link(self):
        try:
            response = xmltodict.parse(self.response)[
                "ConsultarNfseResposta"]["ListaNfse"]
        except:
            response = xmltodict.parse(self.response)["ConsultarNfseResposta"]

        ccm = response["CompNfse"]["Nfse"]["InfNfse"]["PrestadorServico"]["IdentificacaoPrestador"]["InscricaoMunicipal"]
        nf = response["CompNfse"]["Nfse"]["InfNfse"]["Numero"]
        cod = response["CompNfse"]["Nfse"]["InfNfse"]["CodigoVerificacao"].replace(
            "-", "")
        link_nfse_hom = f"https://notacariocahom.rio.gov.br/contribuinte/notaprint.aspx?nf={nf}&inscricao={ccm}&verificacao={cod}"
        link_to_nfse = f"https://notacarioca.rio.gov.br/contribuinte/notaprint.aspx?inscricao={ccm}&nf={nf}&verificacao={cod}"
        if self.env == "sandbox":
            display_link(
                link_nfse_hom, link_text="Clique aqui para visualizar a NFSe de teste")
            set_data("invoice_link", link_nfse_hom)
            
        else:
            display_link(link_to_nfse, link_text="Clique aqui para visualizar a NFSe")
            set_data("invoice_link", link_to_nfse)
