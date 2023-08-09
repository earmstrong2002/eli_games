class Player:
    """Represents player token.

    Params:
        symbol (str): One-character string which is drawn on the board.

    """

    def __init__(self, symbol: str) -> None:
        """Initializes Player object.

        Args:
            symbol (str): One-charcter string.

        Raises:
            TypeError: If given symbol is not a string
            ValueError: If given symbol is not length 1
        """
        # Validate preconditions.
        if type(symbol) != str:
            raise TypeError("Player symbol must be of type str.")
        if len(symbol) != 1:
            raise ValueError("Player symbol must be length 1.")
        # Assign class attributes
        self.symbol = symbol

    def __str__(self):
        """Returns a string representation of this Player object.

        Returns:
            str: String representation of this Player object.
        """
        return self.symbol

    def __repr__(self):
        """Returns unambiguous string representation of this Player object.

        Returns:
            str: Unambiguous string representation of this Player objoct.
        """
        return f"Player: symbol={self.symbol}"


class Board:
    """Stores a board state and contains methods for reading and modifying it.

    Params:
        state (list[list]): 2-D list, 3x3. Row-major order.
        Empty spot is represented by None.
        Spot can also be occupied by Player object.
        If anything else finds its way into the list, something has gone wrong.
    """

    def __init__(self, state: list[list]) -> None:
        """Initializes this Board object.

        Args:
            state (list[list]): 2-D list, 3x3. Row-major order.
            Empty spot is represented by None.
            Spot can also be occupied by Player object.
            If anything else finds its way into the list,
            something has gone wrong.
        """
        self.state = state

    def clear(self):  # TODO
        ...
