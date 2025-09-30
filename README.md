# 🎲 Projeto Monopoly

![Linguagem](https://img.shields.io/badge/Linguagem-Python-blue)
![Status](https://img.shields.io/badge/Status-Em%20Desenvolvimento-yellow)
![Licença](https://img.shields.io/badge/Licença-MIT-green)

---

## 📖 Sobre o Projeto

Este repositório contém o desenvolvimento de uma versão digital do clássico jogo de tabuleiro Monopoly, aplicando conceitos de engenharia e gerenciamento de software.

> Este projeto foi desenvolvido para a disciplina de **Gerência de Projeto e Manutenção de Software** da **Universidade Federal Fluminense (UFF)**.

---

## ✨ Funcionalidades

* Tabuleiro digital e interativo
* Suporte para 2 a 4 jogadores em modo local (hot-seat)
* Lógica de compra, venda e aluguel de propriedades
* Sistema de turnos e rolagem de dados

---

## 💻 Tecnologias

* **Linguagem:** Python
* **Versionamento:** Git & GitHub
* **Gerenciamento:** Jira

---

## 👥 Equipe

* Alexandre Colmenero
* Breno de Carvalho
* Erivelton Campos
* Gabriel Pinho
* João Pedro Barboza
* Leonardo Lima

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

---

*Projeto desenvolvido para o semestre 2025.2*
