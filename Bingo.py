import pygame
import random
import sys

# Initialize Pygame and set up the wider screen
pygame.init()
SCREEN_WIDTH, SCREEN_HEIGHT = 1200, 600  # Adjusted width to accommodate more boards
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Expanded Bingo Game with AI Players")

# Define colors and fonts
BLACK, RED, WHITE, GOLD, GREEN = (0, 0, 0), (139, 0, 0), (255, 255, 255), (255, 215, 0), (0, 100, 0)
font = pygame.font.SysFont('Consolas', 24)
large_font = pygame.font.SysFont('Consolas', 72, bold=True)
x_font = pygame.font.SysFont('Consolas', 48, bold=True)

class Player:
    def __init__(self, balance=100):
        self.balance = balance
        self.bet = 0
        self.wins = 0
        self.losses = 0

    def place_bet(self, amount):
        if amount <= self.balance and amount > 0:
            self.balance -= amount
            self.bet += amount
            return True
        return False

    def win(self):
        # Double the bet amount on win
        self.balance += self.bet * 2
        self.bet = 0
        self.wins += 1

    def lose(self):
        self.bet = 0
        self.losses += 1

    def reset_bet(self):
        self.balance += self.bet
        self.bet = 0

player = Player(100)
ai_players = [Player(100) for _ in range(2)]  # Two AI players

def get_font(size):
    return pygame.font.Font("assets/font.ttf", size)

def auto_mark_player_board(drawn_number, card, marked_positions):
    for row in range(BINGO_CARD_SIZE):
        for col in range(BINGO_CARD_SIZE):
            if card[row][col] == drawn_number:
                marked_positions.append((row, col))

def draw_player_stats(balance, bet, wins, losses, position):
    """Displays the player's balance, current bet, wins, and losses below the bingo card."""
    x, y = position
    screen.blit(font.render(f"Balance: ${balance}", True, WHITE), (x, y))
    screen.blit(font.render(f"Current Bet: ${bet}", True, WHITE), (x, y + 30))
    screen.blit(font.render(f"Wins: {wins}", True, WHITE), (x, y + 60))
    screen.blit(font.render(f"Losses: {losses}", True, WHITE), (x, y + 90))

def draw_ai_stats(ai_player, position):
    """Displays AI stats including wins and losses."""
    x, y = position
    screen.blit(font.render(f"AI Wins: {ai_player.wins}", True, WHITE), (x, y+30))
    screen.blit(font.render(f"AI Losses: {ai_player.losses}", True, WHITE), (x, y + 60))


def autoplay_game():
    global drawn_numbers, NUMBERS_RANGE
    last_drawn_number = None
    game_over = False
    winner = None

    while not game_over:
        # Draw a number
        last_drawn_number = random.choice(NUMBERS_RANGE)
        drawn_numbers.append(last_drawn_number)
        NUMBERS_RANGE.remove(last_drawn_number)

        # Auto-mark cards
        auto_mark_player_board(last_drawn_number, player_card, marked_positions_player)
        auto_mark_ai_boards(last_drawn_number)

        # Check for a win
        if check_win(marked_positions_player):
            winner = "Player"
            game_over = True
        for ai_index, marks in enumerate(marked_positions_ai):
            if check_win(marks):
                winner = f"AI {ai_index + 1}"
                game_over = True

        # Update the display
        screen.fill(BLACK)
        draw_bingo_card(player_card, (50, 50), drawn_numbers, marked_positions_player)
        for ai_index, ai_card in enumerate(ai_cards):
            draw_bingo_card(ai_card, (400 + ai_index * 300, 50), drawn_numbers, marked_positions_ai[ai_index])
        draw_last_drawn_number(last_drawn_number)
        draw_rules()
        pygame.display.flip()
        pygame.time.wait(500)  # Delay to simulate time taken for drawing a number

    return winner

def endgame_screen(winner):
    screen.fill(BLACK)
    winner_text = large_font.render(f"{winner} wins!", True, GOLD)
    screen.blit(winner_text, (SCREEN_WIDTH // 2 - winner_text.get_width() // 2, SCREEN_HEIGHT // 2))
    replay_button = draw_button("Play Again", (SCREEN_WIDTH // 2 - 200, SCREEN_HEIGHT // 2 + 100))
    quit_button = draw_button("Quit", (SCREEN_WIDTH // 2 + 20, SCREEN_HEIGHT // 2 + 100))
    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos
                if replay_button.collidepoint((mouse_x, mouse_y)):
                    return "replay"
                elif quit_button.collidepoint((mouse_x, mouse_y)):
                    return "quit"

def generate_bingo_card():
    """Generates and returns a 5x5 Bingo card with random numbers."""
    card = []
    col_ranges = [(i * 15 + 1, (i + 1) * 15) for i in range(BINGO_CARD_SIZE)]
    for col, (start, end) in enumerate(col_ranges):
        numbers = random.sample(range(start, end + 1), BINGO_CARD_SIZE)
        for row, number in enumerate(numbers):
            if len(card) <= row:
                card.append([])
            card[row].append(number)
    return card


# Bingo settings and variables

BINGO_CARD_SIZE = 5
NUMBERS_RANGE = list(range(1, 76))
player_card = generate_bingo_card()
ai_cards = [generate_bingo_card() for _ in range(2)]  # Two AI players
drawn_numbers = []
marked_positions_player = []
marked_positions_ai = [[], []]  # Tracking marks for AI players


def draw_bingo_card(card, pos, highlighted_nums, marked_positions):
    """Draws the Bingo card at a given position."""
    x, y = pos
    for row in range(BINGO_CARD_SIZE):
        for col in range(BINGO_CARD_SIZE):
            cell_color = BLACK if (row + col) % 2 == 0 else RED
            cell_rect = pygame.Rect(x + col * 50, y + row * 50, 50, 50)
            pygame.draw.rect(screen, cell_color, cell_rect)
            pygame.draw.rect(screen, GOLD, cell_rect, 2)
            number = card[row][col]
            text_surf = font.render(f'{number}', True, WHITE)
            screen.blit(text_surf, (cell_rect.x + 15, cell_rect.y + 10))
            if (row, col) in marked_positions:
                x_surf = x_font.render('X', True, GOLD)
                screen.blit(x_surf, (cell_rect.x + 5, cell_rect.y - 5))


def draw_player_stats(balance, bet, wins, losses, position):
    """Displays the player's balance, current bet, wins, and losses below the bingo card."""
    x, y = position
    screen.blit(font.render(f"Balance: ${balance}", True, WHITE), (x, y + 30))
    screen.blit(font.render(f"Current Bet: ${bet}", True, WHITE), (x, y + 60))
    screen.blit(font.render(f"Wins: {wins}", True, WHITE), (x, y + 90))
    screen.blit(font.render(f"Losses: {losses}", True, WHITE), (x, y + 120))



def auto_mark_ai_boards(drawn_number):
    """Automatically marks the drawn number on AI boards."""
    for ai_index, ai_card in enumerate(ai_cards):
        for row in range(BINGO_CARD_SIZE):
            for col in range(BINGO_CARD_SIZE):
                if ai_card[row][col] == drawn_number:
                    marked_positions_ai[ai_index].append((row, col))


def draw_last_drawn_number(number):
    """Displays the last drawn number prominently on the screen."""
    if number:
        number_surf = large_font.render(str(number), True, GOLD)
        screen.blit(number_surf, (SCREEN_WIDTH - 150, SCREEN_HEIGHT / 2 - 50))


def calculate_needed_numbers_probability(card, drawn, range_):
    """Calculates and returns the probability of drawing a needed number."""
    needed_numbers = [num for row in card for num in row if num not in drawn]
    needed_count = len(needed_numbers)
    total_count = len(range_)
    probability = needed_count / total_count if total_count > 0 else 0
    return probability, needed_numbers


def mark_number_if_drawn(pos, card, drawn, marked_positions):
    x, y = pos
    start_x, start_y = 50, 50  # Adjust these values based on where your card starts
    cell_size = 50
    for row in range(BINGO_CARD_SIZE):
        for col in range(BINGO_CARD_SIZE):
            cell_x = start_x + col * cell_size
            cell_y = start_y + row * cell_size
            if cell_x <= x <= cell_x + cell_size and cell_y <= y <= cell_y + cell_size:
                if card[row][col] in drawn and (row, col) not in marked_positions:
                    marked_positions.append((row, col))
                    return  # Only mark one number per click


def draw_probability(probability, needed_numbers):
    """Displays the probability and needed numbers on the screen."""
    prob_text = f"Prob. of Next Needed Number: {probability * 100:.2f}%"
    prob_surf = font.render(prob_text, True, WHITE)
    screen.blit(prob_surf, (20, SCREEN_HEIGHT - 80))

    needed_text = f"Needed: {', '.join(map(str, needed_numbers[:5]))}{'...' if len(needed_numbers) > 5 else ''}"
    needed_surf = font.render(needed_text, True, WHITE)
    screen.blit(needed_surf, (20, SCREEN_HEIGHT - 40))


def draw_button(text, position, size=(180, 40), color=GREEN):
    """Draws a button and returns its Rect."""
    button_rect = pygame.Rect(position, size)
    pygame.draw.rect(screen, color, button_rect)
    text_surf = font.render(text, True, WHITE)
    text_rect = text_surf.get_rect(center=button_rect.center)
    screen.blit(text_surf, text_rect)
    return button_rect


def check_win(marked_positions):
    """Checks for a win given marked positions on a card."""
    # Check rows, columns, and diagonals for a complete set of marks
    for line in range(BINGO_CARD_SIZE):
        if all((line, col) in marked_positions for col in range(BINGO_CARD_SIZE)) or \
                all((row, line) in marked_positions for row in range(BINGO_CARD_SIZE)):
            return True
    if all((i, i) in marked_positions for i in range(BINGO_CARD_SIZE)) or \
            all((i, BINGO_CARD_SIZE - 1 - i) in marked_positions for i in range(BINGO_CARD_SIZE)):
        return True
    return False


def main():
    global NUMBERS_RANGE, player_card, ai_cards, drawn_numbers, marked_positions_player, marked_positions_ai, player, ai_players

    # Resetting game specific variables
    NUMBERS_RANGE = list(range(1, 76))
    player_card = generate_bingo_card()
    ai_cards = [generate_bingo_card() for _ in range(2)]
    drawn_numbers = []
    marked_positions_player = []
    marked_positions_ai = [[] for _ in range(2)]
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
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos
                if bet_button_rect and bet_button_rect.collidepoint((mouse_x, mouse_y)):
                    if player.place_bet(MIN_BET):
                        continue
                elif draw_button_rect and draw_button_rect.collidepoint((mouse_x, mouse_y)):
                    if NUMBERS_RANGE:
                        last_drawn_number = random.choice(NUMBERS_RANGE)
                        drawn_numbers.append(last_drawn_number)
                        NUMBERS_RANGE.remove(last_drawn_number)
                        auto_mark_player_board(last_drawn_number, player_card, marked_positions_player)
                        auto_mark_ai_boards(last_drawn_number)

                elif autoplay_button_rect and autoplay_button_rect.collidepoint((mouse_x, mouse_y)):
                    autoplay = not autoplay

        if autoplay and NUMBERS_RANGE:
            pygame.time.wait(500)
            last_drawn_number = random.choice(NUMBERS_RANGE)
            drawn_numbers.append(last_drawn_number)
            NUMBERS_RANGE.remove(last_drawn_number)
            auto_mark_player_board(last_drawn_number, player_card, marked_positions_player)
            auto_mark_ai_boards(last_drawn_number)

        # Check for a win
        if check_win(marked_positions_player):
            player.win()
            winner = "Player"
            game_over = True
        for ai_index, marks in enumerate(marked_positions_ai):
            if check_win(marks):
                ai_players[ai_index].win()
                winner = f"AI {ai_index + 1}"
                game_over = True

        if game_over:
            if winner != "Player":
                player.lose()
            for i, ai in enumerate(ai_players):
                if f"AI {i + 1}" != winner:
                    ai.lose()

        # Update the display
        screen.fill(BLACK)
        draw_bingo_card(player_card, (50, 50), drawn_numbers, marked_positions_player)
        draw_player_stats(player.balance, player.bet, player.wins, player.losses, (50, 350))
        for ai_index, ai_card in enumerate(ai_cards):
            draw_bingo_card(ai_card, (400 + ai_index * 300, 50), drawn_numbers, marked_positions_ai[ai_index])
            draw_ai_stats(ai_players[ai_index], (400 + ai_index * 300, 350))
        if last_drawn_number is not None:
            draw_last_drawn_number(last_drawn_number)
        draw_button_rect = draw_button("Draw Number", (SCREEN_WIDTH // 2 - 60, 550))
        autoplay_button_rect = draw_button("Autoplay: ON" if autoplay else "Autoplay: OFF", (SCREEN_WIDTH // 2 - 250, 550))
        bet_button_rect = draw_button("Place Bet: $50", (SCREEN_WIDTH // 2 - 450, 550))

        pygame.display.flip()

    action = endgame_screen(winner)
    if action == "replay":
        main()
    else:
        pygame.quit()

if __name__ == '__main__':
    main()
