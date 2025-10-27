"""
Este módulo gerencia os elementos da interface do usuário (UI), como botões e a exibição de texto.

A classe `Botao` cria um botão interativo que pode ser desenhado na tela e detectar cliques.
As funções auxiliares, como `desenhar_dados`, cuidam da apresentação de informações
dinâmicas, como o resultado da rolagem de dados. Isso ajuda a separar a lógica da UI
da lógica principal do jogo.
"""

import pygame
from utils.constants import BRANCO, VERDE, FONTE_PADRAO, TAMANHO_FONTE_TITULO

class Botao:
    """Cria um botão retangular clicável com texto."""

    def __init__(self, x, y, largura, altura, texto, cor_fundo=VERDE, cor_texto=BRANCO):
        """Inicializa o botão com sua posição, dimensões, texto e cores."""
        self.rect = pygame.Rect(x, y, largura, altura)
        self.texto = texto
        self.cor_fundo = cor_fundo
        self.cor_texto = cor_texto
        self.fonte = pygame.font.SysFont(FONTE_PADRAO, TAMANHO_FONTE_TITULO, True)

    def desenhar(self, tela):
        """Desenha o botão na superfície da tela."""
        pygame.draw.rect(tela, self.cor_fundo, self.rect, border_radius=10)
        texto_surf = self.fonte.render(self.texto, True, self.cor_texto)
        texto_rect = texto_surf.get_rect(center=self.rect.center)
        tela.blit(texto_surf, texto_rect)

    def foi_clicado(self, pos_mouse):
        """Verifica se o botão foi clicado com base na posição do mouse."""
        return self.rect.collidepoint(pos_mouse)

def desenhar_dados(tela, dados, x, y):
    """Exibe o resultado dos dados na tela."""
    fonte = pygame.font.SysFont(FONTE_PADRAO, TAMANHO_FONTE_TITULO, True)
    texto = fonte.render(f"Dados: {dados[0]} e {dados[1]}", True, BRANCO)
    tela.blit(texto, (x, y))
