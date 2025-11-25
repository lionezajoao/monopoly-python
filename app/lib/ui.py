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
    def __init__(self, x, y, l, h, texto, cor, cor_h, fonte=constants.FONTE_TITULO, data=None):
        self.rect = pygame.Rect(x, y, l, h)
        self.texto = texto
        self.cor = cor
        self.cor_h = cor_h  # Cor ao passar o mouse (hover)
        self.fonte = fonte
        self.data = data

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
    px = constants.LADO_MAXIMO_TABULEIRO + 40
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
    desenhar_dados(tela, jogo.dados, px + 440, 640)


class MenuGerenciar:
    """Menu para gerenciar propriedades (casas, hipotecas)."""
    def __init__(self, jogador, log):
        self.jogador = jogador
        self.log = log
        self.jogador.atualizar_monopolios()
        self.botoes_acao = []
        self.botao_voltar = Botao(constants.LARGURA_TELA/2 - 100, constants.ALTURA_TELA - 80, 200, 50, "Voltar", constants.VERMELHO, (255, 50, 50))
        self.rect = pygame.Rect(0, 0, 700, 600)
        self.rect.center = (constants.LARGURA_TELA/2, constants.ALTURA_TELA/2)
        self.grupos = self.jogador.get_propriedades_por_cor()

    def handle_event(self, event):
        """Processa eventos de mouse para o menu."""
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.botao_voltar.foi_clicado(event.pos):
                return 'VOLTAR'
            
            for botao in self.botoes_acao:
                if botao.foi_clicado(event.pos):
                    prop, acao = botao.data 
                    if acao == 'comprar': self.comprar_casa(prop)
                    elif acao == 'vender': self.vender_casa(prop)
                    elif acao == 'hipoteca': self.toggle_hipoteca(prop)
                    return 'ACAO'
        return None

    def comprar_casa(self, prop):
        """Tenta comprar uma casa ou hotel em uma propriedade."""
        if prop.num_casas >= 5:
            self.log.adicionar("Já possui um hotel!")
            return
        if self.jogador.dinheiro < prop.preco_casa:
            self.log.adicionar("Dinheiro insuficiente!")
            return
        
        # Garante construção uniforme
        props_do_grupo = self.grupos[prop.cor]
        min_casas = min(p.num_casas for p in props_do_grupo)
        if prop.num_casas > min_casas:
            self.log.adicionar("Construção deve ser uniforme no grupo!")
            return

        self.jogador.dinheiro -= prop.preco_casa
        prop.num_casas += 1
        tipo = "hotel" if prop.num_casas == 5 else "casa"
        self.log.adicionar(f"Comprou {tipo} em {prop.nome}.")

    def vender_casa(self, prop):
        """Tenta vender uma casa ou hotel de uma propriedade."""
        if prop.num_casas <= 0:
            self.log.adicionar("Nenhuma casa para vender!")
            return

        # Garante venda uniforme
        props_do_grupo = self.grupos[prop.cor]
        max_casas = max(p.num_casas for p in props_do_grupo)
        if prop.num_casas < max_casas:
            self.log.adicionar("Venda deve ser uniforme no grupo!")
            return

        preco_venda = prop.preco_casa // 2
        self.jogador.dinheiro += preco_venda
        prop.num_casas -= 1
        tipo = "hotel" if prop.num_casas == 4 else "casa"
        self.log.adicionar(f"Vendeu {tipo} de {prop.nome} por ${preco_venda}.")

    def toggle_hipoteca(self, prop):
        """Hipoteca ou resgata uma propriedade."""
        if prop.num_casas > 0:
            self.log.adicionar("Venda as casas antes de hipotecar!")
            return

        valor_hipoteca = prop.preco // 2
        valor_resgate = int(valor_hipoteca * 1.1)

        if prop.hipotecada:
            if self.jogador.dinheiro >= valor_resgate:
                self.jogador.dinheiro -= valor_resgate
                prop.hipotecada = False
                self.log.adicionar(f"Resgatou {prop.nome} por ${valor_resgate}.")
            else:
                self.log.adicionar("Dinheiro insuficiente para resgatar.")
        else:
            self.jogador.dinheiro += valor_hipoteca
            prop.hipotecada = True
            self.log.adicionar(f"Hipotecou {prop.nome} por ${valor_hipoteca}.")

    def desenhar(self, tela, mouse_pos):
        """Desenha o menu de gerenciamento na tela."""
        overlay = pygame.Surface(tela.get_size(), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        tela.blit(overlay, (0, 0))
        
        pygame.draw.rect(tela, constants.FUNDO_MODAL, self.rect, border_radius=15)
        pygame.draw.rect(tela, constants.BRANCO, self.rect, 3, border_radius=15)
        
        titulo_surf = constants.FONTE_TITULO.render(f"Gerenciar - {self.jogador.nome} (${self.jogador.dinheiro})", True, constants.BRANCO)
        tela.blit(titulo_surf, titulo_surf.get_rect(center=(self.rect.centerx, self.rect.y + 40)))
        
        self.botao_voltar.desenhar(tela, mouse_pos)
        self.botoes_acao.clear()
        
        y_offset = self.rect.y + 80
        for cor, propriedades in sorted(self.grupos.items()):
            if y_offset > self.rect.bottom - 100: break 
            
            tem_monopolio = self.jogador.tem_monopolio(cor)
            cor_titulo = constants.VERDE if tem_monopolio else constants.BRANCO
            
            titulo_grupo = constants.FONTE_TITULO.render(f"--- Grupo: {cor} {'(Monopólio)' if tem_monopolio else ''} ---", True, cor_titulo)
            tela.blit(titulo_grupo, (self.rect.x + 20, y_offset))
            y_offset += 35

            for prop in propriedades:
                casas_str = "H" if prop.num_casas == 5 else str(prop.num_casas)
                texto_prop = constants.FONTE_PADRAO.render(f"{prop.nome} (Casas: {casas_str})", True, constants.BRANCO)
                tela.blit(texto_prop, (self.rect.x + 30, y_offset + 5))

                if tem_monopolio:
                    if prop.num_casas < 5:
                        btn_comprar = Botao(self.rect.right - 100, y_offset, 30, 30, "+", constants.VERDE, (0, 255, 0), constants.FONTE_PADRAO, (prop, 'comprar'))
                        btn_comprar.desenhar(tela, mouse_pos)
                        self.botoes_acao.append(btn_comprar)
                    if prop.num_casas > 0:
                        btn_vender = Botao(self.rect.right - 50, y_offset, 30, 30, "-", constants.VERMELHO, (255, 50, 50), constants.FONTE_PADRAO, (prop, 'vender'))
                        btn_vender.desenhar(tela, mouse_pos)
                        self.botoes_acao.append(btn_vender)
                
                cor_btn_m = constants.VERMELHO if prop.hipotecada else constants.CINZA
                txt_btn = "R" if prop.hipotecada else "H"
                btn_hipoteca = Botao(self.rect.right - 150, y_offset, 40, 30, txt_btn, cor_btn_m, (200, 200, 0), constants.FONTE_PADRAO, (prop, 'hipoteca'))
                btn_hipoteca.desenhar(tela, mouse_pos)
                self.botoes_acao.append(btn_hipoteca)

                y_offset += 30
            y_offset += 10

class MenuTroca:
    """Menu para realizar trocas de propriedades e dinheiro entre jogadores."""
    def __init__(self, jogador_ativo, oponentes, log):
        self.jogador_ativo = jogador_ativo
        self.oponentes = oponentes
        self.oponente_selecionado = oponentes[0] if oponentes else None
        self.log = log
        self.rect = pygame.Rect(100, 50, constants.LARGURA_TELA - 200, constants.ALTURA_TELA - 100)
        
        self.estado = 'EDICAO'  # EDICAO ou CONFIRMACAO
        self.oferta_dinheiro = 0
        self.pedido_dinheiro = 0
        self.oferta_props = [] 
        self.pedido_props = [] 
        
        self.btn_fechar = Botao(self.rect.right - 120, self.rect.bottom - 60, 100, 40, "Cancelar", constants.VERMELHO, (255,100,100))
        self.btn_propor = Botao(self.rect.centerx - 75, self.rect.bottom - 60, 150, 40, "Propor", constants.VERDE, (100,255,100))
        self.btn_aceitar = Botao(self.rect.centerx - 110, self.rect.bottom - 60, 100, 40, "Aceitar", constants.VERDE, (0,255,0))
        self.btn_recusar = Botao(self.rect.centerx + 10, self.rect.bottom - 60, 100, 40, "Recusar", constants.VERMELHO, (255,0,0))

        self.botoes_oponentes = []
        x_op = self.rect.x + 20
        for op in self.oponentes:
            b = Botao(x_op, self.rect.y + 50, 120, 30, op.nome, constants.CINZA, (150,150,150), fonte=constants.FONTE_PADRAO, data=op)
            self.botoes_oponentes.append(b)
            x_op += 130

    def avaliar_troca_ia(self):
        """Lógica simples para a IA decidir se aceita a troca."""
        valor_dado = self.pedido_dinheiro + sum(p.preco for p in self.pedido_props)
        valor_recebido = self.oferta_dinheiro + sum(p.preco for p in self.oferta_props)
        # IA valoriza completar monopólios
        for p in self.oferta_props:
            if self.oponente_selecionado.tem_monopolio(p.cor):
                valor_recebido += 100
        return valor_recebido >= valor_dado

    def executar_troca(self):
        """Executa a troca de ativos entre os jogadores."""
        # Troca de dinheiro
        self.jogador_ativo.dinheiro -= self.oferta_dinheiro
        self.oponente_selecionado.dinheiro += self.oferta_dinheiro
        self.oponente_selecionado.dinheiro -= self.pedido_dinheiro
        self.jogador_ativo.dinheiro += self.pedido_dinheiro
        
        # Troca de propriedades ofertadas
        for p in self.oferta_props:
            p.dono = self.oponente_selecionado
            self.oponente_selecionado.propriedades.append(p)
            self.jogador_ativo.propriedades.remove(p)
            
        # Troca de propriedades pedidas
        for p in self.pedido_props:
            p.dono = self.jogador_ativo
            self.jogador_ativo.propriedades.append(p)
            self.oponente_selecionado.propriedades.remove(p)

        self.jogador_ativo.atualizar_monopolios()
        self.oponente_selecionado.atualizar_monopolios()
        self.log.adicionar("Troca realizada com sucesso!")

    def handle_event(self, event):
        """Processa eventos de mouse para o menu de troca."""
        if event.type != pygame.MOUSEBUTTONDOWN:
            return None
        
        pos = event.pos
        if self.estado == 'CONFIRMACAO':
            if self.btn_aceitar.foi_clicado(pos):
                self.executar_troca()
                return 'FECHAR'
            if self.btn_recusar.foi_clicado(pos):
                self.log.adicionar(f"{self.oponente_selecionado.nome} recusou a oferta.")
                return 'FECHAR'
            return None

        if self.btn_fechar.foi_clicado(pos): return 'FECHAR'
        
        for btn in self.botoes_oponentes:
            if btn.foi_clicado(pos):
                self.oponente_selecionado = btn.data
                self.pedido_props.clear()
                self.pedido_dinheiro = 0
        
        if self.btn_propor.foi_clicado(pos):
            if self.oponente_selecionado.is_ai:
                if self.avaliar_troca_ia():
                    self.executar_troca()
                else:
                    self.log.adicionar(f"{self.oponente_selecionado.nome} (IA) recusou a oferta.")
                return 'FECHAR'
            else:
                self.estado = 'CONFIRMACAO'
                return None

        # Controles de dinheiro
        if pygame.Rect(self.rect.x + 20, self.rect.bottom - 120, 100, 30).collidepoint(pos):
            if self.jogador_ativo.dinheiro >= self.oferta_dinheiro + 10: self.oferta_dinheiro += 10
        if pygame.Rect(self.rect.x + 130, self.rect.bottom - 120, 100, 30).collidepoint(pos):
            if self.oferta_dinheiro >= 10: self.oferta_dinheiro -= 10
        if pygame.Rect(self.rect.right - 230, self.rect.bottom - 120, 100, 30).collidepoint(pos):
            if self.oponente_selecionado.dinheiro >= self.pedido_dinheiro + 10: self.pedido_dinheiro += 10
        if pygame.Rect(self.rect.right - 120, self.rect.bottom - 120, 100, 30).collidepoint(pos):
            if self.pedido_dinheiro >= 10: self.pedido_dinheiro -= 10

        # Seleção de propriedades
        y = self.rect.y + 120
        for p in self.jogador_ativo.propriedades:
            if pygame.Rect(self.rect.x + 20, y, 200, 25).collidepoint(pos):
                if p in self.oferta_props: self.oferta_props.remove(p)
                else: self.oferta_props.append(p)
            y += 30
            
        if self.oponente_selecionado:
            y = self.rect.y + 120
            for p in self.oponente_selecionado.propriedades:
                if pygame.Rect(self.rect.centerx + 20, y, 200, 25).collidepoint(pos):
                    if p in self.pedido_props: self.pedido_props.remove(p)
                    else: self.pedido_props.append(p)
                y += 30
        return None

    def desenhar(self, tela, mouse):
        """Desenha o menu de troca na tela."""
        pygame.draw.rect(tela, constants.FUNDO_MODAL, self.rect, border_radius=10)
        cor_borda = (255, 255, 0) if self.estado == 'CONFIRMACAO' else constants.BRANCO
        pygame.draw.rect(tela, cor_borda, self.rect, 2, border_radius=10)
        
        titulo_str = f"{self.oponente_selecionado.nome}, aceita?" if self.estado == 'CONFIRMACAO' else "Menu de Trocas"
        t = constants.FONTE_TITULO.render(titulo_str, True, cor_borda)
        tela.blit(t, (self.rect.centerx - t.get_width()//2, self.rect.y + 10))
        
        if self.estado == 'EDICAO':
            for btn in self.botoes_oponentes:
                btn.cor = constants.VERDE if btn.data == self.oponente_selecionado else constants.CINZA
                btn.desenhar(tela, mouse)
        
        pygame.draw.line(tela, constants.BRANCO, (self.rect.centerx, self.rect.y + 90), (self.rect.centerx, self.rect.bottom - 80))
        
        # Painel do jogador ativo (oferta)
        t_eu = constants.FONTE_TITULO.render(f"{self.jogador_ativo.nome} Oferta:", True, constants.BRANCO)
        tela.blit(t_eu, (self.rect.x + 20, self.rect.y + 90))
        y = self.rect.y + 120
        props_para_mostrar = self.oferta_props if self.estado == 'CONFIRMACAO' else self.jogador_ativo.propriedades
        for p in props_para_mostrar:
            cor = constants.VERDE if p in self.oferta_props else constants.BRANCO
            if self.estado == 'CONFIRMACAO': cor = constants.BRANCO
            txt = f"{p.nome} {'(Hipot.)' if p.hipotecada else ''}"
            s = constants.FONTE_PADRAO.render(txt, True, cor)
            tela.blit(s, (self.rect.x + 20, y)); y += 30
            
        # Painel do oponente (pedido)
        if self.oponente_selecionado:
            t_op = constants.FONTE_TITULO.render(f"{self.oponente_selecionado.nome} Pede:", True, constants.BRANCO)
            tela.blit(t_op, (self.rect.centerx + 20, self.rect.y + 90))
            y = self.rect.y + 120
            props_para_mostrar = self.pedido_props if self.estado == 'CONFIRMACAO' else self.oponente_selecionado.propriedades
            for p in props_para_mostrar:
                cor = constants.VERDE if p in self.pedido_props else constants.BRANCO
                if self.estado == 'CONFIRMACAO': cor = constants.BRANCO
                txt = f"{p.nome} {'(Hipot.)' if p.hipotecada else ''}"
                s = constants.FONTE_PADRAO.render(txt, True, cor)
                tela.blit(s, (self.rect.centerx + 20, y)); y += 30
        
        # Dinheiro
        t_din_oferta = constants.FONTE_TITULO.render(f"$ {self.oferta_dinheiro}", True, constants.VERDE)
        tela.blit(t_din_oferta, (self.rect.x + 20, self.rect.bottom - 150))
        t_din_pedido = constants.FONTE_TITULO.render(f"$ {self.pedido_dinheiro}", True, constants.VERMELHO)
        tela.blit(t_din_pedido, (self.rect.right - 230, self.rect.bottom - 150))

        if self.estado == 'EDICAO':
            ts_info = constants.FONTE_PADRAO.render("[+10]  [-10]", True, constants.CINZA)
            tela.blit(ts_info, (self.rect.x + 20, self.rect.bottom - 120))
            tela.blit(ts_info, (self.rect.right - 230, self.rect.bottom - 120))
            self.btn_fechar.desenhar(tela, mouse)
            self.btn_propor.desenhar(tela, mouse)
        elif self.estado == 'CONFIRMACAO':
            self.btn_aceitar.desenhar(tela, mouse)
            self.btn_recusar.desenhar(tela, mouse)

