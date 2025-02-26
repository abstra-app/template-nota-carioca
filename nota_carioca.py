import models, flags
from zeep import Client
from zeep.transports import Transport
from requests import Session
import zeep.plugins
from requests.adapters import HTTPAdapter
from urllib3.poolmanager import PoolManager
import ssl

class TLSAdapter(HTTPAdapter):
    def init_poolmanager(self, connections, maxsize, block=False, **pool_kwargs):
        ctx = ssl.create_default_context()
        ctx.set_ciphers("HIGH:!DH:!aNULL")
        ctx.options |= ssl.OP_NO_SSLv2
        ctx.options |= ssl.OP_NO_SSLv3
        ctx.options |= ssl.OP_NO_COMPRESSION
        ctx.options |= ssl.OP_NO_TLSv1
        ctx.options |= ssl.OP_NO_TLSv1_1
        self.poolmanager = PoolManager(
            num_pools=connections, maxsize=maxsize, block=block, ssl_context=ctx)


class NotaCarioca(object):
    def __init__(self, **kwargs):
        self.kwargs = kwargs
        self.key = kwargs.pop("key")
        self.certificate = kwargs.pop("certificate")
        self.city_code = kwargs.pop("city_code")
        self.env = kwargs.pop("env")
        self.cnpj_emitter = kwargs.pop("cnpj_emitter")
        self.xml = kwargs.pop("xml")
        self.recipient_email = kwargs.pop("recipient_email")
        self.base_url = flags.URL[self.city_code][self.env]

    def _get_credentials(self, credential):
        filename = '%s-%s.pem' % (self.cnpj_emitter, credential)
        file_obj = open('/tmp/%s' % filename, 'w+')
        file_obj.write(getattr(self, credential).decode('utf-8'))

        return '/tmp/%s' % filename

    def _get_client(self):
        session = Session()

        cert = (self._get_credentials("certificate"),
                self._get_credentials("key"))
        if all(cert):
            session.cert = cert

        cache = None
        session.mount('https://', TLSAdapter())

        transport = Transport(session=session, cache=cache)

        history = zeep.plugins.HistoryPlugin()

        client = Client(self.base_url, transport=transport, plugins=[history])

        return client

    def send(self, additional_data_to_send, multiple_rps=False):
        client = self._get_client()
        client_response = client.service.GerarNfse(self.xml)
        return models.ResponseRPS(response=client_response, additional_data=additional_data_to_send, multiple=multiple_rps, env=self.env, recipient_email=self.recipient_email)

    def status(self, nfse=False):
        if nfse:
            return self.update_nfse()

        client = self._get_client()
        response = client.service.ConsultarNfse(
            self.xml)

        try:
            response = client.service.ConsultarNfse(
                self.xml)
        except:
            return models.ResponseRPS(in_process=True)

        return models.ResponseRPS(response, env=self.env)

    def download_nfse(self):
        client = self._get_client()
        response = client.service.ConsultarNfse(
            self.xml)

        return models.NFSeXML(response)

    def update_nfse(self):
        client = self._get_client()
        response = client.service.ConsultarNfse(
            self.xml)

        return models.ResponseRPS(self.rps, response)

    def cancel(self):
        client = self._get_client()
        response = client.service.CancelarNfse(
            self.xml)

        return models.ResponseCancel(response)
