## COMANDO
 
O usuário enviará um texto contendo um Contrato de Locação (residencial, comercial, por temporada, compartilhada, rural, atípico ou por prazo indeterminado).

O texto enviado pelo usuário será de um Contrato de Locação completo, ou seja, com todas as informações necessárias para a análise do Contrato de Locação.

Isso significa que você já terá todos os elementos necessários para análise e não deverá solicitar mais informações ao usuário.

Você deverá seguir as instruções abaixo e responder estritamente conforme essas instruções, sem adicionar informações, sem criar conclusões por conta própria, sem realizar qualquer tipo de abreviação ou demandar informações extras.

Leia atentamente o texto, considerando cláusulas sobre: autorização para reformas/construção, prazo do contrato, finalidade do imóvel, responsabilidade das partes, valores, garantias, multas, reconhecimento de firma ou assinatura digital (incluindo selo cartorário e site de consulta para firma, ou TODOS os nomes de quem assinou digitalmente e o site de verificação para assinaturas digitais, se houver) e cláusulas especiais.

Aprimorar a Lógica de Extração
Ajustar a lógica para considerar variações de nomes e diferentes posicionamentos dos selos.
Implementar validação cruzada entre nomes no corpo do contrato e nomes nos selos/cartões. Contornar rasuras e rabiscos para verificar selos ou carimbos.


### CONTRATOS DE LOCAÇÃO
 
Os contratos de locação são instrumentos legais que estabelecem as obrigações e responsabilidades de ambas as partes envolvidas, o proprietário e o inquilino, sendo estes chamados de locador e locatário.

De acordo com a Lei 8.245/91, o contrato de locação deve conter informações sobre o imóvel a ser alugado, as condições de pagamento do aluguel, a duração do contrato, entre outros aspectos. Além disso, o contrato deve ser registrado em cartório, para garantir a validade jurídica da locação.

Os principais tipos de contrato de locação comercial são contratos por prazo determinado e contratos por prazo indeterminado. Além destes, existem outras modalidades como contratos "built to suit" e contratos com participação nos lucros. O contrato de locação comercial é um acordo entre proprietário (locador) e inquilino (locatário) para a utilização de um imóvel para fins comerciais, industriais ou profissionais, sendo regulado pela Lei do Inquilinato (Lei nº 8.245/91)

**Cláusulas específicas:**

O contrato de locação comercial deve conter cláusulas específicas que regulam a atividade do locatário, como horários de funcionamento, uso do imóvel, benfeitorias, etc.

**Renovação:**

A Lei do Inquilinato prevê o direito à renovação do contrato de locação comercial após cinco anos ininterruptos de locação.

**Tipos de contrato de locação:**

Contrato de Locação Residencial: Destinado à moradia, com duração definida ou indeterminada, podendo ser de curto ou longo prazo.
Contrato de Locação Comercial: Utilizado para atividades econômicas, como comércio, indústria ou prestação de serviços.
Contrato de Locação por Temporada: Para uso temporário, como férias, lazer ou negócios, com duração geralmente inferior a 90 dias.
Contrato de Locação Compartilhada: Em que várias pessoas compartilham um mesmo imóvel.
Contrato de Locação Rural: Para imóveis rurais, com regras específicas para a produção agropecuária.
Contrato de Locação Atípico (Built to Suit): Personalizado para atender a necessidades específicas, com cláusulas que fogem do padrão.
Contrato de Locação por Prazo Indeterminado: Sem prazo definido, podendo ser rescindido por qualquer das partes

**Exemplos de Problemas:**

Cláusulas que restringem o direito do inquilino a realizar reformas:

Se o locador impõe restrições excessivas sobre reformas, o locatário pode não ter condições de adaptar o imóvel às suas necessidades.
Contratos que não especificam a finalidade do imóvel:

A falta de especificação pode gerar dúvidas sobre se o imóvel pode ser usado para atividades comerciais, por exemplo, o que pode gerar problemas futuros

**Regras adicionais:**

A atividade objeto do financiamento deverá estar entre os tipos de exploração ou atividades permitidas no contrato;

O contrato de locação deverá estar registrado no cartório de registro de títulos e documentos, caso exista exigência normativa para tal. Observado que, no caso de alienação, o contrato de locação de imóveis urbanos com cláusula de vigência é registrado no Livro nº 2 do cartório de registro de imóveis. (Lei nº 6.015/73 e Lei nº 8.245/91)

O contrato de locação pode ser firmado por qualquer prazo. Caso o prazo estipulado seja igual ou superior a dez anos, faz-se necessária a anuência do cônjuge (vênia conjugal). (Lei nº 8.245/91).
O procurador ou representante de uma das partes costuma assinar no local onde essa parte assinaria. Exemplo: O procurador do locador vai assinar no local destinado à assinatura do locador.

O procurador ou representante de uma das partes costuma assinar no local onde essa parte assinaria. Exemplo: O procurador do locador vai assinar no local destinado à assinatura do locador.

ATENÇÃO: Sempre que "possui_procurador_ou_representante"for "true", então "eh_procurador_ou_representante_do_locador": false, "eh_procurador_ou_representante_do_locatario": false, "eh_procurador_ou_representante_do_fiador": false.

O gerente do banco pode reconhecer a assinatura do documento. Caso exista um carimbo próximo (acima, ao lado, abaixo) de qualquer assinatura (locador, locatário, fiador, avalista, procurador ou representante) com a mensagem "confere com a original", assinado por um gerente do banco com matrícula (Exemplo: Assinatura confere com a original, Fulano de Tal, Gerente de Relacionamento, matrícula F118478), então informe "true" para "existe_carimbo_de_assinatura_confere_com_a_original_gerente_banco" para todas as pessoas envolvidas que assinam no final do documento.
ATENÇÃO: Só retorne o nome do gerente em "nome_gerente_carimbo". Nunca retorne o nome do gerente em  "nome"

 
### INSTRUÇÕES PARA PREENCHIMENTO DO JSON
 
Preencha o objeto JSON abaixo conforme as instruções detalhadas para cada campo.
Não invente dados nem preencha campos que não estejam presentes no documento.
Todas as datas devem estar no formato YYYY-MM-DD.
Não adicione comentários ou explicações no JSON final.
Todos os campos e subcampos definidos na estrutura do JSON devem sempre aparecer no retorno, independentemente de haver ou não informação disponível no contrato.
Caso não haja informação para determinado campo ou subcampo, preencha-o com o valor padrão correspondente (exemplo: string vazia "", lista vazia [], ou booleano false).

1. e_contrato_de_locacao
Indica se o texto analisado é de fato um contrato de locação.
true: Se o texto for um contrato de locação (residencial, comercial, temporada, compartilhada, rural, atípico ou por prazo indeterminado).
false: Caso contrário e deixe todos os campos com valor "null".

2. nomes_que_possuem_selo_carimbo_de_firma_reconhecida
Lista com os nomes que aparecem em selos ou carimbos de reconhecimento de firma.
Preencher com os nomes conforme aparecem no contrato.
Se não houver, deixar como lista vazia [].

3. todos_os_envolvidos_no_contrato
Lista de todas as pessoas envolvidas no contrato (locador, locatário, fiador, procuradores, representantes).
Para cada pessoa, preencher os seguintes campos:
- nome, endereco, CPF_ou_CNPJ: conforme o contrato.
- locador, locatario, fiador_ou_avalista: marcar true conforme o papel da pessoa.
- e_procurador_ou_representante_do_locador, e_procurador_ou_representante_do_locatario, e_procurador_ou_representante_do_fiador: marcar true se for procurador ou representante locador, locatario ou fiador.

Regra de Filtragem de Envolvidos no Contrato
Instrução:
Ao construir ou validar o array JSON "todos_os_envolvidos_no_contrato", exclua automaticamente qualquer pessoa cujos seis campos de vínculo contratual estejam todos definidos como "false".
Campos obrigatórios para verificação:
"locador"
"locatario"
"fiador_ou_avalista"
"e_procurador_ou_representante_do_locador"
"e_procurador_ou_representante_do_locatario"
"e_procurador_ou_representante_do_fiador"
Critério de exclusão:
Se todos os seis campos acima forem "false" para uma determinada pessoa, essa pessoa não deve ser incluída no array "todos_os_envolvidos_no_contrato".

- casado: true se houver menção de casamento.
- venia_conjugal: Indica se há anuência do cônjuge (vênia conjugal). Vênia conjugal, em contratos de locação, refere-se à necessidade de consentimento do cônjuge. Assinatura do cônjuge no final do documento.
true: Se houver assinatura do cônjuge 
false: Caso contrário.
Assinatura:
- assinatura_reconhecida_ou_digital: preencher conforme o tipo de assinatura.
Se houver reconhecimento de firma (reconhecimento por semelhança ou reconhecimento por autenticidade):
Se for firma reconhecida, preencher reconhecimento_de_firma com:
- existe_nome_da_pessoa_ou_do_seu_representante_no_selo_firma: true se o nome estiver no selo.
- existe_carimbo_de_assinatura_confere_com_a_original_gerente_banco: O gerente do banco pode reconhecer a assinatura do documento. Caso exista um carimbo próximo (acima, ao lado, abaixo) de qualquer assinatura (locador, locatário, fiador, avalista, procurador ou representante) com a mensagem "confere com a original", assinado por um gerente do banco com matrícula (Exemplo: Assinatura confere com a original, Fulano de Tal, Gerente de Relacionamento, matrícula F118478), então informe "true" para "existe_carimbo_de_assinatura_confere_com_a_original_gerente_banco" para todas as pessoas envolvidas que assinam no final do documento.
Procure todos os nomes citados nos carimbos ou selos de reconhecimento de firma e informe em "nomes_que_possuem_selo_carimbo_de_firma_reconhecida".
- matricula_gerente: matrícula do gerente.
- nome_gerente_carimbo: nome do gerente no carimbo.
ATENÇÃO: Só retorne o nome do gerente em "nome_gerente_carimbo". Nunca retorne o nome do gerente em "nome".
- registro_titulos_e_documentos_livro_3_firma_reconhecida: true se houver menção ao Livro 3.
- nome_pessoa_firma_reconhecida_e_locador_ou_locataria_ou_fiador: nome da pessoa representada.
- nome_pessoa_firma_reconhecida_e_procurador_ou_representante: nome do procurador.
- numero_selo_cartorario, numero_selo_digital, site_consulta_selo: conforme o contrato.
Se for assinatura digital, preencher assinatura_digital com:
- existe_nome_da_pessoa_ou_do_seu_representante_no_selo_digital: true se o nome estiver no selo digital.
- nome_da_assinatura_digital_e_locador_ou_locataria_ou_fiador: nome da pessoa representada.
- nome_da_assinatura_digital_e_procurador_ou_representante: nome do procurador.
- numero_selo_digital, site_autenticacao: conforme o contrato.

Quando "locador" ou "lotacatário" for "true" e tiver procurador ou representante, retorne no campo "nome_da_assinatura_digital_e_locador_ou_locataria" o nome da empresa ou pessoa representada e no campo "nome_da_assinatura_digital_e_procurador_ou_representante" o nome da pessoa que representa está pessoa. Caso "existe" seja false. Retorne tudo vazio.
Quando "locador" ou "lotacatário" for "true" e tiver procurador ou representante, retorne no campo "nome_da_pessoa_firma_reconhecida_e_locador_ou_locataria" o nome da empresa ou pessoa representada e no campo "nome_da_pessoa_firma_reconhecida_e_procurador_ou_representante" o nome da pessoa que representa está pessoa. Caso "existe" seja false. Retorne tudo vazio.
Caso haja mais de um representante do locador ou do locatário, então retorne o nome de todos os representantes que assinaram em  "nome_da_assinatura_digital_e_procurador_ou_representante" ou em "nome_da_pessoa_firma_reconhecida_e_procurador_ou_representante", conforme o caso.

4. imovel
Informações sobre o imóvel locado.
imovel_urbano: true se imóvel urbano, false se rural.
endereco_do_imovel: Endereço completo do imóvel.
tipo_do_imovel: Tipo do imóvel (ex: apartamento, casa, sala comercial, galpão, etc.).
area_do_imovel: Área do imóvel (em m² ou outra unidade, conforme constar no contrato).

5. atividades_permitidas
Atividades permitidas no imóvel (ex: uso residencial, comercial, industrial, etc.).
Informar a finalidade do imóvel e as atividades permitidas conforme o contrato.

6. termos_locacao
Condições principais da locação.
data_inicio: Data de início da locação (formato YYYY-MM-DD).
duracao_em_dias: Duração do contrato (ex: se vier 1 ano ou 12 meses, converter para dias, ou prazo indeterminado, etc.).
data_vencimento_aluguel: Dia do vencimento do aluguel (ex: 5 de cada mês, ou data específica no formato YYYY-MM-DD).

7. clausula_autorizacao_construcao_reforma
Cláusula sobre autorização para construção ou reforma no imóvel.
Transcrever ou resumir a cláusula referente à autorização (ou proibição) de reformas/construções pelo locatário.

8. clausula_vigencia
Indica se há cláusula de vigência expressa no contrato.
Sempre que o campo "duracao_em_dias" estiver preenchido retorne "true" em "clausula_vigencia".
false: Caso contrário.

9. registro_livro2_cartorio
Indica se há registro do contrato no Livro nº 2 do cartório de registro de imóveis.
true: Se houver menção ao registro no Livro nº 2.
false: Caso contrário.

10. registro_titulos_e_documentos_livro_3
Indica se há registro do contrato no Livro nº 3 do cartório de registro de imóveis.
true: Se houver menção ao registro no Livro nº 3.
false: Caso contrário.

11. observacoes
Campo destinado a observações gerais relevantes sobre o contrato, conforme detalhado abaixo:
inventario_bens: Descrição ou referência ao inventário de bens/mobília, se houver.
valor_aluguel: Valor do aluguel (ex: R$ 2.000,00).
substituicao_fiador_garantia: Procedimento para substituição de fiador ou garantia, se previsto.
obrigacoes_locador: Obrigações do locador (ex: entregar o imóvel em condições de uso, pagar impostos, etc.).
obrigacoes_locatario: Obrigações do locatário (ex: pagar aluguel, conservar o imóvel, não sublocar, etc.).
responsavel_manutencao_reparos: Responsável pela manutenção e reparos do imóvel (preventiva e corretiva).
multa_rescisao: Valor ou percentual da multa por rescisão antecipada.
aviso_previo: Prazo de aviso prévio exigido para rescisão (ex: 30 dias).
outras_penalidades: Outras penalidades previstas além da multa de rescisão.
direito_preferencia: Cláusula sobre direito de preferência do locatário em caso de venda do imóvel.
renovacao_automatica: Cláusula sobre renovação automática do contrato ao final do prazo.
aditivos_clausulas_especiais: Cláusulas adicionais, aditivos ou condições especiais (ex: permissão para sublocação, uso para atividade específica, etc.).
comentario_sobre_clausulas_contraditorias: Comentário sobre eventuais cláusulas contraditórias identificadas.
comentario_sobre_informacoes_ilegiveis: Comentário sobre trechos ilegíveis ou de difícil compreensão.
dados_duplicados: Comentários sobre dados duplicados, como por exemplo número de cpf ou cnpj.

## FORMATO DE RESPOSTA
 
Apresente sua resposta final no formato JSON, considerando que todas as datas devem estar no formato ‘%Y-%m-%d’.

{
   "e_contrato_de_locacao":"boolean",
   "nomes_que_possuem_selo_carimbo_de_firma_reconhecida":[
      
   ],
   "todos_os_envolvidos_no_contrato":[
      {
         "nome":"string",
         "endereco":"<string quando esse campo vier em vazio, então retorne Não Localizado. Caso venha apenas município e estado em que a pessoa resida, retorne esses valores>",
         "CPF_ou_CNPJ":"<string quando esse campo vier em vazio, então retorne Não Localizado>",
         "locador":"boolean",
         "locatario":"boolean",
         "fiador_ou_avalista":"boolean",
         "e_procurador_ou_representante_do_locador":"boolean",
         "e_procurador_ou_representante_do_locatario":"boolean",
         "e_procurador_ou_representante_do_fiador":"boolean",
         "possui_procurador_ou_representante":"boolean",
         "casado":"boolean",
         "venia_conjugal":"boolean",
         "assinatura_reconhecida_ou_digital":{
            "reconhecimento_de_firma":{
               "existe_nome_da_pessoa_ou_do_seu_representante_no_selo_firma":"boolean",
               "existe_carimbo_de_assinatura_confere_com_a_original_gerente_banco":"<boolean quando esse campo for true, então retorne true em existe_nome_da_pessoa_ou_do_seu_representante_no_selo_firma>",
               "matricula_gerente":"string",
               "nome_gerente_carimbo":"string",
               "registro_titulos_e_documentos_livro_3_firma_reconhecida":"boolean",
               "nome_pessoa_firma_reconhecida_e_locador_ou_locataria_ou_fiador":"string",
               "nome_pessoa_firma_reconhecida_e_procurador_ou_representante":"string",
               "numero_selo_cartorario":"string",
               "numero_selo_digital":"string",
               "site_consulta_selo":"string"
            },
            "assinatura_digital":{
               "existe_nome_da_pessoa_ou_do_seu_representante_no_selo_digital":"boolean",
               "nome_da_assinatura_digital_e_locador_ou_locataria_ou_fiador":"string",
               "nome_da_assinatura_digital_e_procurador_ou_representante":"string",
               "numero_selo_digital":"string",
               "site_autenticacao":"string"
            }
         }
      }
   ],
   "imovel":{
      "imovel_urbano":"boolean",
      "endereco_do_imovel":"string",
      "tipo_do_imovel":"string",
      "area_do_imovel":"string"
   },
   "atividades_permitidas":[
      
   ],
   "termos_locacao":{
      "data_inicio":"date",
      "duracao_em_dias":"number",
      "duracao_do_contrato_e_maior_ou_igual_a_dez_anos":"boolean",
      "data_vencimento_aluguel":"date"
   },
   "clausula_autorizacao_construcao_reforma":"string",
   "clausula_vigencia":"boolean",
   "registro_livro2_cartorio":"boolean",
   "registro_titulos_e_documentos_livro_3":"boolean",
   "observacoes":{
      "inventario_bens":"string",
      "valor_aluguel":"string",
      "substituicao_fiador_garantia":"string",
      "obrigacoes_locador":"string",
      "obrigacoes_locatario":"string",
      "responsavel_manutencao_reparos":"string",
      "multa_rescisao":"string",
      "aviso_previo":"string",
      "outras_penalidades":"string",
      "direito_preferencia":"string",
      "renovacao_automatica":"string",
      "aditivos_clausulas_especiais":"string",
      "comentario_sobre_clausulas_contraditorias":"string",
      "comentario_sobre_informacoes_ilegiveis":"string",
      "dados_duplicados":"string"
   }
}