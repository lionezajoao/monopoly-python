"""
Este módulo é responsável por gerenciar o tabuleiro do jogo.

Ele lida com o carregamento da imagem do tabuleiro e seu redimensionamento para
se ajustar à tela. A classe `Tabuleiro` centraliza a lógica visual do tabuleiro,
deixando o mapeamento de posições para o módulo de constantes.
"""

import sys
import pygame

from utils import constants

class Tabuleiro:
    """Representa o tabuleiro do jogo, focando na sua imagem."""

    def __init__(self, caminho_imagem):
        """Inicializa o tabuleiro, carregando e redimensionando a imagem."""
        self.imagem = self._carregar_e_redimensionar_imagem(caminho_imagem)

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
            pygame.quit()
            sys.exit()

    def desenhar(self, tela):
        """Desenha o tabuleiro na tela."""
        tela.blit(self.imagem, (20, 20))
