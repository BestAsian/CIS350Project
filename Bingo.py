import pygame
import random
import sys

# Initialize Pygame and set up the wider screen
pygame.init()
SCREEN_WIDTH, SCREEN_HEIGHT = 1200, 600  # Adjusted width to accommodate more boards
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Expanded Bingo Game with AI Players")

# Define colors and fonts
BLACK, RED, WHITE, GOLD, GREEN = (0, 0, 0), (139, 0, 0), (255, 255, 255), (255, 215, 0), (0, 255, 0)
font = pygame.font.SysFont('Consolas', 24)
large_font = pygame.font.SysFont('Consolas', 72, bold=True)
x_font = pygame.font.SysFont('Consolas', 48, bold=True)


def get_font(size):
    return pygame.font.Font("assets/font.ttf", size)


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


def draw_rules():
    """Displays the rules of Bingo below the user's card."""
    rules = [
        "Rules of Bingo:",
        "1. Numbers will be drawn randomly.",
        "2. If the drawn number is on your card, click it to mark it out.",
        "3. First to complete a row, column, or diagonal wins.",
        "4. Press 'Draw Number' to draw a new number."
    ]
    start_y = SCREEN_HEIGHT - 250
    for i, rule in enumerate(rules):
        rule_surf = font.render(rule, True, WHITE)
        screen.blit(rule_surf, (20, start_y + i * 20))

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
    global NUMBERS_RANGE, drawn_numbers
    last_drawn_number = None
    game_over = False
    winner = None

    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and not game_over:
                mouse_x, mouse_y = event.pos
                if exit_button_rect.collidepoint(event.pos):
                    return
                if draw_button_rect and not draw_button_rect.collidepoint(mouse_x, mouse_y):
                    mark_number_if_drawn((mouse_x, mouse_y), player_card, drawn_numbers, marked_positions_player)
                if draw_button_rect and draw_button_rect.collidepoint(mouse_x, mouse_y) and NUMBERS_RANGE:
                    last_drawn_number = random.choice(NUMBERS_RANGE)
                    drawn_numbers.append(last_drawn_number)
                    NUMBERS_RANGE.remove(last_drawn_number)
                    # Auto-mark for player and AI
                    mark_number_if_drawn((mouse_x, mouse_y), player_card, drawn_numbers, marked_positions_player)
                    auto_mark_ai_boards(last_drawn_number)
                    # Check for win
                    if check_win(marked_positions_player):
                        winner = "Player"
                        game_over = True
                    for ai_index, marks in enumerate(marked_positions_ai):
                        if check_win(marks):
                            winner = f"AI {ai_index + 1}"
                            game_over = True

        screen.fill(BLACK)
        draw_bingo_card(player_card, (50, 50), drawn_numbers, marked_positions_player)
        for ai_index, ai_card in enumerate(ai_cards):
            draw_bingo_card(ai_card, (400 + ai_index * 300, 50), drawn_numbers, marked_positions_ai[ai_index])
        draw_last_drawn_number(last_drawn_number)
        draw_button_rect = draw_button("Draw Number", (SCREEN_WIDTH // 2 - 60, 550))
        exit_button_rect = draw_button("Exit", (SCREEN_WIDTH - 200, 550))
        draw_rules()  # Display Bingo rules below the user's card

        if game_over:
            winner_text = large_font.render(f"{winner} wins!", True, GOLD)
            screen.blit(winner_text, (SCREEN_WIDTH // 2 - winner_text.get_width() // 2, SCREEN_HEIGHT // 2))
            pygame.time.wait(3000)
            return

        pygame.display.flip()


if __name__ == '__main__':
    main()
