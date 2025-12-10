# Classificador Inteligente de Certidões (Nascimento/Casamento — Antigas e Novas)

Este projeto implementa um sistema completo de classificação automática de imagens de documentos, especificamente certidões de nascimento e certidões de casamento, tanto antigas quanto novas.

Ele inclui:

✔️ Geração de dados sintéticos
✔️ Geração de imagens realistas de certidões
✔️ Extração automática de features via OCR
✔️ Criação de Bag-of-Words personalizada
✔️ Treinamento de modelo de machine learning (XGBoost)
✔️ Avaliação e análise de erros

📌 Objetivo

Treinar um modelo capaz de classificar automaticamente qual tipo de certidão aparece na imagem:

Label	Tipo de Certidão
0	Nascimento — Nova
1	Casamento — Nova
2	Nascimento — Antiga
3	Casamento — Antiga
🧱 Estrutura Geral do Projeto

O pipeline completo é dividido em quatro etapas principais:

Geração de dados sintéticos (CSV)

Geração de imagens contendo os dados

Extração de texto e features via OCR

Treinamento e avaliação do modelo XGBoost

As quatro fases foram implementadas com scripts independentes, permitindo total reprodutibilidade.

## 1. Geração dos Dados Sintéticos (CSV)

📌 Arquivo: gerar_dados_sinteticos.py

Nesta etapa, utilizamos a biblioteca Faker para gerar registros totalmente fictícios contendo:

nome dos cônjuges / genitores

CPF

datas (nascimento e casamento)

matrícula

nacionalidade

UF

município

regime de bens

datas por extenso (com conversão completa)

Além disso, o script implementa:

🔹 Conversão numérica → extenso

Números são formatados ("17" → "dezessete") para simular certidões reais.

🔹 Datas realistas

Datas são geradas com intervalos de idade coerentes.

🔹 Matrícula formatada

Exemplo: 000000 00 00 0000 0 00000 000 0000000 00

🔹 Garantia de nomes com 3 palavras

Evita nomes curtos ("João Silva" → "JOÃO CARLOS SILVA").

🛠️ Execução
python gerar_dados_sinteticos.py


Um arquivo CSV será gerado:

dados_certidao_casamento.csv

## 2. Geração das Imagens Sintéticas

📌 Arquivo: gerar_imagens.py
📌 Usa como base: imagens_base/certidao_casamento.jpg
📌 Usa posições definidas em: posicoes_certidao_casamento_nova.json

O script:

abre a imagem modelo (template da certidão)

imprime os campos sintéticos nas coordenadas especificadas

salva cada certidão como .jpg

Saída:
certidoes_casamento_novas/
 ├── certidao_casamento_nova_1.jpg
 ├── certidao_casamento_nova_2.jpg
 ...

Execução:
python gerar_imagens.py 300

## 3. Extração de Features (OCR → CSV)

📌 Arquivo: extrair_features.py

Etapas do pipeline:
🧪 3.1 Pré-processamento da imagem

conversão para grayscale

filtro bilateral

limiar adaptativo (adaptive threshold Gaussian)

🧪 3.2 OCR
pytesseract.image_to_string(img, lang="por")

🧪 3.3 Normalização do texto

lowercase

remoção de acentos

remoção de símbolos

compactação de espaços

🧪 3.4 Bag-of-Words (contagem de palavras-chave)

Sua bag:

[
    "matricula", "certidao", "registro", "cpf", "genitor",
    "municipio", "data", "uf", "estado", "nome", "brasil", "civil"
]


Gera colunas como:

bag_matricula
bag_cpf
bag_data
bag_nome
...

🧪 3.5 Salvamento do CSV final
Execução:
python extrair_features.py

Saída exemplo:
features2.csv

## 4. Treinamento do Modelo — XGBoost

📌 Arquivo: treinar_modelo.py

4.1 Preparação dos datasets

CSV carregados:

features1.csv → label 0 (nascimento nova)

features2.csv → label 1 (casamento nova)

features3.csv → label 2 (nascimento antiga)

features4.csv → label 3 (casamento antiga)

4.2 Limpeza dos dados

Colunas removidas:

texto_raw
texto_normalizado

4.3 Concatenando tudo
features_completas = pd.concat([features1, features2, features3, features4])

4.4 Divisão treino/teste
train_test_split(X, y, test_size=0.2)

4.5 Modelo XGBoost usado
XGBClassifier(
    n_estimators=100,
    learning_rate=0.1,
    max_depth=5,
    subsample=0.8,
    colsample_bytree=0.8,
    random_state=42
)
