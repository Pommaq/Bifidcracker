from Bokstav import *
from Square import *
"""
TODO: Add machine learning to the algorithm, where the bifidcracker will utilize a dictionary and make make guesses. 
After a guess is made, the algorithm will count character matches against the dictionary. 
The word with the most character matches will be selected, and the algorithm will adapt it's guesses accordingly. 

"""
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
        crypto_index = crypto_letter_index = 0
        for text_index in range(2):
            for i, letter in enumerate(text):
                newrule = letter.upper() + postfix[text_index] + "=" + crypto[crypto_letter_index] + postfix[crypto_index]
                if newrule not in rules:
                    rules.add(newrule)
                crypto_index = (crypto_index + 1) % 2
                if crypto_index == 0:
                    crypto_letter_index += 1
        return rules

    def checklast(self):

        pass

    def checkRelations(self):
        # Enforce the rules, format A1=B2
        changed = False
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
        return changed
    def conclusion(self):
        # Enforces rules and draws conclusions
        changed = True
        while changed:
            changed = False
            changed = changed | self.checkRelations() | self.polybius.fill() | self.checklast()


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
