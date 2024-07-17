import random

## Main function
def main():
    game = PokerFinal()
    game.createHand()

    ## Introducing rules and dropping menu
    print("\nWelcome to Cline Poker!")
    print("\nThe rules are simple.\n1) The game is 5-card-draw, single-discard style.")
    print("2) No antes or blinds, this is single-player.\n3) Winning hands: Flush (any kind), Full House, Straight, 3-or-4-of-a-kind, and pairs.")

    while True:
        print("\nMenu:\n1: Show hand\n2: Discard/draw cards\n3: New game\n4: Exit")
        choice = input("Enter option: ")

        ## printing hand
        if choice == "1":
            game.printHand()

        ## Discard mechanism
        elif choice == "2":
            discard = int(input("How many cards do you wish to discard? "))
            if discard > 0:
                indices = []
                for i in range(discard):
                    index = int(input("Enter the index of the card to discard (1 through 5): ")) - 1
                    indices.append(index)
                game.dropAndDrawMech(indices)

                game.printHand()
                print("\n")
                game.printWinnings()
                print("\nStarting a new game!\n")
                game.resetDeck()
                game.createHand()

            else:
                print("None discarded.\n")
                game.printWinnings()
                print("\nStarting a new game!\n")
                game.resetDeck()
                game.createHand()

        ## New game
        elif choice == "3":
            game.resetDeck()
            game.createHand()
            game.printHand()

        ## Exiting
        elif choice == "4":
            print("Thank you for playing CS 50 Poker!")
            break

        ## Handling invalid input
        else:
            print("Silly you! Please enter a valid option.")

## Defining a class to create a card
class Card:
    ## Initializing the parameters of a card
    def __init__(self, suit, rank):
        self.rank = rank
        self.suit = suit
        self.statOne = self.cardEmpirics()

    ## Method to return suit of card
    def getSuit(self):
        return self.suit

    ## Method to return rank of card
    def getRank(self):
        return self.rank

    ## Method to calculate numeric rank of a card
    def cardEmpirics(self):
        ranks = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]
        return ranks.index(self.rank)

    ## Method to access numeric rank
    def getStatistic(self):
        return self.statOne

    ## Method to print out card parameters
    def __str__(self):
        return f"{self.rank}{self.suit}"

    ## Method to define how to comparte card values
    def __eq__(self, other):
        if isinstance(other, Card):
            return self.getStatistic() == other.getStatistic()
        else:
            return False

## Defining class to implement game mechanics
class PokerFinal:
    suits = ["C", "S", "H", "D"]
    ranks = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]

    ## Initializing arrays for game deck and player hand
    def __init__(self):
        self.deck = []
        self.hand = []
        self.fillDeck()

    ## Method to fill the deck
    def fillDeck(self):
        for suit in self.suits:
            for rank in self.ranks:
                self.deck.append(Card(suit, rank))
        random.shuffle(self.deck)

    ## Method to draw cards from deck to hand
    def drawCards(self, num):
        for i in range(num):
            if self.deck:
                card = self.deck.pop()
                self.hand.append(card)
        self.sortHand()

    ## Method to clear and create a new hand
    def createHand(self):
        self.hand = []
        self.drawCards(5)

    ## Method to reset deck
    def resetDeck(self):
        self.deck.clear()
        self.hand.clear()
        self.fillDeck()

    ## Method to sort hand
    def sortHand(self):
        for i in range(1, len(self.hand)):
            currentCard = self.hand[i]
            currentStat = currentCard.getStatistic()
            j = i - 1
            while j >= 0 and self.hand[j].getStatistic() > currentStat:
                self.hand[j + 1] = self.hand[j]
                j -= 1
            self.hand[j + 1] = currentCard

    ## Method to print hand
    def printHand(self):
        truncate = ' '.join(str(card) for card in self.hand)
        print(f"Current hand: {truncate}")

    ## Method to take inputs to discard
    def dropAndDraw(self, numCards):
        indices = []
        try:
            print("What indexes do you wish to discard?")
            indexes = [int(input(f"Index {i + 1}: ")) for i in range (numCards)]
        except ValueError:
            print("Invalid input. The game continues.")

    ## Method to employ discard/draw
    def dropAndDrawMech(self, indices):
        indices.sort(reverse=True)
        for index in indices:
            if index < len(self.hand):
                self.hand.pop(index)
        self.drawCards(len(indices))

    ## Now, onto the hand value calculations
    def singlePair(self):
        rankCounts = {rank: 0 for rank in self.ranks}
        for card in self.hand:
            rankCounts[card.getRank()] += 1
        pairs = sum(1 for count in rankCounts.values() if count == 2)
        return pairs == 1

    ## Value for double pair
    def doublePair(self):
        rankCounts = {rank: 0 for rank in self.ranks}
        for card in self.hand:
            rankCounts[card.getRank()] += 1
        pairs = sum(1 for count in rankCounts.values() if count == 2)
        return pairs == 2

    ## Value for flush
    def regularFlush(self):
        if len(self.hand) < 5:
            return False
        baseline = self.hand[0].getSuit()
        return all(card.getSuit() == baseline for card in self.hand)

    ## Value for three of a kind
    def threeKind(self):
        rankCounts = {rank: 0 for rank in self.ranks}
        for card in self.hand:
            rankCounts[card.getRank()] += 1
        return any(count == 3 for count in rankCounts.values())

    ## Value for four of a kind
    def fourKind(self):
        rankCounts = {rank: 0 for rank in self.ranks}
        for card in self.hand:
            rankCounts[card.getRank()] += 1
        return any(count == 4 for count in rankCounts.values())

    ## Value for straight
    def regularStraight(self):
        values = [card.getStatistic() for card in self.hand]
        values.sort()
        return all(values[i] - values[i - 1] == 1 for i in range(1, len(values)))

    ## Value for full house
    def fullHouse(self):
        return self.threeKind and self.singlePair()

    ## Value for straight flush
    def straightFlush(self):
        return self.regularFlush() and self.regularStraight()

    ## Value for royal flush
    def royalFlush(self):
        if not self.regularFlush():
            return False
        ranksFlush = {"10", "J", "Q", "K", "A"}
        ranksHand = {card.getRank() for card in self.hand}
        return ranksFlush == ranksHand

    ## Printing winnings
    def printWinnings(self):
        if self.royalFlush():
            print("Royal Flush. You win enough simoleons to be Jeffrey Bezos!")
        elif self.straightFlush():
            print("Straight Flush. You win enough simoleons to quit your job!")
        elif self.fourKind():
            print("4-of-a-Kind. You win a good chunk of simoleons!")
        elif self.fullHouse():
            print("Full House. You win enough simoleons for a lobster dinner!")
        elif self.regularFlush():
            print("Flush. You win enough simoleons to buy a steak dinner!")
        elif self.regularStraight():
            print("Straight. You win a modest amount of simoleons.")
        elif self.threeKind():
            print("3-of-a-Kind. You win some simoleons.")
        elif self.doublePair():
            print("Two-Pair. You win a very modest amount of simoleons.")
        elif self.singlePair():
            print("Pair. You win a modicum of simoleons.")
        else:
            print("No matches. Sorry, you lost.")

## Calling main function to start the game
if __name__ == '__main__':
    main()
