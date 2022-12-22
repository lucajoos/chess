WIDTH = 800
HEIGHT = 800

ROWS = 8
COLS = 8
SQUARE_SIZE = WIDTH // COLS

INITIAL_FEN = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1'

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
    'SQUARE_LIGHT_ACCENT': '#D6D6BD',
    'SQUARE_DARK_ACCENT': '#69874E',
    'SQUARE_LIGHT_HIGHLIGHT_DEFAULT': '#F6F686',
    'SQUARE_DARK_HIGHLIGHT_DEFAULT': '#BACB41',
    'SQUARE_LIGHT_HIGHLIGHT_ACCENT': '#DDDD79',
    'SQUARE_DARK_HIGHLIGHT_ACCENT': '#A7B53B',
    'SQUARE_LIGHT_BORDER': '#F9F9EF',
    'SQUARE_DARK_BORDER': '#CFDAC4',
    'SQUARE_LIGHT_HIGHLIGHT_BORDER': '#FCFCD5',
    'SQUARE_DARK_HIGHLIGHT_BORDER': '#FCFCD5'
}
