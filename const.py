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