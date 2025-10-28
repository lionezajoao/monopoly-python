"""
Este módulo define a classe `Jogador`, que representa um jogador no jogo.

A classe encapsula todo o estado e comportamento de um jogador, incluindo:
- Dinheiro, posição no tabuleiro e propriedades.
- Estado de prisão (se está preso e por quantos turnos).
- Ações como rolar dados, mover-se, pagar aluguel, comprar propriedades
  e tentar sair da prisão.
- Distinção entre jogador humano e IA (Inteligência Artificial).
"""

import random
import pygame
from utils import constants

class Jogador:
    """Representa um jogador no jogo, com seus atributos e ações."""

    def __init__(self, nome, is_ai=False, cor=(255, 0, 0)):
        """
        Inicializa um jogador com nome, tipo (humano ou IA) e cor.
        """
        self.nome = nome
        self.is_ai = is_ai
        self.cor = cor
        self.dinheiro = 1500
        self.posicao = 0
        self.propriedades = []
        self.esta_preso = False
        self.turnos_na_prisao = 0

    def rolar_dados(self):
        """Simula a rolagem de dois dados de 6 lados."""
        return random.randint(1, 6), random.randint(1, 6)

    def mover(self, passos, tamanho_tabuleiro):
        """
        Move o jogador pelo tabuleiro.

        Retorna True se o jogador passou pelo ponto de partida (GO), False caso contrário.
        """
        posicao_antiga = self.posicao
        self.posicao = (self.posicao + passos) % tamanho_tabuleiro

        # Se a nova posição for menor que a antiga, o jogador completou uma volta
        if not self.esta_preso and self.posicao < posicao_antiga:
            self.dinheiro += 200
            return True  # Passou pelo início
        return False

    def pagar_aluguel(self, valor, dono):
        """Paga o aluguel a outro jogador."""
        self.dinheiro -= valor
        dono.dinheiro += valor

    def ir_para_prisao(self):
        """Move o jogador para a prisão."""
        self.posicao = constants.POSICAO_PRISAO_INDEX  # Posição da prisão no tabuleiro
        self.esta_preso = True
        self.turnos_na_prisao = 0

    def tentar_sair_da_prisao(self, log):
        """
        Tenta sair da prisão, seja pagando, rolando dados iguais ou após 3 turnos.

        Para IAs, a lógica é simplificada: pagar se tiver dinheiro.
        Retorna uma tupla (saiu_da_prisao, dados_rolados).
        """
        self.turnos_na_prisao += 1
        dado1, dado2 = self.rolar_dados()

        # Lógica de decisão da IA para sair da prisão
        if self.is_ai:
            if self.dinheiro > 50:
                self.dinheiro -= 50
                self.esta_preso = False
                log.adicionar(f"{self.nome} pagou $50 e saiu da prisão.")
                return True, (dado1, dado2)

        log.adicionar(f"{self.nome} rolou {dado1} e {dado2} para tentar sair.")

        # Condição 1: Rolar dados iguais
        if dado1 == dado2:
            self.esta_preso = False
            log.adicionar(f"{self.nome} tirou dados iguais e saiu da prisão!")
            return True, (dado1, dado2)

        # Condição 2: Pagar fiança após 3 turnos
        if self.turnos_na_prisao >= 3:
            self.dinheiro -= 50
            self.esta_preso = False
            log.adicionar(f"{self.nome} pagou $50 obrigatoriamente para sair.")
            return True, (dado1, dado2)

        log.adicionar(f"{self.nome} não conseguiu sair da prisão.")
        return False, (dado1, dado2)

    def comprar_propriedade(self, propriedade):
        """Tenta comprar uma propriedade se tiver dinheiro suficiente."""
        if self.dinheiro >= propriedade.preco:
            self.dinheiro -= propriedade.preco
            self.propriedades.append(propriedade)
            propriedade.dono = self
            return True
        return False

    def checar_falencia(self):
        """Verifica se o jogador faliu (dinheiro negativo)."""
        return self.dinheiro < 0

    def desenhar(self, tela, pos_pixel, offset):
        """Desenha o peão do jogador na tela com um deslocamento."""
        px, py = pos_pixel
        ox, oy = offset
        pygame.draw.circle(tela, self.cor, (px + ox, py + oy), 12)
        pygame.draw.circle(tela, constants.PRETO, (px + ox, py + oy), 12, 2)
