"""
Autor: Jose L Balcazar, ORCID 0000-0003-4248-4528 
Copyleft: MIT License (https://en.wikipedia.org/wiki/MIT_License)

Headers for functions in abstract board for simple tic-tac-toe-like games, 2021.
Intended for Grau en Intel-ligencia Artificial, Programacio i Algorismes 1.
I would prefer to do everything in terms of object-oriented programming though.
"""

# abs_board_h.py (o abs_board.py)

from constants import BSIZ, NO_PLAYER, ST_PLAYER

def set_board_up(stones_per_player=ST_PLAYER):
    # Tablero: NO_PLAYER = vacio, 0 jugador 0, 1 jugador 1
    board = []
    for i in range(BSIZ):
        fila = []
        for j in range(BSIZ):
            fila.append(NO_PLAYER)
        board.append(fila)

    winner = NO_PLAYER

    # Piedras de cada jugador: guardamos sus posiciones.
    # Si una piedra no está puesta: (-1, -1)
    stones0 = []
    stones1 = []
    for k in range(stones_per_player):
        stones0.append([-1, -1])
        stones1.append([-1, -1])

    curr_player = 0

    # En fase 1, "hay piedra seleccionada" siempre (la siguiente sin colocar)
    # En fase 2, se selecciona por coordenadas con select_st
    selected_player = 0
    selected_index = 0   # índice de piedra seleccionada dentro de stones0/stones1
    selected = True      # main_txt asume que ya hay una seleccionada al empezar

    placed_total = 0
    total_needed = 2 * stones_per_player

    # --------- funciones internas simples ---------

    def all_stones_played():
        return placed_total >= total_needed

    def in_bounds(i, j):
        return 0 <= i < BSIZ and 0 <= j < BSIZ

    def find_unplayed_index(p):
        # devuelve índice de una piedra sin colocar del jugador p, o -1 si no hay
        if p == 0:
            for idx in range(len(stones0)):
                if stones0[idx][0] == -1 and stones0[idx][1] == -1:
                    return idx
        else:
            for idx in range(len(stones1)):
                if stones1[idx][0] == -1 and stones1[idx][1] == -1:
                    return idx
        return -1

    def find_stone_at(p, i, j):
        # devuelve índice de la piedra del jugador p en (i,j), o -1
        if p == 0:
            for idx in range(len(stones0)):
                if stones0[idx][0] == i and stones0[idx][1] == j:
                    return idx
        else:
            for idx in range(len(stones1)):
                if stones1[idx][0] == i and stones1[idx][1] == j:
                    return idx
        return -1

    def check_end():
        nonlocal winner
        winner = NO_PLAYER
        # True si hay una fila/columna/diagonal completa del mismo jugador
        # filas
        for i in range(BSIZ):
            first = board[i][0]
            if first != NO_PLAYER:
                ok = True
                for j in range(BSIZ):
                    if board[i][j] != first:
                        ok = False
                if ok:
                    winner = first
                    return True

        # columnas
        for j in range(BSIZ):
            first = board[0][j]
            if first != NO_PLAYER:
                ok = True
                for i in range(BSIZ):
                    if board[i][j] != first:
                        ok = False
                if ok:
                    winner = first
                    return True

        # diagonal principal
        first = board[0][0]
        if first != NO_PLAYER:
            ok = True
            for k in range(BSIZ):
                if board[k][k] != first:
                    ok = False
            if ok:
                winner = first
                return True

        # diagonal secundaria
        first = board[0][BSIZ - 1]
        if first != NO_PLAYER:
            ok = True
            for k in range(BSIZ):
                if board[k][BSIZ - 1 - k] != first:
                    ok = False
            if ok:
                winner = first
                return True

        return False

    # Al empezar: jugador 0 tiene una piedra "seleccionada" para colocar
    selected_player = curr_player
    selected_index = find_unplayed_index(curr_player)

    # --------- API que usa el main ---------

    def stones():
        # devuelve lista de piedras ya colocadas (solo para compatibilidad)
        lista = []
        for idx in range(len(stones0)):
            if stones0[idx][0] != -1:
                lista.append([stones0[idx][0], stones0[idx][1], 0])
        for idx in range(len(stones1)):
            if stones1[idx][0] != -1:
                lista.append([stones1[idx][0], stones1[idx][1], 1])
        return lista

    def select_st(i, j):
        # Solo se usa en fase 2 (cuando todas las piedras están colocadas)
        nonlocal selected, selected_player, selected_index

        if not all_stones_played():
            return False

        if not in_bounds(i, j):
            return False

        if board[i][j] != curr_player:
            return False

        idx = find_stone_at(curr_player, i, j)
        if idx == -1:
            return False

        selected = True
        selected_player = curr_player
        selected_index = idx
        return True

    def move_st(i, j):
        nonlocal curr_player, selected, selected_player, selected_index, placed_total

        # Si no hay seleccion, no se puede mover
        if not selected:
            return False, curr_player, check_end()

        # destino válido y libre
        if (not in_bounds(i, j)) or board[i][j] != NO_PLAYER:
            # si no es válido, NO hacemos nada y mantenemos selección
            return True, curr_player, check_end()

        end_game = False

        # -------- FASE 1: COLOCAR --------
        if not all_stones_played():
            # colocamos la piedra seleccionada (es una piedra sin poner del jugador actual)
            if curr_player == 0:
                stones0[selected_index][0] = i
                stones0[selected_index][1] = j
            else:
                stones1[selected_index][0] = i
                stones1[selected_index][1] = j

            board[i][j] = curr_player
            placed_total = placed_total + 1

            end_game = check_end()

            # cambia turno
            curr_player = 1 - curr_player

            # si aún quedan piedras por colocar, preselecciona una sin colocar del nuevo jugador
            if not all_stones_played():
                selected_player = curr_player
                selected_index = find_unplayed_index(curr_player)
                selected = True
                return True, curr_player, end_game
            else:
                # empieza fase 2: hay que seleccionar manualmente
                selected = False
                return False, curr_player, end_game

        # -------- FASE 2: MOVER --------
        else:
            # mover una piedra ya puesta del jugador actual a (i,j)
            if selected_player != curr_player:
                # algo raro: no debería pasar
                return True, curr_player, check_end()

            if curr_player == 0:
                old_i = stones0[selected_index][0]
                old_j = stones0[selected_index][1]
                stones0[selected_index][0] = i
                stones0[selected_index][1] = j
            else:
                old_i = stones1[selected_index][0]
                old_j = stones1[selected_index][1]
                stones1[selected_index][0] = i
                stones1[selected_index][1] = j

            board[old_i][old_j] = NO_PLAYER
            board[i][j] = curr_player

            end_game = check_end()

            # después de mover, se deselecciona y cambia turno
            selected = False
            curr_player = 1 - curr_player

            return False, curr_player, end_game

    def draw_txt(end=False):
        # imprime tablero simple: . vacio, X jugador0, O jugador1
        print()
        for i in range(BSIZ):
            for j in range(BSIZ):
                if board[i][j] == NO_PLAYER:
                    print(".", end=" ")
                elif board[i][j] == 0:
                    print("X", end=" ")
                else:
                    print("O", end=" ")
            print()

        if not all_stones_played():
            print("Fase 1: colocar")
        else:
            print("Fase 2: mover")

        print("Turno jugador:", curr_player)
        if end:
            print(">>> FIN (hay 3 en raya)")

    def get_winner():
        return winner

    return stones, select_st, move_st, draw_txt, get_winner
