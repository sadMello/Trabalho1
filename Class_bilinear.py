import numpy as np

class Bilinear:
    def __init__(self, matriz_img):
        """
        Inicializa o interpolador bilinear.
        :param matriz_img: Matriz NumPy que representa a imagem em escala de cinza.
        """
        self.matriz_img = matriz_img
        self.qtd_linhas, self.qtd_colunas = matriz_img.shape

    def pad_imagem(self):
        """
        Aplica padding se necessário (duplica última linha/coluna) para que a imagem tenha dimensões pares.
        :return: matriz_pad, nova_qtd_linhas, nova_qtd_colunas.
        """
        matriz_pad = self.matriz_img.copy()
        linhas, cols = self.qtd_linhas, self.qtd_colunas
        
        if linhas % 2 != 0:
            ult_linha = matriz_pad[-1:, :]
            matriz_pad = np.vstack((matriz_pad, ult_linha))
            linhas += 1
        if cols % 2 != 0:
            ult_col = matriz_pad[:, -1:]
            matriz_pad = np.hstack((matriz_pad, ult_col))
            cols += 1
        return matriz_pad, linhas, cols

    def reduzir(self):
        """
        Reduz a imagem pela metade usando interpolação bilinear.
        Para cada bloco 2x2, calcula a média dos 4 pixels.
        :return: Matriz com a imagem reduzida.
        """
        mat_pad, linhas_pad, cols_pad = self.pad_imagem()
        linhas_reduz = linhas_pad // 2
        cols_reduz = cols_pad // 2
        matriz_reduzida = np.zeros((linhas_reduz, cols_reduz), dtype=np.uint8)
        
        for i in range(linhas_reduz):
            for j in range(cols_reduz):
                orig_lin = i * 2
                orig_col = j * 2
                bloco = mat_pad[orig_lin:orig_lin+2, orig_col:orig_col+2]
                matriz_reduzida[i, j] = np.mean(bloco)
        return matriz_reduzida

    def ampliar(self):
        """
        Amplia a imagem utilizando interpolação bilinear.
        Para cada posição na imagem ampliada, calcula a posição correspondente na imagem original (coordenada fracionária)
        e interpola o valor a partir dos 4 pixels vizinhos.
        Garante que todas as células da imagem ampliada sejam preenchidas, evitando "buracos".
        :return: Matriz com a imagem ampliada.
        """
        nova_lin = self.qtd_linhas * 2
        nova_col = self.qtd_colunas * 2
        matriz_ampliada = np.zeros((nova_lin, nova_col), dtype=np.float32)
        
        # Para cada pixel da imagem ampliada
        for i_dest in range(nova_lin):
            for j_dest in range(nova_col):
                # Mapeia para coordenadas na imagem original
                # Dividindo pelo fator (2) para obter a posição fracionária
                pos_y = i_dest / 2.0
                pos_x = j_dest / 2.0
                y0 = int(pos_y)
                x0 = int(pos_x)
                # Se estiver na borda, garante que não ultrapasse os limites
                if y0 >= self.qtd_linhas - 1:
                    y0 = self.qtd_linhas - 2
                if x0 >= self.qtd_colunas - 1:
                    x0 = self.qtd_colunas - 2
                y1 = y0 + 1
                x1 = x0 + 1

                # Distâncias fracionárias
                dy = pos_y - y0
                dx = pos_x - x0

                # Valores dos 4 pixels vizinhos
                valor00 = self.matriz_img[y0, x0]
                valor10 = self.matriz_img[y0, x1]
                valor01 = self.matriz_img[y1, x0]
                valor11 = self.matriz_img[y1, x1]

                # Interpolação bilinear
                valor_interp = ((1 - dx) * (1 - dy) * valor00 +
                                dx * (1 - dy) * valor10 +
                                (1 - dx) * dy * valor01 +
                                dx * dy * valor11)
                matriz_ampliada[i_dest, j_dest] = valor_interp

        # Converte para uint8 e retorna
        return np.clip(matriz_ampliada, 0, 255).astype(np.uint8)
