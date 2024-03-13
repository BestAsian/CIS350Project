import pygame
import random
import math
import sys
import time

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
LIGHT_GREY = (200, 200, 200)
DARK_GREY = (50, 50, 50)

# Roulette properties
WHEEL_RADIUS = 300
BALL_RADIUS = 12
NUM_SLOTS = 36

# Player properties
INITIAL_BALANCE = 1000

# Initialize screen and clock
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Roulette Game")
clock = pygame.time.Clock()

# Define type buttons for red or black bets and bet amount buttons
type_buttons = [
    {"rect": pygame.Rect(50, 700, 120, 60), "text": "Red", "type": "red"},
    {"rect": pygame.Rect(200, 700, 120, 60), "text": "Black", "type": "black"},
]

bet_buttons = [
    {"rect": pygame.Rect(50, 600, 120, 60), "text": "Bet $5", "bet": 5},
    {"rect": pygame.Rect(200, 600, 120, 60), "text": "Bet $10", "bet": 10},
    {"rect": pygame.Rect(350, 600, 120, 60), "text": "Bet $100", "bet": 100},
]

# Define the custom bet button
custom_bet_button = {"rect": pygame.Rect(900, 580, 200, 60), "text": "Custom Bet", "type": "custom_bet"}

# Button font
button_font = pygame.font.SysFont("Arial", 24)

ball_spinning = False
ball_angle = 0
ball_spin_speed = 0
target_slot = None
balance = INITIAL_BALANCE
bet_amount = 0
last_bet_info = ""

def draw_wheel(angle):
    number_font = pygame.font.SysFont("Arial", 20)
    for i in range(1, NUM_SLOTS + 1):
        slot_angle_degrees = (360 / NUM_SLOTS) * (i - 1) + angle
        radian_angle = math.radians(slot_angle_degrees)
        color = RED if i % 2 == 0 else BLACK
        pygame.draw.polygon(screen, color, [
            (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2),
            (SCREEN_WIDTH // 2 + math.cos(radian_angle) * WHEEL_RADIUS,
             SCREEN_HEIGHT // 2 + math.sin(radian_angle) * WHEEL_RADIUS),
            (SCREEN_WIDTH // 2 + math.cos(radian_angle + math.radians(360 / NUM_SLOTS)) * WHEEL_RADIUS,
             SCREEN_HEIGHT // 2 + math.sin(radian_angle + math.radians(360 / NUM_SLOTS)) * WHEEL_RADIUS)])

        text = number_font.render(str(i), True, WHITE)
        text_x = SCREEN_WIDTH // 2 + math.cos(radian_angle + math.radians(180 / NUM_SLOTS)) * (WHEEL_RADIUS - 50)
        text_y = SCREEN_HEIGHT // 2 + math.sin(radian_angle + math.radians(180 / NUM_SLOTS)) * (WHEEL_RADIUS - 50)
        text_rect = text.get_rect(center=(text_x, text_y))
        screen.blit(text, text_rect)


def draw_ball(angle):
    global ball_spinning, ball_angle, ball_spin_speed, target_slot, balance, bet_amount, last_bet_info
    x = SCREEN_WIDTH // 2 + math.cos(angle) * (WHEEL_RADIUS - BALL_RADIUS * 3)
    y = SCREEN_HEIGHT // 2 + math.sin(angle) * (WHEEL_RADIUS - BALL_RADIUS * 3)
    pygame.draw.circle(screen, WHITE, (int(x), int(y)), BALL_RADIUS)

    if ball_spinning:
        # Apply spin to the ball
        angle += ball_spin_speed
        ball_spin_speed *= 0.99 + random.uniform(-0.002, 0.002)  # Slight variation in deceleration

        if ball_spin_speed < 0.01:
            # Stop spinning when the speed is negligible
            ball_spinning = False

            # Calculate the winning slot based on the final angle
            final_slot = calculate_slot(angle)

            # Update game state based on the winning slot
            if final_slot == target_slot:
                balance += bet_amount * 2  # Win condition
                outcome_msg = "Win!"
            else:
                outcome_msg = "Lose!"
            last_bet_info = f"Landed on: {final_slot}. {outcome_msg}"
            time.sleep(1)


def display(balance, bet_type, bet_amount, last_bet_info):
    font = pygame.font.SysFont(None, 36)
    balance_text = font.render(f"Balance: ${balance}", True, WHITE)
    screen.blit(balance_text, (10, 10))
    bet_text = font.render(f"Bet on: {bet_type}, Amount: ${bet_amount}", True, WHITE)
    screen.blit(bet_text, (10, 50))
    last_bet_surface = font.render(last_bet_info, True, WHITE)
    screen.blit(last_bet_surface, (SCREEN_WIDTH - 400, 650))


def buttons(mouse_pos):
    all_buttons = type_buttons + bet_buttons + [custom_bet_button]
    for button in all_buttons:
        color = LIGHT_GREY if button["rect"].collidepoint(mouse_pos) else DARK_GREY
        pygame.draw.rect(screen, color, button["rect"])
        text_surf = button_font.render(button["text"], True, WHITE)
        text_rect = text_surf.get_rect(center=button["rect"].center)
        screen.blit(text_surf, text_rect)


def check_click(mouse_pos):
    all_buttons = type_buttons + bet_buttons + [custom_bet_button]
    for button in all_buttons:
        if button["rect"].collidepoint(mouse_pos):
            return button
    return None


def calculate_slot(angle):
    degrees_per_slot = 360 / NUM_SLOTS
    normalized_angle = math.degrees(angle) % 360
    slot_number = int((normalized_angle / degrees_per_slot)) + 1  # Adjusted formula
    return slot_number


def handle_custom_bet_input():
    print("Enter your custom bet amount:")
    custom_bet = input()
    if custom_bet.isdigit():
        return int(custom_bet)
    else:
        print("Invalid input. Bet set to 0.")
        return 0


def roll_dice():
    # Simulate rolling a six-sided dice
    return random.randint(1, NUM_SLOTS)


def main():
    global ball_spinning, ball_angle, ball_spin_speed, target_slot, balance, bet_amount, last_bet_info, bet_type

    angle = 0
    ball_spinning = False
    ball_angle = 0
    ball_spin_speed = 0
    target_slot = None
    balance = INITIAL_BALANCE
    bet_amount = 0
    last_bet_info = ""
    bet_type = None  # Define bet_type here

    running = True
    while running:
        mouse_pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and not ball_spinning:
                clicked_button = check_click(mouse_pos)
                if clicked_button and "bet" in clicked_button:
                    # Update bet amount based on clicked button, if balance suffices
                    temp_bet_amount = clicked_button.get("bet", 0)
                    if balance - temp_bet_amount >= 0:
                        bet_amount += temp_bet_amount  # Increment bet amount instead of setting it directly
                        balance -= temp_bet_amount
                        last_bet_info = f"Betting ${bet_amount}"
                    else:
                        last_bet_info = "Insufficient balance!"
                elif clicked_button and clicked_button["type"] in ["red", "black", "custom_bet"]:
                    if clicked_button["type"] == "custom_bet":
                        # Custom bet input
                        custom_bet_amount = handle_custom_bet_input()
                        if balance - custom_bet_amount >= 0 and custom_bet_amount > 0:
                            bet_amount = custom_bet_amount
                            balance -= bet_amount
                            last_bet_info = f"Betting ${bet_amount} on custom bet"
                    else:
                        # Red or Black bet type selection
                        bet_type = clicked_button["type"]
                        last_bet_info = f"Betting ${bet_amount} on {bet_type}"
                        if bet_amount > 0:
                            ball_spin_speed = 0.2
                            ball_spinning = True
                            bet_amount = 0  # Reset bet amount after placing bet
                        else:
                            last_bet_info = "Select bet amount first!"

        screen.fill(BLACK)
        draw_wheel(angle)  # Wheel remains stationary
        x = roll_dice()
        if ball_spinning:
            ball_angle += ball_spin_speed
            ball_spin_speed *= 0.99 + random.uniform(-0.002, 0.002)  # Slight variation in deceleration
            if ball_spin_speed < 0.01:
                final_slot = calculate_slot(ball_angle)
                if int(final_slot) % 2 == 0:
                    win_color = "red"
                else:
                    win_color = "black"
                if (bet_type.lower() == win_color.lower() and bet_type != "custom_bet") or (
                        bet_type == "custom_bet" and final_slot == final_slot):
                    balance += bet_amount * 2  # Win condition
                    outcome_msg = "Win!"
                else:
                    outcome_msg = "Lose!"
                last_bet_info = f"Landed on: {final_slot} {win_color}. {outcome_msg}"
                ball_spinning = False
                time.sleep(1)

        draw_ball(ball_angle)  # Draw the ball with its independent spinning

        display(balance, bet_type if bet_type else "Place your bet", bet_amount, last_bet_info)
        buttons(mouse_pos)

        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()

