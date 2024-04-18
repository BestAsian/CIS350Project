import pygame
import random
import math
import sys

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 950

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
    {"rect": pygame.Rect(50, 700, 120, 60), "text": "Red", "type": "red"},  # Adjusted further down
    {"rect": pygame.Rect(200, 700, 120, 60), "text": "Black", "type": "black"},  # Adjusted further down
]

bet_buttons = [
    {"rect": pygame.Rect(50, 770, 120, 60), "text": "Bet $5", "bet": 5},  # Adjusted further down
    {"rect": pygame.Rect(200, 770, 120, 60), "text": "Bet $10", "bet": 10},  # Adjusted further down
    {"rect": pygame.Rect(350, 770, 120, 60), "text": "Bet $100", "bet": 100},  # Adjusted further down
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

# Font for button text and pop-up
button_font = pygame.font.SysFont("Arial", 24)
popup_font = pygame.font.SysFont("Arial", 36)

# Initialize game state variables
ball_spinning = False
ball_angle = 0
ball_spin_speed = 0
target_slot = None
balance = INITIAL_BALANCE
bet_amount = 0
last_bet_info = ""
bet_type = None
show_popup = False
popup_text = ""
wins = 0  # Count of wins
losses = 0  # Count of losses

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

def draw_popup(text):
    popup_rect = pygame.Rect(SCREEN_WIDTH // 2 - 200, SCREEN_HEIGHT // 2 - 100, 400, 200)
    pygame.draw.rect(screen, LIGHT_GREY, popup_rect)
    pygame.draw.rect(screen, BLACK, popup_rect, 3)
    lines = text.split("\n")
    for i, line in enumerate(lines):
        text_surface = popup_font.render(line, True, BLACK)
        text_rect = text_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50 + i * 50))
        screen.blit(text_surface, text_rect)

def display_info(balance, bet_type, bet_amount, last_bet_info, wins, losses):
    # Increased the x-offset from 10 to 100 for more rightward placement
    # Increased the y-offsets to move down slightly
    font = pygame.font.SysFont(None, 36)
    balance_text = font.render(f"Balance: ${balance}", True, WHITE)
    screen.blit(balance_text, (100, 20))  # Moved right to x=100, down to y=20

    bet_text = font.render(f"Bet on: {bet_type}, Amount: ${bet_amount}", True, WHITE)
    screen.blit(bet_text, (100, 60))  # Moved right to x=100, down to y=60

    last_bet_info_text = font.render(last_bet_info, True, WHITE)
    screen.blit(last_bet_info_text, (SCREEN_WIDTH - 300, 680))  # Adjusted right and down, assuming screen width allows

    win_lose_text = font.render(f"Wins: {wins} Losses: {losses}", True, WHITE)
    screen.blit(win_lose_text, (100, 100))  # Moved right to x=100, down to y=100


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
    global ball_spinning, ball_angle, ball_spin_speed, target_slot, balance, bet_amount, last_bet_info, bet_type, show_popup, popup_text, wins, losses

    running = True
    while running:
        mouse_pos = pygame.mouse.get_pos()
        screen.fill(BLACK)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if show_popup:
                    show_popup = False  # Close the popup if it's open and user clicks
                elif not ball_spinning:
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
                    wins += 1  # Increment win counter
                else:
                    outcome_msg = "Lose!"
                    losses += 1  # Increment loss counter
                last_bet_info = f"Landed on: {final_slot} ({winning_color}). {outcome_msg}"
                popup_text = f"Result: {final_slot} ({winning_color})\nOutcome: {outcome_msg}\nBalance: ${balance}"
                show_popup = True
                bet_amount = 0
                bet_type = None

        draw_wheel(0)
        draw_ball(ball_angle)
        display_info(balance, bet_type if bet_type else "none", bet_amount, last_bet_info, wins, losses)
        handle_buttons(mouse_pos)

        if show_popup:
            draw_popup(popup_text)

        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()
