> **Note**: This repository and the majority of the documentation and code are in Portuguese, as it is a template applied to Brazil. However, contributions and questions in English are also welcome.

# Projeto de Emissão de Notas Fiscais via Nota Carioca com Abstra

Este projeto fornece um template para a emissão, cancelamento e busca de notas fiscais eletrônicas de serviços através do sistema Nota Carioca, utilizando a biblioteca Abstra. O foco deste repositório é auxiliar desenvolvedores e empresas brasileiras a automatizar esses processos.

## Configuração Inicial

Para utilizar este projeto, é necessário realizar algumas configurações iniciais:

1. **Certificado Digital A1**: É necessário possuir um certificado digital A1 válido. As credenciais deste certificado deverão ser configuradas no arquivo `.env` deste projeto.
2. **Arquivo .env**: Crie um arquivo `.env` na raiz do projeto e adicione as seguintes variáveis com as credenciais do seu certificado digital A1:

   ```ini
   INVOICE_CERT_PATH="caminho/para/o/seu/certificado.pfx"
   INVOICE_CERT_PASSWORD="senhaDoCertificado"
   ```

3. **Tabela "invoices"**: É necessário criar uma tabela chamada `invoices` no seu banco de dados da Abstra (tables) com as seguintes colunas:

   - `number_rps`: Número do RPS (Recibo Provisório de Serviços).
   - `serie_rps`: Série do RPS.
   - `batch_number`: Número do lote.

## Uso

Após realizar as configurações iniciais, siga os passos abaixo para começar a usar o projeto:

1. Instale as dependências necessárias utilizando o pip. Abra o terminal e execute o seguinte comando:

   ```sh
   pip install -r requirements.txt
   ```

2. Abra o projeto na Abstra utilizando o seguinte comando:

   ```sh
   abstra editor caminho/para/a/pasta/seu/projeto/
   ```

### Funcionalidades

Este projeto oferece três funcionalidades principais: emitir, cancelar e buscar notas fiscais.

#### Uso Geral

Para interagir com as notas fiscais (emitir, cancelar e buscar), utilize o form Send Invoice, arquivo `send_invoice.py`. Este arquivo contém a lógica para as três funcionalidades:

1. **Emissão de Notas Fiscais**: Envia os dados da nota fiscal para o sistema Nota Carioca.
2. **Cancelamento de Notas Fiscais**: Envia uma solicitação de cancelamento para o sistema Nota Carioca.
3. **Busca de Notas Fiscais**: Recupera informações de uma nota fiscal específica por período consultando o sistema Nota Carioca.

### Arquivos Importantes

#### send_invoice.py

Este é o arquivo principal do projeto. Ele contém a lógica para emitir, cancelar e buscar notas fiscais no sistema Nota Carioca. Dependendo da opção escolhida pelo usuário, ele executará a função correspondente.

#### send_email_with_invoice_link.py

Este script é responsável pelo envio do link da nota emitida para o email cadastrado no formulário "Send Invoice".

## Como Funciona

Este projeto permite a geração, cancelamento e busca de notas fiscais eletrônicas utilizando o sistema Nota Carioca. Ele automatiza os processos de criação do RPS, envio dos dados, cancelamento de notas emitidas e consulta de notas fiscais.

## Contribuições

Contribuições são bem-vindas! Se você deseja melhorar este projeto, sinta-se à vontade para criar um pull request.
