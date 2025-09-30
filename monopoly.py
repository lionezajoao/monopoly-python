import pygame
import random
import sys

# --- INICIALIZAÇÃO E CONFIGURAÇÕES BÁSICAS DO PYGAME ---
pygame.init()

LARGURA_TELA, ALTURA_TELA = 1280, 720
TELA = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA))
pygame.display.set_caption("Seminopoly - Modo Simples")

# Definição de cores e fontes
BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)
VERDE = (0, 150, 0)
COR_JOGADOR = (200, 0, 0) # Vermelho para a peça do jogador
FONTE_TITULO = pygame.font.SysFont('Arial', 30, True)

# --- CARREGAMENTO E REDIMENSIONAMENTO DO TABULEIRO ---
try:
    imagem_original = pygame.image.load('tabuleiro.jpg')
    largura_original, altura_original = imagem_original.get_size()
    
    LADO_MAXIMO = ALTURA_TELA # O tabuleiro usará toda a altura disponível
    
    # Calcula a proporção para não distorcer a imagem
    if largura_original > altura_original:
        fator_escala = LADO_MAXIMO / largura_original
        nova_largura, nova_altura = LADO_MAXIMO, int(altura_original * fator_escala)
    else:
        fator_escala = LADO_MAXIMO / altura_original
        nova_altura, nova_largura = LADO_MAXIMO, int(largura_original * fator_escala)

    TABULEIRO_IMG = pygame.transform.smoothscale(imagem_original, (nova_largura, nova_altura))
except Exception as e:
    print(f"Erro ao carregar ou redimensionar 'tabuleiro.jpg': {e}.")
    print("Certifique-se de que o arquivo de imagem está na pasta correta.")
    sys.exit()

# --- MAPEAMENTO DAS POSIÇÕES (ESSENCIAL PARA O MOVIMENTO) ---
# Cria uma lista de 40 posições e calcula as coordenadas
POSICOES_PIXEL = [(0, 0)] * 40
# Define os 4 cantos como pontos de referência (ajustado para a imagem ocupar a tela toda)
POSICOES_PIXEL[0] = (680, 680)  # GO (Canto inferior direito)
POSICOES_PIXEL[10] = (40, 680)  # Jail (Canto inferior esquerdo)
POSICOES_PIXEL[20] = (40, 40)   # Free Parking (Canto superior esquerdo)
POSICOES_PIXEL[30] = (680, 40)  # Go To Jail (Canto superior direito)

# Calcula as posições intermediárias para cada lado
distancia_entre_casas = 64
for i in range(1, 10):
    POSICOES_PIXEL[i] = (POSICOES_PIXEL[0][0] - i * distancia_entre_casas, 680)
    POSICOES_PIXEL[10 + i] = (40, POSICOES_PIXEL[10][1] - i * distancia_entre_casas)
    POSICOES_PIXEL[20 + i] = (POSICOES_PIXEL[20][0] + i * distancia_entre_casas, 40)
    POSICOES_PIXEL[30 + i] = (680, POSICOES_PIXEL[30][1] + i * distancia_entre_casas)

# --- ELEMENTOS DA INTERFACE ---

class Botao:
    def __init__(self, x, y, largura, altura, texto):
        self.rect = pygame.Rect(x, y, largura, altura)
        self.texto = texto

    def desenhar(self, tela):
        pygame.draw.rect(tela, VERDE, self.rect, border_radius=10)
        texto_surf = FONTE_TITULO.render(self.texto, True, BRANCO)
        texto_rect = texto_surf.get_rect(center=self.rect.center)
        tela.blit(texto_surf, texto_rect)

    def foi_clicado(self, pos_mouse):
        return self.rect.collidepoint(pos_mouse)

def desenhar_dados(tela, dados, x, y):
    texto = FONTE_TITULO.render(f"Dados: {dados[0]} e {dados[1]}", True, BRANCO)
    tela.blit(texto, (x, y))

# --- FUNÇÃO PRINCIPAL DO JOGO ---

def main():
    clock = pygame.time.Clock()
    
    # Dados do jogador (muito simplificado)
    jogador = {
        'posicao': 0,
        'cor': COR_JOGADOR
    }
    
    # Variável para guardar o resultado dos dados
    dados_rolados = (0, 0)
    
    # Cria o botão
    botao_rolar = Botao(850, 300, 300, 80, "Rolar Dados")
    
    # Loop principal do jogo
    rodando = True
    while rodando:
        # Gerenciador de eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                rodando = False
            
            # Detecta clique do mouse
            if event.type == pygame.MOUSEBUTTONDOWN:
                if botao_rolar.foi_clicado(event.pos):
                    # Rola os dados
                    dado1 = random.randint(1, 6)
                    dado2 = random.randint(1, 6)
                    dados_rolados = (dado1, dado2)
                    
                    # Move o jogador
                    movimento = dado1 + dado2
                    jogador['posicao'] = (jogador['posicao'] + movimento) % 40
        
        # --- LÓGICA DE DESENHO ---
        
        # Pinta o fundo da tela
        TELA.fill((10, 10, 25)) # Azul escuro
        
        # Desenha o tabuleiro
        TELA.blit(TABULEIRO_IMG, (20, 20))
        
        # Desenha o jogador na sua posição atual
        pos_pixel = POSICOES_PIXEL[jogador['posicao']]
        pygame.draw.circle(TELA, jogador['cor'], pos_pixel, 15)
        pygame.draw.circle(TELA, PRETO, pos_pixel, 15, 3)
        
        # Desenha o painel da direita
        painel_x = TABULEIRO_IMG.get_width() + 40
        
        # Desenha o botão
        botao_rolar.desenhar(TELA)
        
        # Desenha o resultado dos dados
        if dados_rolados != (0, 0):
            desenhar_dados(TELA, dados_rolados, painel_x, 420)

        # Atualiza a tela
        pygame.display.flip()
        
        # Controla a velocidade do jogo (frames por segundo)
        clock.tick(60)

    pygame.quit()
    sys.exit()

# Roda o jogo
if __name__ == "__main__":
    main()