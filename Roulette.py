"""
This programs run Roulette game using pygame with features such as betting on colors, even/odd numbers,
lower and upper bounds, respectively.
Tri Tran
04/18/2024
Version: 3.11
"""

import pygame
import random
import math
import sys

# Initialize the game
pygame.init()

# Display's Settings
SCREEN_WIDTH, SCREEN_HEIGHT = 1200, 950
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Roulette Game")

# FPS
clock = pygame.time.Clock()

# Colors
WHITE, BLACK, RED, GREEN, LIGHT_GREY, DARK_GREY = ((255, 255, 255), (0, 0, 0),
                                                    (255, 0, 0), (255, 255, 0),
                                                    (200, 200, 200), (50, 50, 50))

# Wheel
WHEEL_RADIUS, BALL_RADIUS, NUM_SLOTS = 300, 12, 37

# Balance
INITIAL_BALANCE = 1000

# Button's font
button_font = pygame.font.SysFont("Arial", 24)
popup_font = pygame.font.SysFont("Arial", 36)

# All Bet's button
bet_buttons = [
    {"rect": pygame.Rect(50, 770, 120, 60), "text": "Bet $5", "bet": 5},
    {"rect": pygame.Rect(200, 770, 120, 60), "text": "Bet $10", "bet": 10},
    {"rect": pygame.Rect(350, 770, 120, 60), "text": "Bet $100", "bet": 100},
]


type_buttons = [
    {"rect": pygame.Rect(50, 850, 120, 60), "text": "Red", "type": "red"},
    {"rect": pygame.Rect(200, 850, 120, 60), "text": "Black", "type": "black"},
    {"rect": pygame.Rect(350, 850, 120, 60), "text": "Odd", "type": "odd"},
    {"rect": pygame.Rect(500, 850, 120, 60), "text": "Even", "type": "even"},
    {"rect": pygame.Rect(650, 850, 120, 60), "text": "Low (1-18)", "type": "low"},
    {"rect": pygame.Rect(800, 850, 120, 60), "text": "High (19-36)", "type": "high"},
]


# Roulette's global variables
ball_spinning, ball_angle, ball_spin_speed = False, 0, 0
target_slot, balance = None, INITIAL_BALANCE
bet_amount, last_bet_info, bet_type = 0, "", None
show_popup, popup_text, wins, losses = False, "", 0, 0
number_bet = None


def handle_number_input(events):
    global number_bet  # Global variable

    for event in events:
        if event.type == pygame.KEYDOWN:  # Check if the key have been pressed
            if event.unicode.isnumeric():  # Digit check
                digit = int(event.unicode)  # Cast to int
                if number_bet is None:  # Check if there's no number
                    number_bet = digit  # New number
                else:
                    number_bet = number_bet * 10 + digit
                if number_bet > 36:  # Check for a valid range
                    number_bet = None  # Reset
                return True

            elif event.key == pygame.K_BACKSPACE:  # Keypress check
                if number_bet is not None:  # Check if a number is there
                    number_bet = number_bet // 10  # Remove the last digit
                    if number_bet == 0:
                        number_bet = None  # Clear the number
                return True

            elif event.key in (pygame.K_RETURN, pygame.K_KP_ENTER):  # Keypress Checker
                if number_bet is not None and 0 <= number_bet <= 36:  # Valid Range
                    return True
                else:  # Invalid Range
                    number_bet = None  # Reset
                    return False  # Invalid

    return False  # No number entered

def draw_wheel(angle):
    # Font for the wheel's number
    number_font = pygame.font.SysFont("Arial", 20)

    # Borders around the wheel
    border_color = RED
    border_thickness = 5

    # Draw the border
    pygame.draw.circle(
        screen, border_color,
        (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2),
        WHEEL_RADIUS + border_thickness, border_thickness
    )

    # draw each wheel slots
    for i in range(NUM_SLOTS):
        slot_angle_degrees = (360 / NUM_SLOTS) * i + angle
        radian_angle = math.radians(slot_angle_degrees)

        # Colors in each slots
        color = GREEN if i == 0 else RED if i % 2 == 0 else BLACK

        # Draw the points
        segment_points = [
            (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2),
            (SCREEN_WIDTH // 2 + math.cos(radian_angle) * WHEEL_RADIUS,
             SCREEN_HEIGHT // 2 + math.sin(radian_angle) * WHEEL_RADIUS),
            (SCREEN_WIDTH // 2 + math.cos(radian_angle + math.radians(360 / NUM_SLOTS)) * WHEEL_RADIUS,
             SCREEN_HEIGHT // 2 + math.sin(radian_angle + math.radians(360 / NUM_SLOTS)) * WHEEL_RADIUS)
        ]
        pygame.draw.polygon(screen, color, segment_points)

        # Draw the number in
        text_surface = number_font.render(str(i), True, WHITE if i != 0 else BLACK)
        text_x = SCREEN_WIDTH // 2 + math.cos(radian_angle + math.radians(180 / NUM_SLOTS)) * (WHEEL_RADIUS - 50)
        text_y = SCREEN_HEIGHT // 2 + math.sin(radian_angle + math.radians(180 / NUM_SLOTS)) * (WHEEL_RADIUS - 50)
        text_rect = text_surface.get_rect(center=(text_x, text_y))
        screen.blit(text_surface, text_rect)

def draw_ball(angle):
    # Ball
    x = SCREEN_WIDTH // 2 + math.cos(angle) * (WHEEL_RADIUS - BALL_RADIUS * 3)
    y = SCREEN_HEIGHT // 2 + math.sin(angle) * (WHEEL_RADIUS - BALL_RADIUS * 3)

    # Draw the ball onto the wheel
    pygame.draw.circle(screen, WHITE, (int(x), int(y)), BALL_RADIUS)

def draw_popup(text):
    # Screen pop-up
    popup_rect = pygame.Rect(SCREEN_WIDTH // 2 - 200, SCREEN_HEIGHT // 2 - 100, 400, 200)

    # Draw the border
    pygame.draw.rect(screen, LIGHT_GREY, popup_rect)
    pygame.draw.rect(screen, BLACK, popup_rect, 3)

    # Split the text into new lines
    lines = text.split("\n")
    for i, line in enumerate(lines):
        text_surface = popup_font.render(line, True, BLACK)
        text_rect = text_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50 + i * 50))
        screen.blit(text_surface, text_rect)

def display_info( balance, bet_type, bet_amount, last_bet_info, wins, losses):
    # Font setting
    font = pygame.font.SysFont(None, 36)

    # Player's balance
    balance_text = font.render(f"Balance: ${balance}", True, WHITE)
    screen.blit(balance_text, (100, 20))

    # Bet information
    bet_text = font.render(f"Bet on: {bet_type}, Amount: ${bet_amount}", True, WHITE)
    screen.blit(bet_text, (100, 60))

    # Last bet information
    last_bet_info_text = font.render(last_bet_info, True, WHITE)
    screen.blit(last_bet_info_text, (SCREEN_WIDTH - 300, 680))

    # Win/loss record
    win_lose_text = font.render(f"Wins: {wins} Losses: {losses}", True, WHITE)
    screen.blit(win_lose_text, (100, 100))

def handle_buttons(mouse_pos):
    all_buttons = type_buttons + bet_buttons  # Combine type and bet buttons
    for button in all_buttons:  # GO through all buttons
        color = LIGHT_GREY if button["rect"].collidepoint(mouse_pos) else DARK_GREY
        # Draw the button
        pygame.draw.rect(screen, color, button["rect"])
        text_surf = button_font.render(button["text"], True, WHITE)
        text_rect = text_surf.get_rect(center=button["rect"].center)
        screen.blit(text_surf, text_rect)

def check_click(mouse_pos):
    all_buttons = type_buttons + bet_buttons  # Combine type and bet buttons
    for button in all_buttons:  # Go through all buttons
        # Check the mouse click area
        if button["rect"].collidepoint(mouse_pos):
            return button  # Return the button clicked
    return None  # Nothing was clicked

def calculate_slot(angle):
    degrees_per_slot = 360 / NUM_SLOTS  # Calculate number of degrees per slot
    normalized_angle = math.degrees(angle) % 360
    slot_number = int(normalized_angle / degrees_per_slot)  # Calculate the slot number
    return slot_number  # Return the slot number

def main():
    # Global variables
    global ball_spinning, ball_angle, ball_spin_speed
    global target_slot, balance, bet_amount, last_bet_info, bet_type
    global show_popup, popup_text, wins, losses


    running = True
    while running:
        mouse_pos = pygame.mouse.get_pos()
        screen.fill(BLACK)  # Clear the screen

        # Event loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if show_popup:
                    show_popup = False  # User dismisses the popup
                else:
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
                            if bet_amount > 0 and bet_type in ["red", "black", "odd", "even", "low", "high"]:
                                ball_spinning = True
                                ball_spin_speed = 0.2 + random.uniform(-0.01, 0.01)
                                target_slot = random.randint(0, NUM_SLOTS - 1)
                                last_bet_info = f"Betting ${bet_amount} on {bet_type}"

        # Game logic
        if ball_spinning:
            ball_angle += ball_spin_speed
            ball_spin_speed *= 0.99
            if ball_spin_speed < 0.05:
                ball_spinning = False
                final_slot = calculate_slot(ball_angle)
                winning_color = "red" if final_slot % 2 == 0 else "black"
                if final_slot == 0:
                    winning_color = "green"
                if (bet_type == winning_color or
                        (bet_type == "odd" and final_slot % 2 != 0 and final_slot != 0) or
                        (bet_type == "even" and final_slot % 2 == 0 and final_slot != 0) or
                        (bet_type == "low" and 1 <= final_slot <= 18) or
                        (bet_type == "high" and 19 <= final_slot <= 36)):
                    balance += bet_amount * 2
                    outcome_msg = "Win!"
                    wins += 1
                else:
                    outcome_msg = "Lose!"
                    losses += 1
                last_bet_info = f"Landed on: {final_slot} ({winning_color}). {outcome_msg}"
                popup_text = f"Result: {final_slot} ({winning_color})\nOutcome: {outcome_msg}\nBalance: ${balance}"
                show_popup = True
                bet_amount = 0
                bet_type = None

        # Rendering
        draw_wheel(0)
        draw_ball(ball_angle)
        display_info(balance, bet_type if bet_type else "none", bet_amount, last_bet_info, wins, losses)
        handle_buttons(mouse_pos)

        # Display the popup
        if show_popup:
            draw_popup(popup_text)

        # Refresh the screen
        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()
