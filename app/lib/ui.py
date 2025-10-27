"""
Este módulo gerencia todos os elementos da interface do usuário (UI).

Inclui componentes interativos como botões, pop-ups e caixas de texto, bem como
elementos de exibição de informações, como o log de eventos do jogo e o painel
de status dos jogadores. A centralização desses componentes facilita a manutenção
e a consistência visual do jogo.
"""

import pygame
from utils import constants

class Botao:
    """Cria um botão retangular clicável com texto e cores personalizáveis."""
    def __init__(self, x, y, l, h, texto, cor, cor_h, fonte=constants.FONTE_TITULO):
        self.rect = pygame.Rect(x, y, l, h)
        self.texto = texto
        self.cor = cor
        self.cor_h = cor_h  # Cor ao passar o mouse (hover)
        self.fonte = fonte

    def desenhar(self, tela, mouse):
        """Desenha o botão, mudando de cor se o mouse estiver sobre ele."""
        cor_atual = self.cor_h if self.rect.collidepoint(mouse) else self.cor
        pygame.draw.rect(tela, cor_atual, self.rect, border_radius=8)
        ts = self.fonte.render(self.texto, True, constants.BRANCO)
        tela.blit(ts, ts.get_rect(center=self.rect.center))

    def foi_clicado(self, pos):
        """Verifica se uma posição (geralmente do mouse) está sobre o botão."""
        return self.rect.collidepoint(pos)

class Popup:
    """Um pop-up para ações de Sim/Não, como comprar uma propriedade."""
    def __init__(self, t, m):
        self.rect = pygame.Rect(0, 0, 400, 200)
        self.rect.center = (constants.LARGURA_TELA / 2, constants.ALTURA_TELA / 2)
        self.t = t  # Título
        self.m = m  # Mensagem
        self.ativo = False
        self.bs = Botao(self.rect.x + 50, self.rect.y + 120, 100, 50, "Sim", constants.VERDE, (0, 200, 0))
        self.bn = Botao(self.rect.x + 250, self.rect.y + 120, 100, 50, "Não", constants.VERMELHO, (255, 0, 0))

    def ativar(self, t, m):
        """Ativa o pop-up com um novo título e mensagem."""
        self.t, self.m, self.ativo = t, m, True

    def desenhar(self, tela, mouse):
        """Desenha o pop-up se ele estiver ativo."""
        if not self.ativo:
            return
        pygame.draw.rect(tela, constants.PRETO, self.rect, border_radius=15)
        pygame.draw.rect(tela, constants.BRANCO, self.rect, width=2, border_radius=15)
        ts = constants.FONTE_TITULO.render(self.t, True, constants.BRANCO)
        ms = constants.FONTE_PADRAO.render(self.m, True, constants.BRANCO)
        tela.blit(ts, (self.rect.x + 20, self.rect.y + 20))
        tela.blit(ms, (self.rect.x + 20, self.rect.y + 70))
        self.bs.desenhar(tela, mouse)
        self.bn.desenhar(tela, mouse)

class Log:
    """Uma caixa de texto com rolagem para exibir o log de eventos do jogo."""
    def __init__(self, x, y, largura, altura):
        self.full_rect = pygame.Rect(x, y, largura, altura)
        self.text_area_rect = pygame.Rect(x, y, largura - 15, altura)
        self.mensagens = []
        self.scroll_offset = 0
        self.line_height = 20
        self.padding = 5
        self.is_dragging = False
        self.drag_start_y = 0
        self.drag_start_scroll_offset = 0
        self.text_surface = pygame.Surface(self.text_area_rect.size, pygame.SRCALPHA)
        self.scrollbar_track_rect = pygame.Rect(self.text_area_rect.right, y, 15, altura)
        self.scrollbar_thumb_rect = pygame.Rect(self.scrollbar_track_rect.x + 2, y, 11, 0)

    def adicionar(self, msg):
        """Adiciona uma mensagem ao log e rola para o final."""
        self.mensagens.append(msg)
        self.scroll_to_bottom()

    def get_content_height(self):
        """Calcula a altura total do conteúdo do log."""
        return max(self.text_area_rect.height, len(self.mensagens) * self.line_height + self.padding * 2)

    def clamp_scroll(self):
        """Garante que o offset de rolagem permaneça dentro dos limites."""
        max_scroll = max(0, self.get_content_height() - self.text_area_rect.height)
        self.scroll_offset = max(0, min(self.scroll_offset, max_scroll))

    def scroll(self, dy_pixel):
        """Rola o conteúdo do log por uma quantidade de pixels."""
        self.scroll_offset += dy_pixel
        self.clamp_scroll()

    def scroll_to_bottom(self):
        """Rola o log para a mensagem mais recente."""
        self.scroll_offset = self.get_content_height() - self.text_area_rect.height
        self.clamp_scroll()

    def update_thumb(self):
        """Atualiza a posição e o tamanho da barra de rolagem."""
        ch = self.get_content_height()
        if ch <= self.text_area_rect.height:
            self.scrollbar_thumb_rect.height = 0
        else:
            vr = self.text_area_rect.height / ch
            self.scrollbar_thumb_rect.height = max(20, self.text_area_rect.height * vr)
            sr = self.scroll_offset / (ch - self.text_area_rect.height)
            ats = self.scrollbar_track_rect.height - self.scrollbar_thumb_rect.height
            self.scrollbar_thumb_rect.y = self.scrollbar_track_rect.y + (sr * ats)

    def handle_mouse_event(self, event, mouse_pos):
        """Processa eventos de mouse para a funcionalidade de rolagem."""
        if not self.full_rect.collidepoint(mouse_pos):
            return False
        if event.type == pygame.MOUSEWHEEL:
            self.scroll(-event.y * self.line_height)
            return True
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.scrollbar_thumb_rect.collidepoint(mouse_pos):
                self.is_dragging = True
                self.drag_start_y = mouse_pos[1]
                self.drag_start_scroll_offset = self.scroll_offset
                return True
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            self.is_dragging = False
            return True
        if event.type == pygame.MOUSEMOTION and self.is_dragging:
            dy = mouse_pos[1] - self.drag_start_y
            ch = self.get_content_height()
            ats = self.scrollbar_track_rect.height - self.scrollbar_thumb_rect.height
            if ch > self.text_area_rect.height and ats > 0:
                ctr = (ch - self.text_area_rect.height) / ats
                self.scroll_offset = self.drag_start_scroll_offset + (dy * ctr)
                self.clamp_scroll()
            return True
        return False

    def desenhar(self, tela):
        """Desenha a caixa de log e sua barra de rolagem."""
        pygame.draw.rect(tela, constants.PRETO, self.text_area_rect)
        pygame.draw.rect(tela, constants.CINZA, self.text_area_rect, 1)
        self.text_surface.fill((0, 0, 0, 0))
        y_pos = self.padding - self.scroll_offset
        for msg in self.mensagens:
            ts = constants.FONTE_PADRAO.render(msg, True, constants.BRANCO)
            self.text_surface.blit(ts, (self.padding, y_pos))
            y_pos += self.line_height
        tela.blit(self.text_surface, self.text_area_rect.topleft)

        if self.get_content_height() > self.text_area_rect.height:
            self.update_thumb()
            pygame.draw.rect(tela, constants.COR_SCROLL_TRACK, self.scrollbar_track_rect)
            pygame.draw.rect(tela, constants.COR_SCROLL_THUMB, self.scrollbar_thumb_rect, border_radius=4)

class TextInputBox:
    """Uma caixa de entrada de texto para o nome dos jogadores."""
    def __init__(self, x, y, w, h, fonte=constants.FONTE_TITULO):
        self.rect = pygame.Rect(x, y, w, h)
        self.color_inactive = constants.CINZA
        self.color_active = constants.BRANCO
        self.color = self.color_inactive
        self.text = ''
        self.fonte = fonte
        self.active = False

    def handle_event(self, event):
        """Processa eventos de teclado e mouse para a caixa de texto."""
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.active = self.rect.collidepoint(event.pos)
            self.color = self.color_active if self.active else self.color_inactive
        if event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_RETURN:
                self.active = False
                self.color = self.color_inactive
            elif event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            else:
                self.text += event.unicode

    def draw(self, tela):
        """Desenha a caixa de texto na tela."""
        txt_surface = self.fonte.render(self.text, True, constants.BRANCO)
        y_pos_texto = self.rect.y + (self.rect.height - txt_surface.get_height()) // 2
        pygame.draw.rect(tela, constants.PRETO, self.rect)
        pygame.draw.rect(tela, self.color, self.rect, 2, border_radius=5)
        tela.blit(txt_surface, (self.rect.x + 10, y_pos_texto))

    def get_text(self):
        """Retorna o texto atual da caixa."""
        return self.text

def desenhar_dados(tela, d, x, y):
    """Desenha os dois dados na tela."""
    dr = pygame.Rect(x, y, 50, 50)
    pygame.draw.rect(tela, constants.BRANCO, dr, border_radius=5)
    t = constants.FONTE_TITULO.render(str(d[0]), True, constants.PRETO)
    tela.blit(t, t.get_rect(center=dr.center))
    dr.x += 60
    pygame.draw.rect(tela, constants.BRANCO, dr, border_radius=5)
    t = constants.FONTE_TITULO.render(str(d[1]), True, constants.PRETO)
    tela.blit(t, t.get_rect(center=dr.center))

def desenhar_painel_info(tela, jogo, log):
    """Desenha o painel de informações com o status de cada jogador."""
    px = constants.LADO_MAXIMO_TABULEIRO + 60
    for i, j in enumerate(jogo.jogadores):
        yb = 20 + i * 110
        # Destaca o jogador da vez
        cor_destaque = j.cor if i == jogo.jogador_da_vez_idx else constants.CINZA
        pygame.draw.rect(tela, cor_destaque, (px, yb, 10, 100))

        ns = constants.FONTE_TITULO.render(f"{j.nome} {'(PC)' if j.is_ai else ''}", True, constants.BRANCO)
        ds = constants.FONTE_PADRAO.render(f"${j.dinheiro}", True, constants.VERDE)
        ps = constants.FONTE_PADRAO.render(f"Propriedades: {len(j.propriedades)}", True, constants.BRANCO)
        tela.blit(ns, (px + 20, yb))
        tela.blit(ds, (px + 20, yb + 30))
        tela.blit(ps, (px + 20, yb + 55))

        if j.esta_preso:
            tela.blit(constants.FONTE_PADRAO.render("Na Prisão", True, constants.VERMELHO), (px + 20, yb + 75))

    log.desenhar(tela)
    desenhar_dados(tela, jogo.dados, px + 20, 640)
