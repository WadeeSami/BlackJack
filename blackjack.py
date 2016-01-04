# Mini-project #6 - Blackjack

import simplegui
import random

# load card sprite - 936x384 - source: jfitz.com
CARD_SIZE = (72, 96)
CARD_CENTER = (36, 48)
card_images = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/cards_jfitz.png")

CARD_BACK_SIZE = (72, 96)
CARD_BACK_CENTER = (36, 48)
card_back = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/card_jfitz_back.png")    

# initialize some useful global variables
in_play = False
outcome = ""
score = 0
deck = ""
player = ""
dealer = ""
# define globals for cards
SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':10, 'Q':10, 'K':10}


# define card class
class Card:
    def __init__(self, suit, rank):
        if (suit in SUITS) and (rank in RANKS):
            self.suit = suit
            self.rank = rank
        else:
            self.suit = None
            self.rank = None
            print "Invalid card: ", suit, rank

    def __str__(self):
        return self.suit + self.rank

    def get_suit(self):
        return self.suit

    def get_rank(self):
        return self.rank

    def draw(self, canvas, pos):
        card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(self.rank), 
                    CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(self.suit))
        canvas.draw_image(card_images, card_loc, CARD_SIZE, [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]], CARD_SIZE)
        
# define hand class
class Hand:
    def __init__(self):
        #should initialize the hand object to have an empty list of cards
        self.cards = []

    def __str__(self):
        contains = ""
        if self.cards == []:
            contains = ""
        else:
            for card in self.cards:
                contains += " " + card.get_suit() + card.get_rank() 
        return "Hand contains" +  contains +  "  " + str(self.get_value())

    def add_card(self, card):
        self.cards.append(card)

    def get_value(self):
        value = 0
        aces = False # a flag to determine if aces exists in the hand of the player or the dealer
        if self.cards == [] :
            return 0
        for card in self.cards:
            if card.get_rank() != 'A':
                value += VALUES[card.get_rank()]
            else :#this is an Ace
                #print "Ace :3"
                value += 1
                aces = True
        if aces:
            if value + 10 <= 21:
                value += 10
        return value          
    def draw(self, canvas, pos):
        i = 0
        for card in self.cards:
            pos[0] += i
            card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(card.get_rank() ), 
                        CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(card.get_suit() ) )
            canvas.draw_image(card_images, card_loc, CARD_SIZE, [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]], CARD_SIZE)
            i += CARD_SIZE[0] + 20  
# define deck class 
class Deck:

    def __init__(self):
        #initialze the deck, it should contain all the types of cards
        self.deck = []
        for s in SUITS:
            for r in RANKS:
                self.deck.append(Card(s , r))  
        #shulffle the deck
        self.shuffle()         
    def shuffle(self):
        # shuffle the deck 
        random.shuffle(self.deck)

    def deal_card(self):
        return self.deck.pop()

    
    def __str__(self):
        contains = ""
        if self.deck == []:
            contains = ""
        else:
            for card in self.deck:
                contains += " " + card.get_suit() + card.get_rank() 
        return "Deck contains" +  contains
        

#define event handlers for buttons
def deal():
    print "new deal"
    global outcome, in_play , deck , player , dealer , score
    #create a new Deck , new player and dealer hands and shuffle the deck
    deck = Deck()# already shuffled 
    player = Hand()
    dealer = Hand()
    #add cards for both the dealer and the player
    print "player"
    card1 = deck.deal_card()
    card2 = deck.deal_card()
    player.add_card(card1)
    player.add_card(card2)
    card1 = deck.deal_card()
    card2 = deck.deal_card()
    dealer.add_card(card1)
    dealer.add_card(card2)

    print player
    print "dealer"
    print dealer
    in_play = True
    if player.get_value() == 21:
        score+= 1
        outcome = "You Win"
        in_play = False
    elif dealer.get_value() == 21:
        score-= 1
        outcome = "You Lose"
        in_play = False

def hit():
    global outcome , deck , in_play , score
        # replace with your code below
    print "hit"
    # if the hand is in play, hit the player
    if in_play:
        #get acard from the deck
        card = deck.deal_card()
        player.add_card(card)
        # if busted, assign a message to outcome, update in_play and score
        if player.get_value() > 21:
                outcome = "You lost"
                score -= 1
                in_play = False   
        print "player  " + str(player)
        print "dealer  " + str(dealer)
        print "The score is " + str(score)
        print "Message is :  " + str(outcome)
    else :
        print "you should start a new game"    
def stand():
    global score , outcome , in_play
    print "stand"
    if not in_play:
        print "you should start a new game"
        return
    if dealer.get_value() >= 17:
        print "can't stand , you have to hit :3"
        return 
    # if hand is in play, repeatedly hit dealer until his hand has value 17 or more
    while dealer.get_value() < 17:
        dealer.add_card(deck.deal_card())
    # assign a message to outcome, update in_play and score
    if dealer.get_value() > 21:
        outcome = "You Win"
        in_play = False
        score += 1
    elif dealer.get_value() >= player.get_value():    
        outcome = "You Lose"
        in_play = False
        score -= 1
    elif dealer.get_value() < player.get_value(): 
        outcome = "You Win"
        in_play = False
        score += 1
    print "player  " + str(player)
    print "dealer  " + str(dealer)
    print "The score is " + str(score)
    print "Message is :  " + outcome
        
# draw handler    
def draw(canvas):
    # test to make sure that card.draw works, replace with your code below
    dealer.draw(canvas , [40 ,40 ])
    player.draw(canvas , [40 , 300])
    #card = Card("S", "A")
    #card.draw(canvas, [300, 300])


# initialization frame
frame = simplegui.create_frame("Blackjack", 600, 600)
frame.set_canvas_background("Green")

#create buttons and canvas callback
frame.add_button("Deal", deal, 200)
frame.add_button("Hit",  hit, 200)
frame.add_button("Stand", stand, 200)
frame.set_draw_handler(draw)


# get things rolling
deal()
frame.start()


# remember to review the gradic rubric