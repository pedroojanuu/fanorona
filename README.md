# Fanorona/Fanoron-Tsivy

Tópico 2B - Trabalho prático 1 - IA - Grupo A1_22

- Félix Martins, up202108837
- Pedro Lima, up202108806
- Pedro Januário, up202108768

## Instalação de dependências

O jogo requer a instalação das bibliotecas presentes no ficheiro `requirements.txt`. Tal pode ser feito através dos comandos:

>## Dependency installation
>The game requires the libraries inside the file `requirements.txt`. Their installation can be done through:



### Linux / macOS

```bash
python -m venv .venv        # Create a python virtual environment
source .venv/bin/activate   # Activate the virtual environment
pip install -r requirements.txt # Install the required libraries
```

### Windows

```bash
python -m venv .venv    # Create a python virtual environment
.venv\Scripts\activate  # Activate the virtual environment
pip install -r requirements.txt # Install the required libraries
```

Para desativar o "ambiente", basta correr o comando:
> To deactivate the environment, just run:
```bash
deactivate
```

## Execução

Basta correr o ficheiro ```game.py```, presente no diretório-raiz do projeto.

Para terminar a qualquer momento, basta premir a tecla ESC ou fechar a janela do pygame.

***

>## Execution
>- Just run the file ```game.py```, which is in the project's root directory.
>- To exit at any time, press the ESC key or close pygame window.



### Modos do jogo
Existem vários modos de jogo disponíveis, que podem ser escolhidos para as brancas ou pretas com qualquer combinação:

- Humano
- Aleatório
- Minimax Muito Fácil
    * Profundidade: 2
    * Heurísticas: [Vitória](./heuristics/win_heuristic.py) e [aproximação de peças](./heuristics/approximate_enemy_heuristic.py)
- Minimax Fácil
    * Profundidade: 2
    * Heurística: [Vitória](./heuristics/win_heuristic.py) e [contagem de peças](./heuristics/nr_pieces_heuristic.py)
- Minimax Defensivo Fácil
    * Profundidade: 2
    * Heurísticas: [Vitória](./heuristics/win_heuristic.py), [contagem de peças](./heuristics/nr_pieces_heuristic.py), [número de grupos](./heuristics/groups_heuristic.py), [número de peças adjacentes](./heuristics/adjacent_pieces_heuristic.py) e [controlo do centro](./heuristics/center_control_heuristic.py).
- Minimax Defensivo Difícil
    * Profundidade: 4
    * Heurísticas: [Vitória](./heuristics/win_heuristic.py), [contagem de peças](./heuristics/nr_pieces_heuristic.py), [número de grupos](./heuristics/groups_heuristic.py) e [controlo do centro](./heuristics/center_control_heuristic.py).
- Minimax Agressivo Fácil
    * Profundidade: 2
    * Heurísticas: [Vitória](./heuristics/win_heuristic.py), [contagem de peças](./heuristics/nr_pieces_heuristic.py) e [aproximação de peças]()
- Minimax Agressivo Difícil
    * Profundidade: 4
    * Heurísticas: [Vitória](./heuristics/win_heuristic.py), [contagem de peças](./heuristics/nr_pieces_heuristic.py) e [aproximação de peças](./heuristics/approximate_enemy_heuristic.py)
- MCTS (Monte Carlo Tree Search) Rápido
- MCTS (Monte Carlo Tree Search) Melhor
- MCTS (Monte Carlo Tree Search) Heurísticas

>### Game modes
>There are several game modes available, which can be chosen for white or black with any combination:
>
>- Human
>- Random
>- Minimax Very Easy
>    * Depth: 2
>    * Heuristics: [Win](./heuristics/win_heuristic.py) and [approximate pieces](./heuristics/approximate_enemy_heuristic.py)
>- Minimax Easy
>    * Depth: 2
>    * Heuristic: [Win](./heuristics/win_heuristic.py) and [count pieces](./heuristics/nr_pieces_heuristic.py)
>- Minimax Defensive Easy
>    * Depth: 2
>    * Heuristics: [Win](./heuristics/win_heuristic.py), [count pieces](./heuristics/nr_pieces_heuristic.py), [number of groups](./heuristics/groups_heuristic.py), [number of adjacent pieces](./heuristics/adjacent_pieces_heuristic.py) and [center control](./heuristics/center_control_heuristic.py).
>- Minimax Defensive Hard
>    * Depth: 4
>    * Heuristics: [Win](./heuristics/win_heuristic.py), [count pieces](./heuristics/nr_pieces_heuristic.py), [number of groups](./heuristics/groups_heuristic.py) and [center control](./heuristics/center_control_heuristic.py).
>- Minimax Aggressive Easy
>    * Depth: 2
>    * Heuristics: [Win](./heuristics/win_heuristic.py), [count pieces](./heuristics/nr_pieces_heuristic.py) and [approximate pieces]()
>- Minimax Aggressive Hard
>    * Depth: 4
>    * Heuristics: [Win](./heuristics/win_heuristic.py), [count pieces](./heuristics/nr_pieces_heuristic.py) and [approximate pieces](./heuristics/approximate_enemy_heuristic.py)
>- MCTS (Monte Carlo Tree Search) Quick
>- MCTS (Monte Carlo Tree Search) Better
>- MCTS (Monte Carlo Tree Search) Heuristics


***

Grupo A1_22, março de 2024
