import csv
import json
import os
import sys
from PIL import Image, ImageDraw, ImageFont

def gerar_imagens(quantidade_imagens, imagem_base, csv_arquivo, json_arquivo, pasta_saida):
    # Configurações de fonte
    tamanho_fonte = 20  # ajuste conforme necessário
    cor_fonte = (0, 0, 0)
    fonte_caminho = "Arial.ttf"  # substitua por outra TTF se quiser
    fonte = ImageFont.truetype(fonte_caminho, tamanho_fonte)
    fonte_bold = ImageFont.truetype("arialbd.ttf", tamanho_fonte)

    os.makedirs(pasta_saida, exist_ok=True)

    # Lê os dados do CSV
    with open(csv_arquivo, newline='', encoding='utf-8') as f:
        dados_csv = list(csv.DictReader(f))

    # Lê o JSON com posições
    with open(json_arquivo, encoding='utf-8') as f:
        posicoes = json.load(f)

    quantidade_imagens = min(quantidade_imagens, len(dados_csv))

    for id_item, dado in enumerate(dados_csv[:quantidade_imagens], start=1):
        imagem = Image.open(imagem_base).convert("RGB")
        draw = ImageDraw.Draw(imagem)

        draw.text(tuple(posicoes['numero_casamento']), dado['numero_casamento'], font=fonte, fill=cor_fonte)
        draw.text(tuple(posicoes['folhas']), dado['folhas'], font=fonte, fill=cor_fonte)
        draw.text(tuple(posicoes['livro']), dado['livro'], font=fonte, fill=cor_fonte)
        draw.text(tuple(posicoes['ato']), dado['ato'], font=fonte, fill=cor_fonte)

        for pos in posicoes['nome_completo1']:
            draw.text(tuple(pos), dado['nome_completo1'], font=fonte, fill=cor_fonte)

        for pos in posicoes['nome_completo2']:
            draw.text(tuple(pos), dado['nome_completo2'], font=fonte, fill=cor_fonte)

        draw.text(tuple(posicoes['juiz']), dado['juiz'], font=fonte, fill=cor_fonte)
        draw.text(tuple(posicoes['testemunhas']), dado['testemunhas'], font=fonte, fill=cor_fonte)

        for pos in posicoes['municipio']:
            draw.text(tuple(pos), dado['municipio'], font=fonte, fill=cor_fonte)

        draw.text(tuple(posicoes['dia1']), dado['dia1'], font=fonte, fill=cor_fonte)
        draw.text(tuple(posicoes['mes1']), dado['mes1'], font=fonte, fill=cor_fonte)
        draw.text(tuple(posicoes['ano1']), dado['ano1'], font=fonte, fill=cor_fonte)
        draw.text(tuple(posicoes['dia2']), dado['dia2'], font=fonte, fill=cor_fonte)
        draw.text(tuple(posicoes['mes2']), dado['mes2'], font=fonte, fill=cor_fonte)
        draw.text(tuple(posicoes['ano2']), dado['ano2'], font=fonte, fill=cor_fonte)

        for pos in posicoes['profissao']:
            draw.text(tuple(pos), dado['profissao'], font=fonte, fill=cor_fonte)

        for pos in posicoes['domicilio']:
            draw.text(tuple(pos), dado['domicilio'], font=fonte, fill=cor_fonte)

        for pos in posicoes['residencia']:
            draw.text(tuple(pos), dado['residencia'], font=fonte, fill=cor_fonte)

        draw.text(tuple(posicoes['nome_genitor1']), dado['nome_genitor1'], font=fonte, fill=cor_fonte)
        draw.text(tuple(posicoes['nome_genitor2']), dado['nome_genitor2'], font=fonte, fill=cor_fonte)
        draw.text(tuple(posicoes['nome_genitor3']), dado['nome_genitor3'], font=fonte, fill=cor_fonte)
        draw.text(tuple(posicoes['nome_genitor4']), dado['nome_genitor4'], font=fonte, fill=cor_fonte)

        # Salva imagem final
        nome_saida = os.path.join(pasta_saida, f"certidao_casamento_antiga_{id_item}.jpg")
        imagem.save(nome_saida, "JPEG")

    print(f"{quantidade_imagens} imagens geradas na pasta '{pasta_saida}'")

def main():
    if len(sys.argv) > 1:
        quantidade_imagens = int(sys.argv[1])
    else:
        quantidade_imagens = int(input("Quantas imagens deseja gerar? "))

    imagem_base = "imagens_base/certidao_casamento_antiga.png"
    csv_arquivo = "dados_certidao_casamento_antiga.csv"
    json_arquivo = "posicoes/posicoes_certidao_casamento_antiga.json"
    pasta_saida = "certidoes_casamento_antigas"

    gerar_imagens(quantidade_imagens, imagem_base, csv_arquivo, json_arquivo, pasta_saida)

if __name__ == "__main__":
    main()