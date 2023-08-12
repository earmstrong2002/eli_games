side_length = 3
blank = " "
board = [blank] * side_length**2
reg_indices = (
    (0, 1, 2),
    (3, 4, 5),
    (6, 7, 8),
    (0, 3, 6),
    (1, 4, 7),
    (2, 5, 8),
    (0, 4, 8),
    (0, 2, 4),
)
corner_indices = (0, 2, 6, 8)
X = "X"
O = "O"
players = (X, O)
