# colors.py

##################################################
### OPACITY IS NOT IMPLEMENTED IN THIS VERSION ###
##################################################

colors = {
    'red': {
        'light': (255, 102, 102),
        'dark': (204, 0, 0),
        'opaque': (255, 0, 0, 153)  # Opacità a 0.6 (255 * 0.6 ≈ 153)
    },
    'green': {
        'light': (102, 255, 102),
        'dark': (0, 204, 0),
        'opaque': (0, 255, 0, 153)  # Opacità a 0.6
    },
    'blue': {
        'light': (102, 102, 255),
        'dark': (0, 0, 204),
        'opaque': (0, 0, 255, 153)  # Opacità a 0.6
    },
    'yellow': {
        'light': (255, 255, 102),
        'dark': (204, 204, 0),
        'opaque': (255, 255, 0, 153)  # Opacità a 0.6
    },
    'cyan': {
        'light': (102, 255, 255),
        'dark': (0, 204, 204),
        'opaque': (0, 255, 255, 153)  # Opacità a 0.6
    },
    'magenta': {
        'light': (255, 102, 255),
        'dark': (204, 0, 204),
        'opaque': (255, 0, 255, 153)  # Opacità a 0.6
    },
    'gray': {
        'light': (200, 200, 200),
        'dark': (100, 100, 100),
        'opaque': (169, 169, 169, 153)  # Opacità a 0.6
    },
    'black': (0, 0, 0),
    'white': (255, 255, 255)
}