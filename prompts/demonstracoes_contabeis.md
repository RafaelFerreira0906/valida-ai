**ATENÇÃO:**
O resultado deverá conter o retorno concatenado dos jsons dos 3 prompts, apenas para o ano mais recente. Você não deve utilizar instruções de um prompt em outro prompt, e você não deve excluir campos dos jsons.

PROMPT 1

# CONTEXTO

O usuário enviará um texto ou um arquivo PDF contendo as demonstrações financeiras de uma empresa.
Esse texto é fruto de OCR e pode conter ruídos, trechos de timbres e carimbos em meio ao texto do Balanço Patrimonial.
O OCR estará representado no formato de tabelas MARKDOWN, mas nem todos os dados estavam em tabelas inicialmente.

# COMANDO

Você deverá analisar esse documento e preencher as informações relativas às contas do Balanço Patrimonial.
Ignore todo o texto não relacionado às contas do Balanço Patrimonial
Você nunca deverá realizar cálculos (somas ou subtrações) ou deduzir valores que não estejam no OCR.
Você deve tentar, sempre que possível, encaixar os nomes das contas do Balanço Patrimonial nas variáveis de saída do resultado.
Sempre retorne os dados "Controladora", quando houver dados de mesmo período para a "Controladora" e para o "Consolidado".
Sempre retorne os dados das "Demonstrações financeiras consolidadas", quando houver dados de mesmo período para a "Demonstrações financeiras consolidadas" e para o "Demonstrações financeiras individuais".
Sempre preencha os campos "outras_contas" somente com as contas que não foram enquadradas nas existentes.
Sempre utilize os valores das contas presentes no balanço patrimonial quando houver contas com nomes correspondentes em outras demonstrações financeiras.
Você não deve em hipotese alguma, retornar informação de uma determinada conta em outra. Caso a informação de uma determinada conta existente no JSON, não exista no documento enviado, retorne no campo correspondente a valor "null". Exemplo: Se no documento existe uma conta chamada "DISPONIBILIDADES" ou "CRÉDITOS", você não deve retornar a valor dessa conta em qualquer outro campo de uma das contas do JSON.

Leia o texto do Balanço Patrimonial fornecido pelo usuário e identifique e extraia as seguintes informações: 

## 1. INSTRUÇÃO PARA ANÁLISE DE BALANÇO PATRIMONIAL

Ao realizar a análise, **utilize estritamente os dados e valores apresentados nas seções do Balanço Patrimonial (Ativo, Passivo e Patrimônio Líquido)**, desconsiderando quaisquer outras informações, comentários, notas explicativas, relatórios de administração, demonstrações de resultado, fluxos de caixa ou quaisquer outros dados presentes no restante do documento.
Somente as informações contidas diretamente no Balanço Patrimonial devem ser consideradas para a extração, cálculo de indicadores e validação das pendências solicitadas.
Os valores devem ser extraídos exatamente como apresentados no quadro do balanço patrimonial.
 
## 2. BALANÇO PATRIMONIAL

O balanço patrimonial é um relatório financeiro que apresenta a situação contábil e econômica de uma empresa em um determinado período. Seus principais requisitos incluem a listagem de todos os ativos, passivos e o patrimônio líquido da empresa. As informações obrigatórias são os bens, direitos, obrigações e investimentos que compõem o negócio, fornecendo uma visão clara da saúde financeira da empresa.

### 2.2 Balanço Patrimonial Consolidado

A controladora é responsável por consolidar as demonstrações financeiras das empresas controladas e apresentar as informações consolidadas no seu próprio balanço patrimonial. O balanço consolidado é a soma das demonstrações contábeis das empresas do grupo, que podem ser controladoras ou controladas. Sempre Retorne os dados "Controladora", quando houver dados de mesmo período para a "Controladora" e para o "Consolidado".

O balanço patrimonial consolidado é um relatório financeiro que apresenta a situação financeira de um grupo de empresas como se fosse uma única entidade. Ele é elaborado pela empresa-mãe e é importante para avaliar a situação do grupo e de cada uma das empresas que o compõem.

O balanço consolidado é feito combinando as demonstrações financeiras de cada empresa do grupo, eliminando transações entre elas e ajustando para refletir a participação de cada empresa.

- O balanço consolidado é importante por:

Permitir que as partes interessadas avaliem a empresa-mãe como um todo
Permitir que os investidores tomem decisões com base nas informações reais sobre a situação financeira das empresas
Oferecer uma visão mais ampla dos negócios e do operacional de todas as empresas do grupo
A elaboração do balanço consolidado é obrigatória em alguns casos, como para empresas de capital aberto que detêm 30% do seu património líquido investido em outras empresas

- As informações que não podem faltar em um balanço patrimonial são:

**Data de encerramento do exercício:** Indica o período a que se referem as informações contidas no balanço.
**Moeda utilizada:** Especifica a moeda em que as contas estão expressas.
**Nome da empresa:** Identifica a empresa a que se refere o balanço.
**Ativo:** Representa os bens e direitos da empresa, como:
Ativo circulante: Dinheiro em caixa, contas a receber, estoques, etc.
Ativo não circulante: Imóveis, máquinas, equipamentos, investimentos a longo prazo, etc.
**Passivo:** Representa as obrigações da empresa, como:
Passivo circulante: Fornecedores, impostos a pagar, salários a pagar, etc.
Passivo não circulante: Empréstimos a longo prazo, financiamentos, etc.
**Patrimônio líquido:** Representa a diferença entre o ativo e o passivo, ou seja, o valor que os proprietários têm na empresa. É composto por:
Capital social: Valor do capital investido pelos sócios.
Reservas de lucros: Lucros acumulados e não distribuídos.
Lucros ou prejuízos acumulados: Resultados de exercícios anteriores.

- Além dessas informações básicas, o balanço patrimonial pode conter outros detalhes, como:

**Contas detalhadas:** Cada conta do ativo, passivo e patrimônio líquido deve ser detalhada para facilitar a análise.
Notas explicativas: Informações complementares que esclarecem os valores apresentados no balanço.
Comparativo com exercícios anteriores: Permite identificar tendências e variações na situação financeira da empresa.
Para ser válido, um balanço patrimonial precisa conter:

Termo de abertura e de encerramento
Demonstração do resultado do exercício (DRE)
Balanço patrimonial do último exercício social
Assinatura do contador e do representante legal da empresa
Registro na Junta Comercial
Informações sobre ativos, passivos e patrimônio líquido
O balanço patrimonial deve ser apresentado até o final do quarto mês do ano seguinte ao exercício social, ou seja, até 30 de abril. A partir dessa data, os informes anteriores perdem a sua validade.

### 2.3 Balanço Patrimonial auditado por um auditor registrado na Comissão de Valores Mobiliários (CVM) ou em uma autoridade equivalente no exterior.

Em balanços patrimoniais, especialmente para empresas de grande porte, há a obrigatoriedade de auditoria independente. Isso significa que o balanço patrimonial deve ser auditado por um auditor registrado na Comissão de Valores Mobiliários (CVM) ou em uma autoridade equivalente no exterior.

A Lei 11.638/2007 estabelece que empresas com ativo total superior a R$ 240.000.000,00 ou receita bruta anual superior a R$ 300.000.000,00 devem ter suas demonstrações financeiras auditadas por um auditor independente. Além disso, o Manual de Orientação da ECD (Escrituração Contábil Digital) também exige o registro dos auditores independentes.

## 3. ÍNDICES:

- Analise os dados fornecidos, busque até, no máximo, os dados dos últimos 3 exercícios/anos e calcule os seguintes indicadores financeiros:

**Liquidez Corrente:** Razão entre o Ativo Circulante e o Passivo Circulante.
Fórmula: Liquidez Corrente = Ativo Circulante / Passivo Circulante
**Liquidez Seca:** Razão entre o Ativo Circulante menos Estoques e o Passivo Circulante.
Fórmula: Liquidez Seca = (Ativo Circulante - Estoques) / Passivo Circulante
**Liquidez Imediata:** Razão entre Disponibilidades (Caixa, Bancos Conta Movimento e Aplicações Financeiras) e o Passivo Circulante.
Fórmula: Liquidez Imediata = (Caixa + Bancos Conta Movimento + Aplicações Financeiras) / Passivo Circulante
**Índice de Solvência Geral:** Razão entre o Ativo Total e o Passivo Total.
Fórmula: Índice de Solvência Geral = Ativo Total / Passivo Total
**Rentabilidade do Ativo (ROA):** Razão entre o Lucro Líquido e o Ativo Total.
Fórmula: ROA = Lucro Líquido / Ativo Total
(Caso o Lucro Líquido não esteja disponível, utilize lucros_prejuizos_acumulados / Ativo Total)
**Rentabilidade do Patrimônio (ROE):** Razão entre o Lucro Líquido e o Patrimônio Líquido.
Fórmula: ROE = Lucro Líquido / Patrimônio Líquido
(Caso o Lucro Líquido não esteja disponível, utilize lucros_prejuizos_acumulados / Patrimônio Líquido)

## 4. CONTAS DO ATIVO COM SALDO CREDOR

No ativo, apenas as contas de "depreciacao_acumulada" e "provisao_devedores_duvidosos" podem ter valores negativos. As demais contas do ativo no balanço patrimonial NÃO podem ter valores negativos (saldo credor), pois são de natureza devedora. Sempre que houver saldo credor (valor negativo) em alguma conta do Ativo, exceto depreciação acumulada e provisão devedores duvidosos, retorne "pendencia_conta_ativo_credor" como "true". Se não houver, retorne "false".

## 5. CONTAS DO PASSIVO COM SALDO DEVEDOR

As contas do passivo no balanço patrimonial NÃO podem ter valores negativos (saldo devedor), pois são de natureza credora. Sempre que houver saldo devedor (valor negativo) em alguma conta do Passivo, retorne "pendencia_conta_passivo_devedor" como "true". Se não houver, retorne "false".

## 6. ATIVO E PASSIVO COMPENSADO

A conta Ativo Compensado compreende contas de COMODATO + SERVIÇOS CONTRATADOS + GARANTIAS DIVERSAS. A conta Passivo Compensado compreende contas de COMODATO + SERVIÇOS CONTRATADOS + GARANTIAS DIVERSAS. Os valores da conta ativo compensado devem ser iguais aos valores da conta passivo compensado. Sempre retorne "true" no campo "pendencia_comodato", quando dentro dos valores de cada balanço o valor do "passivo_compensado" for diferente do "ativo_compensado", ou "servicos_contratados_ativo" for diferente de "servicos_contratados_passivo", ou "garantias_diversas_ativo" for diferente de "garantias_diversas_passivo", ou "comodato_de_bens_ativo" for diferente de "comodato_de_bens_passivo". Nos demais casos, retorne "false" no campo "pendencia_comodato".

## 7. PENDÊNCIAS:

Caso detecte Resultado Líquido do exercício com prejuízo ou Patrimônio Líquido negativo, favor comentar no campo de "observacoes".

## 8. VÁRIOS BALANÇOS

Certifique-se de que todos os anos disponíveis sejam considerados.
Sempre que houver múltiplos períodos, selecione os dados dos últimos três anos. Caso existam menos de três anos, utilize todos os anos disponíveis.

Sempre considere que 01 de janeiro de um ano, como sendo 31 de dezembro do ano anterior.
Exemplo:
-"01/01/2020, será considerado como balanço de 31/12/2019;
-01/01/2021, será considerado como balanço de 31/12/2020;
-01/01/2022, será considerado como balanço de 31/12/2021;
-01/01/2023, será considerado como balanço de 31/12/2022;
-01/01/2025, será considerado como balanço de 31/12/2024;
-E assim por diante.

É crucial que você sempre utilize os saldos iniciais ou saldos anteriores apresentados no documento como referência para compor os dados do balanço patrimonial do ano anterior. Isso significa que, ao identificar um período de balanço, os valores listados como 'saldos iniciais' devem ser interpretados como pertencentes ao final do exercício do ano anterior. Assim, ao processar o balanço patrimonial, considere esses saldos como representativos do estado financeiro da empresa no encerramento do ano anterior.

**Exemplo:**

Suponha que você tenha um documento de balanço patrimonial para o ano de 2023, com os seguintes dados:

Saldos Iniciais (01/01/2023):
Total Ativo: R$ 31.333.569,30
Ativo Circulante: R$ 13.424.696,50
Passivo Circulante: R$ 2.117.567,01
Patrimônio Líquido: R$ -4.127.340,11
Saldos Finais (31/12/2023):
Total Ativo: R$ 41.029.988,96
Ativo Circulante: R$ 11.574.303,10
Passivo Circulante: R$ 5.456.269,32
Patrimônio Líquido: R$ 177.567,40

**Aplicação da Instrução:**

Para compor o balanço patrimonial do ano de 2022, utilize os saldos iniciais de 2023 como os saldos finais de 2022. Assim, o balanço para o ano de 2022 seria:
Balanço Patrimonial para 2022 (31/12/2022):
Total Ativo: R$ 31.333.569,30
Ativo Circulante: R$ 13.424.696,50
Passivo Circulante: R$ 2.117.567,01
Patrimônio Líquido: R$ -4.127.340,11

**Identificação de Períodos:**
- Ao analisar o documento, identifique todos os períodos de balanço patrimonial presentes. Certifique-se de que todos os anos disponíveis sejam considerados.
**Seleção dos Últimos Três Anos:**
-Sempre que houver múltiplos períodos, selecione os dados dos últimos três anos. Caso existam menos de três anos, utilize todos os anos disponíveis.
**Estrutura de Resposta:**
- Para cada ano identificado, crie um novo objeto dentro do array "balanco_patrimonial_detalhado".
- As informações devem ser organizadas em ordem decrescente, começando pelo ano mais recente.
**Preenchimento de Campos:**
- Certifique-se de preencher todos os campos relevantes para cada ano, conforme o modelo JSON fornecido.
- Caso alguma informação não esteja disponível para um determinado ano, preencha o campo correspondente com "null".
**Cálculo de Indicadores:**
- Calcule os indicadores financeiros para cada ano individualmente, utilizando os dados específicos daquele período.
**Consistência e Verificação:**
- Verifique a consistência dos dados entre os anos, especialmente em relação a ativos, passivos e patrimônio líquido.
- Inclua observações sobre a evolução financeira da empresa ao longo dos anos analisados.

## 9. FORMATO DE RESPOSTA

Sempre crie um array contendo os dados detalhados do balanço patrimonial para os últimos três exercícios/anos. Sempre que não encontrar as informações deixe os campos vazios.

Apresente sua resposta final no formato JSON, considerando que as datas do orçamento devem estar no formato ‘%Y-%m-%d’.

{
   "e_balanco_patrimonial":"boolean",
   "nome_empresa":"string",
   "cnpj_empresa":"string",
   "assinatura_representante":"string",
   "assinatura_contador":"string",
   "observacoes":"string",
   "pendencia_nao_existe_dre":"boolean",
   "balanco_auditado_por_auditor_registrado":"boolean",
   "balanco_patrimonial_consolidado_grupo":"boolean",
   "balanco_patrimonial_detalhado":[
      {
         "ano_balanco":"number",
         "data_encerramento_exercicio":"date",
         "pendencia_conta_ativo_credor":"boolean",
         "pendencia_conta_passivo_devedor":"boolean",
         "total_ativo":"number",
         "ativo_circulante":"number",
         "ativos_detalhados":{
            "caixa":"number",
            "bancos_conta_movimento":"number",
            "aplicacoes_financeiras":"number",
            "titulos_valores_mobiliarios":"number",
            "contas_receber":"number",
            "provisao_devedores_duvidosos":"number",
            "adiantamento_fornecedores":"number",
            "impostos_recuperar":"number",
            "estoques":"number",
            "outras_contas_ativo_circulante":[
               {
                  "nome":"string",
                  "valor":"number"
               }
            ]
         },
         "realizavel_longo_prazo":"number",
         "realizavel_longo_prazo_detalhado":{
            "investimentos_longo_prazo":"number",
            "adiantamentos_fornecedores":"number",
            "emprestimos_empresas_ligadas":"number",
            "outras_contas_realizavel_longo_prazo":[
               {
                  "nome":"string",
                  "valor":"number"
               }
            ]
         },
         "ativo_permanente":"number",
         "investimentos_ativo_permante":"number",
         "ativo_investimento_detalhado":{
            "participacoes_empresas_ligadas_ou_coligadas_ou_controladas":"number",
            "outras_contas_investimentos_ativo_permante":[
               {
                  "nome":"string",
                  "valor":"number"
               }
            ]
         },
         "imobilizado":"number",
         "imobilizado_detalhado":{
            "imoveis":{
               "terrenos":"number",
               "edificacoes":"number"
            },
            "bens_em_uso":{
               "moveis_utensilios":"number",
               "veiculos":"number",
               "maquinas_equipamentos_ferramentas":"number"
            },
            "depreciacao_acumulada":"number",
            "outras_contas_imobilizado":[
               {
                  "nome":"string",
                  "valor":"number"
               }
            ]
         },
         "diferido":"number",
         "diferido_detalhado":{
            "gastos":"number"
         },
         "conta_compensacao_ativo":"number",
         "conta_compensacao_ativo_detalhado":{
            "servicos_contratados_ativo":"number",
            "garantias_diversas_ativo":"number",
            "comodato_de_bens_ativo":"number"
         },
         "total_passivo":"number",
         "passivo_circulante":"number",
         "passivos_detalhados":{
            "duplicatas_descontadas":"number",
            "emprestimos_financiamentos":"number",
            "debentures":"number",
            "fornecedores":"number",
            "dividas_empresas_ligadas":"number",
            "dividendos_pagar":"number",
            "salarios_encargos_tributos_contribuicoes":[
               {
                  "nome":"string",
                  "valor":"number"
               }
            ]
         },
         "provisoes_para_contingencias":[
            {
               "nome":"string",
               "valor":"number"
            }
         ],
         "provisoes_circulante":[
            {
               "nome":"string",
               "valor":"number"
            }
         ],
         "outras_contas_passivo_circulante":[
            {
               "nome":"string",
               "valor":"number"
            }
         ],
         "exigivel_longo_prazo":"number",
         "exigivel_longo_prazo_detalhado":{
            "emprestimos_financiamentos":"number",
            "debentures":"number",
            "dividas_empresas_ligadas":"number",
            "provisoes_contingencias":"number",
            "impostos_parcelados":"number",
            "resultados_exercicios_futuros":"number",
            "participacoes_minoritarios":"number",
            "outras_contas_exigivel_longo_prazo":[
               {
                  "nome":"string",
                  "valor":"number"
               }
            ]
         },
         "conta_compensacao_passivo":"number",
         "conta_compensacao_passivo_detalhado":{
            "servicos_contratados_passivo":"number",
            "garantias_diversas_passivo":"number",
            "comodato_de_bens_passivo":"number"
         },
         "patrimonio_liquido":"number",
         "patrimonio_liquido_detalhado":{
            "capital_social_realizado_integralizado":"number",
            "capital_social_subscrito":"number",
            "reservas_capital":"number",
            "reservas_lucros":"number",
            "reservas_reavaliacao":"number",
            "lucros_prejuizos_acumulados":"number",
            "outras_contas_patrimonio_liquido":[
               {
                  "nome":"string",
                  "valor":"number"
               }
            ]
         },
         "indicadores_financeiros":{
            "rentabilidade_do_patrimonio":"number",
            "liquidez_corrente":"number",
            "liquidez_seca":"number",
            "liquidez_imediata":"number",
            "indice_de_solvencia_geral":"number",
            "rentabilidade_do_ativo":"number",
            "pendencia_comodato":"boolean"
         }
      }
   ]
}

Sempre que o conteúdo do documento não for de um Balanço Patrimonial o campo "e_balanco_patrimonial" deve ser respondido com o valor "false", e os demais campos devem ficar preenchidos com "null".

Sempre retorne "true" no campo "pendencia_comodato", quando dentro dos valores de cada balanço o valor do "conta_compensacao_passivo" for diferente do "conta_compensacao_ativo", ou "servicos_contratados_ativo" for diferente de "servicos_contratados_passivo", ou "garantias_diversas_ativo" for diferente de "garantias_diversas_passivo", ou "comodato_de_bens_ativo" for diferente de "comodato_de_bens_passivo". Nos demais casos, retorne "false" no campo "pendencia_comodato".

Sempre considere que 01 de janeiro de um determinado ano, como sendo 31 de dezembro do ano anterior para preencher o campo "data_encerramento_exercicio".

Os campos assinatura_representante e assinatura_contador devem conter, quando presentes, os respectivos nomes completos do representante e do contador. Caso contrário, deverão vir vazios.

O array do "balanco_patrimonial_detalhado", de ano/exercício deverá ser em com base no ano de cada exercício em ordem decrescente e sucessivamente.

Sempre retorne o(s) resultado(s) do cálculo do Lucro Líquido / Patrimônio Líquido no campo "rentabilidade_do_patrimonio". Caso o Lucro Líquido não esteja disponível, utilize lucros_prejuizos_acumulados / Patrimônio Líquido.

Sempre retorne o(s) resultado(s) do cálculo Ativo Circulante / Passivo Circulante no campo "liquidez_corrente".

Sempre retorne o(s) resultado(s) do cálculo (Ativo Circulante - Estoque) / Passivo Circulante, no campo "liquidez_seca".

Sempre retorne o(s) resultado(s) do cálculo (Caixa + Bancos Conta Movimento + Aplicações Financeiras) / Passivo Circulante, no campo "liquidez_imediata".

Sempre retorne o(s) resultado(s) do cálculo do Ativo Total / Passivo Total, no campo "indice_de_solvencia_geral".

Sempre retorne o(s) resultado(s) do cálculo do Lucro Líquido / Ativo Total no campo "rentabilidade_do_ativo". Caso o Lucro Líquido não esteja disponível, utilize lucros_prejuizos_acumulados / Ativo Total.

Sempre que houver saldo credor (valor negativo) em alguma conta do Ativo, exceto depreciação acumulada e provisão devedores duvidosos, retorne "pendencia_conta_ativo_credor" como "true". Se não houver, retorne "false".

Sempre que houver saldo devedor (valor negativo) em alguma conta do Passivo, retorne "pendencia_conta_passivo_devedor" como "true". Se não houver, retorne "false".

Sempre que houver um Período da Escrituração selecionado com saldo inicial e saldo final. Os primeiros valores numéricos de cada item do Balanço patrimonial referem-se à data do período anterior e os segundos valores referem-se à data do período posterior.

Sempre retorne "true" no campo "pendencia_nao_existe_dre" quando NÃO detectar que existe o Demonstrativo do Resultado do Exercício (DRE). Nos demais casos, retorne "false".

O valor atribuído ao campo "lucros_prejuízos_acumulados" varia de acordo com o contexto: pode ser positivo, indicando lucros acumulados, ou negativo, representando prejuízos acumulados.

No campo "observacoes", retorne um resumo de no máximo 15 linhas da evolução do balanço patrimonial da empresa ao longo dos últimos anos. Compare os ativos, passivos e patrimônio líquido em cada ano. Identifique as principais tendências e mudanças significativas, considerando o contexto econômico de cada período. Com base nessa análise, forneça recomendações práticas para melhorar a saúde financeira da empresa nos próximos anos.

Os campos de "outras_contas", deveram trazer todas as informações do balanço patrimonial, onde não haja campos específicos no JSON, com exceção dos campos com rubricas próprias, com por exemplo "salarios_encargos_tributos_contribuicoes".

No campo "bancos_conta_movimento" podem estar contidos os valores das seguintes contas: Conta corrente Banco do Brasil, Conta corrente Caixa Econômica Federal, Conta corrente Bradesco, Conta corrente Itaú, Conta corrente Santander, Conta corrente Banco Inter, Conta corrente Nubank, Conta corrente em moeda estrangeira, Conta corrente vinculada a empréstimos, Conta corrente para folha de pagamento, Depósitos Bancários à Vista.

No campo "investimentos_ativo_permante", podem estar contidos os valores das seguintes contas: Aplicações em Fundos de Investimento, Aplicações em Títulos Públicos (Tesouro Direto), Aplicações em RDBs (Recibos de Depósito Bancário), Aplicações em Letras Financeiras, Aplicações em Debêntures, Aplicações em Operações Compromissadas, Aplicações em Poupança, Aplicações em Moeda Estrangeira, Aplicações com Resgate Superior a 12 Meses.

No campo "salarios_encargos_tributos_contribuicoes", podem estar contidos os valores das seguintes contas: Provisão para 13º salário, Provisão para férias, Provisão para INSS patronal, Provisão para FGTS, Provisão para IRPJ ou CSLL, Provisão para encargos sociais sobre salários, IRRF a recolher, INSS a recolher, ISS a recolher, ICMS a recolher, PIS a recolher, COFINS a recolher, CSLL a recolher, Simples Nacional a recolher, IPI a recolher, Parcelamentos fiscais, FGTS a recolher, Taxas municipais a recolher, Taxas estaduais a recolher, IRPJ a recolher, Multas fiscais a pagar, Juros de tributos a pagar, Contribuição sindical a recolher, Retenções de terceiros (INSS, IRRF, ISS sobre serviços contratados), Tributos retidos sobre nota fiscal, Obrigações acessórias pendentes, IRRF sobre serviços tomados, INSS patronal sobre folha, INSS sobre pró-labore, IRPJ estimado, CSLL estimada, Retenção de PIS/COFINS/CSLL, IRRF sobre aluguéis, INSS sobre cessão de mão de obra, Tributos sobre importação, Obrigações fiscais de exercícios anteriore.

No campo "provisoes_para_contingencias", podem estar contidos os valores das seguintes contas: Provisão para contingências judiciais, Provisão para garantias de produtos, Provisão para perdas com clientes, Provisão para indenizações futuras

No campo "provisoes_circulante", podem estar contidos os valores das seguintes contas: Provisão para Férias, Provisão para 13º Salário, Provisão para Contingências, Provisão para Garantias de Produtos, Provisão para Devedores Duvidosos (quando classificada no passivo, em casos específicos), Provisão para Rescisões Trabalhistas, Provisão para Impostos e Contribuições a Recolher.

No campo "capital_social_realizado_integralizado", podem estar contidos os valores das seguintes contas: Capital integralizado em dinheiro, Capital integralizado em bens móveis, Capital integralizado em bens imóveis, Capital integralizado por transferência bancária, Capital integralizado por veículos, Capital integralizado por equipamentos, Capital integralizado por direitos autorais ou marcas, Capital integralizado por títulos de crédito, Capital integralizado por imóveis rurais, Capital integralizado por quotas de outras empresas.

No campo "capital_social_subscrito", podem estar contidos os valores das seguintes contas: Capital subscrito em dinheiro, Capital subscrito em bens móveis, Capital subscrito em bens imóveis, Capital subscrito por transferência bancária, Capital subscrito por veículos, Capital subscrito por equipamentos, Capital subscrito por direitos autorais ou marcas, Capital subscrito por títulos de crédito, Capital subscrito por imóveis rurais, Capital subscrito por quotas de outras empresas.

No campo "edificacoes", podem estar contidos os valores das seguintes contas: Prédios comerciais, Prédios industriais, Imóveis residenciais, Construções em andamento, Benfeitorias em imóveis de terceiros, Reformas e ampliações, Imóveis rurais, Imóveis para investimento.

Sempre que o conteúdo do documento houver balanços de anos diferentes, na variável "ano_balanco", deverá vir com esses anos, em ordem decrescente, e as demais informações devem ser replicadas, na sequência, com as informações de seus respectivos anos.

## Lista de Possíveis Outras Denominações para os Campos de "balanco_patrimonial_detalhado"
 
1. ano_balanco: exercício, exercício social, ano do balanço, período de referência, ano-base.
2. data_encerramento_exercicio: data de encerramento, data de fechamento, data do balanço, data final do exercício, data de referência.
3. pendencia_conta_ativo_credor: ativo com saldo credor, ativo negativo indevido, inconsistência no ativo, saldo credor em contas do ativo.
4. pendencia_conta_passivo_devedor: passivo com saldo devedor, passivo negativo indevido, inconsistência no passivo, saldo devedor em contas do passivo.
5. total_ativo: ativo total, total do ativo, soma do ativo, ativo consolidado, total dos bens e direitos.
6. ativo_circulante: circulante, ativo de curto prazo, ativo corrente, bens e direitos realizáveis no exercício seguinte.
7. ativos_detalhados:
- caixa: disponível, dinheiro em caixa, numerário, saldo em caixa.
- bancos_conta_movimento: bancos, bancos conta corrente, depósitos bancários, saldo bancário.
- aplicacoes_financeiras: aplicações financeiras, investimentos de liquidez imediata, aplicações de curto prazo, investimentos temporários.
- titulos_valores_mobiliarios: títulos e valores mobiliários, TVM, investimentos em títulos, valores mobiliários.
- contas_receber: clientes, duplicatas a receber, contas a receber de clientes, recebíveis.
- provisao_devedores_duvidosos: PDD, provisão para créditos de liquidação duvidosa, provisão para devedores duvidosos, provisão para perdas em créditos.
- adiantamento_fornecedores: adiantamentos a fornecedores, adiantamentos concedidos, adiantamentos pagos.
- impostos_recuperar: impostos a recuperar, tributos a recuperar, créditos tributários.
- estoques: estoque, inventário, mercadorias para revenda, produtos acabados, produtos em elaboração, matérias-primas.
- outras_contas_ativo_circulante: outros créditos, outros valores do ativo circulante, demais ativos circulantes.
8. realizavel_longo_prazo: ativo não circulante realizável a longo prazo, realizável a longo prazo, créditos de longo prazo, ativos de longo prazo.
9. realizavel_longo_prazo_detalhado:
- investimentos_longo_prazo: investimentos permanentes, participações societárias, aplicações em empresas coligadas/controladas.
- adiantamentos_fornecedores: adiantamentos a fornecedores de longo prazo, adiantamentos concedidos a longo prazo.
- emprestimos_empresas_ligadas: empréstimos a partes relacionadas, créditos com empresas ligadas, empréstimos a coligadas/controladas.
- outras_contas_realizavel_longo_prazo: outros créditos de longo prazo, demais ativos de longo prazo..
10. ativo_permanente: ativo não circulante, ativo fixo, ativo imobilizado e investimentos, bens permanentes.
11. investimentos_ativo_permante: investimentos, participações permanentes, investimentos em outras empresas.
12. ativo_investimento_detalhado:
- participacoes_empresas_ligadas_ou_coligadas_ou_controladas: participações em coligadas, participações em controladas, investimentos em empresas do grupo.
- outras_contas_investimentos_ativo_permante: outros investimentos, aplicações permanentes diversas.
13. imobilizado: ativo imobilizado, imobilizado, bens do ativo fixo, bens tangíveis.
14. imobilizado_detalhado:
- imoveis:		  
- terrenos: terrenos e benfeitorias, propriedades para uso.
- edificacoes: edifícios, construções, imóveis.
- bens_em_uso:			  
- moveis_utensilios: móveis e utensílios, equipamentos de escritório, mobiliário.
- veiculos: veículos automotores, frota.
- depreciacao_acumulada: depreciação acumulada, provisão para depreciação, ajuste de depreciação.
- outras_contas_imobilizado: outros bens do imobilizado, demais ativos imobilizados.
15. diferido: ativo diferido, despesas diferidas, gastos diferidos.
16. diferido_detalhado:
- gastos: despesas a apropriar, gastos a apropriar, despesas diferidas.
17. conta_compensacao_ativo: contas de compensação do ativo, ativo compensado, contas compensatórias do ativo.
18. conta_compensacao_ativo_detalhado:
- servicos_contratados_ativo: serviços contratados (ativo), contratos de serviços ativos.
- garantias_diversas_ativo: garantias prestadas, garantias diversas (ativo).
- comodato_de_bens_ativo: comodato de bens (ativo), bens em comodato (ativo).
19. total_passivo: passivo total, total do passivo, soma do passivo, total das obrigações.
20. passivo_circulante: circulante (passivo), passivo de curto prazo, obrigações de curto prazo.
21. passivos_detalhados:
- duplicatas_descontadas: duplicatas descontadas, títulos descontados.
- emprestimos_financiamentos: empréstimos e financiamentos, financiamentos bancários, dívidas bancárias.
- debentures: debêntures, títulos de dívida.
- fornecedores: contas a pagar a fornecedores, fornecedores a pagar.
- dividas_empresas_ligadas: dívidas com partes relacionadas, obrigações com empresas ligadas.
- dividendos_pagar: dividendos a pagar, distribuição de lucros a pagar.
- salarios_encargos_tributos_contribuicoes: salários a pagar, encargos sociais a pagar, tributos a recolher, contribuições a recolher.
- provisoes_para_contingencias: provisões para contingências, provisões trabalhistas/judiciais.
- outras_contas_passivo_circulante: outros passivos circulantes, demais obrigações de curto prazo.
22. exigivel_longo_prazo: passivo não circulante, exigível a longo prazo, obrigações de longo prazo.
23. exigivel_longo_prazo_detalhado:
- emprestimos_financiamentos: empréstimos e financiamentos de longo prazo, financiamentos a longo prazo.
- debentures: debêntures de longo prazo.
- dividas_empresas_ligadas: dívidas com partes relacionadas de longo prazo.
- provisoes_contingencias: provisões para contingências de longo prazo.
- provisoes_circulante: Obrigações Estimadas de Curto Prazo, Encargos Provisionados, Passivos Estimados, Reservas para Obrigações de Curto Prazo, Passivos Contingentes Prováveis, Despesas Provisionadas, Obrigações Provisionadas, Encargos a Pagar Estimados, Provisões Operacionais, Provisões de Exercício Social, Provisões de Responsabilidades, Provisões de Passivo Circulante, Provisões de Curto Prazo, Estimativas de Obrigações, Contas de Provisão de Curto Prazo.
- impostos_parcelados: impostos parcelados, tributos parcelados.
- resultados_exercicios_futuros: receitas diferidas, resultados de exercícios futuros.
- participacoes_minoritarios: participações de não controladores, interesses minoritários.
- outras_contas_exigivel_longo_prazo: outros passivos de longo prazo, demais obrigações de longo prazo.						 
24. conta_compensacao_passivo: contas de compensação do passivo, passivo compensado, contas compensatórias do passivo.
25. conta_compensacao_passivo_detalhado:
- servicos_contratados_passivo: serviços contratados (passivo), contratos de serviços passivos.
- garantias_diversas_passivo: garantias recebidas, garantias diversas (passivo).
- comodato_de_bens_passivo: comodato de bens (passivo), bens em comodato (passivo).
26. patrimonio_liquido: patrimônio líquido, PL, capital próprio, total do patrimônio líquido.
27. patrimonio_liquido_detalhado:
- capital_social_realizado_integralizado: capital social integralizado, capital realizado, capital subscrito e integralizado.
- capital_social_subscrito: Capital social subscrito, ainda não integralizado.
- reservas_capital: reservas de capital.
- reservas_lucros: reservas de lucros.
- reservas_reavaliacao: reservas de reavaliação.
- lucros_prejuizos_acumulados: lucros acumulados, prejuízos acumulados, resultados acumulados.
- outras_contas_patrimonio_liquido: outras reservas, reservas estatutárias.		  
28. indicadores_financeiros:
- rentabilidade_do_patrimonio: ROE, rentabilidade do patrimônio líquido, retorno sobre o patrimônio líquido.
- liquidez_corrente: índice de liquidez corrente, razão corrente.
- liquidez_seca: índice de liquidez seca.
- liquidez_imediata: índice de liquidez imediata.
- indice_de_solvencia_geral: índice de solvência, solvência geral.
- rentabilidade_do_ativo: ROA, rentabilidade do ativo, retorno sobre o ativo.
- pendencia_comodato: pendência em contas de compensação, divergência em contas compensatórias.

Sempre que uma informação não estiver disponível no texto do orçamento, retorne no campo correspondente "null".

PROMPT 2

## CONTEXTO

O usuário enviará um texto ou um arquivo PDF contendo a Demonstração do Resultado do Exercício (DRE) de uma empresa.
Esse texto pode ser fruto de OCR e conter ruídos, timbres, carimbos ou informações não estruturadas.
O OCR estará representado no formato de tabelas MARKDOWN, mas nem todos os dados estavam em tabelas inicialmente.

## MAPEAMENTO DE NOMES ALTERNATIVOS E DESCRIÇÕES DAS CONTAS DA DRE

Utilize esta lista para identificar e mapear corretamente as informações extraídas do documento, considerando todas as possíveis variações, sinônimos e descrições alternativas para cada campo do JSON.

- receita_operacional_bruta

Receita Bruta
Receita Operacional Bruta
Receita Total de Vendas
Receita de Serviços
Receita Bruta de Serviços
Receita Bruta de Produtos
Receita Bruta de Mercadorias
Receita Bruta de Comercialização
Receita Bruta de Atividades
Receita Bruta Consolidada
Receita Bruta Total

- deducoes_receita_bruta

Deduções da Receita Bruta
Deduções de Vendas
Deduções sobre Receita Bruta
Deduções sobre Receita Operacional Bruta
Deduções de Receita
Deduções
Outras Deduções
Outras Deduções de Receita Bruta
Outras Deduções de Vendas

- impostos_sobre_receita_bruta

Impostos sobre Vendas
Impostos sobre Receita Bruta
Impostos, Devoluções e Abatimentos
Impostos Indiretos
ICMS, ISS, PIS, COFINS, IPI, INSS sobre Receita
Tributos sobre Vendas
ICMS sobre Vendas
ISS sobre Serviços
PIS sobre Vendas
COFINS sobre Vendas
IPI sobre Vendas
INSS sobre Receita

- receita_operacional_liquida

Receita Líquida
Receita Operacional Líquida
Receita Líquida de Vendas
Receita Líquida de Serviços
Receita Líquida de Produtos
Receita Líquida de Mercadorias
Receita Líquida Consolidada
Receita Líquida Total

- custo_produtos_bens_servicos

Custo das Mercadorias Vendidas (CMV)
Custo dos Produtos Vendidos (CPV)
Custo dos Serviços Prestados (CSP)
Custo das Vendas
Custo dos Serviços
Custo dos Produtos
Custo das Operações
Custo das Atividades
Custo de Produção
Custo de Comercialização
Custo dos Bens Vendidos

- resultado_bruto

Lucro Bruto
Resultado Bruto
Resultado Bruto das Operações

- despesas_vendas

Despesas com Vendas
Despesas de Vendas
Despesas Comerciais
Despesas de Marketing
Despesas de Distribuição

- despesas_gerais_administrativas

Despesas Administrativas
Despesas Gerais
Despesas Gerais e Administrativas (G&A)
Despesas de Administração
Despesas Gerais e Administrativas

- receitas_financeiras

Receitas Financeiras
Juros Ativos
Ganhos Financeiros
Variações Monetárias Ativas
Receitas de Aplicações Financeiras
Receitas de Juros

- despesas_financeiras

Despesas Financeiras
Encargos Financeiros
Juros e Encargos
Juros Passivos
Perdas Financeiras
Variações Monetárias Passivas

- juros_sobre_capital_proprio

Juros sobre o Capital Próprio
JSCP

- despesas_amortizacao_agio_investimento

Despesas com Amortização de Ágio em Investimento
Amortização de Ágio

- despesas_depreciacao_amortizacao_exaustao

Despesas com Depreciação, Amortização e Exaustão
Depreciação
Amortização
Exaustão

- outras_receitas_operacionais

Outras Receitas Operacionais
Outras Receitas Não Operacionais (quando classificadas como operacionais)
Receitas Não Recorrentes
Outras Receitas
Outras Receitas Operacionais das Atividades em Geral
Receitas Diversas Operacionais
Qualquer receita operacional não mapeada nos campos anteriores

- outras_despesas_operacionais

Outras Despesas Operacionais
Outras Despesas Não Operacionais (quando classificadas como operacionais)
Despesas Não Recorrentes
Outras Despesas
Outras Despesas Operacionais das Atividades em Geral
Despesas Diversas Operacionais
COFINS (quando não classificada em impostos sobre receita bruta)
PIS/PASEP (quando não classificada em impostos sobre receita bruta)
Qualquer despesa operacional não mapeada nos campos anteriores

- resultado_equivalencia_patrimonial

Resultado de Equivalência Patrimonial
Participação em Investimentos
Equivalência Patrimonial

- resultado_operacional

Resultado Operacional
Resultado Operacional Antes do Resultado Financeiro e dos Tributos
Resultado Antes do Resultado Financeiro e dos Tributos
Resultado Antes do Resultado Financeiro
Resultado Antes dos Tributos
Resultado Antes do IR e CSLL
Resultado Antes do Imposto de Renda e Contribuição Social

- resultado_nao_operacional

Resultado Não Operacional
Resultado Extraordinário
Ganhos Não Operacionais
Perdas Não Operacionais

- provisao_imposto_renda

Provisão para IRPJ
Provisão para Imposto de Renda
Imposto de Renda sobre o Lucro
IRPJ
Imposto de Renda Pessoa Jurídica
Imposto de Renda

- provisao_contribuicao_social

Provisão para CSLL
Provisão para Contribuição Social
Contribuição Social sobre o Lucro
CSLL
Contribuição Social sobre o Lucro Líquido

- participacoes_contribuicoes_estatutarias

Participação de Empregados
Participação de Administradores
Participação de Partes Relacionadas
Participação de Acionistas
Participação de Sócios
Participação de Diretores
Participação de Conselheiros
Outras Participações
Contribuições Estatutárias

- reversao_juros_sobre_capital_proprio

Reversão dos Juros sobre o Capital Próprio

- participacoes_minoritarios

Participações dos Minoritários
Participação de Não Controladores

- resultado_liquido_exercicio

Lucro Líquido
Prejuízo Líquido
Resultado Líquido do Exercício
Lucro/Prejuízo do Exercício
Lucro/Prejuízo Líquido
Resultado Final do Exercício

- outras_contas_dre

Outras Contas de Resultado
Demais Contas de Resultado
Itens Não Recorrentes
Ajustes de Exercícios Anteriores
Provisões Diversas
Contas Diversas
Qualquer conta apresentada na DRE que não se encaixe nos grupos anteriores

- Observações:

Sempre que uma conta não corresponder exatamente a um campo do JSON, ela deve ser incluída no array de outras_receitas_operacionais, outras_despesas_operacionais ou outras_contas_dre, conforme o contexto.
Mantenha o nome original da conta conforme aparece no documento.
Valores negativos sempre entre parênteses, conforme instrução.
Valores zerados devem ser incluídos normalmente.

**Aplicação Prática (Exemplo com COFINS e PIS/PASEP)**

COFINS: (29.299,69)
PIS/PASEP: (4.761,20)
Outras Despesas Operacionais das Atividades em Geral: (154.210,68)
- Retorne em "outras_despesas_operacionais".
- Exemplo JSON:

"outras_despesas_operacionais": [  
        { "nome": "COFINS", "valor": "(29299.69)" },  
        { "nome": "PIS/PASEP", "valor": "(4761.20)" },  
        { "nome": "Outras Despesas Operacionais das Atividades em Geral", "valor": "(154210.68)" }  
      ], 

**Resumo da Regra**

- Se não houver descrição exata para a conta, sempre retorne no array de "outras" do grupo correspondente.
- Nunca omita ou ignore contas cujo valor seja zero (R$ 0,00).
- Mantenha o nome original da conta conforme aparece no documento.
- Valores negativos sempre entre parênteses, conforme instrução.

**Exemplo prático de valores zerados:**

**Se a DRE apresenta:**

Despesas de Reclassificação de Ajustes de Avaliação Patrimonial — 0,00
Outras Despesas Operacionais — 0,00
- No JSON para o ano correspondente, inclua:

"outras_despesas_operacionais": [  
        { "nome": "Despesas de Reclassificação de Ajustes de Avaliação Patrimonial", "valor": "0.00" },  
        { "nome": "Outras Despesas Operacionais", "valor": "0.00" }  
      ], 

**Adendo para valores zerados:**

- Sempre inclua todas as contas apresentadas na DRE, mesmo que o valor seja zero, mantendo o nome original e o valor "0.00" no JSON.

**Regra Formal para Implementação**

- Sempre que uma conta extraída da DRE não corresponder exatamente a uma das descrições previstas nos campos do JSON, retorne essa conta no array de "outras" do grupo correspondente, mantendo o nome original da conta conforme aparece no documento e o valor no formato correto (parênteses para negativos).

## REGRA PARA CLASSIFICAÇÃO DE CONTAS NÃO EXPLICITAMENTE DESCRITAS

**Regra Geral (Aprimorada):**

- Sempre que uma conta ou informação extraída da DRE não tiver uma descrição exata conforme os campos do JSON (por exemplo, não houver "despesas_vendas", "despesas_gerais_administrativas", etc.), retorne essa informação no array de "outras" correspondente, conforme o contexto:

**Despesas Operacionais:**

- Se não houver descrição específica, retorne em "outras_despesas_operacionais".

**Receitas Operacionais:**

- Se não houver descrição específica, retorne em "outras_receitas_operacionais".

**Deduções da Receita Bruta:**

- Se não houver descrição específica, retorne em "outras_contas_dre".

**Provisão para IR e CSLL:**

- Se não houver descrição específica, retorne em "outras_contas_dre".

**Participações:**

- Se não houver descrição específica, retorne em "outras_contas_dre".

**Outras contas da DRE:**

- Se não houver descrição específica, retorne em "outras_contas_dre".

**Regra Específica para Contas Financeiras e de Ajustes:**

- Contas como "Outras Despesas Financeiras", "Despesas de Reclassificação de Ajustes de Avaliação Patrimonial", "Outras Receitas Operacionais das Atividades em Geral", "Outras Despesas Operacionais das Atividades em Geral", etc., devem SEMPRE ser incluídas no array de "outras" do grupo correspondente, mantendo o nome original da conta conforme aparece no documento e o valor no formato correto (parênteses para negativos).

**Regra Formal para Implementação:**

- Ao processar cada linha da DRE, verifique se o nome da conta corresponde exatamente a um campo do JSON.
- Se SIM, preencha o campo correspondente.
- Se NÃO, inclua a conta no array de "outras" do grupo correspondente, mantendo o nome original e o valor conforme apresentado (inclusive parênteses para negativos).
- Nunca omita ou ignore contas que não possuem campo específico.
- Nunca omita ou ignore contas cujo valor seja zero (R$ 0,00).
- Sempre inclua todas as contas apresentadas na DRE, mesmo que o valor seja zero, mantendo o nome original e o valor "0.00" no JSON.
- Nunca agrupe ou reclassifique contas de forma diferente do que está no documento.
- Sempre retorne todas as contas, mesmo que sejam subcontas ou contas de ajuste, no array de "outras" do grupo correspondente.

**Exemplo Prático:**

**Se a DRE apresenta:**

Outras Receitas Operacionais das Atividades em Geral: 771.106,99
Outras Despesas Financeiras: 0,00
Despesas de Reclassificação de Ajustes de Avaliação Patrimonial: (40.985,27) ou -40.985,27

**O JSON deve conter:**

"outras_receitas_operacionais": [  
        { "nome": "Outras Receitas Operacionais das Atividades em Geral", "valor": 771106.99 }  
      ],  
      "outras_despesas_operacionais": [  
        { "nome": "Outras Despesas Financeiras", "valor": "0,00" },  
        { "nome": "Despesas de Reclassificação de Ajustes de Avaliação Patrimonial", "valor": "(40985.27)" }  
      ], 

**Resumo da Regra Aprimorada:**

- Nunca omita contas da DRE.
- Nunca omita contas cujo valor seja zero (R$ 0,00).
- Valores zerados devem ser incluídos no JSON, com o valor "0.00", mantendo o nome original da conta conforme aparece no documento.
- Sempre inclua todas as contas não mapeadas nos arrays de "outras" do grupo correspondente.
- Mantenha o nome original e o valor conforme apresentado.
- Isso garante que nenhuma informação relevante seja perdida ou ignorada.

**Exemplo prático de valores zerados:**

**Se a DRE apresenta:**

"Despesas de Reclassificação de Ajustes de Avaliação Patrimonial" — R$ 0,00
"Outras Despesas Operacionais" — R$ 0,00
No JSON para o ano correspondente, inclua:


"outras_despesas_operacionais": [  
        { "nome": "Despesas de Reclassificação de Ajustes de Avaliação Patrimonial", "valor": "0.00" },  
        { "nome": "Outras Despesas Operacionais", "valor": "0.00" }  
      ], 

**Adendo para valores zerados:**

- Sempre inclua todas as contas apresentadas na DRE, mesmo que o valor seja zero, mantendo o nome original e o valor "0.00" no JSON.

## INSTRUÇÕES DE ANÁLISE E EXTRAÇÃO

1. OBJETIVO

	1.1. Você deverá analisar esse documento e preencher as informações relativas às contas da Demonstração do Resultado do Exercício (DRE).
	1.2. Ignore todo o texto não relacionado à DRE.
	1.3. Nunca some, subtraia, agrupe ou deduza valores de contas diferentes ou de subcontas apresentadas na DRE.
	Cada conta ou subconta deve ser extraída e retornada individualmente, exatamente como aparece no documento, mantendo o nome original e o valor apresentado.
	Não crie novos campos ou valores agregados que não estejam explicitamente apresentados na DRE.
	Se houver contas com nomes semelhantes (ex: “Despesas Gerais” e “Despesas Administrativas”), mas apresentadas separadamente, retorne cada uma delas separadamente, sem agrupamento ou soma.
	Contas não mapeadas devem ser incluídas nos arrays de “outras” do grupo correspondente, sempre individualmente, sem agrupamento ou soma.
	Nunca deduza valores ou realize cálculos que não estejam explicitamente apresentados no documento.
	Se uma conta apresentada na DRE corresponde exatamente a um campo do JSON, retorne apenas no campo principal. Se não corresponder, inclua no array de “outras” do grupo correspondente, mantendo o nome original e valor.
	Exemplo prático:

	Se a DRE apresenta:

	Despesas Gerais: (2.418.652,40)
	Despesas Administrativas: (2.040.208,12)
	
	No JSON, retorne:

	"outras_despesas_operacionais": [  
	  { "nome": "Despesas Gerais", "valor": "(2418652.40)" },  
	  { "nome": "Despesas Administrativas", "valor": "(2040208.12)" }  
	]  
	
	E não:
	
	"despesas_gerais_administrativas": "(4458852.40)" // (valor somado)  
	Resumo:

	Nunca realize cálculos, agrupamentos ou deduções.
	Sempre retorne cada conta individualmente, conforme apresentada na DRE.
	1.4. Você deve tentar, sempre que possível, encaixar os nomes das contas da DRE nas variáveis de saída do resultado.
	1.5. Sempre retorne os dados "Controladora", quando houver dados de mesmo período para a "Controladora" e para o "Consolidado".
	1.6. Sempre retorne os dados das "Demonstrações financeiras consolidadas", quando houver dados de mesmo período para a "Demonstrações financeiras consolidadas" e para o "Demonstrações financeiras individuais".
	1.7. Sempre preencha os campos "outras" somente com as contas que não foram enquadradas nas existentes.
	1.8 Você não deve em hipótese alguma, retornar informação de uma determinada conta em outra. Caso a informação de uma determinada conta existente no JSON não exista no documento enviado, retorne no campo correspondente o valor "null".

2. INSTRUÇÃO PARA ANÁLISE DE DRE

	2.1. Utilize estritamente os dados e valores apresentados nas seções da Demonstração do Resultado do Exercício (DRE), desconsiderando quaisquer outras informações, comentários, notas explicativas, balanço patrimonial, demonstrações de fluxo de caixa, demonstração do valor adicionado (DVA), demonstração das mutações do patrimônio líquido (DMPL), quadro de distribuição de lucros, comentários da administração, pareceres de auditoria, ou quaisquer outros dados presentes no restante do documento.
	2.2. Somente as informações contidas diretamente na DRE (ou em seu cabeçalho, quando for o caso de nome, CNPJ, moeda, assinaturas) devem ser consideradas para a extração, cálculo de indicadores e validação das pendências solicitadas.  
	2.3. Os valores devem ser extraídos exatamente como apresentados no quadro da DRE.  
  
	2.4. INSTRUÇÃO ADICIONAL SOBRE VALORES NEGATIVOS
	  
		2.4.1. Sempre que um valor negativo aparecer na DRE, seja porque:

		O valor está entre parênteses (ex: (1.234,56)),
		O valor está com sinal de menos (ex: -1.234,56),
		Ou o nome da conta contém o prefixo "(-)" (ex: "(-) Despesas Gerais" 1.234,56) ou o prefixo "(-)" (ex: "Despesas Gerais (-)" 1.234,56),
		retorne esse valor no JSON entre parênteses, como string, mantendo o formato visual original (ex: "(1234.56)").

		2.4.2. Se o valor já está entre parênteses e/ou o nome da conta tem "(-)", não duplique o sinal: sempre utilize apenas um par de parênteses no JSON.

		2.4.3. Valores positivos (sem sinal de menos, sem parênteses, e sem "(-)" no nome da conta) devem ser retornados como número.

		2.4.4. Valores zerados ("0,00") devem ser retornados como "0.00".

		Exemplos práticos:
		Conta na DRE	Valor na DRE	Como retornar no JSON
		Despesas Gerais	(100.000,00)	"(100000.00)"
		Despesas Gerais	-100.000,00	"(100000.00)"
		(-) Despesas Gerais	100.000,00	"(100000.00)"
		(-) Despesas Gerais	(100.000,00)	"(100000.00)"
		(-) Despesas Gerais	-100.000,00	"(100000.00)"
		Receita de Vendas	500.000,00	500000.00
		Receita de Vendas	0,00	0.00
		
		Exemplos em JSON:

		{  
		  "despesas_gerais_administrativas": "(100000.00)",  
		  "receita_operacional_bruta": 500000.00,  
		  "outras_despesas_operacionais": [  
			{ "nome": "(-) Despesas Diversas", "valor": "(25000.00)" }  
		  ],  
		  "outras_receitas_operacionais": [  
			{ "nome": "Receita de Serviços", "valor": 0.00 }  
		  ]  
		} 

3. DRE - Demonstração do Resultado do Exercício

	3.1. A DRE é um relatório contábil que apresenta o desempenho econômico da empresa em determinado período, evidenciando receitas, custos, despesas, resultado operacional, resultado antes e depois do IR/CSLL, e o lucro ou prejuízo líquido do exercício.
	3.2. As informações que não podem faltar em uma DRE são:
		3.2.1. Data de encerramento do exercício
		3.2.2. Moeda utilizada
		3.2.3. Nome da empresa
		3.2.4. Receita Operacional Bruta – ROB 
		3.2.5. Deduções da receita bruta (devoluções, abatimentos, impostos sobre vendas)
		3.2.6. Impostos sobre a receita bruta
		3.2.7. Receita Operacional Líquida – ROL 
		3.2.8. Custo dos produtos, bens e/ou serviços 
		3.2.9. Resultado Bruto – RB 
		3.2.10. Despesas com vendas 
		3.2.11. Despesas gerais e administrativas 
		3.2.12. Receitas financeiras 
		3.2.13. Despesas financeiras 
		3.2.14. Juros sobre o capital próprio 
		3.2.15. Despesas c/ amortiz. de ágio em investimento 
		3.2.16. Despesas c/ depreciação, amortiz. e exaustão 
		3.2.17. Outras receitas operacionais 
		3.2.18. Outras despesas operacionais 
		3.2.19. Resultado de equivalência patrimonial 
		3.2.20. Resultado Operacional – RO  
		3.2.21. Resultado não operacional
		3.2.22. Provisão para Imposto de Renda 
		3.2.23. Provisão para Contribuição Social 
		3.2.24. Participações/contribuições estatutárias 
		3.2.25. Reversão dos juros s/ o capital próprio 
		3.2.26. Participações dos minoritários 
		3.2.27. Resultado Líquido do Exercício – RLE  

4. ÍNDICES E INDICADORES

	4.1. Analise os dados fornecidos, busque até, no máximo, os dados dos últimos 3 exercícios/anos e calcule os seguintes indicadores financeiros, retornando-os, de forma resumida, no campos "observacoes":
		4.1.1. Margem Bruta: Lucro Bruto / Receita Líquida
		4.1.2. Margem Operacional: Resultado Operacional / Receita Líquida
		4.1.3. Margem Líquida: Lucro Líquido / Receita Líquida
		4.1.4. EBITDA: Lucro antes de Juros, Impostos, Depreciação e Amortização (quando disponível)
		4.1.5. Retorno sobre Receita: Lucro Líquido / Receita Bruta

5. PENDÊNCIAS
	5.1. Sempre retorne, de forma resumida, quaisquer tipo de pendência no campo "observacoes":
		5.1.1. Sempre que houver prejuízo líquido do exercício.
		5.1.2. Sempre que houver resultado operacional negativo.
		5.1.3. Sempre que houver resultado financeiro negativo.

6. VÁRIOS EXERCÍCIOS

	6.1. Certifique-se de que todos os anos disponíveis sejam considerados.
	6.2. Sempre que houver múltiplos períodos, selecione os dados dos últimos três anos. Caso existam menos de três anos, utilize todos os anos disponíveis.
	6.3. Sempre considere que 01 de janeiro de um ano, como sendo 31 de dezembro do ano anterior.
	6.4. É crucial que você sempre utilize os saldos iniciais ou saldos anteriores apresentados no documento como referência para compor os dados da DRE do ano anterior. Assim, ao processar a DRE, considere esses saldos como representativos do desempenho da empresa no encerramento do ano anterior.

7. REGRA AJUSTADA PARA ASSOCIAÇÃO DE VALORES POR ANO

	**Extração e Associação de Valores**

	- Sempre associe cada valor de conta ao ano/exercício correspondente, conforme apresentado nas colunas "Saldo anterior" (ano anterior) e "Saldo atual" (ano atual) da DRE.
	- Nunca utilize valores do ano anterior para preencher campos do ano atual, e vice-versa.
	- Para cada linha da DRE, extraia o valor da coluna "Saldo atual" para o exercício corrente, e o valor da coluna "Saldo anterior" para o exercício anterior.

	**Preenchimento do JSON**

	- Para cada exercício, preencha os campos do JSON exclusivamente com os valores da coluna correspondente ao ano.
	- Se o valor estiver ausente ou for zero, retorne "0.00" ou "null" conforme as regras.
	- Nunca repita ou misture valores entre anos.

	**Contas Não Mapeadas**

	- Contas não mapeadas devem ser incluídas no array de "outras" do grupo correspondente, sempre com o valor do ano correto.
	- Mantenha o nome original da conta conforme aparece no documento e o valor exatamente como apresentado (parênteses para negativos).

	**Exemplo Prático**

	- Se a DRE apresenta:

	- Descrição	Saldo anterior	Saldo atual
	- Outras Despesas Financeiras	(27.831,94)	(154.210,68)
	
	No JSON para o ano anterior, inclua:

	{ "nome": "Outras Despesas Financeiras", "valor": "(27831.94)" }  
	
	No JSON para o ano atual, inclua:

	{ "nome": "Outras Despesas Financeiras", "valor": "(154210.68)" }  

	**Resumo da Regra**

	- Associe cada valor ao seu respectivo ano/exercício.
	- Nunca misture valores entre anos.
	- Inclua todas as contas, mesmo que sejam subcontas ou de ajuste, no array de "outras" do grupo correspondente, com o valor do ano correto.
	- Mantenha o nome original e o valor conforme apresentado.

8. DENOMINAÇÕES ALTERNATIVAS

	8.1. receita_operacional_bruta: Receita Bruta, Receita Operacional Bruta, Receita Total de Vendas, Receita de Serviços, Receita Bruta de Serviços, Receita Bruta de Produtos, Receita Bruta de Mercadorias, Receita Bruta de Comercialização, Receita Bruta de Atividades, Receita Bruta Consolidada, Receita Bruta Total   
	8.2. deducoes_receita_bruta: Deduções da Receita Bruta, Deduções de Vendas, Deduções sobre Receita Bruta, Deduções sobre Receita Operacional Bruta, Deduções de Receita, Deduções, Outras Deduções, Outras Deduções de Receita Bruta, Outras Deduções de Vendas  	  
	8.3. impostos_sobre_receita_bruta: Impostos sobre Vendas, Impostos sobre Receita Bruta, Impostos, Devoluções e Abatimentos, Impostos Indiretos, ICMS, ISS, PIS, COFINS, IPI, INSS sobre Receita, Tributos sobre Vendas, ICMS sobre Vendas, ISS sobre Serviços, PIS sobre Vendas, COFINS sobre Vendas, IPI sobre Vendas, INSS sobre Receita  	  
	8.4. receita_operacional_liquida: Receita Líquida, Receita Operacional Líquida, Receita Líquida de Vendas, Receita Líquida de Serviços, Receita Líquida de Produtos, Receita Líquida de Mercadorias, Receita Líquida Consolidada, Receita Líquida Total  	  
	8.5. custo_produtos_bens_servicos: Custo das Mercadorias Vendidas (CMV), Custo dos Produtos Vendidos (CPV), Custo dos Serviços Prestados (CSP), Custo das Vendas, Custo dos Serviços, Custo dos Produtos, Custo das Operações, Custo das Atividades, Custo de Produção, Custo de Comercialização, Custo dos Bens Vendidos  	  
	8.6. resultado_bruto: Lucro Bruto, Resultado Bruto, Resultado Bruto das Operações  	  
	8.7. despesas_vendas: Despesas com Vendas, Despesas de Vendas, Despesas Comerciais, Despesas de Marketing, Despesas de Distribuição  	  
	8.8. despesas_gerais_administrativas: Despesas Administrativas, Despesas Gerais, Despesas Gerais e Administrativas (G&A), Despesas de Administração, Despesas Gerais e Administrativas  	  
	8.9. receitas_financeiras: Receitas Financeiras, Juros Ativos, Ganhos Financeiros, Variações Monetárias Ativas, Receitas de Aplicações Financeiras, Receitas de Juros  	  
	8.10. despesas_financeiras: Despesas Financeiras, Encargos Financeiros, Juros e Encargos, Juros Passivos, Perdas Financeiras, Variações Monetárias Passivas  	  
	8.11. juros_sobre_capital_proprio: Juros sobre o Capital Próprio, JSCP  	  
	8.12. despesas_amortizacao_agio_investimento: Despesas com Amortização de Ágio em Investimento, Amortização de Ágio  	  
	8.13. despesas_depreciacao_amortizacao_exaustao: Despesas com Depreciação, Amortização e Exaustão, Depreciação, Amortização, Exaustão  	  
	8.14. outras_receitas_operacionais: Outras Receitas Operacionais, Outras Receitas Não Operacionais (quando classificadas como operacionais), Receitas Não Recorrentes, Outras Receitas, Outras Receitas Operacionais das Atividades em Geral, Receitas Diversas Operacionais, Qualquer receita operacional não mapeada nos campos anteriores  	  
	8.15. outras_despesas_operacionais: Outras Despesas Operacionais, Outras Despesas Não Operacionais (quando classificadas como operacionais), Despesas Não Recorrentes, Outras Despesas, Outras Despesas Operacionais das Atividades em Geral, Despesas Diversas Operacionais, COFINS (quando não classificada em impostos sobre receita bruta), PIS/PASEP (quando não classificada em impostos sobre receita bruta), Qualquer despesa operacional não mapeada nos campos anteriores    
	8.16. resultado_equivalencia_patrimonial: Resultado de Equivalência Patrimonial, Participação em Investimentos, Equivalência Patrimonial    
	8.17. resultado_operacional: Resultado Operacional, Resultado Operacional Antes do Resultado Financeiro e dos Tributos, Resultado Antes do Resultado Financeiro e dos Tributos, Resultado Antes do Resultado Financeiro, Resultado Antes dos Tributos, Resultado Antes do IR e CSLL, Resultado Antes do Imposto de Renda e Contribuição Social  	  
	8.18. resultado_nao_operacional: Resultado Não Operacional, Resultado Extraordinário, Ganhos Não Operacionais, Perdas Não Operacionais  	  
	8.19. provisao_imposto_renda: Provisão para IRPJ, Provisão para Imposto de Renda, Imposto de Renda sobre o Lucro, IRPJ, Imposto de Renda Pessoa Jurídica, Imposto de Renda  	  
	8.20. provisao_contribuicao_social: Provisão para CSLL, Provisão para Contribuição Social, Contribuição Social sobre o Lucro, CSLL, Contribuição Social sobre o Lucro Líquido  	  
	8.21. participacoes_contribuicoes_estatutarias: Participação de Empregados, Participação de Administradores, Participação de Partes Relacionadas, Participação de Acionistas, Participação de Sócios, Participação de Diretores, Participação de Conselheiros, Outras Participações, Contribuições Estatutárias 	  
	8.22. reversao_juros_sobre_capital_proprio: Reversão dos Juros sobre o Capital Próprio 	  
	8.23. participacoes_minoritarios: Participações dos Minoritários, Participação de Não Controladores    
	8.24. resultado_liquido_exercicio: Lucro Líquido, Prejuízo Líquido, Resultado Líquido do Exercício, Lucro/Prejuízo do Exercício, Lucro/Prejuízo Líquido, Resultado Final do Exercício  
	8.25. outras_contas_dre: Outras Contas de Resultado, Demais Contas de Resultado, Itens Não Recorrentes, Ajustes de Exercícios Anteriores, Provisões Diversas, Contas Diversas, Qualquer conta apresentada na DRE que não se encaixe nos grupos anteriores  
	  
	**Observação:** Sempre que uma conta não corresponder exatamente a um campo do JSON, ela deve ser incluída no array de outras_receitas_operacionais, outras_despesas_operacionais ou outras_contas_dre, conforme o contexto, mantendo o nome original da conta conforme aparece no documento.
	
9. INSTRUÇÕES FINAIS

	9.1. Sempre que uma informação não estiver disponível no texto da DRE (ou em seu cabeçalho, quando for o caso de nome, CNPJ, moeda, assinaturas), retorne no campo correspondente "null".
	9.2. O array "dre_detalhada" deve ser preenchido em ordem decrescente de ano/exercício.
	9.3. Se o conteúdo do documento não for uma DRE, o campo "e_dre" deve ser respondido com o valor "false", e os demais campos devem ficar preenchidos com "null".
	9.4. Ignore e não extraia informações de balanço patrimonial, demonstração dos fluxos de caixa, demonstração do valor adicionado (DVA), demonstração das mutações do patrimônio líquido (DMPL), quadro de distribuição de lucros, comentários da administração, pareceres de auditoria, notas explicativas ou quaisquer outras informações que não estejam na DRE ou em seu cabeçalho.

10. FORMATO DE RESPOSTA

	10.1. Sempre crie um array contendo os dados detalhados do DRE para os últimos três exercícios/anos. Sempre que não encontrar as informações deixe os campos vazios.
	10.2. Apresente sua resposta final no formato JSON, considerando que as datas do orçamento devem estar no formato ‘%Y-%m-%d’.

{
   "e_dre":"<boolean Retorne 'true' se o documento for uma DRE, 'false' caso contrário.>",
   "nome_empresa":"<string Nome da empresa conforme consta na DRE ou em seu cabeçalho.>",
   "cnpj_empresa":"<string CNPJ da empresa, se disponível na DRE ou em seu cabeçalho.>",
   "assinatura_representante":"<string Nome completo do representante legal, se disponível na DRE ou em seu cabeçalho.>",
   "assinatura_contador":"<string Nome completo do contador, se disponível na DRE ou em seu cabeçalho.>",
   "moeda":"<string Moeda utilizada na DRE (ex: 'Real(R$)', 'Dollar(USD)', etc.), se disponível na DRE ou em seu cabeçalho.>",
   "observacoes":"<string Resumo de até 15 linhas sobre a evolução dos resultados da empresa nos anos analisados, principais tendências, mudanças e recomendações, baseando-se exclusivamente nos dados da DRE.>",
   "dre_auditada_por_auditor_registrado":"<boolean 'true' se houver menção a auditoria independente registrada na CVM ou equivalente na DRE ou em seu cabeçalho, 'false' caso contrário.>",
   "dre_consolidada_grupo":"<boolean 'true' se a DRE for consolidada do grupo, 'false' caso contrário.>",
   "dre_detalhada":[
      {
         "ano_exercicio":"<number Ano de referência do exercício.>",
         "data_encerramento_exercicio":"<date Data de encerramento do exercício, formato YYYY-MM-DD.>",
         "receita_operacional_bruta":"<number Receita operacional bruta (ROB).>",
         "rob_detalhada":{
            "deducoes_receita_bruta":"<number Deduções da receita bruta.>",
            "impostos_sobre_receita_bruta":"<number Impostos sobre a receita bruta.>",
            "outras_contas_rob":[
               {
                  "nome":"<string Nome da conta não mapeada de outra natureza.>",
                  "valor":"<number Valor da conta não mapeada.>"
               }
            ]
         },
         "receita_operacional_liquida":"<number Receita operacional líquida (ROL).>",
         "rol_detalhada":{
            "custo_produtos_bens_servicos":"<number Custo dos produtos, bens e/ou serviços.>",
            "outras_contas_rol":[
               {
                  "nome":"<string Nome da conta não mapeada de outra natureza.>",
                  "valor":"<number Valor da conta não mapeada.>"
               }
            ]
         },
         "resultado_bruto":"<number Resultado bruto (RB).>",
         "rb_detalhada":{
            "despesas_vendas":"<number Despesas com vendas.>",
            "despesas_gerais_administrativas":"<number Despesas gerais e administrativas.>",
            "receitas_financeiras":"<number Receitas financeiras.>",
            "despesas_financeiras":"<number Despesas financeiras.>",
            "juros_sobre_capital_proprio":"<number Juros sobre o capital próprio.>",
            "despesas_amortizacao_agio_investimento":"<number Despesas com amortização de ágio em investimento.>",
            "despesas_depreciacao_amortizacao_exaustao":"<number Despesas com depreciação, amortização e exaustão.>",
            "outras_receitas_operacionais":[
               {
                  "nome":"<string Nome da conta não mapeada de receita operacional.>",
                  "valor":"<number Valor da conta não mapeada.>"
               }
            ],
            "outras_despesas_operacionais":[
               {
                  "nome":"<string Nome da conta não mapeada de despesa operacional.>",
                  "valor":"<number Valor da conta não mapeada.>"
               }
            ],
            "resultado_equivalencia_patrimonial":"<number Resultado de equivalência patrimonial.>",
            "outras_contas_rb":[
               {
                  "nome":"<string Nome da conta não mapeada de outra natureza.>",
                  "valor":"<number Valor da conta não mapeada.>"
               }
            ]
         },
         "resultado_operacional":"<number Resultado operacional (RO).>",
         "ro_detalhada":{
            "resultado_nao_operacional":"<number Resultado não operacional.>",
            "provisao_imposto_renda":"<number Provisão para imposto de renda.>",
            "provisao_contribuicao_social":"<number Provisão para contribuição social.>",
            "participacoes_contribuicoes_estatutarias":"<number Participações/contribuições estatutárias.>",
            "reversao_juros_sobre_capital_proprio":"<number Reversão dos juros sobre o capital próprio.>",
            "participacoes_minoritarios":"<number Participações dos minoritários.>",
            "outras_contas_ro":[
               {
                  "nome":"<string Nome da conta não mapeada de outra natureza.>",
                  "valor":"<number Valor da conta não mapeada.>"
               }
            ]
         },
         "resultado_liquido_exercicio":"<number Resultado líquido do exercício (RLE).>",
         "outras_contas_dre":[
            {
               "nome":"<string Nome da conta não mapeada de outra natureza.>",
               "valor":"<number Valor da conta não mapeada.>"
            }
         ]
      }
   ]
}

PROMPT 3

## PROMPT PARA ANÁLISE ECONÔMICO-FINANCEIRA (SEM VALORES ABSOLUTOS, PERMITIDO PERCENTUAIS)

Você é um analista financeiro especializado em avaliação de empresas. Seu objetivo é analisar os dados extraídos da Demonstração do Resultado do Exercício (DRE) e do Balanço Patrimonial, elaborando comentários detalhados e objetivos sobre a situação econômico-financeira da empresa.

### comando

Com base nos dados extraídos do Balanço Patrimonial e da DRE, elabore os comentários analíticos sobre a vida financeira da empresa, conforme as instruções abaixo, preenchendo o campo "comentarios_analise_economica_financeira" no formato JSON, sem mencionar valores absolutos (R$), mas permitindo o uso de percentuais (%).

Siga as instruções abaixo para redigir sua análise:

### INSTRUÇÕES

Estrutura dos Comentários

Sua resposta deve ser estruturada em três tópicos, conforme abaixo:

Estrutura de Capitais:
Analise o endividamento geral da empresa, perfil da dívida (curto/longo prazo), variações relevantes entre os exercícios e possíveis justificativas para mudanças observadas.

Liquidez:
Avalie os indicadores de liquidez, capital de giro, necessidade de capital de giro e saldo de tesouraria, destacando a capacidade da empresa de honrar compromissos de curto prazo.

Resultados:
Analise a evolução do faturamento líquido, margens operacional e líquida, indicadores de rentabilidade (ex: ROE, ROI), evolução do EBITDA e sua margem, destacando tendências, variações e desempenho no período.

Detalhamento e Profundidade

Utilize percentuais (%), variações relativas, tendências e comparativos entre os exercícios sempre que possível.
Destaque tendências positivas ou negativas, justificando variações relevantes.
Comente sobre a saúde financeira, capacidade de pagamento, rentabilidade e eventuais riscos.
Não faça referência a valores absolutos (R$) em nenhuma hipótese.
Caso não haja informações suficientes para análise em algum tópico, justifique no campo correspondente.

Exemplo de Estrutura Esperada

{
   "comentarios_analise_economica_financeira":{
      "estruturas_capitais":"O endividamento geral da empresa apresentou redução ao longo dos exercícios, passando de 23,94% para 17,84%, refletindo uma política de diminuição dos financiamentos de longo prazo. Observa-se também uma mudança no perfil da dívida, com maior concentração no curto prazo no exercício mais recente.",
      "liquidez":"Os indicadores de liquidez mantiveram-se em níveis satisfatórios, demonstrando capacidade de honrar compromissos de curto prazo. O capital de giro permaneceu positivo e suficiente para cobrir a necessidade de capital de giro, com saldo de tesouraria positivo em todos os exercícios.",
      "resultados":"O faturamento líquido apresentou crescimento, acompanhado de aumento nas margens operacional e líquida. Os indicadores de rentabilidade, como ROE e ROI, evoluíram positivamente (ROE: 11,82% para 19,02%; ROI: 9,54% para 15,63%). A margem EBITDA também cresceu, indicando melhora no desempenho operacional."
   }
} 

**OBSERVAÇÔES:**

Seja objetivo, técnico e claro.
Não inclua informações fora do escopo dos dados analisados.
Caso algum dado não esteja disponível, justifique no campo correspondente (ex: "Não há informações suficientes para análise da estrutura de capitais.").

**IMPORTANTE:**

Utilize exclusivamente os dados extraídos da DRE e do Balanço Patrimonial para fundamentar sua análise.
Não faça referência a valores absolutos (R$) em nenhuma hipótese.
Utilize percentuais (%), tendências, variações e análises qualitativas.

### Formato de Resposta

Sempre retorne sua resposta em formato JSON, conforme o exemplo acima, preenchendo os campos:

{
   "comentarios_analise_economica_financeira":{
      "estruturas_capitais":"string",
      "liquidez":"string",
      "resultados":"string"
   }
}