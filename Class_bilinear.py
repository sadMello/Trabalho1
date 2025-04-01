import numpy as np

class Bilinear:
    def __init__(self, matriz):
        self.matriz = matriz
        self.altura, self.largura = matriz.shape
    
    def reduzir(self):
        new_h = self.altura // 2
        new_w = self.largura // 2
        nova_matriz = np.zeros((new_h, new_w), dtype=np.uint8)
        
        # Limita aos pixels válidos
        for i in range(new_h): 
            for j in range(new_w):
                x = min(i*2, self.altura-1) # limita os pixels assim: 0 <= x <= altura-1, ou seja, não ultrapassa a altura da matriz original
                y = min(j*2, self.largura-1) # limita os pixels assim: 0 <= y <= largura-1 , ou seja, não ultrapassa a largura da matriz original
                nova_matriz[i,j] = np.mean(self.matriz[x:x+2, y:y+2]) # essa linha faz a média dos 4 pixels vizinhos
                
        return nova_matriz
    
    def ampliar(self):
        nova_altura = self.altura * 2 # dobra a altura
        nova_largura = self.largura * 2 # dobra a largura
        # Cria uma nova matriz com zeros
        nova_matriz = np.zeros((nova_altura, nova_largura), dtype=np.uint8)
        
        # Preenche com verificação de bordas
        for i in range(self.altura):
            for j in range(self.largura):
                x = min(i, self.altura-2) # limita os pixels assim: 0 <= x <= altura-2
                y = min(j, self.largura-2)  # limita os pixels assim: 0 <= y <= largura-2
                
                # Coeficientes de interpolação bilinear (a, b, c, d)
                a = self.matriz[x, y]
                b = self.matriz[x, y+1] if y+1 < self.largura else a # se y+1 < largura, b = matriz[x, y+1], senão b = a
                c = self.matriz[x+1, y] if x+1 < self.altura else a # se x+1 < altura, c = matriz[x+1, y], senão c = a
                d = self.matriz[x+1, y+1] if (x+1 < self.altura and y+1 < self.largura) else a # se x+1 < altura e y+1 < largura, d = matriz[x+1, y+1], senão d = a
                
                # Interpolação bilinear
                nova_matriz[i*2, j*2] = a
                nova_matriz[i*2, j*2+1] = (a + b) // 2
                nova_matriz[i*2+1, j*2] = (a + c) // 2
                nova_matriz[i*2+1, j*2+1] = (a + b + c + d) // 4
                
        return nova_matriz