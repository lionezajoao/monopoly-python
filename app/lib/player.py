"""
Este módulo define a classe `Jogador`, que representa um jogador no jogo.

A classe encapsula o estado de um jogador, como sua posição no tabuleiro e sua cor.
Isso torna o gerenciamento de múltiplos jogadores mais simples e o código mais limpo.
O método `mover` atualiza a posição do jogador com base no resultado dos dados,
garantindo que ele permaneça dentro das 40 casas do tabuleiro.
"""

import pygame
from utils import constants

class Jogador:
    """Representa um jogador no jogo."""

    def __init__(self, cor=constants.COR_JOGADOR):
        """Inicializa o jogador com uma posição inicial e uma cor."""
        self.posicao = 0
        self.cor = cor

    def mover(self, casas):
        """Move o jogador pelo tabuleiro, tratando o loop de 40 posições."""
        self.posicao = (self.posicao + casas) % 40

    def desenhar(self, tela, pos_pixel):
        """Desenha o peão do jogador na tela."""
        pygame.draw.circle(tela, self.cor, pos_pixel, 15)  # Círculo principal
        pygame.draw.circle(tela, constants.PRETO, pos_pixel, 15, 3) # Borda preta
