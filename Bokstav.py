class Bokstav:
    def __init__(self, letter="?", row="?", column="?"):
        self.letter = letter
        self.row = row
        self.column = column

    def __eq__(self, other):
        return self.letter == other
