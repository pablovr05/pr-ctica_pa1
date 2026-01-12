"""
Author: Jose L Balcazar, ORCID 0000-0003-4248-4528 
Copyleft: MIT License (https://en.wikipedia.org/wiki/MIT_License)

Pygame-based handling of a simple tic-tac-toe-like board, 2021.
Intended for Grau en Intel-ligencia Artificial, Programacio i Algorismes 1.
"""

# Import library for game programming 
import pygame

# Import: colors BLACK, GRAY, WHITE, PLAYER_COLOR; 
#         board dimensions BSIZ, WIDTH, HEIGHT, SLOT, SEP, ROOM, RAD
from constants import *

# Initialize the game engine, indicate a caption and
# set the height and width of the screen.
pygame.init()
screen = pygame.display.set_mode( (WIDTH, HEIGHT) )
pygame.display.set_caption("A name here for your game")
clock = pygame.time.Clock()

# Import initialization of the separately programmed abstract board:
from abs_board_h import set_board_up

# Prepare board:
# this will set up all stones as unplayed, select a first stone to play,
# and obtain functions to handle them as follows:
#   the call stones() allows one to loop on all stones,
#   the call select_st(i, j) marks as selected the stone at these coordinates,
#   the call move_st(i, j) 
#     if the square at these coordinates is free, moves the selected  
#     stone there, changes player, unselects the stone and checks for 
#     end of game; otherwise, does nothing, leaving the stone selected;
#     returns: bool "stone still selected", next player (may be the same), 
#     and bool "end of game"
#   the call to draw_txt(end) prints a text-based version of the board
#   the call to get_winner() returns the player that has aligned three stones
stones, select_st, move_st, draw_txt, get_winner = set_board_up(ST_PLAYER)

# Grid:
def trans_coord(x, y):
    'translates pixel coordinates into board coordinates'
    return round((x - ROOM - SEP - 0.5*SLOT)/(SEP + SLOT)), round((y - SEP - 0.5*SLOT)/(SEP + SLOT))

def draw_square(screen, i, j):
    # Dibuja un cuadrado de la rejilla en (i,j)
    pygame.draw.polygon(screen, GRAY,
        ( (ROOM + SEP + i*(SLOT + SEP), SEP + j*(SLOT + SEP)),
          (ROOM + SEP + i*(SLOT + SEP) + SLOT, SEP + j*(SLOT + SEP)),
          (ROOM + SEP + i*(SLOT + SEP) + SLOT, SEP + j*(SLOT + SEP) + SLOT),
          (ROOM + SEP + i*(SLOT + SEP), SEP + j*(SLOT + SEP) + SLOT)
        ))

def draw_stone(screen, i, j, player):
    # Dibuja la ficha cruz (0) o círculo (1) en el centro de cada  casilla
    """Draw a cross for player 0 and a circle outline for player 1."""
    coordenada_x = ROOM + 0.5 * SEP + (i + 0.5) * (SLOT + SEP)
    coordenada_y = 0.5 * SEP + (j + 0.5) * (SLOT + SEP)
    color = PLAYER_COLOR[player]

    if player == 0:
        arm = int(RAD * 0.7)
        width = max(2, int(RAD * 0.2))
        pygame.draw.line(screen, color, (coordenada_x - arm, coordenada_y - arm), (coordenada_x + arm, coordenada_y + arm), width)
        pygame.draw.line(screen, color, (coordenada_x + arm, coordenada_y - arm), (coordenada_x - arm, coordenada_y + arm), width)
    else:
        pygame.draw.circle(screen, color, (coordenada_x, coordenada_y), RAD, width=max(2, int(RAD * 0.2)))

def draw_board(curr_player = 0, end = False, winner = None):
    # Redibuja la pantalla según el estado del juego
    'on fresh screen, draw grid, stones, player turn mark, then make it appear'
    if end:
        screen.fill(WHITE)
        message = "Juego terminado"
        if winner in (0, 1):
            final_winner = winner
            if GAME_MODE == "misery":
                final_winner = 1 - winner
                message = f"Jugador {final_winner + 1} ha ganado"
            else:
                message = f"Jugador {final_winner + 1} ha ganado"
        font = pygame.font.SysFont(None, 64)
        text = font.render(message, True, BLACK)
        text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        screen.blit(text, text_rect)
        pygame.display.flip()
        return

    screen.fill(WHITE)
    for i in range(BSIZ):
        for j in range(BSIZ):
            draw_square(screen, i, j)
    for s in stones():
        draw_stone(screen, *s)
    'colored rectangle indicates who plays next'
    pygame.draw.rect(screen, PLAYER_COLOR[curr_player], 
    (ROOM + SEP, BSIZ*(SEP + SLOT) + SEP, BSIZ*(SEP + SLOT) - SEP, SLOT)
    )
    pygame.display.flip()

# set_board_up() already selects a first stone; set curr_player to zero.
stone_selected = True
curr_player = 0

# Show grid and stones:
draw_board()

# Loop until the user clicks the close button.
done = False

# Play until game ends
end = False
winner = None

while not done:
    
    # This limits the while loop to a max of 10 times per second.
    # Leave this out and we will use all CPU we can.
    clock.tick(10)
    
    for event in pygame.event.get(): 
        "User did something"
        if event.type == pygame.QUIT:
            "User clicked 'close window', set flag to exit loop"
            done = True
        if event.type == pygame.MOUSEBUTTONDOWN and not end:
            "game is afoot and user clicked something"
            if stone_selected:
                "User should click on a free destination square, otherwise ignore event"
                stone_selected, curr_player, end = move_st(*trans_coord(*event.pos))
                winner = get_winner() if end else None
                draw_board(curr_player, end, winner)
            else:
                "User should click on a stone to select it"
                stone_selected = select_st(*trans_coord(*event.pos))

# Friendly finish-up:
pygame.quit()
