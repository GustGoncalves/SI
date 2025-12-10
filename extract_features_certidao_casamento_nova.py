import cv2
import pytesseract
import os
import pandas as pd
import unicodedata
import re

# ============================================================
#  PRE-PROCESSAMENTO DA IMAGEM
# ============================================================
def preprocessar(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = cv2.bilateralFilter(gray, 11, 17, 17)
    thresh = cv2.adaptiveThreshold(
        gray, 255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY,
        31, 10
    )
    return thresh

# ============================================================
#  NORMALIZAÇÃO
# ============================================================
def normalizar_texto(texto):
    texto = texto.lower()
    texto = unicodedata.normalize("NFD", texto)
    texto = "".join(c for c in texto if unicodedata.category(c) != "Mn")  # tira acentos

    # remove símbolos, mantendo letras e números
    texto = re.sub(r"[^a-z0-9 ]+", " ", texto)

    # compacto espaços
    texto = re.sub(r"\s+", " ", texto).strip()
    return texto

# ============================================================
#  DESGRUDAR PALAVRAS COMUNS EM CERTIDÕES
# ============================================================


# ============================================================
#  OCR
# ============================================================
def extrair_texto(img):
    config = "--oem 3 --psm 6"
    return pytesseract.image_to_string(img, config=config, lang="por")

def contar_palavras(texto):
    return len(texto.split())

# ============================================================
#  PROCESSAMENTO DE UMA ÚNICA IMAGEM
# ============================================================
def processar_imagem(caminho):
    img = cv2.imread(caminho)
    img_prep = preprocessar(img)

    texto_raw = extrair_texto(img_prep)

    # normalização
    texto_norm = normalizar_texto(texto_raw)

    return {
        "nome_arquivo": os.path.basename(caminho),
        "texto_raw": texto_raw.strip(),
        "texto_normalizado": texto_norm,
        "quantidade_palavras": contar_palavras(texto_norm)
    }

# ============================================================
#  BAG OF WORDS — usando substring matching
# ============================================================
def obter_bag_palavras():
    return [
        "matricula",
        "certidao",
        "registro",
        "cpf",
        "genitor",
        "municipio",
        "data",
        "uf",
        "estado",
        "nome",
        "brasil",
        "civil"
    ]

def gerar_features_bag_palavras(df, bag):
    for palavra in bag:
        df[f"bag_{palavra}"] = df["texto_normalizado"].apply(
            lambda t: t.count(palavra)
        )
    return df

# ============================================================
#  CARREGAR IMAGENS
# ============================================================
def carregar_imagens(pasta):
    caminhos = []
    for arquivo in os.listdir(pasta):
        caminho = os.path.join(pasta, arquivo)
        if cv2.imread(caminho) is not None:
            caminhos.append(caminho)
        else:
            print(f"Arquivo inválido ignorado: {arquivo}")
    return caminhos

# ============================================================
#  PIPELINE PRINCIPAL
# ============================================================
def main():
    pasta_imagens = "minidataset2"
    csv_saida = "features2.csv"

    caminhos = carregar_imagens(pasta_imagens)

    resultados = []
    from tqdm import tqdm

    for caminho in tqdm(caminhos, desc="Processando imagens"):
        resultado = processar_imagem(caminho)
        resultados.append(resultado)

    df = pd.DataFrame(resultados)

    bag = obter_bag_palavras()
    df = gerar_features_bag_palavras(df, bag)

    df.to_csv(csv_saida, index=False, encoding="utf-8")
    print(f"\nCSV criado com sucesso: {csv_saida}")

if __name__ == "__main__":
    main()