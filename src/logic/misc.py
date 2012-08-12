TARGETS = ['g', 'b', 'y', 'r']  # Tile.v

SNAKE_VALUES = ['G', 'B', 'Y', 'R', 'O', 'P']

colors = {
          "Y": (255, 255, 0),
          "G": (0, 255, 0),
          "B": (0,0,255),
          "R": (255,0,0),
          "O": (255,102,51),
          "P": (153,51,153),
          'g': (0,102,0),
          'b': (0,0,102),
          'y': (102,102,0),
          'r': (102,0,0),
          '0': (20,20,20),
          '1': (50,50,50)
          }
          
def letter_to_color(letter):
    global colors

    if letter not in colors:
        return (0,0,0)
    else:
        return colors[letter]