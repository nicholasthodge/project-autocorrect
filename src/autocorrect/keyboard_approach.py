# Dictionary for Keyboard Cartesian Coordinates
# Credit: https://replit.com/@marmeladze1/Cartesian-QWERTY?v=1
keyboard_cartesian = {
    'q': {'y': 0, 'x': 0},
    'w': {'y': 0, 'x': 1},
    'e': {'y': 0, 'x': 2},
    'r': {'y': 0, 'x': 3},
    't': {'y': 0, 'x': 4},
    'y': {'y': 0, 'x': 5},
    'u': {'y': 0, 'x': 6},
    'i': {'y': 0, 'x': 7},
    'o': {'y': 0, 'x': 8},
    'p': {'y': 0, 'x': 9},

    'a': {'y': 1, 'x': 0},
    's': {'y': 1, 'x': 1},
    'd': {'y': 1, 'x': 2},
    'f': {'y': 1, 'x': 3},
    'g': {'y': 1, 'x': 4},
    'h': {'y': 1, 'x': 5},
    'j': {'y': 1, 'x': 6},
    'k': {'y': 1, 'x': 7},
    'l': {'y': 1, 'x': 8},

    'z': {'y': 2, 'x': 0},
    'x': {'y': 2, 'x': 1},
    'c': {'y': 2, 'x': 2},
    'v': {'y': 2,  'x': 3},
    'b': {'y': 2, 'x': 4},
    'n': {'y': 2, 'x': 5},
    'm': {'y': 2, 'x': 6},

    # Add the top row keys (optional)
    '1': {'y': 3, 'x': 0},
    '2': {'y': 3, 'x': 1},
    '3': {'y': 3, 'x': 2},
    '4': {'y': 3, 'x': 3},
    '5': {'y': 3, 'x': 4},
    '6': {'y': 3, 'x': 5},
    '7': {'y': 3, 'x': 6},
    '8': {'y': 3, 'x': 7},
    '9': {'y': 3, 'x': 8},
    '0': {'y': 3, 'x': 9},

    # Add special characters (optional)
    # You can define positions for symbols like #'-', '=', '[', ']', etc. based on your specific needs.
}


# Function to return distance of keys on keyboard - given in Chebyshev (chessboard) distance
def keyboard_distance(char1, char2):
    # Given char1, char2, we can find the distance using the keyboard_cartesian dict (provided in this file)
    # Get char1 coordinates
    char1_coord = keyboard_cartesian[char1]
    char1_y = char1_coord['y']
    char1_x = char1_coord['x']

    # Get char2 coordinates
    char2_coord = keyboard_cartesian[char2]
    char2_y = char2_coord['y']
    char2_x = char2_coord['x']

    # Return (|x1-x2| + |y1+y2|)
    return (abs(char1_x - char2_x) + abs(char1_y - char2_y))


# Driver area

# Example
print(keyboard_distance('q', 'm')) # Should print '8'