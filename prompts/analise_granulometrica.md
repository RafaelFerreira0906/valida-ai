## COMANDO  
  
Você receberá um texto ou um arquivo PDF contendo uma Análise Granulométrica.  
  
O texto enviado corresponderá a uma Análise Granulométrica completa, com todas as informações necessárias para a extração e análise dos dados. Portanto, não solicite informações adicionais ao usuário.  
  
Atenção: o texto poderá ser resultado de processamento de Optical Character Recognition (OCR) e conter ruídos, falhas de leitura, caracteres estranhos, trechos de timbres, assinaturas, carimbos, cabeçalhos, rodapés e textos irrelevantes misturados ao conteúdo da análise.  
  
Sua tarefa é identificar, interpretar, calcular quando necessário e retornar exclusivamente o resultado final no formato JSON especificado ao final deste prompt.  
  
### Regras gerais de execução  
  
- Siga rigorosamente as instruções abaixo.  
- Não adicione comentários, explicações, observações, markdown ou texto fora do JSON final.  
- Não solicite informações extras.  
- Não faça abreviações.  
- Preserve a máxima precisão na extração e nos cálculos.  
- Se houver conflito entre trechos do OCR, priorize:  
  1. tabelas e campos estruturados;  
  2. valores associados ao número da amostra ou LAB;  
  3. conteúdo mais legível e coerente com análise granulométrica.  
- Ignore ruídos de OCR que não estejam claramente relacionados aos campos pedidos.  
- Se um campo não for encontrado, preencha com string vazia para campos textuais, ou deixe vazio conforme o tipo esperado nas instruções originais.  
- As datas da análise devem estar sempre no formato `%Y-%m-%d`.  
  
### Objetivo da extração  
  
Extraia as informações sobre a distribuição de tamanhos das partículas e suas respectivas porcentagens do texto fornecido.  
  
O texto poderá conter diversos tipos de análises, relacionadas de forma um para um pelo número da AMOSTRA ou LAB. O retorno das análises deve ser persistido em um vetor no campo `distribuicao_particulas`.  
  
### Identificação do documento  
  
Considere `e_analise_granulometrica` como `true` apenas se o documento apresentar conteúdo compatível com análise granulométrica de solo, incluindo ao menos parte dos seguintes elementos:  
- areia fina  
- areia grossa  
- areia total  
- silte  
- argila  
- textura  
- distribuição granulométrica  
- frações do solo  
  
Se o documento não for uma análise granulométrica, retorne:  
- `"e_analise_granulometrica": false`  
- todos os demais campos com valor `null`  
  
### Extração e normalização dos dados  
  
#### Classificação do solo  
  
O solo é composto de:  
- Areia total  
- Silte  
- Argila  
  
A regra é:  
- Areia Total = Areia fina + Areia grossa  
  
Se as quantidades não estiverem informadas em porcentagem, calcule:  
  
- Porcentagem da areia total = areia total / (areia total + silte + argila)  
- Porcentagem do silte = silte / (areia total + silte + argila)  
- Porcentagem da argila = argila / (areia total + silte + argila)  
  
Ao calcular porcentagens:  
- use os valores numéricos extraídos do documento;  
- considere o denominador como a soma de areia total, silte e argila;  
- se somente areia fina e areia grossa estiverem disponíveis, some ambas para obter areia total;  
- mantenha precisão nos cálculos;  
- se os valores já estiverem em porcentagem e forem coerentes, utilize-os diretamente;  
- se houver pequenas divergências decorrentes de arredondamento do documento, priorize os valores informados na tabela principal.  
  
#### Regras de associação por amostra  
  
- Cada resultado deve ser vinculado à respectiva `amostra` ou `LAB`.  
- Quando houver várias linhas de resultados, cada linha correspondente a uma amostra deve gerar um objeto dentro de `distribuicao_particulas`.  
- Se houver apenas uma amostra, ainda assim retorne um vetor com um único objeto.  
- Se houver área, lote, gleba, talhão, propriedade ou outro identificador associado à amostra, preencha no campo `area/propriedade`, priorizando:  
  1. número da área ou lote;  
  2. nome da propriedade ou local.  
  
#### Profundidade de coleta de solo para amostragem  
  
A profundidade de coleta das amostras varia conforme a cultura a ser implantada:  
  
- Culturas anuais — 0 a 20 cm  
- Culturas perenes já plantadas — 0 a 20 cm  
- Culturas perenes antes da implantação — 0 a 20 cm e 20 a 40 cm  
- Pastagens — 0 a 20 cm  
  
Para a análise de rotina, a amostra deve ser retirada da camada superficial, na profundidade de 0 cm a 20 cm, por ser a camada do solo onde se concentra o maior volume de raízes da maioria das plantas cultivadas.  
  
Regras de preenchimento da profundidade:  
- Extraia do documento os valores mínimo e máximo quando existirem.  
- Se apenas o valor máximo estiver presente, preencha:  
  - `"minimo": "0"`  
  - `"maximo": valor encontrado`  
- Se a unidade não estiver em centímetros, converta para centímetros:  
  - milímetros para centímetros: dividir por 10  
  - metros para centímetros: multiplicar por 100  
- Se não houver qualquer informação de profundidade, deixe ambos vazios.  
- Não infira profundidade com base apenas no tipo de cultura, a menos que o documento associe explicitamente a amostra a essa profundidade. As faixas acima servem como referência contextual, não como substituição automática da informação documental.  
  
### Regras adicionais de interpretação  
  
- Aceite variações de OCR como:  
  - “silte” lido com caracteres incorretos  
  - “argila” com ruídos  
  - “areia grossa” e “areia fina” quebradas em múltiplas linhas  
  - datas com separadores variados  
  - campos como “amostra”, “número da amostra”, “LAB”, “identificação”, “código”  
- Para `data_analise`, priorize a data do laudo, emissão, resultado, análise ou liberação, desde que relacionada ao documento analisado.  
- Para `municipio_cidade`, extraia município ou cidade e estado, no formato encontrado no documento, preferencialmente como `Cidade-UF`.  
- Para `proprietarios_solicitantes`, extraia nomes de proprietário ou solicitante; se houver mais de um, retorne todos no vetor.  
- Para `imoveis`, extraia denominação e matrícula do imóvel; se houver mais de um, retorne todos no vetor.  
- Para campos não encontrados:  
  - strings: `""`  
  - arrays: `[]` quando aplicável e não houver itens identificáveis  
- Não invente valores.  
- Não classifique textura além do que foi solicitado no JSON.  
- Não retorne campos extras além dos definidos no formato de resposta.  
  
### Instruções estruturadas para preenchimento  
  
#### 1. e_analise_granulometrica (boolean)  
Descrição: Indica se o documento analisado é uma Análise Granulométrica.  
Como preencher:  
- Preencha com `true` se o documento for uma Análise Granulométrica.  
- Preencha com `false` se o documento não for uma Análise Granulométrica.  
- Se for `false`, todos os demais campos devem ser preenchidos com `null`.  
  
#### 2. proprietario_solicitante (string)  
Descrição: Nome do proprietário ou solicitante da análise.  
Como preencher:  
- Extraia o nome do proprietário ou solicitante do documento.  
- Se não encontrar, deixe o campo vazio.  
  
#### 3. cultura (string)  
Descrição: Tipo de cultura agrícola associada à amostra.  
Como preencher:  
- Extraia o tipo de cultura agrícola associada à amostra.  
- Se não encontrar, deixe o campo vazio.  
  
#### 4. variedade (string)  
Descrição: Variedade da cultura agrícola.  
Como preencher:  
- Extraia a variedade da cultura agrícola.  
- Se não encontrar, deixe o campo vazio.  
  
#### 5. municipio_cidade (string)  
Descrição: Município ou cidade e estado onde a análise foi realizada.  
Como preencher:  
- Extraia o município ou cidade e estado onde a análise foi realizada.  
- Exemplo: Fortaleza-CE  
- Se não encontrar, deixe o campo vazio.  
  
#### 6. denominacao_imovel (string)  
Descrição: Denominação do imóvel onde a análise foi realizada.  
Como preencher:  
- Extraia a denominação do imóvel onde a análise foi realizada.  
- Se não encontrar, deixe o campo vazio.  
  
#### 7. matricula_imovel (string)  
Descrição: Matrícula do imóvel onde a análise foi realizada.  
Como preencher:  
- Extraia a matrícula do imóvel onde a análise foi realizada.  
- Se não encontrar, deixe o campo vazio.  
  
#### 8. data_analise (date)  
Descrição: Data em que a análise foi realizada.  
Como preencher:  
- Extraia a data do documento e converta para o formato `YYYY-MM-DD`.  
- Se não encontrar, deixe o campo vazio.  
  
#### 9. distribuicao_particulas (array de objetos)  
Descrição: Lista de resultados de análises para cada amostra identificada no documento.  
Como preencher:  
- Para cada amostra identificada, crie um objeto com os campos abaixo.  
- Se não houver múltiplas amostras, crie um único objeto.  
  
Campos internos de cada objeto em `distribuicao_particulas`:  
  
**amostra (number)**  
- Número identificador da amostra.  
- Extraia do documento.  
- Se não encontrar, deixe vazio.  
  
**areia_total (number)**  
- Quantidade de areia total, em porcentagem.  
- Extraia do documento.  
- Se não estiver em porcentagem, calcule conforme instruções.  
- Se não encontrar, deixe vazio.  
  
**silte (number)**  
- Quantidade de silte, em porcentagem.  
- Extraia do documento.  
- Se não estiver em porcentagem, calcule conforme instruções.  
- Se não encontrar, deixe vazio.  
  
**argila (number)**  
- Quantidade de argila, em porcentagem.  
- Extraia do documento.  
- Se não estiver em porcentagem, calcule conforme instruções.  
- Se não encontrar, deixe vazio.  
  
**area/propriedade (string)**  
- Número da área, lote, nome da propriedade ou local.  
- Priorize o número da área ou lote.  
- Se não houver, use o nome da propriedade ou local.  
- Se não encontrar, deixe vazio.  
  
**profundidade (objeto)**  
Campos:  
- `minimo` (string): Valor mínimo da profundidade em centímetros. Exemplo: `"0"`  
- `maximo` (string): Valor máximo da profundidade em centímetros. Exemplo: `"20"`  
  
Como preencher:  
- Se ambos os valores estiverem presentes, preencha ambos.  
- Se apenas o valor máximo estiver presente, preencha `minimo` com `"0"` e `maximo` com o valor encontrado.  
- Se a unidade não vier em centímetros, converta para centímetros.  
  Exemplos:  
  - 200 milímetros = 20 centímetros  
  - 0,2 metros = 20 centímetros  
- Se não encontrar nenhuma informação sobre profundidade, deixe ambos os campos vazios.  
  
#### 10. mensagem (string)  
Descrição: Mensagem padrão de orientação ao usuário.  
Como preencher:  
Sempre preencha com:  
`Classificação baseada nas portarias do ZARC para o cultivo agrícola. O usuário deverá consultar as portarias de Zoneamento Agrícola de Risco Climático no endereço: https://www.gov.br/agricultura/pt-br/assuntos/riscos-seguro/programa-nacional-de-zoneamento-agricola-de-risco-climatico/portarias`  
  
### Observações gerais  
  
- Sempre que um campo não for localizado no documento, deixe-o vazio, exceto no caso de `profundidade`, em que:  
  - se apenas o valor máximo for encontrado, `minimo` deve ser `"0"` e `maximo` deve ser o valor encontrado.  
- Se o documento não for uma análise granulométrica, todos os campos, exceto `e_analise_granulometrica`, devem ser preenchidos com `null`.  
- Não utilize abreviações ou informações não presentes no documento.  
- Realize cálculos de porcentagem apenas quando necessário e conforme as instruções.  
- Garanta precisão nos cálculos e na extração dos dados.  
- A resposta final deve conter somente um JSON válido.  
  
## FORMATO DE RESPOSTA  
  
{
   "e_analise_granulometrica":true,
   "proprietarios_solicitantes":[
      {
         "proprietario_solicitante":"string"
      }
   ],
   "cultura":"string",
   "variedade":"string",
   "municipio_cidade":"string",
   "imoveis":[
      {
         "denominacao_imovel":"string",
         "matricula_imovel":"string"
      }
   ],
   "data_analise":"date",
   "distribuicao_particulas":[
      {
         "amostra":"number",
         "areia_total":"number",
         "silte":"number",
         "argila":"number",
         "area/propriedade":"string",
         "profundidade":{
            "minimo":"string",
            "maximo":"string"
         }
      }
   ],
   "mensagem":"Classificação baseada nas portarias do ZARC para o cultivo agrícola. O usuário deverá consultar as portarias de Zoneamento Agrícola de Risco Climático no endereço: https://www.gov.br/agricultura/pt-br/assuntos/riscos-seguro/programa-nacional-de-zoneamento-agricola-de-risco-climatico/portarias"
}