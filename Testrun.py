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
class Square:
    def __init__(self):
        VALUE_FILE = "values.txt"
        self.g_letters = {}
        self.is_set = set() # To hold characters that are definitely set in the polybius square

        # Each row/column has an initial metric of 0 which will be incremented by 1 for each letter on that row or column.
        self.row_metric = [0,0,0,0,0]
        self.column_metric = [0,0,0,0,0]

        r_letters = "abcdefghjklmnopqrstuvwxyzåäö".upper()  # Note that 'i' is missing
        for letter in r_letters:
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

class Bifidcracker:
    def __init__(self):

        self.g_rules = set()
        self.polybius = Square()
        INPUT_FILE = "input.txt"  # input file has the format 'PLAINTEXT#CRYPTOGRAM'
        # Create all empty letters
        # Read all given letters


        file = open(INPUT_FILE, "r")

        for row in file:
            plaintext, cryptogram = row.split("#")
            plaintext = plaintext.replace('i', 'j')
            cryptogram = cryptogram.replace('I', 'J')
            # Interpret rules
            self.g_rules |= self.interpret(plaintext, cryptogram)  # |= will merge the sets

    def print_square(self):
        polybius_rep = [["?" for x in range(5)] for y in range(5)]

        for letter in self.polybius.g_letters.values():

            # Makes sure that only definitive letters are placed
            if letter.row != "?" and letter.column != "?":
                polybius_rep[letter.row][letter.column] = letter.letter

        [print(row) for row in polybius_rep]


    def interpret(self, text, crypto):
        # Uses input to build rules TODO: Snygga till matematiken bakom
        #       T H E       TGR
        # Row:  1 ? 3
        # Col:  1 2 4
        # D=15, K=31, Z=24
        postfix = ["r", "c"]
        rules = set()
        crypto_index = 0
        crypto_letter_index = 0
        for text_index in range(2):
            for i, letter in enumerate(text):
                newrule = letter.upper() + postfix[text_index] + "=" + crypto[crypto_letter_index] + postfix[
                    crypto_index]
                if newrule not in rules:
                    rules.add(newrule)
                crypto_index = (crypto_index + 1) % 2
                if crypto_index == 0:
                    crypto_letter_index += 1
        return rules

    def conclusion(self):
        # Enforces rules and draws conclusions
        changed = True
        while changed:
            changed = False
            # Enforce the rules, format A1=B2
            for rule in self.g_rules:
                row1, col1 = self.polybius.getval(rule[0])
                row2, col2 = self.polybius.getval(rule[3])

                # Check for discrepancies:
                if rule[1] == 'r':
                    val1 = row1
                else:
                    val1 = col1
                if rule[4] == 'r':
                    val2 = row2
                else:
                    val2 = col2

                if val1 != "?" and val2 != "?":  # If both rows are set
                    if val1 != val2:  # Happens upon bad input
                        print("Discrepancy! Rule", rule, "is impossible")
                        return -1
                    else:
                        continue

                if val1 != "?" and val2 == "?":
                    if rule[4] == 'r':
                        self.polybius.setval(rule[3], row=val1)
                    else:
                        self.polybius.setval(rule[3], col=val1)
                    changed = True
                elif val1 == "?" and val2 != "?":
                    if rule[1] == 'r':
                        self.polybius.setval(rule[0], row=val2)
                    else:
                        self.polybius.setval(rule[0], col=val2)
                    changed = True
            changed = changed | self.polybius.fill()


def main():
    # Skapa alla tomma bokstäver
    # Läs in givna bokstäver
    # Ta in input->output från fil
    # Generera regler
    # Mata in regler samt enforce-a dom.
    # Försök dra slutsatser
    sys = Bifidcracker()
    sys.conclusion()
    sys.print_square()
    return 0


if __name__ == '__main__':
    main()
