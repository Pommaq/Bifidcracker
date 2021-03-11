class Bokstav:
    def __init__(self, letter="?", row="?", column="?"):
        self.letter = letter
        self.row = row
        self.column = column

    def __eq__(self, other):
        return self.letter == other

    def change(self, index, val):
        if int(index) == 1:
            self.row = val
        else:
            self.column = val

    def getrow(self):
        return self.row

    def getcol(self):
        return self.column

    def getval(self, rc):
        if rc == 'r':
            return self.row
        else:
            return self.column

    def setval(self, rc, val):
        if rc == 'r':
            self.row = val
        else:
            self.column = val