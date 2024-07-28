def findPokerHand(hand):

    ranks = []
    suits = []
    possibleRanks = []

    for card in hand:
        if len(card) == 2:
            rank = card[0]
            suit = card[1]
        else:
            rank = card[0:2]
            suit = card[2]
        if rank == "A":
            rank = 14
        elif rank == "K":
            rank = 13
        elif rank == "Q":
            rank = 12
        elif rank == "J":
            rank = 11
        ranks.append(int(rank))
        suits.append(suit)
    # print(ranks)
    sortedRanks = sorted(ranks)
    # print(sortedRanks)

    # Royal flush
    if suits.count(suits[0]) == 5:
        if 14 in sortedRanks and 13 in sortedRanks and 12 in sortedRanks and 11 in sortedRanks and 10 in sortedRanks:
           possibleRanks.append(10)
        elif all(sortedRanks[i] == sortedRanks[i - 1] + 1 for i in range(1, len(sortedRanks))):
            possibleRanks.append(5)
        else:
           possibleRanks.append(6)
    # straight
    if all(sortedRanks[i] == sortedRanks[i-1] + 1 for i in range(1, len(sortedRanks))):
        possibleRanks.append(9)
    # four of a kind and full house
    handleuniquevalue = list(set(sortedRanks))
    if len(handleuniquevalue) == 2:
        for val in handleuniquevalue:
            if sortedRanks.count(val) == 4:
                possibleRanks.append(8)
            if sortedRanks.count(val) == 3:
                possibleRanks.append(7)
    # Three of a kind and pair
    if len(handleuniquevalue) == 3:
        for val in handleuniquevalue:
            if sortedRanks.count(val) == 3:
                possibleRanks.append(4)
            if sortedRanks.count(val) == 2:
                possibleRanks.append(3)
    # pair
    if len(handleuniquevalue) == 4:
        possibleRanks.append(2)
    if not possibleRanks:
        possibleRanks.append(1)
    pokerHandRank = {10: "Royal Flush", 9: "Straight Flush", 8: "Four of the Kind", 7: "Full House", 6: "Flush",
                     5: "Straight", 4: "Three Of The Kind", 3: "Two Pair", 2: "Pair", 1: "High Card"}
    output = pokerHandRank[max(possibleRanks)]
    print(hand, output)
    return output

if __name__ == "__main__":
    findPokerHand(["KH", "AH", "QH", "JH", "10H"])   # Royal flush
    findPokerHand(["QC", "JC", "10C", "9C", "8C"])  # straight flush
    findPokerHand(["5C", "5S", "5H", "5D", "QH"])  # Four of a kind
    findPokerHand(["2H", "2D", "2S", "10H", "10C"])  # full house
    findPokerHand(["2D", "KH", "7D", "6D", "5D"])  # flush
    findPokerHand(["JC", "10H", "9C", "8C", "7D"])  # straight
    findPokerHand(["10H", "10C", "10D", "2D", "5S"])  # Three of a kind
    findPokerHand(["KD", "KH", "5C", "5S", "6D"])  # Two pair
    findPokerHand(["2D", "2S", "9C", "KD", "10C"])  # Pair
    findPokerHand(["KD", "5H", "2D", "10C", "JH"])  # High Card
