"""
Este módulo armazena todas as constantes globais do jogo, como cores,
configurações de tela e fontes. Manter essas constantes em um único
local facilita a manutenção e o ajuste dos parâmetros do jogo.
"""

# --- DIMENSÕES DA TELA ---
LARGURA_TELA = 1280
ALTURA_TELA = 720

# --- CORES ---
BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)
VERDE = (0, 150, 0)
AZUL_ESCURO = (10, 10, 25)
COR_JOGADOR = (200, 0, 0)

# --- FONTES ---
FONTE_PADRAO = 'Arial'
TAMANHO_FONTE_TITULO = 30

# --- CONFIGURAÇÕES DO TABULEIRO ---
LADO_MAXIMO_TABULEIRO = ALTURA_TELA
NUM_POSICOES = 40

# --- POSIÇÕES DE REFERÊNCIA (CANTOS) ---
# As coordenadas são (x, y) e foram ajustadas para um tabuleiro específico.
# Modifique se o seu tabuleiro tiver um layout diferente.
POSICAO_INICIAL = (680, 680)    # Canto inferior direito (Go)
POSICAO_PRISAO = (40, 680)      # Canto inferior esquerdo (Jail)
POSICAO_ESTACIONAMENTO = (40, 40) # Canto superior esquerdo (Free Parking)
POSICAO_VAPARAPRISAO = (680, 40) # Canto superior direito (Go to Jail)

# --- MOVIMENTO ---
# Distância em pixels entre o centro de duas casas consecutivas no tabuleiro.
DISTANCIA_ENTRE_CASAS = 64
