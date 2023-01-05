ENVIRONMENT = 'production'
VERSION = '1.0.0'

ID = f'lucajoos.chess.{VERSION}'

ICON_SMALL = 'assets/images/icon_small.png'
ICON = 'assets/images/icon.png'

BOARD_WIDTH = 600
BOARD_HEIGHT = 600
MENU_HEIGHT = 75

SCREEN_WIDTH = BOARD_WIDTH
SCREEN_HEIGHT = BOARD_HEIGHT + MENU_HEIGHT * 2

BOARD_ROWS = 8
BOARD_COLS = 8
SQUARE_SIZE = BOARD_WIDTH // BOARD_COLS

STARTING_FEN = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1'
DEFAULT_FEN = STARTING_FEN

PIECES = ['p', 'n', 'b', 'r', 'q', 'k']

PIECE_VALUES = {
    'p': 1.0,
    'n': 3.0,
    'b': 3.001,
    'r': 5.0,
    'q': 9.0,
    'k': 10000.0
}

COLORS = {
    'SQUARE_LIGHT_DEFAULT': '#EEEED2',
    'SQUARE_DARK_DEFAULT': '#759656',
    'SQUARE_LIGHT_HIGHLIGHT_DEFAULT': '#F6F686',
    'SQUARE_DARK_HIGHLIGHT_DEFAULT': '#BACB41',
    
    'SQUARE_LIGHT_ACCENT': '#D6D6BD',
    'SQUARE_DARK_ACCENT': '#69874E',
    'SQUARE_LIGHT_HIGHLIGHT_ACCENT': '#DDDD79',
    'SQUARE_DARK_HIGHLIGHT_ACCENT': '#A7B53B',
    
    'SQUARE_LIGHT_BORDER': '#F9F9EF',
    'SQUARE_DARK_BORDER': '#CFDAC4',
    'SQUARE_LIGHT_HIGHLIGHT_BORDER': '#FCFCD5',
    'SQUARE_DARK_HIGHLIGHT_BORDER': '#FCFCD5',
    
    'SQUARE_LIGHT_THREAT': '#EE7F6B',
    'SQUARE_DARK_THREAT': '#D66D52',
    'SQUARE_LIGHT_HIGHLIGHT_THREAT': '#EE7F6B',
    'SQUARE_DARK_HIGHLIGHT_THREAT': '#D66D52',

    'MENU': '#302E2B',

    'FONT_PRIMARY': '#FFFFFF',
    'FONT_SECONDARY': '#474542',
    'FONT_HOVER': '#63605b',
    'FONT_LIGHT': '#989795'
}
