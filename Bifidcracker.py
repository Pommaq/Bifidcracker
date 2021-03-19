from Bokstav import *
from Square import *
import random
import copy
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
        """
        Uses input to build rules
               T H E       TGR
         Row:  1 ? 3
         Col:  1 2 4
         D=15, K=31, Z=24
         """
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
        """
        Used for the special case when there is only one position left in the square and the last letter does not have row or column set.
        :return changed: 
        """
        row, column = self.polybius.getLastpos()
        if row != -1:
            emptyletter = "?"
            failed = False
            for letter in self.polybius.r_letters:
                tmp = self.polybius.g_letters[letter]
                if tmp.column == "?" or tmp.row == "?": # We know we will get here if there is only 1 spot left
                    emptyletter = tmp.letter
                    """
                    There is a special case during the guessing portion where there is a letter left and one attribute is set.
                    e.g. C=?3, and the last position is NOT on column 3 (Note: Without internal offset)
                    I am not sure how to handle that situation, so we'll simply accept it.
                    """

            if not failed:
                self.polybius.setval(emptyletter, row, column)
                return True
            else:
                return False
        return False

    def checkRelations(self, Silenced):
        # Enforce the rules, format A1=B2
        changed = 0
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
                    if not Silenced:
                        print("Discrepancy! Rule", rule, "is impossible. Check your input!")
                    return -1
                else:
                    continue

            if val1 != "?" and val2 == "?":
                if rule[4] == 'r':
                    self.polybius.setval(rule[3], row=val1)
                else:
                    self.polybius.setval(rule[3], col=val1)
                changed = 1
            elif val1 == "?" and val2 != "?":
                if rule[1] == 'r':
                    self.polybius.setval(rule[0], row=val2)
                else:
                    self.polybius.setval(rule[0], col=val2)
                changed = 1
        return changed

    def conclusion(self, silenced):
        # Enforces rules and draws conclusions
        changed = True
        while changed:
            relations = self.checkRelations(silenced)
            if relations == -1:
                return -1

            changed = relations | self.polybius.fill() | self.checklast()
        return 0

    def decrypt(self):
        """
        I believe the name speaks for itself.
        :return decrypted text:
        """
        CRYPTOGRAM_FILENAME = "cryptogram.txt"
        crypto_file = open(CRYPTOGRAM_FILENAME, "r")
        cryptogram = crypto_file.readline()

        pairs = "" 
        plaintext = ""

        for c in cryptogram:
            pairs += str(self.polybius.g_letters[c].row) + str(self.polybius.g_letters[c].column)  # make a str of all the 'pairs' as seen in the illustration below

        half = len(pairs)//2  # Will always work because we will always have an even number of 'pairs'.
        top = pairs[:half]
        bottom = pairs[half:]

        for x, y in zip(top, bottom):
            matched = False
            for bokstav in self.polybius.g_letters.values():
                    if x.isdigit() and y.isdigit():
                        if bokstav.row == int(x) and bokstav.column == int(y):
                            plaintext += bokstav.letter
                            matched = True
            if not matched:
                plaintext += "?"

        """
        In the example of cryptogram 'OLCOSZBQTXRF' and plaintext 'HAPPYNEWYEAR': 

                        H A P P Y N E W Y E A R <- Plaintext
                        1 3 5 5 4 3 1 3 4 1 3 2 <- Top 
                        2 3 2 2 2 1 4 5 2 4 3 4 <- Bottom
        
                        13 55 43 13 41 32 23 22 21 45 24 34 <- Referenced illustration of pairs
                        O  L  C  O  S  Z  B  Q  T  X  R  F
        
        """
        return plaintext, top, bottom

    def encrypt(self, cleartext):
        """
        Assumes the polybiussquare is complete.
        :param cleartext:
        :return:
        """
        cryptogram = ""

        top = ""
        bottom = ""

        for clear_letter in cleartext.upper():
            top += str(self.polybius.g_letters[clear_letter].row)
            bottom += str(self.polybius.g_letters[clear_letter].column)

        all = top + bottom

        while all != "":
            coords = all[:2]
            all = all[2:]

            for letter in self.polybius.g_letters.values():
                if letter.row == int(coords[0]) and letter.column == int(coords[1]):
                    cryptogram += letter.letter



        return cryptogram

    def print(self, plaintext, top, bottom):
        print("The plaintext is:", plaintext)
        print(" " * 17, top)
        print(" " * 17, bottom)

    def getfree(self):
        """
        Gets free coordinates and returns them in a list
        :param metrics:
        :return:
        """
        free = []
        for i in range(5):
            for k in range(5):
                found = False
                for letter in self.polybius.g_letters.values():
                    if letter.row == i and letter.column == k:
                        found = True
                if not found:
                    free.append((i, k))
        return free

    def guess(self):
        """
        Picks a letter and guesses its location in the polybiussquare.
        """
        # Get letters qualified for guessing, make a guess
        qualified = []
        for letter in self.polybius.g_letters.values():
            if letter.row == "?" or letter.column == "?":
                qualified.append(letter)
        if len(qualified) != 0:
            # Get free rows and columns
            freecoordinates = self.getfree()

            # Get a random letter, pick a random location.
            letter_index = random.randint(0, len(qualified) - 1)
            letter = qualified[letter_index]

            if letter.row == "?" and letter.column == "?":
                # Its completely unknown. Pick a spot through some algorithm.
                # Random?
                choice = random.choice(freecoordinates)
                self.polybius.setval(letter.letter, choice[0], choice[1])

            elif letter.row == "?" and letter.column != "?":
                # Find a free location with a matching column.
                for coordinate in freecoordinates:
                    if coordinate[1] == int(letter.column):
                        self.polybius.setval(letter.letter, row=coordinate[0])
            elif letter.row != "?" and letter.column == "?":
                # Find a free location with a matching row
                for coordinate in freecoordinates:
                    if coordinate[0] == int(letter.row):
                        self.polybius.setval(letter.letter, col=coordinate[1])
                        break


def guessing_game(cracker):
    """
    Responsible for making guesses and controlling if they're reasonable. Finishes once a reasonable key is found.
    :param cracker:
    :return:
    """
    plaintext, top, bottom = cracker.decrypt()
    if cracker.polybius.column_metric.count(5) != 5 or cracker.polybius.row_metric.count(5) != 5:
        backup = copy.deepcopy(cracker)  # Used upon failure
        success = False
        result = 0
        while not success:
            foundwords = False
            if "?" in plaintext:
                cracker.guess()
                result = cracker.conclusion(silenced=True)
            if result == -1: # Bad guess
                cracker = copy.deepcopy(backup)
                result = 0
                continue
            plaintext, top, bottom = cracker.decrypt()
            bad = False
            if "?" not in plaintext:
                for word in open("ordlista.txt"):
                    if word.upper().strip() in plaintext:
                        foundwords = True
                if foundwords:
                    # Success! Check so everything encrypts into what we expect
                    for row in open("input.txt"):
                        cleartext, cryptogram = row.split('#')
                        if cracker.encrypt(cleartext) != cryptogram.strip():
                            # Its a bad square.
                            bad = True
                    if not bad:
                        plaintext, top, bottom = cracker.decrypt()
                        return plaintext, top, bottom, cracker

            if not foundwords or bad:
                cracker = copy.deepcopy(backup)

    return plaintext, top, bottom, cracker


def main():
    sys = Bifidcracker()
    sys.conclusion(False)
    plaintext, top, bottom, sys = guessing_game(sys)
    sys.print_square()
    sys.print(plaintext, top, bottom)
    print("""Note: There is a chance this key is faulty (but happened to work on the given cryptograms)
So keep that in mind when using it. The chances of it being so can be decreased by giving the program more input.""")
    return 0


if __name__ == '__main__':
    main()
