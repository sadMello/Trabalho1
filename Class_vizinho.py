import numpy as np

class VizinhoMaisProximo:
    def __init__(self, matriz):
        self.matriz = matriz
        self.altura, self.largura = matriz.shape

    def reduzir(self):
        # Garante que índices pares existam
        new_h = self.altura // 2 # reduz a altura pela metade
        new_w = self.largura // 2 # reduz a largura pela metade
        return self.matriz[:new_h*2:2, :new_w*2:2] # reduz a matriz para os índices pares, ou seja, pega os pixels 0, 2, 4, etc.

    def ampliar(self):
        nova_altura = self.altura * 2 # dobra a altura
        nova_largura = self.largura * 2 # dobra a largura
        # Cria uma nova matriz com zeros
        nova_matriz = np.zeros((nova_altura, nova_largura), dtype=np.uint8)
        
        # Preenche sem ultrapassar limites
        for i in range(self.altura):
            for j in range(self.largura):
                i2 = min(i*2, nova_altura-1) # limita os pixels assim: 0 <= i2 <= nova_altura-1
                j2 = min(j*2, nova_largura-1) # limita os pixels assim: 0 <= j2 <= nova_largura-1
                nova_matriz[i2:i2+2, j2:j2+2] = self.matriz[i, j] # preenche com o valor do pixel original
                
        return nova_matriz