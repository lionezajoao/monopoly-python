# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "pygame",
# ]
# ///
from lib.game import Jogo

if __name__ == "__main__":
    """Cria uma instância do jogo e o executa."""
    jogo = Jogo()
    jogo.rodar()
