
BSIZ = 3  # Este número define el tamaño del tablero tablero, BSIZ x BSIZ

TOTAL_CASILLAS = BSIZ * BSIZ

# Cada jugador tendrá (N^2 - 1) / 2 piedras si ese valor es par
if (TOTAL_CASILLAS - 1) % 2 != 0:
	raise ValueError("(N^2 - 1) debe ser par; cambia BSIZ para que funcione")

ST_PLAYER = (TOTAL_CASILLAS - 1) // 2  # piedras por jugador

# Define the colors we will use in RGB format
BLACK =   (  0,   0,   0)
GRAY =    (150, 150, 150) 
WHITE =   (255, 255, 255)
# Chosen so that they are still friendly to colorblind people:
BLUISH =  ( 26, 133, 255)
REDDISH = (212,  17,  89)
PLAYER_COLOR = (BLUISH, REDDISH) 

# Define the game window width and height and the slot size and separation in pixels
SLOT = 100        # squares size
SEP = 20          # squares separation
ROOM = SLOT + SEP # extra room at sides 
HEIGHT = BSIZ * SLOT + (BSIZ + 1) * SEP + ROOM # room for 3 squares with margin and internal separators and extra below
WIDTH = HEIGHT + ROOM              # extra at both sides
RAD = SLOT / 3                     # circle radius

NO_PLAYER = -1

# Modo de juego: "default" (quien hace 3 en raya gana) o "misery" (quien hace 3 en raya pierde)
GAME_MODE = "castañas"