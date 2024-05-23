import colors

# Window Settings
WIDTH = 750
HEIGHT = 750
COLOR = colors.BLACK
FPS = 60

# Player Settings
PLAYER_WIDTH = 10
PLAYER_HEIGHT = 75
PLAYER_MARGIN = 20
PLAYER_VEL = 10
PLAYER_COLOR = colors.RED
PLAYER_COMPUTER_DIFFICULTY = 4 # The Higher the number, the easier the computer is

# Ball Settings
BALL_RADIUS = 5
BALL_COLOR = colors.WHITE
BALL_VELS = {
    'straight': {'x': 10, 'y': 0},
    'slant_max': {'x': 8, 'y': 6},
    'slant_min': {'x': 9, 'y': 4},
}

# Score Font Settings
SCORE_FONT_NAME = 'Press-Start-2P'
SCORE_FONT_SIZE = 30
SCORE_FONT_X_MARGIN = 5
SCORE_FONT_Y_MARGIN = 5
SCORE_FONT_COLOR = colors.WHITE

# Winner Font Settings
WINNER_FONT_NAME = 'Press-Start-2P'
WINNER_FONT_SIZE = 60
WINNER_FONT_COLOR = colors.WHITE

# Button Font Settings
BUTTON_FONT_NAME = 'Press-Start-2P'
BUTTON_FONT_SIZE = 50
BUTTON_FONT_COLOR = colors.WHITE
BUTTON_FONT_HOVER_COLOR = colors.GREY

# Menu Font Settings
MENU_FONT_SIZE = 60
MENU_FONT_COLOR = colors.WHITE

# Landmark Settings
LANDMARK_COLOR = colors.BGR_RED
LANDMARK_RADIUS = 5