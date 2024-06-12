gerar = '''
    <GerarNfseEnvio xmlns="http://notacarioca.rio.gov.br/WSNacional/XSD/1/nfse_pcrj_v01.xsd"> 
        <Rps>
            <InfRps xmlns="http://www.abrasf.org.br/ABRASF/arquivos/nfse.xsd" Id="{{nfse.id}}">
                <IdentificacaoRps>
                    <Numero>{{nfse.numero}}</Numero>
                    <Serie>{{nfse.serie}}</Serie>
                    <Tipo>{{nfse.tipo_rps}}</Tipo>
                </IdentificacaoRps>
                {% if nfse.rps_substituto %}
                        <RpsSubstituido>
                            <Numero>{{nfse.rps_substituido.numero}}</Numero>
                            <Serie>{{nfse.rps_substituido.serie}}</Serie>
                            <Tipo>{{nfse.rps_substituido.tipo_rps}}</Tipo>
                        </RpsSubstituido>
                {% endif %}
                <DataEmissao>{{nfse.data_emissao}}</DataEmissao>
                <NaturezaOperacao>{{nfse.natureza_operacao}}</NaturezaOperacao>
                <OptanteSimplesNacional>{{nfse.emissor.optante_simples_nacional}}</OptanteSimplesNacional>
                <IncentivadorCultural>{{nfse.emissor.incentivador_cultural}}</IncentivadorCultural>
                <Status>{{nfse.status}}</Status>
                <Servico>
                    <Valores>
                        <ValorServicos>{{nfse.servico.valor.valor_servicos}}</ValorServicos>
                        <ValorDeducoes>{{nfse.servico.valor.valor_deducoes}}</ValorDeducoes>
                        <ValorPis>{{nfse.servico.valor.valor_pis}}</ValorPis>
                        <ValorCofins>{{nfse.servico.valor.valor_cofins}}</ValorCofins>
                        <ValorInss>{{nfse.servico.valor.valor_inss}}</ValorInss>
                        <ValorIr>{{nfse.servico.valor.valor_ir}}</ValorIr>
                        <ValorCsll>{{nfse.servico.valor.valor_csll}}</ValorCsll>
                        <IssRetido>{{nfse.servico.valor.iss_retido}}</IssRetido>
                        <ValorIss>{{nfse.servico.valor.valor_iss}}</ValorIss>
                        <ValorIssRetido> {{nfse.servico.valor.valor_iss_retido}}</ValorIssRetido>
                        <OutrasRetencoes>{{nfse.servico.valor.outras_retencoes}}</OutrasRetencoes>
                        <Aliquota>{{nfse.servico.valor.aliquota}}</Aliquota>
                        <DescontoIncondicionado>{{nfse.servico.valor.desconto_incondicionado}}</DescontoIncondicionado>
                        <DescontoCondicionado>{{nfse.servico.valor.desconto_condicionado}}</DescontoCondicionado>
                    </Valores>
                    <ItemListaServico>{{nfse.servico.item_lista_servicos}}</ItemListaServico>
                    <CodigoTributacaoMunicipio>{{nfse.servico.codigo_tributacao_municipio}}</CodigoTributacaoMunicipio>
                    <Discriminacao>{{nfse.servico.discriminacao}}</Discriminacao>
                    <CodigoMunicipio>{{nfse.servico.codigo_municipio}}</CodigoMunicipio>
                </Servico>
                <Prestador>
                    <Cnpj>{{nfse.emissor.cnpj}}</Cnpj>
                    <InscricaoMunicipal>{{nfse.emissor.inscricao_municipal}}</InscricaoMunicipal>
                </Prestador>
                <Tomador>
                    <IdentificacaoTomador>
                        {% if not nfse.cliente_estrangeiro %}
                            <CpfCnpj>
                                    {% if nfse.pessoa_juridica %}
                                        <Cnpj>{{nfse.tomador.cnpj}}</Cnpj>
                                    {% else %}
                                        <Cpf>{{nfse.tomador.cpf}}</Cpf>
                                    {% endif %}
                            </CpfCnpj>
                        {% endif %}
                    </IdentificacaoTomador>
                    <RazaoSocial>{{nfse.tomador.razao_social}}</RazaoSocial>
                        <Endereco>
                            <Endereco>{{nfse.tomador.endereco.endereco}}</Endereco>
                            {% if nfse.tomador.endereco.numero %}
                                <Numero>{{nfse.tomador.endereco.numero}}</Numero>
                            {% endif %}
                            {% if nfse.tomador.endereco.complemento %}
                                <Complemento>{{nfse.tomador.endereco.complemento}}</Complemento>
                            {% endif %}
                            {% if nfse.tomador.endereco.bairro %}
                                <Bairro>{{nfse.tomador.endereco.bairro}}</Bairro>
                            {% endif %}
                            {% if nfse.tomador.endereco.codigo_municipio %}
                                <CodigoMunicipio>{{nfse.tomador.endereco.codigo_municipio}}</CodigoMunicipio>
                            {% endif %}
                            <Uf>{{nfse.tomador.endereco.uf}}</Uf>
                            {% if nfse.tomador.endereco.cep %}
                                <Cep>{{nfse.tomador.endereco.cep}}</Cep>
                            {% endif %}
                            </Endereco>
                    <Contato>
                        {% if nfse.tomador.telefone %}
                            <Telefone>{{nfse.tomador.telefone}}</Telefone>
                        {% endif %}
                        {% if nfse.tomador.email %}
                            <Email>{{nfse.tomador.email}}</Email>
                        {% endif %}
                    </Contato>
                </Tomador>
            </InfRps>
        </Rps>
    </GerarNfseEnvio>
'''

consultar = '''
<ConsultarNfseEnvio xmlns="http://www.abrasf.org.br/ABRASF/arquivos/nfse.xsd">
<Prestador>
   <Cnpj>{{nfse.emissor.cnpj}}</Cnpj>
   <InscricaoMunicipal>{{nfse.emissor.inscricao_municipal}}</InscricaoMunicipal>  
</Prestador>
<PeriodoEmissao>
   <DataInicial>{{nfse.data_inicial}}</DataInicial> 
   <DataFinal>{{nfse.data_final}}</DataFinal> 
</PeriodoEmissao>
</ConsultarNfseEnvio> 
'''


cancelar = '''
<CancelarNfseEnvio xmlns="http://www.abrasf.org.br/ABRASF/arquivos/nfse.xsd">
    <Pedido>
        <InfPedidoCancelamento Id="NFSe{{nfse.numero}}">
            <IdentificacaoNfse>
                <Numero>{{nfse.numero}}</Numero>
                <Cnpj>{{nfse.emissor.cnpj}}</Cnpj>
                <InscricaoMunicipal>{{nfse.emissor.inscricao_municipal}}</InscricaoMunicipal>
                <CodigoMunicipio>{{nfse.servico.codigo_municipio}}</CodigoMunicipio>
            </IdentificacaoNfse>
            <CodigoCancelamento>{{nfse.codigo_cancelamento}}</CodigoCancelamento>
        </InfPedidoCancelamento>
    </Pedido>
</CancelarNfseEnvio>
'''


gerar_multiplos_rps = '''
            <Rps>
                <InfRps Id="{{nfse.id}}">
                    <IdentificacaoRps>
                        <Numero>{{nfse.numero}}</Numero>
                        <Serie>{{nfse.serie}}</Serie>
                        <Tipo>{{nfse.tipo_rps}}</Tipo>
                    </IdentificacaoRps>
                    {% if nfse.rps_substituto %}
                            <RpsSubstituido>
                                <Numero>{{nfse.rps_substituido.numero}}</Numero>
                                <Serie>{{nfse.rps_substituido.serie}}</Serie>
                                <Tipo>{{nfse.rps_substituido.tipo_rps}}</Tipo>
                            </RpsSubstituido>
                    {% endif %}
                    <DataEmissao>{{nfse.data_emissao}}</DataEmissao>
                    <NaturezaOperacao>{{nfse.natureza_operacao}}</NaturezaOperacao>
                    <OptanteSimplesNacional>{{nfse.emissor.optante_simples_nacional}}</OptanteSimplesNacional>
                    <IncentivadorCultural>{{nfse.emissor.incentivador_cultural}}</IncentivadorCultural>
                    <Status>{{nfse.status}}</Status>
                    <Servico>
                        <Valores>
                            <ValorServicos>{{nfse.servico.valor.valor_servicos}}</ValorServicos>
                            <ValorDeducoes>{{nfse.servico.valor.valor_deducoes}}</ValorDeducoes>
                            <ValorPis>{{nfse.servico.valor.valor_pis}}</ValorPis>
                            <ValorCofins>{{nfse.servico.valor.valor_cofins}}</ValorCofins>
                            <ValorInss>{{nfse.servico.valor.valor_inss}}</ValorInss>
                            <ValorIr>{{nfse.servico.valor.valor_ir}}</ValorIr>
                            <ValorCsll>{{nfse.servico.valor.valor_csll}}</ValorCsll>
                            <IssRetido>{{nfse.servico.valor.iss_retido}}</IssRetido>
                            <ValorIss>{{nfse.servico.valor.valor_iss}}</ValorIss>
                            <ValorIssRetido> {{nfse.servico.valor.valor_iss_retido}}</ValorIssRetido>
                            <OutrasRetencoes>{{nfse.servico.valor.outras_retencoes}}</OutrasRetencoes>
                            <Aliquota>{{nfse.servico.valor.aliquota}}</Aliquota>
                            <DescontoIncondicionado>{{nfse.servico.valor.desconto_incondicionado}}</DescontoIncondicionado>
                            <DescontoCondicionado>{{nfse.servico.valor.desconto_condicionado}}</DescontoCondicionado>
                        </Valores>
                        <ItemListaServico>{{nfse.servico.item_lista_servicos}}</ItemListaServico>
                        <CodigoTributacaoMunicipio>{{nfse.servico.codigo_tributacao_municipio}}</CodigoTributacaoMunicipio>
                        <Discriminacao>{{nfse.servico.discriminacao}}</Discriminacao>
                        <CodigoMunicipio>{{nfse.servico.codigo_municipio}}</CodigoMunicipio>
                    </Servico>
                    <Prestador>
                        <Cnpj>{{nfse.emissor.cnpj}}</Cnpj>
                        <InscricaoMunicipal>{{nfse.emissor.inscricao_municipal}}</InscricaoMunicipal>
                    </Prestador>
                    <Tomador>
                        <IdentificacaoTomador>
                            {% if not nfse.cliente_estrangeiro %}
                                <CpfCnpj>
                                        {% if nfse.pessoa_juridica %}
                                            <Cnpj>{{nfse.tomador.cnpj}}</Cnpj>
                                        {% else %}
                                            <Cpf>{{nfse.tomador.cpf}}</Cpf>
                                        {% endif %}
                                </CpfCnpj>
                            {% endif %}
                        </IdentificacaoTomador>
                        <RazaoSocial>{{nfse.tomador.razao_social}}</RazaoSocial>
                            <Endereco>
                                <Endereco>{{nfse.tomador.endereco.endereco}}</Endereco>
                                {% if nfse.tomador.endereco.numero %}
                                    <Numero>{{nfse.tomador.endereco.numero}}</Numero>
                                {% endif %}
                                {% if nfse.tomador.endereco.complemento %}
                                    <Complemento>{{nfse.tomador.endereco.complemento}}</Complemento>
                                {% endif %}
                                {% if nfse.tomador.endereco.bairro %}
                                    <Bairro>{{nfse.tomador.endereco.bairro}}</Bairro>
                                {% endif %}
                                {% if nfse.tomador.endereco.codigo_municipio %}
                                    <CodigoMunicipio>{{nfse.tomador.endereco.codigo_municipio}}</CodigoMunicipio>
                                {% endif %}
                                <Uf>{{nfse.tomador.endereco.uf}}</Uf>
                                {% if nfse.tomador.endereco.cep %}
                                    <Cep>{{nfse.tomador.endereco.cep}}</Cep>
                                {% endif %}
                                </Endereco>
                        <Contato>
                            {% if nfse.tomador.telefone %}
                                <Telefone>{{nfse.tomador.telefone}}</Telefone>
                            {% endif %}
                            {% if nfse.tomador.email %}
                                <Email>{{nfse.tomador.email}}</Email>
                            {% endif %}
                        </Contato>
                    </Tomador>
                </InfRps>
            </Rps>
'''

enviarlote = '''
<EnviarLoteRpsEnvio xmlns="http://www.abrasf.org.br/ABRASF/arquivos/nfse.xsd">
    <LoteRps Id="{{lote_id}}">
        <NumeroLote>{{numero_lote}}</NumeroLote>
        <Cnpj>{{cnpj}}</Cnpj>
        <InscricaoMunicipal>{{inscricao_municipal}}</InscricaoMunicipal>
        <QuantidadeRps>{{len(rps_list)}}</QuantidadeRps>
        <ListaRps>
            {{rps_string}}
        </ListaRps>
    </LoteRps>
</EnviarLoteRpsEnvio>
'''
