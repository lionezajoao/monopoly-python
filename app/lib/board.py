"""
Este módulo é responsável por gerenciar o tabuleiro do jogo.

Ele lida com o carregamento da imagem do tabuleiro, seu redimensionamento para
se ajustar à tela e o cálculo das coordenadas de cada uma das 40 posições.
A classe `Tabuleiro` centraliza toda a lógica relacionada ao tabuleiro,
facilitando a interação de outros componentes do jogo com o espaço físico do tabuleiro.
"""

import sys
import pygame

from utils import constants

class Tabuleiro:
    """Representa o tabuleiro do jogo, incluindo a imagem e as posições."""

    def __init__(self, caminho_imagem):
        """Inicializa o tabuleiro, carregando a imagem e calculando as posições."""
        self.imagem = self._carregar_e_redimensionar_imagem(caminho_imagem)
        self.posicoes_pixels = self._mapear_posicoes()

    def _carregar_e_redimensionar_imagem(self, caminho_imagem):
        """Carrega a imagem do tabuleiro e a redimensiona para a tela."""
        try:
            imagem_original = pygame.image.load(caminho_imagem)
            largura_original, altura_original = imagem_original.get_size()

            if largura_original > altura_original:
                fator_escala = constants.LADO_MAXIMO_TABULEIRO / largura_original
                nova_largura = constants.LADO_MAXIMO_TABULEIRO
                nova_altura = int(altura_original * fator_escala)
            else:
                fator_escala = constants.LADO_MAXIMO_TABULEIRO / altura_original
                nova_altura = constants.LADO_MAXIMO_TABULEIRO
                nova_largura = int(largura_original * fator_escala)

            return pygame.transform.smoothscale(imagem_original, (nova_largura, nova_altura))
        except pygame.error as e:
            print(f"Erro ao carregar ou redimensionar a imagem '{caminho_imagem}': {e}")
            print("Verifique se o arquivo está no caminho correto e se o Pygame foi inicializado.")
            pygame.quit()
            sys.exit()

    def _mapear_posicoes(self):
        """Calcula e retorna as coordenadas de pixel para cada posição do tabuleiro."""
        posicoes = [(0, 0)] * constants.NUM_POSICOES

        # Define os 4 cantos como pontos de referência
        posicoes[0] = constants.POSICAO_INICIAL
        posicoes[10] = constants.POSICAO_PRISAO
        posicoes[20] = constants.POSICAO_ESTACIONAMENTO
        posicoes[30] = constants.POSICAO_VAPARAPRISAO

        # Calcula as posições intermediárias para cada lado do tabuleiro
        for i in range(1, 10):
            # Lado inferior (do Go para a Prisão)
            posicoes[i] = (posicoes[0][0] - i * constants.DISTANCIA_ENTRE_CASAS, posicoes[0][1])
            # Lado esquerdo (da Prisão ao Estacionamento)
            posicoes[10 + i] = (posicoes[10][0], posicoes[10][1] - i * constants.DISTANCIA_ENTRE_CASAS)
            # Lado superior (do Estacionamento ao Vá para a Prisão)
            posicoes[20 + i] = (posicoes[20][0] + i * constants.DISTANCIA_ENTRE_CASAS, posicoes[20][1])
            # Lado direito (do Vá para a Prisão ao Go)
            posicoes[30 + i] = (posicoes[30][0], posicoes[30][1] + i * constants.DISTANCIA_ENTRE_CASAS)

        return posicoes

    def desenhar(self, tela):
        """Desenha o tabuleiro na tela."""
        # O tabuleiro é desenhado com um pequeno deslocamento para centralizá-lo
        tela.blit(self.imagem, (20, 20))
