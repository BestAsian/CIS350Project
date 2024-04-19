import random
import pygame
from Button import Button
import sys


pygame.init()
pygame.font.init()
font = pygame.font.SysFont(None, 30)
clock = pygame.time.Clock()
screen = pygame.display.set_mode((1000, 900))
comCords = [250, 450]
faceDownCard = pygame.image.load('assets\Cards\\back_red_basic_white.png')
font = pygame.font.SysFont(None, 30)
black = (0, 0, 0)

class Card:
    def __init__(self, val, suit, path, numval):
        self.val = val
        self.suit = suit
        self.path = f"assets\Cards\{path}"
        self.numVal = numval

    def getVal(self):
        return self.val
    
    def getSuit(self):
        return self.suit
        
    def getPath(self):
        return self.path
    
    def getImage(self):
        return pygame.image.load(self.path)
    
    def getNumVal(self):
        return self.numVal
    
def createDeck():
    deck = []
    suits = ['spades', 'hearts', 'clubs', 'diamonds']

    for suit in suits:
        for i in range(2, 11):
            deck.append(Card(i, suit, f"{i}_{suit}_white.png", i))
        deck.append(Card('ace', suit, f"ace_{suit}_white.png", 14))
        deck.append(Card('jack', suit, f"jack_{suit}_white.png", 11))
        deck.append(Card('queen', suit, f"jack_{suit}_white.png", 12))
        deck.append(Card('king', suit, f"jack_{suit}_white.png", 13))
    random.shuffle(deck)
    return deck

class Player:

    def __init__(self, funds, name, cardPos):
        self.funds = funds
        self.hand = []
        self.name = name
        self.cardPos = cardPos
        self.folded = False


    def addCard(self, card):
        self.hand.append(card)

    def clearHand(self):
        self.hand = []

    def setNext(self, Player):
        self.next = Player

    def getNext(self):
        return self.next
    
    def getFunds(self):
        return self.funds
    
    def placeUserBet(self, phase, players, cards, bet):
        userInput = False
        userText = '$'
        newBet = bet
        betting = True
        insufficientFunds = False
        while betting:
            mousePos = pygame.mouse.get_pos()
            screen.fill((60, 179, 113))
            renderPlayerCards(players)
            match phase:
                case 0:
                    renderFlop(cards)
                case 1:
                    renderTurn(cards)
                case 2:
                    renderRiver(cards)
            callButton = Button(None, [400, 600], f"Call: ${bet}", font, 'black', 'gray')
            raiseButton = Button(None, [500, 600], "Raise", font, 'black', 'gray')
            foldButton = Button(None, [600, 600], "Fold", font, 'black', 'gray')
            IFMessage = font.render("You have insufficient funds to perform this action. If you do not have enough money to continue playing, you must fold", True, black)
            callButton.update(screen)
            raiseButton.update(screen)
            foldButton.update(screen)
            if insufficientFunds:
                screen.blit(IFMessage, (400, 700))
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if callButton.checkForInput(mousePos):
                        if bet <= self.funds:
                            self.funds -= bet
                            betting = False
                            self.increaseBet(bet)
                        else:
                            insufficientFunds = True
                    if raiseButton.checkForInput(mousePos):
                        userInput = True
                    if foldButton.checkForInput(mousePos):
                        self.folded = True
                        betting = False
                if event.type == pygame.KEYDOWN and userInput:
                    insufficientFunds = False
                    if event.key == pygame.K_BACKSPACE:
                        userText = userText[0:-1]
                    if event.key == pygame.K_RETURN:
                        inputInt = int(userText[1:])
                        if inputInt <= self.funds:
                            userInput = False
                            self.funds -= inputInt
                            newBet += inputInt
                            self.increaseBet(newBet)
                            betting = False
                        else:
                            insufficientFunds = True
                            userInput = False
                    else:
                        userText += event.unicode
            if userInput:
                inputPrompt = font.render("Please input the amount you would like to input in using only digits. Press Enter to place bet.", True, black)
                screen.blit(inputPrompt, (600, 700))
                currentInput = font.render(userText, True, black)
                screen.blit(currentInput, (600, 750))
                pygame.display.update()

        return newBet


    def getBet(self):
        return self.bet
    
    def getCardPos(self):
        return self.cardPos
    
    def getHand(self):
        return self.hand
    
    def balanceCheck(self, amount):
        if amount > self.funds:
            return False
        return True
    
    def fold(self):
        self.folded = True
        self.bet = 0

    def getFold(self):
        return self.folded
    
    def unFold(self):
        self.folded = False

    def increaseBet(self, bet):
        self.bet = bet

    def resetBet(self):
        self.bet = 0

    def getName(self):
        return self.name
    
    def addToFunds(self, amount):
        self.funds += amount
    

def findLongestConseq(lst):
    lst = sorted(lst)
    currentConsecutive = []
    longest = 0

    for i in range(len(lst) - 1):
        if currentConsecutive == []:
            currentConsecutive = [lst[i]]
        elif lst[i] == lst[i-1] + 1:
            currentConsecutive.append(lst[i])
        else:
            longest = max(longest, len(currentConsecutive))
            currentConsecutive = []
        

    return longest

def findStrait(lst):
    lst = sorted(lst)
    currentConsecutive = []

    for i in range(len(lst) - 1):
        if currentConsecutive == []:
            currentConsecutive = [lst[i]]
        elif lst[i] == lst[i-1] + 1:
            currentConsecutive.append(lst[i])
        elif len(currentConsecutive) < 5:
            currentConsecutive = []
        
    if len(currentConsecutive) < 5:
        return None
    temp = len(currentConsecutive) - 5

    return currentConsecutive[temp:]
        


def findWinners(activePlayers, comCards):
    '''
    p1Hand = p1.copy()
    if measure == False:
        p2Hand = p2.copy()
        p3Hand = p3.copy()
        p4Hand = p4.copy()
        p1Hand.extend(comCards)
        p2Hand.extend(comCards)
        p3Hand.extend(comCards)
        p4Hand.extend(comCards)
        '''
    hands = []
    for player in activePlayers:
        x = player.getHand()
        x.extend(comCards)
        hands.append(x)


    #setTraits = [0:set, 1:highestCard, 2:largest group of same val, 3:pairs, 4:hasStrait (int of lowest card), 5:hasFlush, 6:tripleVal]
    """
    p1Traits = [p1Hand, 0, 0, [0, 0, 0], 0, False, 0, 1]
    if measure == False:
        p2Traits = [p2Hand, 0, 0, [0, 0, 0], 0, False, 0, 2]
        p3Traits = [p3Hand, 0, 0, [0, 0, 0], 0, False, 0, 3]
        p4Traits = [p4Hand, 0, 0, [0, 0, 0], 0, False, 0, 4]
"""
    players = []

    for i in range(len(hands)):
        players.append([hands[i], 0, 0, [0, 0, 0], 0, False, 0, activePlayers[i]])
    

    for player in players:
        for card in player[0]:
            if card.getNumVal() > player[1]:
                player[1] = card.getNumVal()
        
        for card in player[0]:
            matches = 1
            for x in player[0]:
                if x is not card:
                    if card.getNumVal() == x.getNumVal():
                        matches += 1
            player[2] = max(player[2], matches)
            if matches == 2:
                if player[3][0] < 2:
                    player[3][0] += 1
                    if player[3][1] == 0:
                        player[3][1] = card.getNumVal()
                    else:
                        player[3][2] = card.getNumVal()
                else:
                    if player[3][1] < player[3][2]:
                        player[3][1] = max(player[3][1], card.getNumVal())
                    else:
                        player[3][2] = max(player[3][2], card.getNumVal())
            if matches == 3:
                player[6] = max(player[6], card.getNumVal())

        for card in player[0]:
            suitMatches = 1
            for x in player[0]:
                if card is not x:
                    if card.getSuit() == x.getSuit():
                        suitMatches += 1
            if suitMatches == 5:
                player[5] = True

        cardVals = []
        for card in player[0]:
            cardVals.append(card.getNumVal())
            
        straight = findStrait(cardVals)
        if straight is not None:
            player[4] = straight[0]
        if 14 in cardVals and player[4] == 0:
            cardVals.remove(14)
            cardVals.append(1)
            straight = findStrait(cardVals)
            if straight is not None:
                player[4] = straight[0]

    winners = []
    winType = ''
    #check for royal flush
    for player in players:
        if player[5] == True and player[4] == 10:
            winners.append(player)
            winType = 'Royal Flush'

    #check for straight flush
    if winners == []:
        potentialWinners = []
        for player in players:
            if player[5] == True and player[4] > 0:
                potentialWinners.append(player)
        for x in potentialWinners:
            for y in potentialWinners:
                if y[4] < x[4]:
                    potentialWinners.remove(y)
        winners = potentialWinners
        if winners is not []:
            winType = 'Straight Flush'

    #check for four of a kind
    if winners == []:
        potentialWinners = []
        highest = 0
        for player in players:
            if player[2] > highest:
                potentialWinners = [player]
                highest = player[2]
            elif player[2] == highest and highest != 0:
                potentialWinners.append(player)
        if potentialWinners is not []:
            winners = potentialWinners
            winType = 'Four of a Kind'

    #check for full house
    if winners == []:
        potentialWinners = []
        threes = 0
        pair = 0
        for player in players:
            if player[6] > 0 and player[3][0] > 0:
                potentialWinners.append(player)

        for candidate in potentialWinners:
            candidatePair = max(candidate[3][1], candidate[3][2])
            for x in potentialWinners:
                xPair = max(x[3][1], x[3][2])
                if x is not candidate:
                    if x[6] < candidate[6]:
                        potentialWinners.remove(x)
                    elif x[6] == candidate[6]:
                        if xPair < candidatePair:
                            potentialWinners.remove(x)
                        if candidatePair < xPair:
                            potentialWinners.remove(candidate)
                    else:
                        potentialWinners.remove(candidate)
        
        if potentialWinners is not []:
            winners = potentialWinners
            winType = 'Full House'

    #check for flush
    if winners == []:
        potentialWinners = []
        for player in players:
            if player[5] == True:
                potentialWinners.append(player)
        
        if potentialWinners is not []:
            winners = potentialWinners
            winType = 'Flush'

    #check for straight
    if winners == []:
        potentialWinners = []
        highest = 0
        for player in players:
            if player[4] > highest:
                potentialWinners = [player]
                highest = player[4]
            elif player[4] == highest and highest != 0:
                potentialWinners.append(player)

        if potentialWinners is not []:
            winners = potentialWinners
            winType = 'Straight'

    #check for three of a kind
    if winners == []:
        potentialWinners = []
        highest = 0
        for player in players:
            if player[6] > highest:
                potentialWinners = [player]
                highest = player[6]
            elif player[6] == highest and highest != 0:
                potentialWinners.append(player)
        
        if potentialWinners is not []:
            winners = potentialWinners
            winType = "Three of a Kind"

    #check for two pair
    if winners == []:
        potentialWinners = []
        highest = 0
        secondHighest = 0
        for player in players:
            if player[3][0] == 2:
                if max(player[3][1:]) > highest:
                    potentialWinners = [player]
                    highest = max(player[3][1:])
                    secondHighest = min(player[3][1:])
                elif max(player[3][1:]) == highest and highest != 0:
                    if min(player[3][1:]) > secondHighest:
                        potentialWinners = [player]
                        secondHighest = min(player[3][1:])
                    elif min(player[3][1:]) == secondHighest:
                        potentialWinners.append(player)

        if potentialWinners is not []:
            winners = potentialWinners
            winType = 'Two Pair'

    #check for a pair
    if winners == []:
        potentialWinners = []
        highest = 0
        for player in players:
            if player[3][0] == 1:
                if player[3][1] > highest:
                    potentialWinners = [player]
                    highest = player[3][1]
                elif player[3][1] == highest and highest != 0:
                    potentialWinners.append(player)

        if potentialWinners is not []:
            winners = potentialWinners
            winType = 'Pair'

    #high card
    if winners == []:
        potentialWinners = []
        highest = 0
        secondHighest = 0
        for player in players:
            secondCard = min(player[0] - comCards)
            if player[1] > highest:
                potentialWinners = [player]
                highest = player[1]
                secondHighest = secondCard
            elif player[1] == highest and highest != 0:
                if secondCard > secondHighest:
                    potentialWinners = [player]
                    secondHighest = secondCard
                elif secondCard == secondHighest:
                    potentialWinners.append(player)

        winners = potentialWinners
        winType = 'High Card'

    result = []

    for winner in winners:
        result.append(winner[7])

    return [result, winType]
            


class AI(Player):
    def __init__(self, funds, name, cardPos):
        self.funds = funds
        self.hand = []
        self.name = name
        self.cardPos = cardPos
        self.folded = False

    def foldPreFlop(self):
        if self.getHand()[0].getSuit() == self.getHand()[1].getSuit():
            return 'stay'
        cardValues = [self.getHand()[0].getNumVal(), self.getHand()[1].getNumVal()]
        if cardValues[0] == cardValues[1]:
            return 'stay'
        if (cardValues[0] - cardValues[1]) in range(-1, 2):
            return 'stay'
        for val in cardValues:
            if val > 4:
                return 'stay'
        return 'fold'
    
    def increaseBet(self, bet):
        self.bet += bet
    
    
    def measureHand(self, visComCards): 
        print("Ran meansureHand")
        pHand = self.hand.copy()
        comCards = visComCards.copy()
        cardsNeeded = 5 - len(comCards)
        bestHands = []
        games = []
        simDeck = createDeck()

         #setTraits = [0:set, 1:highestCard, 2:largest group of same val, 3:pairs, 4:longestStraight 5:hasFlush, 6:tripleVal]

        match cardsNeeded:
            case 0:
                bestHands.append(findWinners([self], comCards)[1])
            case 1:
                origComCards = comCards.copy()
                for i in range(52):
                    if simDeck[i-1] in comCards and simDeck[i-1] not in origComCards:
                        comCards.remove(simDeck[i-1])
                    comCards.append(simDeck[i])

                    games.append(findWinners([self], comCards))
            case 2:
                print("Reached check A")
                origComCards = comCards.copy()
                possibleCombos = []
                for i in range(52):
                    print(f"i={i}")
                    if simDeck[i-1] in comCards and simDeck[i-1] not in origComCards:
                        comCards.remove(simDeck[i-1])
                    comCards.append(simDeck[i])

                    for j in range(52):
                        #print(f"i={i}, j={j}")
                        if simDeck[j-1] in comCards and simDeck[j-1] not in origComCards:
                            comCards.remove(simDeck[j-1])
                        elif j != i:
                            comCards.append(simDeck[j])
                            possibleCombos.append(comCards)

                for combo in possibleCombos:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.quit()
                            sys.exit()
                    thinkMessage = font.render("Please wait while the computer think <3 (he's doing his best)", True, black)
                    screen.blit(thinkMessage, (200, 600))
                    pygame.display.update()
                    games.append(findWinners([self], combo))

        for game in games:
            bestHands.append(game[1])

        numGames = len(games)
        if numGames == 0:
            numGames = 1
        royalCount = fhCount = straightCount = flushCount = fourKindCount = threeCount = twoPairCount = pairCount = hcCount = straightFlushCount = 0
        for hand in bestHands:
            if hand == 'Royal Flush':
                royalCount += 1
            if hand == 'Straight Flush':
                straightFlushCount +=1
            if hand == 'Full House':
                fhCount += 1
            if hand == 'Flush':
                flushCount += 1
            if hand == 'Straight':
                straightCount += 1
            if hand == 'Four of a Kind':
                fourKindCount += 1
            if hand == 'Three of a Kind':
                threeCount += 1
            if hand == 'Two Pair':
                twoPairCount += 1
            if hand == 'Pair':
                pairCount += 1
            if  hand == 'High Card':
                hcCount += 1

        royalRatio = royalCount/numGames
        sfRatio = straightFlushCount/numGames
        fhRatio = fhCount/numGames
        flushRatio = flushCount/numGames
        straightRatio = straightCount/numGames
        fourKindRatio = fourKindCount/numGames
        threeRatio = threeCount/numGames
        tpratio = twoPairCount/numGames
        pairRatio = pairCount/numGames
        hcRatio = hcCount/numGames
        
        
        if cardsNeeded == 0:
            if bestHands[0] == 'Royal Flush':
                return (100, 100)
            if bestHands[0] == 'Straight Flush':
                return (100, 100)
            if bestHands[0] == 'Full House':
                return (80, 100)
            if bestHands[0] == 'Flush':
                return (70, 100)
            if bestHands[0] == 'Straight':
                return (60, 100)
            if bestHands[0] == 'Four of a Kind':
                return (60, 100)
            if bestHands[0] == 'Three of a Kind':
                return (40, 80)
            if bestHands[0] == 'Two Pair':
                return (20, 70)
            if bestHands[0] == 'Pair':
                return (5, 15)
            if bestHands[0] == 'High Card':
                return (1, 10)
            
        elif cardsNeeded == 1:
            if royalRatio + sfRatio + flushRatio + straightRatio + fhRatio + fourKindRatio >= 0.5:
                return (40, 100)
            if royalRatio + sfRatio + flushRatio + straightRatio + fhRatio + fourKindRatio + threeRatio + tpratio >= 0.5:
                return (20, 80)
            if royalRatio + sfRatio + flushRatio + straightRatio + fhRatio + fourKindRatio + threeRatio + tpratio + pairRatio >= 0.5:
                return (5, 25)
            else:
                return (1, 10)
            
        else:
            if royalRatio + sfRatio + flushRatio + straightRatio + fhRatio + fourKindRatio >= 0.5:
                return (20, 100)
            if royalRatio + sfRatio + flushRatio + straightRatio + fhRatio + fourKindRatio + threeRatio + tpratio >= 0.5:
                return (5, 50)
            if royalRatio + sfRatio + flushRatio + straightRatio + fhRatio + fourKindRatio + threeRatio + tpratio + pairRatio >= 0.5:
                return (1, 10)
            else:
                return (1, 10)




    
def renderPlayerCards(players):
    screen.fill((60, 179, 113))
    for player in players:
        x = player.getCardPos()[0]
        y = player.getCardPos()[1]
        if player.getName() == 'You':
            screen.blit(player.getHand()[0].getImage(), (x, y))
            screen.blit(player.getHand()[1].getImage(), (x+50, y))
        else:
            screen.blit(faceDownCard, (x, y))
            screen.blit(faceDownCard, (x+50, y))
    pygame.display.update()

def renderFlop(cards):
    x = comCords[0]
    y = comCords[1]
    for num in range(3):
        screen.blit(cards[num].getImage(), (x + (num*100), y))
    screen.blit(faceDownCard, (x + 300, y))
    screen.blit(faceDownCard, (x + 400, y))
    pygame.display.update()

def renderTurn(cards):
    x = comCords[0]
    y = comCords[1]
    for num in range(4):
        screen.blit(cards[num].getImage(), (x + (num*100), y))
    screen.blit(faceDownCard, (x + 400, y))
    pygame.display.update()

def renderRiver(cards):
    x = comCords[0]
    y = comCords[1]
    for num in range(5):
        screen.blit(cards[num].getImage(), (x + (num*100), y))
    pygame.display.update()
        
def renderPreFlop():
    x = comCords[0]
    y = comCords[1]
    for num in range(5):
        screen.blit(faceDownCard, (x + (num*100), y))
    pygame.display.update()

def renderAllCards(cards, players, phase):
    match phase:
        case 0:
            renderFlop(cards)
        case 1:
            renderTurn(cards)
        case 2:
            renderRiver(cards)
        case 3:
            renderPreFlop()
    renderPlayerCards(players)

def placeBets(activePlayers, cards, phase):
    #phases: 0 = postFlopBets, 1 = turnBets, 2 = riverBets
    currentBet = 0
    for player in activePlayers:
        renderAllCards(cards, activePlayers, phase)
        if player.getName() != 'You':
            temp = player.measureHand(cards)
            if (temp[0]/100)*player.getFunds() > currentBet + player.getBet():
                player.increaseBet((temp[0]/100)*player.getFunds())
                currentBet = (temp[0]/100)*player.getFunds() - player.getBet()
                player.increaseBet(currentBet)
            else:
                player.fold()
                activePlayers.remove(player)
        else:
            player.placeUserBet(phase, activePlayers, cards, currentBet)
            if player.getFold():
                activePlayers.remove(player)

    maxBet = 0
    minBet = 0
    for player in activePlayers:
        maxBet = max(maxBet, player.getBet())
        if minBet > 0:
            minBet = min(minBet, player.getBet())
        else:
            minBet = player.getBet()

    while maxBet > minBet:
        print("Reached max min block")
        placeBets(activePlayers, cards, phase)

    return currentBet




def main():
    user = Player(1000, 'You', [850, 800])
    player2 = AI(1000, 'Player 2', [150, 800])
    Player.setNext(user, player2)
    player3 = AI(1000, 'Player 3', [150, 100])
    Player.setNext(player2, player3)
    player4 = AI(1000, 'Player 4', [800, 100])
    Player.setNext(player3, player4)
    Player.setNext(player4, user)

    players = [user, player2, player3, player4]
    activePlayers = players.copy()

    dealer = user
    newRound = True
    preflop = False
    flop = False
    wonByElimination = False
    turn = False
    pot = 0
    while True:
        screen.fill((60, 179, 113))
        potMessage = font.render(f"Pot: ${pot}", True, black)
        screen.blit(potMessage, (450, 20))
        dealer = Player.getNext(dealer)
        smallBlind = Player.getNext(dealer)
        bigBlind = Player.getNext(smallBlind)
        pot = 0
        pos = pygame.mouse.get_pos()
        if newRound:
            print("Reached NewRound")
            deck = createDeck()
            communityCards = []
            for x in range(5):
                communityCards.append(deck.pop())
            for player in players:
                player.unFold()
                player.resetBet()
                player.clearHand()
                player.addCard(deck.pop())
                player.addCard(deck.pop())
                if player.getFunds() < 100:
                    player.increaseFunds(200)
            newRound = False
            preflop = True
            flop = False
            wonByElimination = False
            turn = False
            pot = 0
            finalJudgement = False
            visibleComCards = []
            river = False
        
        renderAllCards(visibleComCards, activePlayers, 3)

        if preflop:
            print("Reached preflop")
            renderPreFlop()
            renderPlayerCards(activePlayers)
            visibleComCards = []
            '''
            if smallBlind.balanceCheck(5):
                smallBlind.placeBet(5)
                pot += 5
            else:
                smallBlind.fold()
                activePlayers.remove(smallBlind)
            
            if bigBlind.balanceCheck(10):
                bigBlind.placeBet(10)
                pot += 10
            else:
                bigBlind.fold()
                activePlayers.remove(bigBlind)
'''
            preflop = False
            flop = True

        if flop == True:
            print("Reached flop")
            for player in activePlayers:
                if player.getFold() == True:
                    activePlayers.remove(player)

            visibleComCards = communityCards[0:3].copy()
            pot += placeBets(activePlayers, visibleComCards, 0)

            for player in activePlayers:
                if player.getFold() == True:
                    activePlayers.remove(player)

            if len(activePlayers) == 1:
                wonByElimination = True
            else:
                turn = True
            
            flop = False

        if wonByElimination:
            winner = activePlayers[0]
            wonByEliminationMessage = font.render(f"{winner.getName()} has won by elimination, as all other players have folded.", True, black)
            screen.blit(wonByEliminationMessage, (450, 600))
            newRoundButton = Button(None, [450, 700], "Begin New Round", font, black, 'gray')
            newRoundButton.update(screen)
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if newRoundButton.checkForInput(pos):
                    winner.addToFunds(pot)
                    pot = 0
                    newRound = True

        if turn:
            visibleComCards = communityCards[0:4].copy()
            pot += placeBets(activePlayers, visibleComCards, 1)

            for player in activePlayers:
                if player.getFold() == True:
                    activePlayers.remove(player)

            if len(activePlayers) == 1:
                wonByElimination = True
            else:
                river = True
            
            turn = False

        if river:
            pot += placeBets(activePlayers, communityCards, 2)
            for player in activePlayers:
                if player.getFold() == True:
                    activePlayers.remove(player)

            if len(activePlayers) == 1:
                wonByElimination = True
            else:
                finalJudgement = True
            
            river = False

        if finalJudgement: 
            winList = findWinners(activePlayers, communityCards)
            numWinners = len(winList[0])
            winMessages = []
            for winner in winList[0]:
                winner.addToFunds(pot/numWinners)
                winMessages.append(font.render(f"{winner.getName()} won with a {winList[1]}", True, black))
            pot = 0
            for i in range(len(winMessages)):
                y = 600 + (50*i)
                screen.blit(winMessages[i], (450, y))
            newRoundButton = Button(None, [450, 800], "Begin New Round", font, black, 'gray')
            newRoundButton.update(screen)
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if newRoundButton.checkForInput(pos):
                        newRound = True
            

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        clock.tick(60)


main()
