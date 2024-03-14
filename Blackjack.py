
import random
import pygame
from button2 import Button
import sys

pygame.init()
pygame.font.init()
font = pygame.font.SysFont(None, 30)
black = (0, 0, 0)
white = (255, 255, 255)
gray = (105, 105, 105)
class Card:
    def __init__(self, val, suit, path):
        self.val = val
        self.suit = suit
        self.path = path

    def getVal(self):
        return self.val
    
    def getSuit(self):
        return self.suit
    
    def getPath(self):
        return f"Cards\{self.path}.png"
    
#Creates a deck
def createDeck():
    deck = []
    suits = ['spades', 'hearts', 'clubs', 'diamonds']

    for suit in suits:
        for i in range(2, 11):
            deck.append(Card(i, suit, f"{i}_{suit}_white"))
        deck.append(Card('ace', suit, f"ace_{suit}_white"))
        deck.append(Card('jack', suit, f"jack_{suit}_white"))
        deck.append(Card('queen', suit, f"jack_{suit}_white"))
        deck.append(Card('king', suit, f"jack_{suit}_white"))
    random.shuffle(deck)
    return deck



class Player:

    def __init__(self, funds):
        self.funds = funds
        self.hand = []
        self.bet = 0

    def addCard(self, card):
        self.hand.append(card)
    
    def setBet(self, bet):
        self.bet = bet
        
    def getBet(self):
        return self.bet
    
    def getHand(self):
        return self.hand
    
    def resetHand(self):
        self.hand = []

    def doubleDown(self):
        self.bet += self.bet

    def updateFunds(self, amount):
        self.funds += amount

    def getFunds(self):
        return self.funds

def validBet(bet, player):
    if bet > player.funds:
        return False
    return True
    
class Dealer:
    def __init__(self):
        self.hand = []
    
    def addCard(self, card):
        self.hand.append(card)

    def getHand(self):
        return self.hand

    def resetHand(self):
        self.hand = []
        
def countHand(hand):
    total = 0
    aceCount = 0
    for card in hand:
        val = Card.getVal(card)
        if type(val) == int:
            total += val
        if val in ['jack', 'queen', 'king']:
            total += 10
        if val == 'ace':
            aceCount += 1
    for i in range(aceCount):
        if total >= 11:
            total += 1
        else:
            total += 11
    return total

def hasBlackjack(hand):
    has10 = False
    hasAce = False
    if len(hand) != 2:
        return False
    for card in hand:
        if card.getVal() in ['Jack', 'King', 'Queen', 10]:
            has10 = True
        if card.getVal() == 'Ace':
            hasAce = True
    if has10 and hasAce:
        return True
    else:
        return False

def main():
    running = True
    screen = pygame.display.set_mode((800, 600))
    dealer = Dealer()
    player = Player(1000)
    newRound = True
    while running == True:
        if newRound == True:
            player.resetHand()
            dealer.resetHand()
            deck = createDeck()
            newRound = False
            readyToJudge = False
            paid = False
            betSizeMessage = False
            player.setBet(0)
            dealer.addCard(deck.pop())
            dealer.addCard(deck.pop())
            player.addCard(deck.pop())
            player.addCard(deck.pop())
        screen.fill((60, 179, 113))

        mousePos = pygame.mouse.get_pos()

        playerCard1 = pygame.image.load(player.getHand()[0].getPath())
        playerCard2 = pygame.image.load(player.getHand()[1].getPath())

        dealerCard1 = pygame.image.load(dealer.getHand()[0].getPath())
        dealerCard2 = pygame.image.load(dealer.getHand()[1].getPath())
        faceDownCard = pygame.image.load('Cards\\back_red_basic_white.png')

        balance = font.render(f"Current Balance: {player.getFunds()}", True, black)
        screen.blit(balance, (400, 50))
        bet = font.render(f"Current Bet: {player.getBet()}", True, black)
        screen.blit(bet, (100, 50))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()
                break
        
        if player.getBet() == 0:
            fiveD = Button(None, [250, 300], "$5", font, 'black', 'gray')
            tenD = Button(None, [350, 300], "$10", font, 'black', 'gray')
            twentyD = Button(None, [450, 300], "$20", font, 'black', 'gray')
            #customButton = Button(None, [400, 450], "Custom Bet", font, 'black', 'gray')

            fiveD.update(screen)
            tenD.update(screen)
            twentyD.update(screen)
            #customButton.update(screen)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if fiveD.checkForInput(mousePos):
                        if validBet(5, player):
                            player.setBet(5)
                            betSizeMessage = False
                            player.updateFunds(-5)
                        else:
                            betSizeMessage = True
                    if tenD.checkForInput(mousePos):
                        if validBet(10, player):
                            player.setBet(10)
                            betSizeMessage = False
                            player.updateFunds(-10)
                        else:
                            betSizeMessage = True
                    if twentyD.checkForInput(mousePos):
                        if validBet(20, player):
                            player.setBet(20)
                            betSizeMessage = False
                            player.updateFunds(-20)
                        else:
                            betSizeMessage = True
            continue

        screen.blit(playerCard1, (250, 400))
        screen.blit(playerCard2, (450, 400))
        screen.blit(dealerCard1, (250, 100))
        screen.blit(faceDownCard, (450, 100))
        pygame.display.update()

        if hasBlackjack(player.getHand()):
            blackjackMessage = font.render('You got a Blackjack', True, black)
            screen.blit(blackjackMessage, (0, 200))
            screen.blit(dealerCard2, (100, 400))
            if hasBlackjack(dealer.getHand()):
                dealerBlackjackMessage = font.render('The dealer also got a blackjack. Your bet will be refunded', True, black)
                screen.blit(dealerBlackjackMessage, (50, 200))
            hasBJContinueButton = Button(None, [250, 250], 'Continue', 'black')
            hasBJContinueButton.update(screen)
            for event in pygame.event.get():
                if hasBJContinueButton.checkForInput(mousePos):
                    if hasBlackjack(dealer.getHand()):
                        player.updateFunds(player.getBet())
                        player.setBet(0)
                        newRound = True
                    else:
                        player.updateFunds(1.5 * player.getBet())
                        player.setBet(0)
                        newRound = True
            continue

        if readyToJudge == False:
            standButton = Button(None, [100, 300], 'Stand', font, 'black', 'gray')
            hitButton = Button(None, [250, 300], 'Hit', font, 'black', 'gray')
            ddButton = Button(None, [400, 300], 'Double Down', font, 'black', 'gray')
            surrenderButton = Button(None, [600, 300], 'Surrender', font, 'black', 'gray')

            standButton.update(screen)
            hitButton.update(screen)
            ddButton.update(screen)
            surrenderButton.update(screen)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if standButton.checkForInput(mousePos):
                        readyToJudge = True
                    if surrenderButton.checkForInput(mousePos):
                        player.updateFunds(0.5 * player.getBet())
                        player.setBet(0)
                        newRound = True
                    if hitButton.checkForInput(mousePos):
                        player.addCard(deck.pop())
                    if ddButton.checkForInput(mousePos):
                        player.setBet(2 * player.getBet())
                        player.addCard(deck.pop())
                        player.updateFunds(-1 * player.getBet())
                        readyToJudge = True

            x = 0
            for card in player.getHand():
                if x > 1:
                    screen.blit(pygame.image.load(card.getPath()), (100 * (x-1) + 450, 400))
                    pygame.display.update()
                x += 1
            continue
        
        x = 0
        for card in player.getHand():
            if x > 1:
                screen.blit(pygame.image.load(card.getPath()), (100 * (x-1) + 450, 400))
                pygame.display.update()
            x += 1

        while countHand(dealer.getHand()) < 17:
            dealer.addCard(deck.pop())

        screen.blit(dealerCard2, (450, 100))
        x = 0
        for card in dealer.getHand():
            if x > 1:
                screen.blit(pygame.image.load(card.getPath()), (100 * (x-1) + 450, 100))
                pygame.display.update()
            x += 1

        if countHand(player.getHand()) > 21:
            playerBustedMessage = font.render('You Busted!', True, black)
            screen.blit(playerBustedMessage, (300, 300))
            pygame.display.update()
        elif countHand(dealer.getHand()) > 21:
            dealerBustedMessage = font.render('The Dealer Busted! You Win!', True, black)
            screen.blit(dealerBustedMessage, (300, 300))
            pygame.display.update()
            if paid == False:
                player.updateFunds(2 * player.getBet())
                paid = True
        elif countHand(player.getHand()) > countHand(dealer.getHand()):
            playerWinMessage = font.render("You Beat The Dealer's hand!", True, black)
            screen.blit(playerWinMessage, (300, 300))
            pygame.display.update()
            if paid == False:
                player.updateFunds(2 * player.getBet())
                paid = True
        else:
            playerLossMessage = font.render("The Dealer Beat Your Hand", True, black)
            screen.blit(playerLossMessage, (300, 300))
            pygame.display.update()

        newRoundButton = Button(None, [400, 350], 'Begin New Round', font, black, 'gray')
        newRoundButton.update(screen)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if newRoundButton.checkForInput(mousePos):
                    newRound = True
