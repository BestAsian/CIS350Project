import pygame
import random
import math
import sys

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
LIGHT_GREY = (200, 200, 200)
DARK_GREY = (50, 50, 50)

# Roulette properties
WHEEL_RADIUS = 300
BALL_RADIUS = 12
NUM_SLOTS = 37

# Player properties
INITIAL_BALANCE = 1000

# Initialize screen and clock
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Roulette Game")
clock = pygame.time.Clock()

# Define buttons for betting on colors and specific bet amounts
type_buttons = [
    {"rect": pygame.Rect(50, 700, 120, 60), "text": "Red", "type": "red"},
    {"rect": pygame.Rect(200, 700, 120, 60), "text": "Black", "type": "black"},
]

bet_buttons = [
    {"rect": pygame.Rect(50, 600, 120, 60), "text": "Bet $5", "bet": 5},
    {"rect": pygame.Rect(200, 600, 120, 60), "text": "Bet $10", "bet": 10},
    {"rect": pygame.Rect(350, 600, 120, 60), "text": "Bet $100", "bet": 100},
]

# Font for button text
button_font = pygame.font.SysFont("Arial", 24)

# Initialize game state variables
ball_spinning = False
ball_angle = 0
ball_spin_speed = 0
target_slot = None
balance = INITIAL_BALANCE
bet_amount = 0
last_bet_info = ""
bet_type = None


def draw_wheel(angle):
    number_font = pygame.font.SysFont("Arial", 20)
    for i in range(NUM_SLOTS):
        slot_angle_degrees = (360 / NUM_SLOTS) * i + angle
        radian_angle = math.radians(slot_angle_degrees)
        if i == 0:
            color = GREEN
        else:
            color = RED if i % 2 == 0 else BLACK
        pygame.draw.polygon(screen, color, [
            (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2),
            (SCREEN_WIDTH // 2 + math.cos(radian_angle) * WHEEL_RADIUS,
             SCREEN_HEIGHT // 2 + math.sin(radian_angle) * WHEEL_RADIUS),
            (SCREEN_WIDTH // 2 + math.cos(radian_angle + math.radians(360 / NUM_SLOTS)) * WHEEL_RADIUS,
             SCREEN_HEIGHT // 2 + math.sin(radian_angle + math.radians(360 / NUM_SLOTS)) * WHEEL_RADIUS)])

        text = number_font.render(str(i), True, WHITE if i != 0 else BLACK)
        text_x = SCREEN_WIDTH // 2 + math.cos(radian_angle + math.radians(180 / NUM_SLOTS)) * (WHEEL_RADIUS - 50)
        text_y = SCREEN_HEIGHT // 2 + math.sin(radian_angle + math.radians(180 / NUM_SLOTS)) * (WHEEL_RADIUS - 50)
        text_rect = text.get_rect(center=(text_x, text_y))
        screen.blit(text, text_rect)


def draw_ball(angle):
    global ball_spinning, ball_angle, ball_spin_speed, target_slot, balance, bet_amount, last_bet_info
    x = SCREEN_WIDTH // 2 + math.cos(angle) * (WHEEL_RADIUS - BALL_RADIUS * 3)
    y = SCREEN_HEIGHT // 2 + math.sin(angle) * (WHEEL_RADIUS - BALL_RADIUS * 3)
    pygame.draw.circle(screen, WHITE, (int(x), int(y)), BALL_RADIUS)


def display_info(balance, bet_type, bet_amount, last_bet_info):
    font = pygame.font.SysFont(None, 36)
    balance_text = font.render(f"Balance: ${balance}", True, WHITE)
    screen.blit(balance_text, (10, 10))
    bet_text = font.render(f"Bet on: {bet_type}, Amount: ${bet_amount}", True, WHITE)
    screen.blit(bet_text, (10, 50))
    last_bet_info_text = font.render(last_bet_info, True, WHITE)
    screen.blit(last_bet_info_text, (SCREEN_WIDTH - 400, 650))


def handle_buttons(mouse_pos):
    all_buttons = type_buttons + bet_buttons
    for button in all_buttons:
        color = LIGHT_GREY if button["rect"].collidepoint(mouse_pos) else DARK_GREY
        pygame.draw.rect(screen, color, button["rect"])
        text_surf = button_font.render(button["text"], True, WHITE)
        text_rect = text_surf.get_rect(center=button["rect"].center)
        screen.blit(text_surf, text_rect)


def check_click(mouse_pos):
    all_buttons = type_buttons + bet_buttons
    for button in all_buttons:
        if button["rect"].collidepoint(mouse_pos):
            return button
    return None


def calculate_slot(angle):
    degrees_per_slot = 360 / NUM_SLOTS
    normalized_angle = math.degrees(angle) % 360
    slot_number = int(normalized_angle / degrees_per_slot)
    return slot_number


def main():
    global ball_spinning, ball_angle, ball_spin_speed, target_slot, balance, bet_amount, last_bet_info, bet_type

    running = True
    while running:
        mouse_pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and not ball_spinning:
                clicked_button = check_click(mouse_pos)
                if clicked_button:
                    if "bet" in clicked_button:
                        temp_bet_amount = clicked_button["bet"]
                        if balance - temp_bet_amount >= 0:
                            bet_amount += temp_bet_amount
                            balance -= temp_bet_amount
                            last_bet_info = f"Total Bet: ${bet_amount}"
                        else:
                            last_bet_info = "Insufficient balance!"
                    elif "type" in clicked_button:
                        bet_type = clicked_button["type"]
                        if bet_amount > 0 and bet_type in ["red", "black"]:
                            ball_spinning = True
                            ball_spin_speed = 0.2 + random.uniform(-0.01, 0.01)
                            target_slot = random.randint(0, NUM_SLOTS - 1)
                            last_bet_info = f"Betting ${bet_amount} on {bet_type}"

        if ball_spinning:
            ball_angle += ball_spin_speed
            ball_spin_speed *= 0.99
            if ball_spin_speed < 0.05:
                ball_spinning = False
                final_slot = calculate_slot(ball_angle)
                winning_color = "red" if final_slot % 2 == 0 else "black"
                if final_slot == 0:
                    winning_color = "green"

                if (bet_type == winning_color) or (bet_type == "green" and final_slot == 0):
                    balance += bet_amount * 2
                    outcome_msg = "Win!"
                else:
                    outcome_msg = "Lose!"
                last_bet_info = f"Landed on: {final_slot} ({winning_color}). {outcome_msg}"
                bet_amount = 0
                bet_type = None

        screen.fill(BLACK)
        draw_wheel(0)
        draw_ball(ball_angle)
        display_info(balance, bet_type if bet_type else "none", bet_amount, last_bet_info)
        handle_buttons(mouse_pos)

        # Draw back button at the top right corner
        back_button_rect = pygame.Rect(SCREEN_WIDTH - 110, 10, 100, 50)
        pygame.draw.rect(screen, RED, back_button_rect)
        back_button_text = button_font.render("Back", True, WHITE)
        back_button_text_rect = back_button_text.get_rect(center=back_button_rect.center)
        screen.blit(back_button_text, back_button_text_rect)

        pygame.display.flip()
        clock.tick(60)

        if pygame.mouse.get_pressed()[0] and back_button_rect.collidepoint(pygame.mouse.get_pos()):
            return


if __name__ == "__main__":
    main()
