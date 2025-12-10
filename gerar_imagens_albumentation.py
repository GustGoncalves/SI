import cv2
import albumentations as A
import os

# Pasta de saída (onde as imagens transformadas serão salvas)
pasta_saida = "aug_certidao_casamento_antiga"
os.makedirs(pasta_saida, exist_ok=True)

# Transformação Albumentations (realista para documentos)
transformacao = A.Compose([
    A.RandomBrightnessContrast(p=0.5, brightness_limit=0.2, contrast_limit=0.2),
    A.Rotate(limit=3, p=0.5),                        # giro leve e realista
    A.Perspective(scale=(0.02, 0.05), p=0.3),        # deformação realista
    A.ImageCompression(quality_range=(60, 95), p=0.4),      # compressão típica de fotos
])

# Pasta de entrada (onde estão as imagens originais)
pasta_entrada = "certidoes_casamento_antigas"

# Lista todas as imagens da pasta
arquivos = os.listdir(pasta_entrada)

# Extensões aceitáveis (evita erros com .txt, .json etc)
extensoes_validas = {".jpg", ".jpeg", ".png", ".bmp", ".webp", ".tif"}

for arquivo in arquivos:

    # Ignora arquivos não imagem
    _, ext = os.path.splitext(arquivo.lower())
    if ext not in extensoes_validas:
        continue

    caminho_arquivo = os.path.join(pasta_entrada, arquivo)

    # Carrega a imagem
    imagem = cv2.imread(caminho_arquivo)
    if imagem is None:
        print(f"Erro ao ler: {arquivo}")
        continue

    # Aplica a transformação
    imagem_aumentada = transformacao(image=imagem)["image"]

    # Salva a imagem transformada
    caminho_saida = os.path.join(pasta_saida, "aug_" + arquivo)
    cv2.imwrite(caminho_saida, imagem_aumentada)

    print(f"✔ Transformada: {arquivo}")