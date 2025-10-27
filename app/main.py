# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "pygame",
# ]
# ///

"""
Ponto de entrada principal para a aplicação do jogo Monopoly.

Este script inicializa e executa o jogo. Ele cria uma instância da classe `Jogo`,
que é responsável por toda a lógica e pelo loop principal, e então chama o método
`rodar()` para iniciar a aplicação.
"""

from lib.game import Jogo

if __name__ == "__main__":
    # Cria uma instância do jogo e inicia o loop principal
    jogo = Jogo()
    jogo.rodar()

