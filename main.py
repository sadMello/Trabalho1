from PIL import Image
import numpy as np
import os

from Class_vizinho import VizinhoMaisProximo
from Class_bilinear import Bilinear

def salvar(imagem_obj, nome_saida):
    """
    Salva a imagem na pasta 'output' e a exibe.
    :param imagem_obj: Objeto Image do Pillow.
    :param nome_saida: Nome do arquivo de saída.
    """
    os.makedirs("output", exist_ok=True)
    caminho_saida = os.path.join("output", nome_saida)
    imagem_obj.save(caminho_saida)
    print(f"Imagem salva em: {caminho_saida}")


def main():
    caminho_imagem = "imagem.jpg"  # Imagem deve estar na pasta do projeto
    try:
        imagem_orig = Image.open(caminho_imagem).convert("L") # Converte para escala de cinza
    except Exception as erro:
        print("Erro ao carregar a imagem:", erro)
        return

    matriz_img = np.array(imagem_orig, dtype=np.uint8)

    # Processamento com o método Vizinho Mais Próximo
    interp_vizinho = VizinhoMaisProximo(matriz_img)

    matriz_reduzida_vizinho = interp_vizinho.reduzir()
    img_reduzida_vizinho = Image.fromarray(matriz_reduzida_vizinho)
    salvar(img_reduzida_vizinho, "imagem_vizinho_reduzida.jpg")

    matriz_ampliada_vizinho = interp_vizinho.ampliar()
    img_ampliada_vizinho = Image.fromarray(matriz_ampliada_vizinho)
    salvar(img_ampliada_vizinho, "imagem_vizinho_ampliada.jpg")

    # Processamento com o método Bilinear
    interp_bilinear = Bilinear(matriz_img)

    matriz_reduzida_bilinear = interp_bilinear.reduzir()
    img_reduzida_bilinear = Image.fromarray(matriz_reduzida_bilinear)
    salvar(img_reduzida_bilinear, "imagem_bilinear_reduzida.jpg")

    matriz_ampliada_bilinear = interp_bilinear.ampliar()
    img_ampliada_bilinear = Image.fromarray(matriz_ampliada_bilinear)
    salvar(img_ampliada_bilinear, "imagem_bilinear_ampliada.jpg")

if __name__ == "__main__":
    main()
