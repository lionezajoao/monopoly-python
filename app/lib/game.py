"""
Este módulo contém a classe `Jogo`, que orquestra todo o fluxo do jogo.

A classe `Jogo` é responsável por inicializar o Pygame, gerenciar o loop principal,
processar eventos (como cliques de mouse e fechamento da janela), atualizar o estado
dos objetos (jogador, dados) e desenhar tudo na tela. Separar essa lógica
na classe `Jogo` torna o `main.py` apenas um ponto de entrada, melhorando a
organização e a legibilidade do código.
"""

import pygame
import random
import sys

from lib.player import Jogador
from lib.board import Tabuleiro
from lib.ui import Botao, desenhar_dados
from utils.constants import LARGURA_TELA, ALTURA_TELA, AZUL_ESCURO

class Jogo:
    """Classe principal que gerencia o jogo Monopoly simplificado."""

    def __init__(self):
        """Inicializa o Pygame, a tela e os componentes do jogo."""
        pygame.init()
        self.tela = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA))
        pygame.display.set_caption("Seminopoly - Modo Simples")
        self.clock = pygame.time.Clock()
        self.rodando = True
        self.dados_rolados = (0, 0)

        # Componentes do jogo
        self.tabuleiro = Tabuleiro('app/static/tabuleiro.jpg')
        self.jogador = Jogador()
        self.botao_rolar = Botao(850, 300, 300, 80, "Rolar Dados")

    def _processar_eventos(self):
        """Cuida de todos os eventos do Pygame (teclado, mouse, etc.)."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.rodando = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if self.botao_rolar.foi_clicado(event.pos):
                    self._rolar_dados_e_mover_jogador()

    def _rolar_dados_e_mover_jogador(self):
        """Rola os dados, move o jogador e atualiza o estado."""
        dado1 = random.randint(1, 6)
        dado2 = random.randint(1, 6)
        self.dados_rolados = (dado1, dado2)
        movimento = dado1 + dado2
        self.jogador.mover(movimento)

    def _desenhar(self):
        """Desenha todos os elementos do jogo na tela."""
        self.tela.fill(AZUL_ESCURO)

        # Desenha o tabuleiro
        self.tabuleiro.desenhar(self.tela)

        # Desenha o jogador
        pos_pixel = self.tabuleiro.posicoes_pixels[self.jogador.posicao]
        self.jogador.desenhar(self.tela, pos_pixel)

        # Painel direito (UI)
        painel_x = self.tabuleiro.imagem.get_width() + 40
        self.botao_rolar.desenhar(self.tela)

        if self.dados_rolados != (0, 0):
            desenhar_dados(self.tela, self.dados_rolados, painel_x, 420)

        pygame.display.flip()

    def rodar(self):
        """Inicia e mantém o loop principal do jogo."""
        while self.rodando:
            self._processar_eventos()
            self._desenhar()
            self.clock.tick(60)  # Limita a 60 FPS

        self.finalizar()

    def finalizar(self):
        """Encerra o Pygame e fecha o jogo."""
        pygame.quit()
        sys.exit()
