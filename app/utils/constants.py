"""
Este módulo armazena todas as constantes globais do jogo, como cores,
configurações de tela e fontes. Manter essas constantes em um único
local facilita a manutenção e o ajuste dos parâmetros do jogo.
"""

import pygame

# --- DIMENSÕES DA TELA ---
LARGURA_TELA = 1280
ALTURA_TELA = 720

# --- CORES ---
BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)
VERDE = (0, 150, 0)
VERMELHO = (200, 0, 0)
CINZA = (100, 100, 100)
AZUL_ESCURO = (10, 10, 25)
COR_JOGADOR = (200, 0, 0)
COR_SCROLL_TRACK = (50, 50, 50)
COR_SCROLL_THUMB = (150, 150, 150)
FUNDO_ESCURO = (10, 10, 25)

# --- FONTES ---
pygame.init()
FONTE_PADRAO = pygame.font.SysFont('Arial', 18)
FONTE_TITULO = pygame.font.SysFont('Arial', 24, True)
FONTE_MENU_TITULO = pygame.font.SysFont('Arial', 72, True)

# --- CONFIGURAÇÕES DO TABULEIRO ---
LADO_MAXIMO_TABULEIRO = ALTURA_TELA - 40
NUM_POSICOES = 40
POSICAO_PRISAO_INDEX = 10

# --- POSIÇÕES DE PIXEL NO TABULEIRO ---
# Mapeia o índice de uma casa (0-39) para sua coordenada (x, y) na tela.
POSICOES_PIXEL = [(0, 0)] * NUM_POSICOES

# Cantos
POSICOES_PIXEL[0] = (655, 655)   # Go
POSICOES_PIXEL[10] = (45, 655)    # Jail
POSICOES_PIXEL[20] = (45, 45)     # Free Parking
POSICOES_PIXEL[30] = (655, 45)    # Go to Jail

# Lados
for i in range(1, 10):
    # Lado inferior (1-9)
    POSICOES_PIXEL[i] = (POSICOES_PIXEL[0][0] - i * 61, 655)
    # Lado esquerdo (11-19)
    POSICOES_PIXEL[10 + i] = (45, POSICOES_PIXEL[10][1] - i * 61)
    # Lado superior (21-29)
    POSICOES_PIXEL[20 + i] = (POSICOES_PIXEL[20][0] + i * 61, 45)
    # Lado direito (31-39)
    POSICOES_PIXEL[30 + i] = (655, POSICOES_PIXEL[30][1] + i * 61)

# Deslocamento para múltiplos jogadores na mesma casa
OFFSET_JOGADOR = [(-10, -10), (10, -10), (-10, 10), (10, 10)]

