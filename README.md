# Monopoly Python

Uma implementação simples do jogo Monopoly em Python utilizando Pygame.

## Como Executar

Este projeto utiliza o `uv` como gerenciador de pacotes e ambientes virtuais. Certifique-se de que o `uv` está instalado em seu sistema.

1.  **Instale o `uv`:**
    Siga as instruções oficiais para instalar o `uv`: [https://github.com/astral-sh/uv](https://github.com/astral-sh/uv)

2.  **Crie um ambiente virtual:**
    O `uv` será utilizado para criar um ambiente virtual isolado para o projeto.
    ```bash
    uv venv
    ```

3.  **Instale as dependências:**
    O `uv` instalará as dependências definidas no arquivo `pyproject.toml`.
    ```bash
    uv pip install .
    ```

4.  **Execute o jogo:**
    Utilize o `uv run` para executar o script do jogo dentro do ambiente virtual gerenciado pelo `uv`.
    ```bash
    uv run python app/monopoly.py
    ```

## Documentação

A documentação do desenvolvimento do projeto pode ser encontrada no diretório `docs/`. Ela inclui detalhes sobre a arquitetura do código, como contribuir e outras informações relevantes.