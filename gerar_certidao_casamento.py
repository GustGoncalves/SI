import csv
import json
import os
import sys
from PIL import Image, ImageDraw, ImageFont

def gerar_imagens(quantidade_imagens, imagem_base, csv_arquivo, json_arquivo, pasta_saida):
    # Configurações de fonte
    tamanho_fonte = 12  # ajuste conforme necessário
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

        largura_img, _ = imagem.size  # usamos só a largura para centralizar

        for pos in posicoes['nome_completo1']:
            draw.text(tuple(pos), dado['nome_completo1'], font=fonte, fill=cor_fonte)

        for pos in posicoes['nome_completo2']:
            draw.text(tuple(pos), dado['nome_completo2'], font=fonte, fill=cor_fonte)

        draw.text(tuple(posicoes['numero_cpf1']), dado['numero_cpf1'], font=fonte, fill=cor_fonte)
        draw.text(tuple(posicoes['numero_cpf2']), dado['numero_cpf2'], font=fonte, fill=cor_fonte)

        # Matrícula centralizada (negrito)
        texto_matricula = dado['matricula']
        largura_texto_matricula = draw.textlength(texto_matricula, font=fonte_bold)
        x_matricula = (largura_img - largura_texto_matricula) / 2
        y_matricula = posicoes['matricula'][1]
        draw.text((x_matricula, y_matricula), texto_matricula, font=fonte_bold, fill=cor_fonte)

        # Restante dos campos
        draw.text(tuple(posicoes['dia1']), dado['dia1'], font=fonte, fill=cor_fonte)
        draw.text(tuple(posicoes['mes1']), dado['mes1'], font=fonte, fill=cor_fonte)
        draw.text(tuple(posicoes['ano1']), dado['ano1'], font=fonte, fill=cor_fonte)
        draw.text(tuple(posicoes['dia2']), dado['dia2'], font=fonte, fill=cor_fonte)
        draw.text(tuple(posicoes['mes2']), dado['mes2'], font=fonte, fill=cor_fonte)
        draw.text(tuple(posicoes['ano2']), dado['ano2'], font=fonte, fill=cor_fonte)

        for pos in posicoes['nacionalidade']:
            draw.text(tuple(pos), dado['nacionalidade'], font=fonte, fill=cor_fonte)

        for pos in posicoes['estado_civil']:
            draw.text(tuple(pos), dado['estado_civil'], font=fonte, fill=cor_fonte)

        for pos in posicoes['municipio']:
            draw.text(tuple(pos), dado['municipio'], font=fonte, fill=cor_fonte)

        for pos in posicoes['uf']:
            draw.text(tuple(pos), dado['uf'], font=fonte, fill=cor_fonte)

        draw.text(tuple(posicoes['genitores1']), dado['genitores1'], font=fonte, fill=cor_fonte)
        draw.text(tuple(posicoes['genitores2']), dado['genitores2'], font=fonte, fill=cor_fonte)

        for pos in posicoes['data_por_extenso']:
            draw.text(tuple(pos), dado['data_por_extenso'], font=fonte, fill=cor_fonte)

        for pos in posicoes['dia3']:
            draw.text(tuple(pos), dado['dia3'], font=fonte, fill=cor_fonte)

        for pos in posicoes['mes3']:
            draw.text(tuple(pos), dado['mes3'], font=fonte, fill=cor_fonte)

        for pos in posicoes['ano3']:
            draw.text(tuple(pos), dado['ano3'], font=fonte, fill=cor_fonte)

        draw.text(tuple(posicoes['regime_de_bens']), dado['regime_de_bens'], font=fonte, fill=cor_fonte)

        # Salva imagem final
        nome_saida = os.path.join(pasta_saida, f"certidao_casamento_nova_{id_item}.jpg")
        imagem.save(nome_saida, "JPEG")

    print(f"{quantidade_imagens} imagens geradas na pasta '{pasta_saida}'")

def main():
    if len(sys.argv) > 1:
        quantidade_imagens = int(sys.argv[1])
    else:
        quantidade_imagens = int(input("Quantas imagens deseja gerar? "))

    imagem_base = "imagens_base/certidao_casamento.jpg"
    csv_arquivo = "dados_certidao_casamento.csv"
    json_arquivo = "posicoes/posicoes_certidao_casamento_nova.json"
    pasta_saida = "certidoes_casamento_novas"

    gerar_imagens(quantidade_imagens, imagem_base, csv_arquivo, json_arquivo, pasta_saida)

if __name__ == "__main__":
    main()