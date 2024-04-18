"""
This programs run Bingo using pygame with features such as betting, autoplay, 
manual plays, versus AI, respectively. 
Tri Tran
04/18/2024
Version: 3.11
"""
import pygame
import random
import sys

# Initialize Pygame and the game screen
pygame.init()
SCREEN_WIDTH, SCREEN_HEIGHT = 1200, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Bingo Game versus AI")

# Define used colors and fonts
BLACK = (0, 0, 0)
RED = (139, 0, 0)
WHITE = (255, 255, 255)
GOLD = (255, 215, 0)
GREEN = (0, 100, 0)
font = pygame.font.SysFont('Consolas', 24)
large_font = pygame.font.SysFont('Consolas', 72, bold=True)
x_font = pygame.font.SysFont('Consolas', 48, bold=True)


class Player:
    def __init__(self, balance=100):
        self.balance = balance  # Player's balances
        self.bet = 0  # Player's bet
        self.wins = 0  # Player's wins
        self.losses = 0  # Player's losses

    def place_bet(self, amount):
        if amount <= self.balance and amount > 0:
            self.balance -= amount
            self.bet += amount
            return True
        return False

    def win(self):
        self.balance += self.bet * 2
        self.bet = 0
        self.wins += 1

    def lose(self):
        self.bet = 0
        self.losses += 1

    def reset_bet(self):
        self.balance += self.bet
        self.bet = 0


# Creating instances of the Player for the Bingo.
player = Player(100)  # Starting the player with the balance of 100 dollars.
ai_players = [Player(100) for _ in range(2)]  # Create two AI players.


def get_font(size):
    # Get font for the board
    return pygame.font.Font("Ariel", size)


def auto_mark_player_board(drawn_number, card, marked_positions):
    # Player's card with randomized numbers
    for row in range(BINGO_CARD_SIZE):
        for col in range(BINGO_CARD_SIZE):
            # Check the card for the drawn number
            if card[row][col] == drawn_number:
                marked_positions.append((row, col))


def draw_player_stats(balance, bet, wins, losses, position):
    # Display player's game statistics
    x, y = position
    # Display the balance
    screen.blit(font.render(f"Balance: ${balance}", True, WHITE), (x, y))
    # Display the bet amount
    screen.blit(font.render(f"Current Bet: ${bet}", True, WHITE), (x, y + 30))
    # Display the number of wins
    screen.blit(font.render(f"Wins: {wins}", True, WHITE), (x, y + 60))
    # Display the number of losses
    screen.blit(font.render(f"Losses: {losses}", True, WHITE), (x, y + 90))


def draw_ai_stats(ai_player, position):
    # Display AI player's statistics
    x, y = position
    # Display the AI's number of wins
    screen.blit(font.render(f"AI Wins: {ai_player.wins}", True, WHITE), (x, y + 30))
    # Display the AI's number of losses
    screen.blit(font.render(f"AI Losses: {ai_player.losses}", True, WHITE), (x, y + 60))


def autoplay_game():
    # Track the game state
    global drawn_numbers, NUMBERS_RANGE
    last_drawn_number = None
    game_over = False
    winner = None

    # Continue the game until a win is detected
    while not game_over:
        # Randomly select a new number
        last_drawn_number = random.choice(NUMBERS_RANGE)
        drawn_numbers.append(last_drawn_number)
        NUMBERS_RANGE.remove(last_drawn_number)

        # Update player and AI cards with the new number
        auto_mark_player_board(last_drawn_number, player_card, marked_positions_player)

        # Determine the winner
        if check_win(marked_positions_player):  # Player's win check
            winner = "Player"
            game_over = True
        # Check each AI's win condition
        for ai_index, marks in enumerate(marked_positions_ai):
            if check_win(marks):
                winner = f"AI {ai_index + 1}"
                game_over = True

        # Display
        screen.fill(BLACK)  # Clear the screen
        # Draw the player's and AI's bingo cards with the marked numbers
        draw_bingo_card(player_card, (50, 50), drawn_numbers, marked_positions_player)
        for ai_index, ai_card in enumerate(ai_cards):
            draw_bingo_card(ai_card, (400 + ai_index * 300, 50), drawn_numbers, marked_positions_ai[ai_index])
        # Show the last number that was drawn
        draw_last_drawn_number(last_drawn_number)
        pygame.display.flip()  # Update the screen with the new drawing
        pygame.time.wait(500)

    # Game is over, return a winner
    return winner


def endgame_screen(winner):
    # The endgame message
    screen.fill(BLACK)
    # Display the winning message
    winner_text = large_font.render(f"{winner} wins!", True, GOLD)
    screen.blit(winner_text, (SCREEN_WIDTH // 2 - winner_text.get_width() // 2, SCREEN_HEIGHT // 2))
    # Draw buttons for playing again or quit
    replay_button = draw_button("Play Again", (SCREEN_WIDTH // 2 - 200, SCREEN_HEIGHT // 2 + 100))
    quit_button = draw_button("Quit", (SCREEN_WIDTH // 2 + 20, SCREEN_HEIGHT // 2 + 100))
    pygame.display.flip()  # Display with the endgame screen

    # Loop for the endgame screen
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # Exit
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:  # Check button clicks
                mouse_x, mouse_y = event.pos
                if replay_button.collidepoint((mouse_x, mouse_y)):
                    return "replay"  # Return 'replay'
                elif quit_button.collidepoint((mouse_x, mouse_y)):
                    return "quit"  # Return 'quit'


def generate_bingo_card():
    # Create a new Bingo card with random numbers
    card = []
    # Set up the for a  5x5 card
    col_ranges = [(i * 15 + 1, (i + 1) * 15) for i in range(BINGO_CARD_SIZE)]
    for col, (start, end) in enumerate(col_ranges):
        # Sample random numbers for each column
        numbers = random.sample(range(start, end + 1), BINGO_CARD_SIZE)
        for row, number in enumerate(numbers):
            if len(card) <= row:
                card.append([])
            # Append the number to the appropriate row
            card[row].append(number)
    # Return the completed card
    return card


# Bingo settings and variables
BINGO_CARD_SIZE = 5
NUMBERS_RANGE = list(range(1, 76))
player_card = generate_bingo_card()
ai_cards = [generate_bingo_card() for _ in range(2)]  # Two AI
drawn_numbers = []
marked_positions_player = []
marked_positions_ai = [[], []]  # Tracking marks for AI


def draw_bingo_card(card, pos, highlighted_nums, marked_positions):
    # Start drawing the Bingo card
    x, y = pos

    # Go over each row and column of the Bingo card
    for row in range(BINGO_CARD_SIZE):
        for col in range(BINGO_CARD_SIZE):
            cell_color = BLACK if (row + col) % 2 == 0 else RED
            cell_rect = pygame.Rect(x + col * 50, y + row * 50, 50, 50)
            # Draw the cell background
            pygame.draw.rect(screen, cell_color, cell_rect)
            # Draw the border
            pygame.draw.rect(screen, GOLD, cell_rect, 2)
            number = card[row][col]
            # Display the number as text
            text_surf = font.render(f'{number}', True, WHITE)
            screen.blit(text_surf, (cell_rect.x + 15, cell_rect.y + 10))
            # If the current position is marked, draw an 'X' over it
            if (row, col) in marked_positions:
                x_surf = x_font.render('X', True, GOLD)
                screen.blit(x_surf, (cell_rect.x + 5, cell_rect.y - 5))


def draw_player_stats(balance, bet, wins, losses, position):
    # Displays the player's game statistics
    x, y = position

    screen.blit(font.render(f"Balance: ${balance}", True, WHITE), (x, y + 30))
    screen.blit(font.render(f"Current Bet: ${bet}", True, WHITE), (x, y + 60))
    screen.blit(font.render(f"Wins: {wins}", True, WHITE), (x, y + 90))
    screen.blit(font.render(f"Losses: {losses}", True, WHITE), (x, y + 120))


def auto_mark_ai_boards(drawn_number):
    # Automatically mark the drawn number on AI's Bingo card.
    for ai_index, ai_card in enumerate(ai_cards):
        for row in range(BINGO_CARD_SIZE):
            for col in range(BINGO_CARD_SIZE):
                # If the drawn number is on the card MARK it.
                if ai_card[row][col] == drawn_number:
                    marked_positions_ai[ai_index].append((row, col))

def draw_last_drawn_number(number):
    # Display the last number drawn in the game.
    if number:  # Make sure the number is valid.
        number_surf = large_font.render(str(number), True, GOLD)
        screen.blit(number_surf, (SCREEN_WIDTH - 150, SCREEN_HEIGHT / 2 - 50))


def mark_number_if_drawn(pos, card, drawn, marked_positions):
    # Mark a number on the player's card if it's drawn.
    x, y = pos
    start_x, start_y = 50, 50
    cell_size = 50
    # Check if the mouse click.
    for row in range(BINGO_CARD_SIZE):
        for col in range(BINGO_CARD_SIZE):
            cell_x = start_x + col * cell_size
            cell_y = start_y + row * cell_size
            # If click the same as drawn number MARK it.
            if cell_x <= x <= cell_x + cell_size and cell_y <= y <= cell_y + cell_size:
                if card[row][col] in drawn and (row, col) not in marked_positions:
                    marked_positions.append((row, col))
                    return  # Exit after marking a single number.


def draw_button(text, position, size=(180, 40), color=GREEN):
    # Create a clickable button.
    button_rect = pygame.Rect(position, size)
    # Draw the button.
    pygame.draw.rect(screen, color, button_rect)
    # Putting the button text.
    text_surf = font.render(text, True, WHITE)
    text_rect = text_surf.get_rect(center=button_rect.center)
    screen.blit(text_surf, text_rect)
    return button_rect


def check_win(marked_positions):
    # Determine if a player has satisfied a winning condition.
    for line in range(BINGO_CARD_SIZE):
        # Check if all numbers in a row are marked.
        if all((line, col) in marked_positions for col in range(BINGO_CARD_SIZE)):
            return True
        # Check if all numbers in a column are marked.
        if all((row, line) in marked_positions for row in range(BINGO_CARD_SIZE)):
            return True
    # Check the diagonal from top-left to bottom-right.
    if all((i, i) in marked_positions for i in range(BINGO_CARD_SIZE)):
        return True
    # Check the diagonal from top-right to bottom-left.
    if all((i, BINGO_CARD_SIZE - 1 - i) in marked_positions for i in range(BINGO_CARD_SIZE)):
        return True
    # No win condition return False.
    return False


def main():
    # Manage the game loop for the bingo game.
    global NUMBERS_RANGE, player_card, ai_cards, drawn_numbers, marked_positions_player, marked_positions_ai, player, ai_players

    # Reset and start a new game.
    NUMBERS_RANGE = list(range(1, 76))  # Numbers range
    player_card = generate_bingo_card()  # Generate a new card for the player.
    ai_cards = [generate_bingo_card() for _ in range(2)]  # Generate cards for the AIs.
    drawn_numbers = []  # Track numbers that have been drawn.
    marked_positions_player = []  # Track marks.
    marked_positions_ai = [[] for _ in range(2)]  # Track marks on AI's cards.

    # Game Variables

    MIN_BET = 50
    autoplay = False
    game_over = False
    winner = None
    last_drawn_number = None
    draw_button_rect = None
    autoplay_button_rect = None
    bet_button_rect = None

    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # Check for window close.
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:  # Check for mouse clicks.
                mouse_x, mouse_y = event.pos
                # Track the betting.
                if bet_button_rect and bet_button_rect.collidepoint((mouse_x, mouse_y)):
                    if player.place_bet(MIN_BET):
                        continue
                # Track the number drawing.
                elif draw_button_rect and draw_button_rect.collidepoint((mouse_x, mouse_y)):
                    if NUMBERS_RANGE:
                        last_drawn_number = random.choice(NUMBERS_RANGE)
                        drawn_numbers.append(last_drawn_number)
                        NUMBERS_RANGE.remove(last_drawn_number)
                        auto_mark_player_board(last_drawn_number, player_card, marked_positions_player)
                        auto_mark_ai_boards(last_drawn_number)
                # Turn on/off autoplay.
                elif autoplay_button_rect and autoplay_button_rect.collidepoint((mouse_x, mouse_y)):
                    autoplay = not autoplay

        if autoplay and NUMBERS_RANGE:  # Autoplay drawing.
            pygame.time.wait(500)
            last_drawn_number = random.choice(NUMBERS_RANGE)
            drawn_numbers.append(last_drawn_number)
            NUMBERS_RANGE.remove(last_drawn_number)
            auto_mark_player_board(last_drawn_number, player_card, marked_positions_player)
            auto_mark_ai_boards(last_drawn_number)

        # Check for a win everytime a number is picked.
        if check_win(marked_positions_player):
            player.win()
            winner = "Player"
            game_over = True
        for ai_index, marks in enumerate(marked_positions_ai):
            if check_win(marks):
                ai_players[ai_index].win()
                winner = f"AI {ai_index + 1}"
                game_over = True

        # Take care of the end game and losses.
        if game_over:
            if winner != "Player":
                player.lose()
            for i, ai in enumerate(ai_players):
                if f"AI {i + 1}" != winner:
                    ai.lose()

        # Update the display.
        screen.fill(BLACK)
        draw_bingo_card(player_card, (50, 50), drawn_numbers, marked_positions_player)
        draw_player_stats(player.balance, player.bet, player.wins, player.losses, (50, 350))
        for ai_index, ai_card in enumerate(ai_cards):
            draw_bingo_card(ai_card, (400 + ai_index * 300, 50), drawn_numbers, marked_positions_ai[ai_index])
            draw_ai_stats(ai_players[ai_index], (400 + ai_index * 300, 350))
        if last_drawn_number is not None:
            draw_last_drawn_number(last_drawn_number)
        draw_button_rect = draw_button("Draw Number", (SCREEN_WIDTH // 2 - 60, 550))
        autoplay_button_rect = draw_button("Autoplay: ON" if autoplay else "Autoplay: OFF",
                                           (SCREEN_WIDTH // 2 - 250, 550))
        bet_button_rect = draw_button("Place Bet: $50", (SCREEN_WIDTH // 2 - 450, 550))

        pygame.display.flip()

    action = endgame_screen(winner)  # Display the end game screen.
    if action == "replay":
        main()  # Restart.
    else:
        pygame.quit()  # End the game.


if __name__ == '__main__':
    main()
