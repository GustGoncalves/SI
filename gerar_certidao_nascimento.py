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

        # Nome completo centralizado
        texto_nome = dado['nome_completo'].upper()
        largura_texto_nome = draw.textlength(texto_nome, font=fonte)
        x_nome = (largura_img - largura_texto_nome) / 2
        y_nome = posicoes['nome_completo'][1]  # mantém a posição vertical do JSON
        draw.text((x_nome, y_nome), texto_nome, font=fonte, fill=cor_fonte)

        # CPF centralizado
        texto_cpf = dado['numero_cpf'].upper()
        largura_texto_cpf = draw.textlength(texto_cpf, font=fonte)
        x_cpf = (largura_img - largura_texto_cpf) / 2
        y_cpf = posicoes['numero_cpf'][1]  # mantém a posição vertical do JSON
        draw.text((x_cpf, y_cpf), texto_cpf, font=fonte, fill=cor_fonte)

        # Matrícula centralizada (negrito)
        texto_matricula = dado['matricula']
        largura_texto_matricula = draw.textlength(texto_matricula, font=fonte_bold)
        x_matricula = (largura_img - largura_texto_matricula) / 2
        y_matricula = posicoes['matricula'][1]
        draw.text((x_matricula, y_matricula), texto_matricula, font=fonte_bold, fill=cor_fonte)

        # Restante dos campos
        for pos in posicoes['data_por_extenso']:
            draw.text(tuple(pos), dado['data_por_extenso'], font=fonte, fill=cor_fonte)
        draw.text(tuple(posicoes['dia']), dado['dia'], font=fonte, fill=cor_fonte)
        draw.text(tuple(posicoes['mes']), dado['mes'], font=fonte, fill=cor_fonte)
        draw.text(tuple(posicoes['ano']), dado['ano'], font=fonte, fill=cor_fonte)
        draw.text(tuple(posicoes['horario_nascimento']), dado['horario_nascimento'], font=fonte, fill=cor_fonte)

        for pos in posicoes['municipio']:
            draw.text(tuple(pos), dado['municipio'], font=fonte, fill=cor_fonte)

        for pos in posicoes['uf']:
            draw.text(tuple(pos), dado['uf'], font=fonte, fill=cor_fonte)

        draw.text(tuple(posicoes['local_nascimento']), dado['local_nascimento'], font=fonte, fill=cor_fonte)
        draw.text(tuple(posicoes['sexo']), dado['sexo'], font=fonte, fill=cor_fonte)
        draw.text(tuple(posicoes['nome_genitor1']), dado['nome_genitor1'], font=fonte, fill=cor_fonte)
        draw.text(tuple(posicoes['avos_genitor1']), dado['avos_genitor1'], font=fonte, fill=cor_fonte)
        draw.text(tuple(posicoes['nome_genitor2']), dado['nome_genitor2'], font=fonte, fill=cor_fonte)
        draw.text(tuple(posicoes['avos_genitor2']), dado['avos_genitor2'], font=fonte, fill=cor_fonte)
        draw.text(tuple(posicoes['gemeo']), dado['gemeo'], font=fonte, fill=cor_fonte)

        # Salva imagem final
        nome_saida = os.path.join(pasta_saida, f"certidao_nascimento_nova_{id_item}.jpg")
        imagem.save(nome_saida, "JPEG")

    print(f"{quantidade_imagens} imagens geradas na pasta '{pasta_saida}'")

def main():
    if len(sys.argv) > 1:
        quantidade_imagens = int(sys.argv[1])
    else:
        quantidade_imagens = int(input("Quantas imagens deseja gerar? "))

    imagem_base = "imagens_base/certidao_nascimento.jpg"
    csv_arquivo = "dados_fakes.csv"
    json_arquivo = "posicoes/posicoes_certidao_nascimento_nova.json"
    pasta_saida = "certidoes_nascimento_novas"

    gerar_imagens(quantidade_imagens, imagem_base, csv_arquivo, json_arquivo, pasta_saida)

if __name__ == "__main__":
    main()