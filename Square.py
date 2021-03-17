from Bokstav import Bokstav

class Square:
    def __init__(self):
        VALUE_FILE = "values.txt"
        self.g_letters = {}
        self.is_set = set() # To hold characters that are definitely set in the polybius square

        # Each row/column has an initial metric of 0 which will be incremented by 1 for each letter on that row or column.
        self.row_metric = [0,0,0,0,0]
        self.column_metric = [0,0,0,0,0]

        self.r_letters = "abcdefghjklmnopqrstuvwxyz".upper()  # Note that 'i' is missing
        for letter in self.r_letters:
            self.g_letters[letter] = Bokstav(letter)

        """
        Reads the input which is all given letters in the polybiussquare. 
        The input will be formatted as "A=nt" where n,t are integers. 
        n represents the row and t represents the column in the polybiussquare. 
        """
        file = open(VALUE_FILE, "r")

        for row in file:
            letter, values = row.split("=")
            self.setval(letter, int(values[0]) - 1, int(values[1]) - 1) # -1 because the rows and columns should be represented as indexes in the given function call.

    def getLastpos(self):
        """
        If we have only one spot left in the square, and there is a letter where neither the row or column is set, we have to find what positions it can fit into.
        :return:
        """
        if self.row_metric.count(5) == 4 and self.column_metric.count(5) == 4: # We have only 1 spot left
            return self.row_metric.index(4), self.column_metric.index(4)
        else:
            return (-1, -1)

    def setval(self, character, row=-1, col=-1):
        """
        Sets a given letter on the virtual polybiussquare -
        in addition to incrementing the metrics for the row and column respectively.
        """
        if character in self.is_set:
            return 0 # Do nothing because this character is in the polybiussquare, definitively.

        if row != -1:
            self.g_letters[character].row = row
        if col != -1:
            self.g_letters[character].column = col

        if self.g_letters[character].row != "?" and self.g_letters[character].column != "?":
            self.is_set.add(character)  # Add to set to indicate the character is definitively set.
            self.row_metric[int(self.g_letters[character].row)] += 1
            self.column_metric[int(self.g_letters[character].column)] += 1

        if self.row_metric[row] > 5:
            print("Error, row metric exceeded 5.")
        if self.column_metric[col] > 5:
            print("Error, column metric exceeded 5.")

        return 0

    def getval(self, character):
        """
        :param character:  The character we want the row/col for
        :return: (row, column) for the character
        """

        return self.g_letters[character].row, self.g_letters[character].column

    def fill(self):
        """
        Name pending
        # TODO: Comment this
        returns True/False if it changes anything
        """
        freerows, freecolumns = self.returnones()  # Get what rows and columns that have one free spot respectively
        changed = False

        for row in freerows:
            # Get the column so we know exactly what spot
            spots = [False for _ in range(5)]

            for letter in self.g_letters.values():
                if letter.row == row and letter.column != "?":
                    spots[letter.column] = True
            col_spot = spots.index(False)  # There should now be only 1 index that is free

            for i, letter in enumerate(self.g_letters.values()):
                if letter.row == row and letter.column == "?":
                    self.setval(letter.letter, col=col_spot)
                    if col_spot in freecolumns:
                        freecolumns.remove(col_spot)
                    changed = True
                if letter.column == col_spot and letter.row == "?" and col_spot in freecolumns:
                    self.setval(letter.letter, row=row)
                    freecolumns.remove(col_spot)
                    changed = True

        for col in freecolumns:
            spots = [False for _ in range(5)]

            for letter in self.g_letters.values():
                if letter.column == col and letter.row != "?":
                    spots[letter.row] = True
            col_spot = spots.index(False)  # There should now be only 1 index that is free

            for i, letter in enumerate(self.g_letters.values()):
                if letter.column == col and letter.row == "?":
                    self.setval(letter.letter,row=col_spot)
                    if col_spot in freerows:
                        freerows.remove(col_spot)
                    changed = True
                    break
        return changed


    def returnones(self):
        """
        Returns a tuple (rows, columns) containing lists of all rows/columns where metric==4, i.e. only 1 free spot is left
        """
        rows = []
        for i, num in enumerate(self.row_metric):
            if num == 4:
                rows.append(i)

        columns = []
        for i, num in enumerate(self.column_metric):
            if num == 4:
                columns.append(i)

        return rows, columns