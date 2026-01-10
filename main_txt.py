"""
Author: Jose L Balcazar, ORCID 0000-0003-4248-4528 
Copyleft: MIT License (https://en.wikipedia.org/wiki/MIT_License)

Text handling of a simple tic-tac-toe-like board, 2021.
Intended for Grau en Intel-ligencia Artificial, Programacio i Algorismes 1.
"""



"""
Author: Jose L Balcazar, ORCID 0000-0003-4248-4528 
Copyleft: MIT License (https://en.wikipedia.org/wiki/MIT_License)

Text handling of a simple tic-tac-toe-like board, 2021.
Intended for Grau en Intel-ligencia Artificial, Programacio i Algorismes 1.
"""

import os
from abs_board_h import set_board_up


def clear_console():
    # Limpia consola según sistema operativo
    if os.name == "nt":      # Windows
        os.system("cls")
    else:                    # Linux / macOS
        os.system("clear")


# Prepare board
stones, select_st, move_st, draw_txt = set_board_up()

# set_board_up() already selects a first stone
stone_selected = True

# Loop until game ends
end = False
clear_console()
draw_txt(False)

while not end:
    while not stone_selected:
        i, j = input("Select stone coordinates: ").split()
        stone_selected = select_st(int(i), int(j))
        clear_console()
        draw_txt(end)

    while stone_selected and not end:
        i, j = input("Select destination coordinates: ").split()
        stone_selected, curr_player, end = move_st(int(i), int(j))
        clear_console()
        draw_txt(end)

# Wait for the user to look at the screen before ending the program.
input("\nGame over. Press Enter to exit.")
