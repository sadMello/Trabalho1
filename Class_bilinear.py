import numpy as np

class Bilinear:
    def __init__(self, matriz):
        
        self.matriz = matriz
        self.qtd_linhas, self.qtd_colunas = matriz.shape
    
    def reduzir(self):
        new_h = self.qtd_linhas // 2
        new_w = self.qtd_colunas // 2
        matriz_reduzida = np.zeros((new_h, new_w), dtype=np.uint8)
        
        # Limita aos pixels válidos
        for i in range(new_h): 
            for j in range(new_w):
                x = min(i*2, self.qtd_linhas-1) # limita os pixels assim: 0 <= x <= qtd_linhas-1, ou seja, não ultrapassa a qtd_linhas da matriz original
                y = min(j*2, self.qtd_colunas-1) # limita os pixels assim: 0 <= y <= qtd_colunas-1 , ou seja, não ultrapassa a qtd_colunas da matriz original

                matriz_reduzida[i,j] = np.mean([self.matriz[x, y], self.matriz[x, y + 1], self.matriz[x + 1, y], self.matriz[x + 1, y + 1]]).astype(np.uint8) # calcula a média dos 4 pixels
               
        return matriz_reduzida

    def ampliar(self):

        linhas_ampliadas = self.qtd_linhas * 2
        cols_ampliadas = self.qtd_colunas * 2

        matriz_ampliada = np.zeros((linhas_ampliadas, cols_ampliadas), dtype=np.uint8)

        # preenche a matriz ampliada com os valores da matriz original nas linhas e colunas pares
        for i in range(self.qtd_linhas):
            for j in range(self.qtd_colunas):
                # Posição original
                matriz_ampliada[i*2, j*2] = self.matriz[i, j]

        # calcula os pixels horizontais (f(i,j+1))
        for i in range(0, linhas_ampliadas, 2):
            for j in range(1, cols_ampliadas - 1, 2):
                matriz_ampliada[i, j] = ((int(matriz_ampliada[i, j - 1]) + int(matriz_ampliada[i, j + 1])) // 2)

        # calcula os pixels verticais (f(i+1,j))
        for i in range(1, linhas_ampliadas - 1, 2):
            for j in range(0, cols_ampliadas, 2):
                matriz_ampliada[i, j] = ((int(matriz_ampliada[i - 1, j]) + int(matriz_ampliada[i + 1, j])) // 2)

        # diagonalmente (f(i+1,j+1))
        for i in range(1, linhas_ampliadas - 1, 2):
            for j in range(1, cols_ampliadas - 1, 2):
                soma = (
                    int(matriz_ampliada[i - 1, j - 1]) +
                    int(matriz_ampliada[i - 1, j + 1]) +
                    int(matriz_ampliada[i + 1, j - 1]) +
                    int(matriz_ampliada[i + 1, j + 1])
                )
                matriz_ampliada[i, j] = soma // 4

        return matriz_ampliada
