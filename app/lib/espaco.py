"""
Este módulo define as diferentes tipos de espaços (casas) no tabuleiro do jogo.

- `Espaco`: Classe base para qualquer casa no tabuleiro.
- `Propriedade`: Representa uma propriedade que pode ser comprada, como terrenos,
  estações ou companhias. Contém lógica para calcular aluguel.
- `EspacoAcao`: Representa uma casa que dispara uma ação, como pagar impostos,
  receber dinheiro (sorte) ou ir para a prisão.
"""

class Espaco:
    """Classe base para um espaço no tabuleiro."""
    def __init__(self, nome):
        self.nome = nome

    def acao(self, jogador, jogo, rolagem_dados=0, log=None):
        """Ação padrão ao parar em um espaço. Apenas anuncia a parada."""
        if log:
            log.adicionar(f"{jogador.nome} parou em '{self.nome}'.")

class Propriedade(Espaco):
    """Representa uma propriedade que pode ser comprada e ter aluguel."""
    def __init__(self, nome, tipo, preco, aluguel_base, cor):
        super().__init__(nome)
        self.tipo = tipo
        self.preco = preco
        self.aluguel_base = aluguel_base
        self.cor = cor
        self.dono = None

    def calcular_aluguel(self, rolagem_dados=0):
        """Calcula o valor do aluguel com base no tipo e no dono."""
        if not self.dono:
            return 0
        if self.tipo == 'terreno':
            return self.aluguel_base
        if self.tipo == 'estacao':
            # O aluguel dobra para cada estação que o dono possui
            num_estacoes = sum(1 for p in self.dono.propriedades if p.tipo == 'estacao')
            return 25 * (2 ** (num_estacoes - 1))
        if self.tipo == 'companhia':
            # O aluguel é baseado na rolagem dos dados
            num_companhias = sum(1 for p in self.dono.propriedades if p.tipo == 'companhia')
            multiplicador = 10 if num_companhias == 2 else 4
            return rolagem_dados * multiplicador
        return 0

    def acao(self, jogador, jogo, rolagem_dados=0, log=None):
        """
        Define a ação ao parar em uma propriedade: pagar aluguel se tiver dono,
        ou oferecer a compra se não tiver.
        """
        super().acao(jogador, jogo, rolagem_dados, log)
        if self.dono and self.dono != jogador:
            aluguel = self.calcular_aluguel(rolagem_dados)
            log.adicionar(f"Propriedade de {self.dono.nome}. Pagar aluguel de ${aluguel}.")
            jogador.pagar_aluguel(aluguel, self.dono)

class EspacoAcao(Espaco):
    """Representa um espaço que dispara uma ação específica (imposto, sorte, etc.)."""
    def __init__(self, nome, tipo_acao, valor=0):
        super().__init__(nome)
        self.tipo_acao = tipo_acao
        self.valor = valor

    def acao(self, jogador, jogo, rolagem_dados=0, log=None):
        """Executa a ação correspondente ao tipo do espaço."""
        super().acao(jogador, jogo, rolagem_dados, log)
        if self.tipo_acao == 'imposto':
            log.adicionar(f"Você deve pagar imposto de ${self.valor}.")
            jogador.dinheiro -= self.valor
        elif self.tipo_acao == 'sorte':
            log.adicionar(f"Sorte! Você ganhou ${self.valor}!")
            jogador.dinheiro += self.valor
        elif self.tipo_acao == 'prisao':
            log.adicionar("👮 Vá para a prisão!")
            jogador.ir_para_prisao()
