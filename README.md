> **Note**: This repository and the majority of the documentation and code are in Portuguese, as it is a template applied to Brazil. However, contributions and questions in English are also welcome.

# Projeto de Emissão de Notas Fiscais via Nota Carioca com Abstra

## Como Funciona

Este projeto fornece um template para a emissão, cancelamento e busca de notas fiscais eletrônicas de serviços através do sistema Nota Carioca, utilizando Python e Abstra. O foco deste repositório é auxiliar desenvolvedores e empresas brasileiras a automatizar esses processos.

Para customizar este template para o seu time e explorar ainda mais possibilidades, [agende uma demonstração aqui](https://meet.abstra.app/demo?url=template-nota-carioca).

## Configuração Inicial

Para utilizar este projeto, é necessário realizar algumas configurações iniciais:

1. **Certificado Digital A1**: É necessário possuir um certificado digital A1 válido. As credenciais deste certificado deverão ser configuradas no arquivo `.env` deste projeto.
2. **Variáveis de ambiente**: Crie um arquivo `.env` na raiz do projeto e adicione as seguintes variáveis com as credenciais do seu certificado digital A1:

   ```ini
   INVOICE_CERT_PATH="caminho/para/o/seu/certificado.pfx"
   INVOICE_CERT_PASSWORD="senhaDoCertificado"
   ```

3. **Dependências**: Para instalar as dependências necessárias para este projeto, um arquivo `requirements.txt` é fornecido. Este arquivo inclui todas as bibliotecas necessárias.

   Siga estes passos para instalar as dependências:

   1. Abra seu terminal e navegue até o diretório do projeto.
   2. Execute o seguinte comando para instalar as dependências a partir do `requirements.txt`:

      ```sh
      pip install -r requirements.txt
      ```

4. **Configuração de Tabelas**: Configure suas tabelas de banco de dados no Abstra Cloud Tables de acordo com o schema definido em `abstra-tables.json`.

   Para criar automaticamente o schema da tabela, siga estes passos:

   1. Abra seu terminal e navegue até o diretório do projeto.

   2. Execute o seguinte comando para instalar o schema da tabela a partir de `abstra-tables.json`:
      ```sh
      abstra restore
      ```

   Para obter orientações sobre como criar e gerenciar tabelas no Abstra, consulte a [documentação do Abstra Tables](https://docs.abstra.io/cloud/tables).

5. **Controle de Acesso**: O formulário gerado é protegido por padrão. Para testes locais, nenhuma configuração adicional é necessária. No entanto, para uso na nuvem, é necessário adicionar suas próprias regras de acesso.

   Para obter mais informações sobre como configurar o controle de acesso, consulte a [documentação para controle de acesso da Abstra](https://docs.abstra.io/concepts/access-control).

6. **Dependências**: Para acesso ao editor local com o projeto, utilize o seguinte comando:

   ```sh
      abstra editor caminho/para/a/pasta/do/seu/projeto/
   ```

## Funcionalidades

Este projeto oferece três funcionalidades principais: emitir, cancelar e buscar notas fiscais. Para interagir com as notas fiscais (emitir, cancelar e buscar), utilize o form Send Invoice, arquivo `send_invoice.py`. Este arquivo contém a lógica para as três funcionalidades:

1. **Emissão de Notas Fiscais**: Envia os dados da nota fiscal para o sistema Nota Carioca.
2. **Cancelamento de Notas Fiscais**: Envia uma solicitação de cancelamento para o sistema Nota Carioca.
3. **Busca de Notas Fiscais**: Recupera informações de uma nota fiscal específica por período consultando o sistema Nota Carioca.

## Arquivos Importantes

- **send_invoice.py**: Este é o arquivo principal do projeto. Ele contém a lógica para emitir, cancelar e buscar notas fiscais no sistema Nota Carioca. Dependendo da opção escolhida pelo usuário, ele executará a função correspondente.

- **send_email_with_invoice_link.py**: Este script é responsável pelo envio do link da nota emitida para o email cadastrado no formulário "Send Invoice".

Se você estiver interessado em personalizar este template para a sua equipe em menos de 30 minutos, [agende uma sessão de personalização aqui.](https://meet.abstra.app/demo?url=template-nota-carioca)
