> **Note**: This repository and the majority of the documentation and code are in Portuguese, as it is a template applied to Brazil. However, contributions and questions in English are also welcome.

# Projeto de Emissão de Notas Fiscais via Nota Carioca com ABSTRA

Este projeto fornece um template para a emissão de notas fiscais eletrônicas através do sistema Nota Carioca, utilizando a biblioteca Abstra. O foco deste repositório é auxiliar desenvolvedores e empresas brasileiras a automatizar o processo de emissão de notas fiscais.

## Configuração Inicial

Para utilizar este projeto, é necessário realizar algumas configurações iniciais:

1. **Certificado Digital A1**: É necessário possuir um certificado digital A1 válido. As credenciais deste certificado deverão ser configuradas no arquivo `.env` deste projeto.
2. **Arquivo .env**: Crie um arquivo `.env` na raiz do projeto e adicione as seguintes variáveis com as credenciais do seu certificado digital A1:

   ```
   INVOICE_CERT_PASSWORD="caminho/para/o/seu/certificado.pfx"
   INVOICE_CERT_PASSWORD="senhaDoCertificado"
   ```

3. **Tabela "invoices"**: É necessário criar uma tabela chamada `invoices` no seu banco de dados (tables) com as seguintes colunas:

   - `number_rps`: Número do RPS (Recibo Provisório de Serviços).
   - `serie_rps`: Série do RPS.
   - `batch_number`: Número do lote.

## Uso

Para emitir uma nota fiscal, utilize o form `send_invoice.py`. Este formulário é responsável por preparar e enviar os dados da nota fiscal para o sistema Nota Carioca através da Abstra.

### send_invoice.py

Este é o arquivo principal do projeto. Ele contém a lógica para enviar os dados da nota fiscal para o sistema Nota Carioca. Antes de executar este script, certifique-se de que todas as configurações iniciais foram realizadas corretamente.

## Contribuições

Contribuições são bem-vindas! Se você deseja melhorar este projeto, sinta-se à vontade para criar um pull request.
