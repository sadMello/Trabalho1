import numpy as np

class VizinhoMaisProximo:
    def __init__(self, matriz_img):
        """
        Inicializa o interpolador do vizinho mais próximo.

        """
        self.matriz_img = matriz_img
        self.qtd_linhas, self.qtd_colunas = matriz_img.shape

    def ajustar_dimensao(self):
        """
        Se a imagem tiver dimensões ímpares, duplica a última linha e/ou coluna para que
        seja possível formar blocos completos de 2x2.

        """
        matriz_ajustada = self.matriz_img.copy()
        linhas, cols = self.qtd_linhas, self.qtd_colunas
        
        if linhas % 2 != 0:
            ultima_linha = matriz_ajustada[-1:, :]
            matriz_ajustada = np.vstack((matriz_ajustada, ultima_linha))
            linhas += 1
        if cols % 2 != 0:
            ultima_coluna = matriz_ajustada[:, -1:]
            matriz_ajustada = np.hstack((matriz_ajustada, ultima_coluna))
            cols += 1
        return matriz_ajustada, linhas, cols

    def reduzir(self):
        """
        Reduz a imagem pela metade selecionando os pixels de índices pares.
        Se a imagem tiver dimensões ímpares, primeiro aplica padding.

        """
        mat_ajustada, linhas_aj, cols_aj = self.ajustar_dimensao()
        qtd_linhas_reduz = linhas_aj // 2
        qtd_cols_reduz = cols_aj // 2
        # Seleciona os pixels de índice par (0,2,4,…) em linhas e colunas
        matriz_reduzida = mat_ajustada[:qtd_linhas_reduz*2:2, :qtd_cols_reduz*2:2]
        return matriz_reduzida

    def ampliar(self):
        """
        Amplia a imagem duplicando cada pixel para formar um bloco 2x2.
        Calcula os índices de destino sem usar a função min(), usando condicionais para
        garantir que os índices não ultrapassem os limites.

        """
        nova_qtd_linhas = self.qtd_linhas * 2
        nova_qtd_colunas = self.qtd_colunas * 2
        matriz_ampliada = np.zeros((nova_qtd_linhas, nova_qtd_colunas), dtype=np.uint8)
        
        # Percorre cada pixel da imagem original
        for lin in range(self.qtd_linhas):
            for col in range(self.qtd_colunas):
                dest_lin = lin * 2
                dest_col = col * 2
                # Caso os índices ultrapassem os limites (condicional simples)
                if dest_lin > nova_qtd_linhas - 1:
                    dest_lin = nova_qtd_linhas - 1
                if dest_col > nova_qtd_colunas - 1:
                    dest_col = nova_qtd_colunas - 1
                # Preenche o bloco 2x2 com o mesmo valor do pixel original
                matriz_ampliada[dest_lin:dest_lin+2, dest_col:dest_col+2] = self.matriz_img[lin, col]
        return matriz_ampliada
