directions = [
    (0, -1),
    (1, 0),
    (0, 1),
    (-1, 0)
]

def is_in_map(pos, m):
    col, row = pos
    if not (0 <= row < len(m)):
        return False
    if not (0 <= col < len(m[row])):
        return False
    return True