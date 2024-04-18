import pygame
import random
import time


# Initialize Pygame
pygame.init()

# Set up display
BG = pygame.image.load("assets/Background.png")
HEADS = pygame.image.load("assets/HEADS.png")
TAILS = pygame.image.load("assets/TAILS.png")

WIDTH, HEIGHT = 1280, 720
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Coin Flip Game")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
GRAY = (128, 128, 128)

mainClock = pygame.time.Clock()

# Fonts
FONT = pygame.font.SysFont(None, 50)


# Function to flip the coin
def flip_coin():
    return random.choice(["HEADS", "TAILS"])


# Function to update the balance based on the outcome
def update_balance(outcome, bet_amount, balance, win):
    if win:
        return balance + bet_amount
    else:
        return balance - bet_amount


# Function to display the result of the coin flip
def display_result(outcome):
    result_text = FONT.render(f"The result is: {outcome}", True, BLACK)
    WIN.blit(result_text, (WIDTH // 2 - result_text.get_width() // 2, HEIGHT // 2 + 50))
    if outcome == "HEADS":
        WIN.blit(HEADS, (500, 50))
    elif outcome == "TAILS":
        WIN.blit(TAILS, (500, 50))
    pygame.time.wait(20)
    pygame.display.update()


# Function to display the current balance and current bet
def display_info(balance, current_bet, current_selection):
    balance_text = FONT.render(f"Balance: {balance}", True, BLACK)
    WIN.blit(balance_text, (10, 10))

    current_bet_text = FONT.render(f"Current Bet: {current_bet}", True, BLACK)
    WIN.blit(current_bet_text, (10, 70))

    current_bet_text = FONT.render(f"Current Choice: {current_selection}", True, BLACK)
    WIN.blit(current_bet_text, (10, 130))

    pygame.display.update()


# Function to draw the chip buttons
def draw_chips(current_bet):
    chip_sizes = [1, 5, 10, 20, 100]
    chip_colors = [GRAY if current_bet != size else GREEN for size in chip_sizes]
    chip_radius = 30
    chip_spacing = 20
    chip_y = HEIGHT - 100

    for i, size in enumerate(chip_sizes):
        pygame.draw.circle(WIN, chip_colors[i],
                           (chip_spacing + (2 * chip_radius + chip_spacing) * i + chip_radius, chip_y + chip_radius),
                           chip_radius)
        chip_text = FONT.render(str(size), True, BLACK)
        WIN.blit(chip_text, (
        chip_spacing + (2 * chip_radius + chip_spacing) * i + chip_radius - chip_text.get_width() // 2,
        chip_y + chip_radius - chip_text.get_height() // 2))


# Function to check if the bet amount is valid
def is_valid_bet(amount, balance):
    if amount <= balance:
        return True
    else:
        return False


# Main function to play the game
def main():
    balance = 1000
    current_bet = 0
    selected_outcome = None

    run = True
    while run:
        WIN.blit(BG, (0, 0))
        draw_chips(current_bet)
        display_info(balance, current_bet, selected_outcome)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                chip_sizes = [1, 5, 10, 20, 100]
                chip_radius = 30
                chip_spacing = 20
                chip_y = HEIGHT - 100

                for i, size in enumerate(chip_sizes):
                    chip_x = chip_spacing + (2 * chip_radius + chip_spacing) * i + chip_radius
                    if pygame.math.Vector2(chip_x, chip_y + chip_radius).distance_to(
                            pygame.math.Vector2(mouse_x, mouse_y)) <= chip_radius:
                        current_bet += size
                        break

                if 500 <= mouse_x <= 670 and 490 <= mouse_y <= 570:
                    selected_outcome = "HEADS"
                elif 500 <= mouse_x <= 670 and 590 <= mouse_y <= 670:
                    selected_outcome = "TAILS"
                elif 700 <= mouse_x <= 850 and 500 <= mouse_y <= 570:
                    if current_bet > 0:
                        if not is_valid_bet(current_bet, balance):
                            invalidbet_text = FONT.render(f"{current_bet} is greater than your balance.", True, (255, 0, 0))
                            WIN.blit(invalidbet_text, (300, 500))
                            pygame.display.update()
                            time.sleep(2)
                        else:
                            outcome = flip_coin()
                            display_result(outcome)
                            if outcome == selected_outcome:
                                balance = update_balance(outcome, current_bet, balance, 1)
                            else:
                                balance = update_balance(outcome, current_bet, balance, 0)
                            current_bet = 0
                            time.sleep(2)
                elif 700 <= mouse_x <= 930 and 600 <= mouse_y <= 670:
                    # Clear bet button
                    current_bet = 0
                # Check if "Back to Menu" button is clicked
                elif 1100 <= mouse_x <= 1200 and 50 <= mouse_y <= 100:
                    return

        # Draw the buttons
        pygame.draw.rect(WIN, GRAY, (510, 500, 150, 70))  # HEADS button
        pygame.draw.rect(WIN, GRAY, (510, 600, 150, 70))  # TAILS button
        pygame.draw.rect(WIN, GREEN if current_bet > 0 else GRAY, (700, 500, 150, 70))  # FLIP button
        pygame.draw.rect(WIN, GRAY, (700, 600, 230, 70))  # Clear Bet button

        # Display the button texts
        heads_text = FONT.render("HEADS", True, BLACK)
        WIN.blit(heads_text, (530, 520))

        tails_text = FONT.render("TAILS", True, BLACK)
        WIN.blit(tails_text, (535, 620))

        flip_text = FONT.render("FLIP", True, BLACK)
        WIN.blit(flip_text, (740, 520))

        clear_bet_text = FONT.render("CLEAR BET", True, BLACK)
        WIN.blit(clear_bet_text, (715, 620))

        # Draw the "Back to Menu" button
        pygame.draw.rect(WIN, GRAY, (1100, 50, 100, 50))
        back_text = FONT.render("Back", True, BLACK)
        WIN.blit(back_text, (1110, 60))

        pygame.display.update()
        mainClock.tick(4)




if __name__ == "__main__":
    main()
