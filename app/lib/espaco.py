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
    def __init__(self, nome, tipo, preco, alugueis, preco_casa, cor):
        super().__init__(nome)
        self.tipo = tipo
        self.preco = preco
        self.alugueis = alugueis
        self.preco_casa = preco_casa
        self.cor = cor
        self.dono = None
        self.num_casas = 0  # 0=sem casa, 1-4=casas, 5=hotel
        self.hipotecada = False

    def calcular_aluguel(self, rolagem_dados=0):
        """Calcula o valor do aluguel com base no tipo, dono, casas e hipoteca."""
        if not self.dono or self.hipotecada:
            return 0

        if self.tipo == 'terreno':
            aluguel_base = self.alugueis[self.num_casas]
            # Dobra o aluguel do terreno vazio se o dono tiver o monopólio
            if self.num_casas == 0 and self.dono.tem_monopolio(self.cor):
                return aluguel_base * 2
            return aluguel_base

        if self.tipo == 'estacao':
            # O aluguel depende do número de estações não hipotecadas
            num_estacoes = sum(1 for p in self.dono.propriedades if p.tipo == 'estacao' and not p.hipotecada)
            return self.alugueis[num_estacoes - 1] if num_estacoes > 0 else 0

        if self.tipo == 'companhia':
            # O aluguel é baseado na rolagem dos dados e no número de companhias
            num_companhias = sum(1 for p in self.dono.propriedades if p.tipo == 'companhia' and not p.hipotecada)
            multiplicador = self.alugueis[num_companhias - 1] if num_companhias > 0 else 0
            return rolagem_dados * multiplicador
        return 0

    def acao(self, jogador, jogo, rolagem_dados=0, log=None):
        """
        Define a ação ao parar em uma propriedade: pagar aluguel se tiver dono,
        ou oferecer a compra se não tiver.
        """
        super().acao(jogador, jogo, rolagem_dados, log)
        if self.dono and self.dono != jogador:
            if self.hipotecada:
                log.adicionar("Propriedade hipotecada. Sem aluguel.")
            else:
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
