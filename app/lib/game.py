"""
Este módulo contém a classe `Jogo`, que orquestra todo o fluxo do jogo Monopoly.

A classe `Jogo` gerencia o estado principal (menu, jogando, fim de jogo),
 o loop de eventos, a configuração dos jogadores (humanos e IAs), a lógica de turnos
 e a renderização de todos os elementos na tela. Ela integra os outros módulos,
 como `Tabuleiro`, `Jogador`, `Espaco` e `UI`, para criar a experiência completa.
"""

import pygame
import random
import sys
import os

from lib.player import Jogador
from lib.board import Tabuleiro
from lib.espaco import Espaco, Propriedade, EspacoAcao
from lib.ui import Botao, Popup, Log, TextInputBox, desenhar_painel_info, MenuGerenciar, MenuTroca
from utils import constants

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

class Jogo:
    """Classe principal que gerencia o jogo Monopoly completo."""

    def __init__(self):
        """Inicializa o Pygame, a tela e os componentes do jogo."""
        pygame.init()
        self.tela = pygame.display.set_mode((constants.LARGURA_TELA, constants.ALTURA_TELA))
        pygame.display.set_caption("Seminopoly")
        self.clock = pygame.time.Clock()
        self.game_state = 'MENU'  # Estados: MENU, JOGANDO, GERENCIAR, TROCAR, FIM_DE_JOGO
        self.dados = (0, 0)
        self.jogadores = []
        self.tabuleiro_casas = self.criar_tabuleiro_completo()
        self.jogador_da_vez_idx = 0
        self.estado_turno = 'ESPERANDO_ROLAGEM'

        # Componentes visuais
        self.tabuleiro_visual = Tabuleiro(resource_path('app/static/tabuleiro.jpg'))
        self.log = None
        self.popup_compra = None
        self.botoes_jogo = {}
        self.menu_gerenciamento = None
        self.menu_troca = None

        # Componentes do menu
        self._inicializar_menu()

    def _inicializar_menu(self):
        """Cria os componentes da interface do usuário para o menu principal."""
        self.num_jogadores_humanos = 1
        self.botoes_num_jogadores = [
            Botao(constants.LARGURA_TELA/2 - 220, 250, 100, 50, "1", constants.CINZA, constants.VERDE, fonte=constants.FONTE_TITULO),
            Botao(constants.LARGURA_TELA/2 - 110, 250, 100, 50, "2", constants.CINZA, constants.VERDE, fonte=constants.FONTE_TITULO),
            Botao(constants.LARGURA_TELA/2 + 0, 250, 100, 50, "3", constants.CINZA, constants.VERDE, fonte=constants.FONTE_TITULO),
            Botao(constants.LARGURA_TELA/2 + 110, 250, 100, 50, "4", constants.CINZA, constants.VERDE, fonte=constants.FONTE_TITULO)
        ]
        self.caixas_nome = [
            TextInputBox(constants.LARGURA_TELA/2 - 150, 350, 300, 40, fonte=constants.FONTE_PADRAO),
            TextInputBox(constants.LARGURA_TELA/2 - 150, 400, 300, 40, fonte=constants.FONTE_PADRAO),
            TextInputBox(constants.LARGURA_TELA/2 - 150, 450, 300, 40, fonte=constants.FONTE_PADRAO),
            TextInputBox(constants.LARGURA_TELA/2 - 150, 500, 300, 40, fonte=constants.FONTE_PADRAO)
        ]
        self.labels_nome = [constants.FONTE_TITULO.render(f"Jogador {i+1}:", True, constants.BRANCO) for i in range(4)]
        self.botao_iniciar = Botao(constants.LARGURA_TELA/2 - 100, 600, 200, 60, "INICIAR", constants.VERDE, (0, 200, 0))

    def setup_jogadores(self, nomes_jogadores_humanos):
        """Configura jogadores humanos e preenche o restante com IAs."""
        cores = [(255,0,0), (0,0,255), (0,255,0), (255,255,0)]
        num_humanos = len(nomes_jogadores_humanos)

        for i in range(num_humanos):
            nome = nomes_jogadores_humanos[i] if nomes_jogadores_humanos[i] else f"Jogador {i+1}"
            self.jogadores.append(Jogador(nome, is_ai=False, cor=cores[i]))

        num_ai = 4 - num_humanos
        for i in range(num_ai):
            self.jogadores.append(Jogador(f"PC {i+1}", is_ai=True, cor=cores[num_humanos+i]))

        random.shuffle(self.jogadores)

    def proximo_jogador(self):
        """Avança o turno para o próximo jogador."""
        self.jogador_da_vez_idx = (self.jogador_da_vez_idx + 1) % len(self.jogadores)

    def criar_tabuleiro_completo(self):
        """Cria a lista de objetos de Espaco que compõem o tabuleiro."""
        return [
            EspacoAcao("GO", "nada"),
            Propriedade("Wreck Room", "terreno", 60, [2, 10, 30, 90, 160, 250], constants.PRECOS_CASAS["Marrom"], "Marrom"),
            EspacoAcao("Community Chest", "sorte", 50),
            Propriedade("Boiler Room", "terreno", 60, [4, 20, 60, 180, 320, 450], constants.PRECOS_CASAS["Marrom"], "Marrom"),
            EspacoAcao("Formation Fee", "imposto", 200),
            Propriedade("Red Van", "estacao", 200, [25, 50, 100, 200], 0, "Branco"),
            Propriedade("Tennis Courts", "terreno", 100, [6, 30, 90, 270, 400, 550], constants.PRECOS_CASAS["Azul Claro"], "Azul Claro"),
            EspacoAcao("Chance", "sorte", 100),
            Propriedade("Laundry Room", "terreno", 100, [6, 30, 90, 270, 400, 550], constants.PRECOS_CASAS["Azul Claro"], "Azul Claro"),
            Propriedade("Weight Room", "terreno", 120, [8, 40, 100, 300, 450, 600], constants.PRECOS_CASAS["Azul Claro"], "Azul Claro"),
            EspacoAcao("Jail (Visiting)", "nada"),
            Propriedade("The Dorm", "terreno", 140, [10, 50, 150, 450, 625, 750], constants.PRECOS_CASAS["Rosa"], "Rosa"),
            Propriedade("Kenrick Light & Magic", "companhia", 150, [4, 10], 0, "Branco"),
            Propriedade("The Library", "terreno", 140, [10, 50, 150, 450, 625, 750], constants.PRECOS_CASAS["Rosa"], "Rosa"),
            Propriedade("The Auditorium", "terreno", 160, [12, 60, 180, 500, 700, 900], constants.PRECOS_CASAS["Rosa"], "Rosa"),
            Propriedade("Silver Van", "estacao", 200, [25, 50, 100, 200], 0, "Branco"),
            Propriedade("The Gym", "terreno", 180, [14, 70, 200, 550, 750, 950], constants.PRECOS_CASAS["Laranja"], "Laranja"),
            EspacoAcao("Community Chest", "sorte", 50),
            Propriedade("The Heights", "terreno", 180, [14, 70, 200, 550, 750, 950], constants.PRECOS_CASAS["Laranja"], "Laranja"),
            Propriedade("The Rectory", "terreno", 200, [16, 80, 220, 600, 800, 1000], constants.PRECOS_CASAS["Laranja"], "Laranja"),
            EspacoAcao("Free Parking", "nada"),
            Propriedade("The Lobby", "terreno", 220, [18, 90, 250, 700, 875, 1050], constants.PRECOS_CASAS["Vermelho"], "Vermelho"),
            EspacoAcao("Chance", "sorte", 100),
            Propriedade("The Courtyard", "terreno", 220, [18, 90, 250, 700, 875, 1050], constants.PRECOS_CASAS["Vermelho"], "Vermelho"),
            Propriedade("Priest Dining Room", "terreno", 240, [20, 100, 300, 750, 925, 1100], constants.PRECOS_CASAS["Vermelho"], "Vermelho"),
            Propriedade("White Van", "estacao", 200, [25, 50, 100, 200], 0, "Branco"),
            Propriedade("Convent", "terreno", 260, [22, 110, 330, 800, 975, 1150], constants.PRECOS_CASAS["Amarelo"], "Amarelo"),
            Propriedade("Mary Mother of the Word Chapel", "terreno", 260, [22, 110, 330, 800, 975, 1150], constants.PRECOS_CASAS["Amarelo"], "Amarelo"),
            Propriedade("Student Services", "companhia", 150, [4, 10], 0, "Branco"),
            Propriedade("St. Charles Chapel", "terreno", 280, [24, 120, 360, 850, 1025, 1200], constants.PRECOS_CASAS["Amarelo"], "Amarelo"),
            EspacoAcao("Go to Jail", "prisao"),
            Propriedade("Glennon Lounge", "terreno", 300, [26, 130, 390, 900, 1100, 1275], constants.PRECOS_CASAS["Verde"], "Verde"),
            Propriedade("Priest's Lounge", "terreno", 300, [26, 130, 390, 900, 1100, 1275], constants.PRECOS_CASAS["Verde"], "Verde"),
            EspacoAcao("Community Chest", "sorte", 50),
            Propriedade("Kenrick Lounge", "terreno", 320, [28, 150, 450, 1000, 1200, 1400], constants.PRECOS_CASAS["Verde"], "Verde"),
            Propriedade("Sisters' Car", "estacao", 200, [25, 50, 100, 200], 0, "Branco"),
            EspacoAcao("Chance", "sorte", 100),
            Propriedade("St. Joseph Chapel", "terreno", 350, [35, 175, 500, 1100, 1300, 1500], constants.PRECOS_CASAS["Azul Escuro"], "Azul Escuro"),
            EspacoAcao("Room and Board", "imposto", 75),
            Propriedade("The Tower", "terreno", 400, [50, 200, 600, 1400, 1700, 2000], constants.PRECOS_CASAS["Azul Escuro"], "Azul Escuro")
        ]

    def rodar(self):
        """Inicia e mantém o loop principal do jogo."""
        while True:
            if self.game_state == 'MENU':
                self._rodar_menu()
            elif self.game_state == 'JOGANDO':
                self._rodar_jogo()
            elif self.game_state == 'GERENCIAR':
                self._rodar_gerenciar()
            elif self.game_state == 'TROCAR':
                self._rodar_troca()
            
            self.clock.tick(60)

    def _rodar_menu(self):
        """Executa a lógica e a renderização do menu principal."""
        mouse_pos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.finalizar()
            
            for i in range(self.num_jogadores_humanos):
                self.caixas_nome[i].handle_event(event)

            if event.type == pygame.MOUSEBUTTONDOWN:
                for i, botao in enumerate(self.botoes_num_jogadores):
                    if botao.foi_clicado(mouse_pos):
                        self.num_jogadores_humanos = i + 1
                
                if self.botao_iniciar.foi_clicado(mouse_pos):
                    nomes = [self.caixas_nome[i].get_text() for i in range(self.num_jogadores_humanos)]
                    self._iniciar_jogo(nomes)
        
        self._desenhar_menu(mouse_pos)

    def _iniciar_jogo(self, nomes_jogadores):
        """Configura o estado inicial do jogo e transita do menu para o jogo."""
        self.setup_jogadores(nomes_jogadores)
        log_largura = constants.LARGURA_TELA - (constants.LADO_MAXIMO_TABULEIRO + 80)
        self.log = Log(constants.LADO_MAXIMO_TABULEIRO + 60, 470, log_largura, 160)
        self.log.adicionar("Bem-vindo ao Seminopoly!")
        self.log.adicionar(f"Ordem: {', '.join([j.nome for j in self.jogadores])}")
        
        self.botoes_jogo['trocar'] = Botao(constants.LADO_MAXIMO_TABULEIRO + 20, 640, 120, 50, "Trocar", constants.CINZA, (150, 150, 150))
        self.botoes_jogo['gerenciar'] = Botao(constants.LADO_MAXIMO_TABULEIRO + 150, 640, 120, 50, "Gerenciar", constants.CINZA, (150, 150, 150))
        self.botoes_jogo['rolar'] = Botao(constants.LADO_MAXIMO_TABULEIRO + 280, 640, 140, 50, "Rolar Dados", constants.VERDE, (0, 200, 0))

        self.popup_compra = Popup("", "")
        self.estado_turno = 'ESPERANDO_ROLAGEM'
        self.game_state = 'JOGANDO'

    def _rodar_jogo(self):
        """Executa a lógica e a renderização de um turno de jogo."""
        mouse_pos = pygame.mouse.get_pos()
        jogador_atual = self.jogadores[self.jogador_da_vez_idx]

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.finalizar()
            if self.log.handle_mouse_event(event, mouse_pos):
                continue
            self._handle_eventos_jogo(event, mouse_pos, jogador_atual)

        if not self.popup_compra.ativo and jogador_atual.is_ai and self.estado_turno != 'FIM_DE_JOGO':
            self._executar_turno_ia(jogador_atual)

        if self.estado_turno != 'FIM_DE_JOGO':
            self._checar_falencias()

        self._desenhar_jogo(mouse_pos)

    def _rodar_gerenciar(self):
        """Executa a lógica do menu de gerenciamento."""
        mouse_pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT: self.finalizar()
            if self.log.handle_mouse_event(event, mouse_pos): continue
            
            if self.menu_gerenciamento:
                acao = self.menu_gerenciamento.handle_event(event)
                if acao == 'VOLTAR':
                    self.game_state = 'JOGANDO'
                    self.menu_gerenciamento = None
        
        self._desenhar_jogo(mouse_pos)

    def _rodar_troca(self):
        """Executa a lógica do menu de troca."""
        mouse_pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT: self.finalizar()
            if self.log.handle_mouse_event(event, mouse_pos): continue

            if self.menu_troca:
                res = self.menu_troca.handle_event(event)
                if res == 'FECHAR':
                    self.game_state = 'JOGANDO'
                    self.menu_troca = None
        
        self._desenhar_jogo(mouse_pos)

    def _handle_eventos_jogo(self, event, mouse_pos, jogador_atual):
        """Processa cliques de mouse durante o jogo."""
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Botões de Ação (Gerenciar, Trocar)
            if self.estado_turno == 'ESPERANDO_ROLAGEM' and not jogador_atual.is_ai:
                if self.botoes_jogo['gerenciar'].foi_clicado(mouse_pos):
                    self.menu_gerenciamento = MenuGerenciar(jogador_atual, self.log)
                    self.game_state = 'GERENCIAR'
                    return
                
                if self.botoes_jogo['trocar'].foi_clicado(mouse_pos):
                    oponentes = [j for j in self.jogadores if j != jogador_atual and not j.checar_falencia()]
                    if oponentes:
                        self.menu_troca = MenuTroca(jogador_atual, oponentes, self.log)
                        self.game_state = 'TROCAR'
                    else:
                        self.log.adicionar("Nenhum jogador disponível para trocar.")
                    return

            # Ação de rolar os dados
            if self.estado_turno == 'ESPERANDO_ROLAGEM' and not jogador_atual.is_ai and self.botoes_jogo['rolar'].foi_clicado(mouse_pos):
                self._executar_turno_humano(jogador_atual)
            # Ação do pop-up de compra
            elif self.estado_turno == 'ACAO' and self.popup_compra.ativo:
                self._resolver_compra(jogador_atual, mouse_pos)

    def _executar_turno_humano(self, jogador_atual):
        """Lógica para o turno de um jogador humano."""
        self.log.adicionar("="*10)
        self.log.adicionar(f"Turno de {jogador_atual.nome}...")

        if jogador_atual.esta_preso:
            saiu, dados_rolados = jogador_atual.tentar_sair_da_prisao(self.log)
            self.dados = dados_rolados
            if not saiu or (saiu and dados_rolados[0] != dados_rolados[1]):
                self.proximo_jogador()
        else:
            self.dados = jogador_atual.rolar_dados()
            self.log.adicionar(f"{jogador_atual.nome} rolou {sum(self.dados)}.")
            if jogador_atual.mover(sum(self.dados), len(self.tabuleiro_casas)):
                self.log.adicionar("Passou pelo início, +$200!")
            
            casa_atual = self.tabuleiro_casas[jogador_atual.posicao]
            casa_atual.acao(jogador_atual, self, sum(self.dados), self.log)

            if isinstance(casa_atual, Propriedade) and casa_atual.dono is None and jogador_atual.dinheiro >= casa_atual.preco:
                self.popup_compra.ativar("Comprar Propriedade", f"{casa_atual.nome} - ${casa_atual.preco}?")
                self.estado_turno = 'ACAO'
            else:
                if self.dados[0] != self.dados[1]:
                    self.proximo_jogador()
                else:
                    self.log.adicionar("Dados iguais! Jogue novamente.")

    def _executar_turno_ia(self, jogador_atual):
        """Lógica para o turno de um jogador IA."""
        pygame.time.wait(1000)
        self.log.adicionar("="*10)
        self.log.adicionar(f"Turno de {jogador_atual.nome}...")

        # IA constrói casas se tiver monopólio
        jogador_atual.atualizar_monopolios()
        for cor in jogador_atual.monopolios:
            props_do_grupo = [p for p in jogador_atual.propriedades if p.cor == cor]
            min_casas = min(p.num_casas for p in props_do_grupo)
            for p in props_do_grupo:
                if p.num_casas == min_casas and jogador_atual.dinheiro > p.preco_casa * 2 and p.num_casas < 5:
                    jogador_atual.dinheiro -= p.preco_casa
                    p.num_casas += 1
                    self.log.adicionar(f"[IA] Construiu casa em {p.nome}.")

        if jogador_atual.esta_preso:
            saiu, dados_rolados = jogador_atual.tentar_sair_da_prisao(self.log)
            self.dados = dados_rolados
            if not saiu or (saiu and dados_rolados[0] != dados_rolados[1]):
                self.proximo_jogador()
                return

        if not jogador_atual.esta_preso:
            self.dados = jogador_atual.rolar_dados()
            self.log.adicionar(f"{jogador_atual.nome} rolou {sum(self.dados)}.")
            if jogador_atual.mover(sum(self.dados), len(self.tabuleiro_casas)):
                self.log.adicionar("Passou pelo início, +$200!")
            
            casa_atual = self.tabuleiro_casas[jogador_atual.posicao]
            casa_atual.acao(jogador_atual, self, sum(self.dados), self.log)

            # Lógica de decisão de compra da IA
            if isinstance(casa_atual, Propriedade) and not casa_atual.dono and jogador_atual.dinheiro > casa_atual.preco * 1.5:
                jogador_atual.comprar_propriedade(casa_atual)
                self.log.adicionar(f"[IA] {jogador_atual.nome} comprou {casa_atual.nome}.")

        if self.dados[0] != self.dados[1]:
            self.proximo_jogador()
        else:
            self.log.adicionar("Dados iguais! PC joga novamente.")

    def _resolver_compra(self, jogador_atual, mouse_pos):
        """Processa a decisão do jogador no pop-up de compra."""
        casa_para_comprar = self.tabuleiro_casas[jogador_atual.posicao]
        if isinstance(casa_para_comprar, Propriedade):
            if self.popup_compra.bs.foi_clicado(mouse_pos):
                if jogador_atual.comprar_propriedade(casa_para_comprar):
                    self.log.adicionar(f"Comprou {casa_para_comprar.nome}.")
                else:
                    self.log.adicionar("Dinheiro insuficiente.")
            elif self.popup_compra.bn.foi_clicado(mouse_pos):
                self.log.adicionar("Não comprou a propriedade.")
        
        self.popup_compra.ativo = False
        self.estado_turno = 'ESPERANDO_ROLAGEM'
        if self.dados[0] != self.dados[1]:
            self.proximo_jogador()

    def _checar_falencias(self):
        """Verifica se algum jogador faliu e o remove do jogo."""
        jogadores_ativos = [j for j in self.jogadores if not j.checar_falencia()]
        if len(jogadores_ativos) < len(self.jogadores):
            jogadores_falidos = set(self.jogadores) - set(jogadores_ativos)
            for j in jogadores_falidos:
                self.log.adicionar(f"!!! {j.nome} faliu e está fora do jogo !!!")
                # Libera as propriedades do jogador falido
                for prop in j.propriedades:
                    prop.dono = None
                    prop.num_casas = 0
                    prop.hipotecada = False
            self.jogadores = jogadores_ativos
            # Garante que o índice do jogador da vez seja válido
            self.jogador_da_vez_idx %= len(self.jogadores) if self.jogadores else 0
        
        if len(self.jogadores) <= 1:
            vencedor = self.jogadores[0].nome if self.jogadores else "Ninguém"
            self.log.adicionar("="*20)
            self.log.adicionar(f"FIM DE JOGO! VENCEDOR: {vencedor}")
            self.estado_turno = 'FIM_DE_JOGO'
            self.game_state = 'FIM_DE_JOGO'

    def _desenhar_menu(self, mouse_pos):
        """Desenha a tela do menu principal."""
        self.tela.fill(constants.FUNDO_ESCURO)
        titulo_surf = constants.FONTE_MENU_TITULO.render("Seminopoly", True, constants.BRANCO)
        self.tela.blit(titulo_surf, titulo_surf.get_rect(center=(constants.LARGURA_TELA/2, 100)))
        
        label_qntd = constants.FONTE_TITULO.render("Jogadores Humanos:", True, constants.BRANCO)
        self.tela.blit(label_qntd, label_qntd.get_rect(center=(constants.LARGURA_TELA/2, 210)))
        
        for i, botao in enumerate(self.botoes_num_jogadores):
            cor_normal = constants.VERDE if (i+1 == self.num_jogadores_humanos) else constants.CINZA
            botao.cor = cor_normal
            botao.desenhar(self.tela, mouse_pos)
        
        for i in range(self.num_jogadores_humanos):
            self.tela.blit(self.labels_nome[i], (self.caixas_nome[i].rect.x - 120, self.caixas_nome[i].rect.y + 5))
            self.caixas_nome[i].draw(self.tela)
        
        self.botao_iniciar.desenhar(self.tela, mouse_pos)
        pygame.display.flip()

    def _desenhar_jogo(self, mouse_pos):
        """Desenha todos os elementos da cena principal do jogo."""
        self.tela.fill(constants.FUNDO_ESCURO)
        self.tabuleiro_visual.desenhar(self.tela)
        desenhar_painel_info(self.tela, self, self.log)
        
        for btn in self.botoes_jogo.values():
            btn.desenhar(self.tela, mouse_pos)

        # Desenha indicadores de hipoteca e casas
        for i, espaco in enumerate(self.tabuleiro_casas):
            if isinstance(espaco, Propriedade):
                px, py = constants.POSICOES_PIXEL[i]
                if espaco.hipotecada:
                    pygame.draw.circle(self.tela, constants.VERMELHO, (int(px), int(py)), 7)
                if espaco.num_casas > 0:
                    cor_casa = constants.VERMELHO if espaco.num_casas == 5 else constants.VERDE
                    tamanho_casa = 15 if espaco.num_casas == 5 else 10
                    # Desenha 1-4 casas ou 1 hotel
                    if espaco.num_casas == 5:
                        pygame.draw.rect(self.tela, cor_casa, (px - 8, py - 30, tamanho_casa, tamanho_casa))
                    else:
                        for k in range(espaco.num_casas):
                            pygame.draw.rect(self.tela, cor_casa, (px + (k*12) - 24, py - 30, tamanho_casa, tamanho_casa))

        # Desenha os peões dos jogadores
        contagem_pos = {}
        for jogador in self.jogadores:
            pos_idx = jogador.posicao
            if pos_idx not in contagem_pos:
                contagem_pos[pos_idx] = 0
            
            offset = constants.OFFSET_JOGADOR[contagem_pos[pos_idx]]
            pos_pixel = constants.POSICOES_PIXEL[pos_idx]
            jogador.desenhar(self.tela, pos_pixel, offset)
            contagem_pos[pos_idx] += 1

        self.popup_compra.desenhar(self.tela, mouse_pos)
        
        # Desenha menus modais por cima de tudo
        if self.menu_gerenciamento:
            self.menu_gerenciamento.desenhar(self.tela, mouse_pos)
        if self.menu_troca:
            self.menu_troca.desenhar(self.tela, mouse_pos)

        pygame.display.flip()

    def finalizar(self):
        """Encerra o Pygame e fecha o jogo."""
        pygame.quit()
        sys.exit()
