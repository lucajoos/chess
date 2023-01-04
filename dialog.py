from tkinter.filedialog import asksaveasfile, askopenfilename

filetypes = [('FEN Files', '*.fen')]
def save(string):
    f = asksaveasfile(mode='w', defaultextension='.fen', filetypes=filetypes)
    if f is None:
        return
    f.write(string)
    f.close()

def load():
    return askopenfilename(
        title='Load File',
        initialdir='/',
        filetypes=filetypes)