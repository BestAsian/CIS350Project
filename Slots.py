import pygame
import sys
import random
import time



# Initialize Pygame
pygame.init()

# Set up screen
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Slot Machine") #Look at again

# Define parameters for item squares
SLOT_WIDTH = 100
SLOT_HEIGHT = 100
SLOT_SPACING = 20
SLOTS_X = (SCREEN_WIDTH - (SLOT_WIDTH * 3 + SLOT_SPACING * 2)) // 2
SLOTS_Y = SCREEN_HEIGHT // 2 - SLOT_HEIGHT // 2



# play button, lever parameters
LEVER_WIDTH = 20
LEVER_HEIGHT = 100
LEVER_COLOR = (255, 0, 0)  # Red color

# Define lever position
LEVER_X = SLOTS_X + SLOT_WIDTH * 3 + SLOT_SPACING * 2 + 20
LEVER_Y = SLOTS_Y + SLOT_HEIGHT // 2 - LEVER_HEIGHT // 2
LEVER_RECT = pygame.Rect(LEVER_X, LEVER_Y, LEVER_WIDTH, LEVER_HEIGHT)


# Define Item class
class Item:
    """
    Represents an item in the game.

    """

    def __init__(self, image, x, y):
        """
        Initializes the Item class.

        Args:
            image (str): The path to the image file.
            x (int): The x-coordinate of the item's position.
            y (int): The y-coordinate of the item's position.
        """
        self.image = pygame.image.load(image)  # Load the images using pygame.image.load()
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

# Item images
items = []
item_files = [
    'cherryslotmachine.png',
    '7slotmachine.png',
    'orangeslotmachine.png',
    'plumslotmachine.png',
    'barslotmachine.png',
    'lemonslotmachine.png'
]

def load_images():
    """
    Load images for the slot machine game.

    This function selects three random items from the `item_files` list and updates the `selected_items` global variable.

    Parameters:
        None

    Returns:
        None
    """
    global selected_items
    selected_items = random.sample(item_files, 3)  # Update selected_items with a new random selection

winning_combinations = {
    ('cherryslotmachine.png', 'cherryslotmachine.png', 'cherryslotmachine.png'): 400,  # 3 cherries (second highest)
    ('7slotmachine.png', '7slotmachine.png', '7slotmachine.png'): 500,  # three sevens (highest)
    ('orangeslotmachine.png', 'orangeslotmachine.png', 'orangeslotmachine.png'): 300,  # three oranges
    ('plumslotmachine.png', 'plumslotmachine.png', 'plumslotmachine.png'): 250,  # Three plums
    ('barslotmachine.png', 'barslotmachine.png', 'barslotmachine.png'): 200,  # three bars
    ('lemonslotmachine.png', 'lemonslotmachine.png', 'lemonslotmachine.png'): 150   # three Lemons
}

games_played = 0


# Function to handle lever pull
def handle_lever_pull():
    """
    Handles the action of pulling the lever in the slot machine game.

    This function selects three random items from the item_files list and performs a few actions.
    If the number of games played is less than 5 or more than 5, it increments the games_played counter, loads images, and checks for winning combinations.
    If the number of games played is equal to 5, it says the user wins, shows three sevens, and resets the games_played counter to 0.
    Finally, it selects three random items again and checks for winning combinations.
    """
    global games_played
    selected_items = random.sample(item_files, 3)
    if games_played < 5 or games_played > 5:
        games_played += 1
        load_images()
        print("Playing game", games_played)
        animate_lever_pull()
        check_winning(selected_items)
    else:
        print("You have won!")
        # If the user has played 5 times, show three sevens
        selected_items = ['7slotmachine.png', '7slotmachine.png', '7slotmachine.png']
        animate_lever_pull()
        check_winning(selected_items)
        games_played = 0  # Reset games_played to 0 after winning
    selected_items = random.sample(item_files, 3)
    check_winning(selected_items)


# Function to animate lever pull
def animate_lever_pull():
    """
    Animates the lever pull by moving the lever up and down.

    Parameters:
    None

    Returns:
    None
    """
    lever_y = LEVER_Y
    while lever_y > SLOTS_Y:
        screen.fill((255, 255, 255))
        for item in slot_items:
            screen.blit(item.image, item.rect)
        pygame.draw.rect(screen, LEVER_COLOR, LEVER_RECT)
        pygame.draw.line(screen, (0, 0, 0), (LEVER_X + LEVER_WIDTH // 2, lever_y),
                         (LEVER_X + LEVER_WIDTH // 2, lever_y + LEVER_HEIGHT), 4)
        pygame.display.flip()
        time.sleep(0.01)
        lever_y -= 1
    while lever_y < SLOTS_Y + SLOT_HEIGHT:
        screen.fill((255, 255, 255))
        for item in slot_items:
            screen.blit(item.image, item.rect)
        pygame.draw.rect(screen, LEVER_COLOR, LEVER_RECT)
        pygame.draw.line(screen, (0, 0, 0), (LEVER_X + LEVER_WIDTH // 2, lever_y),
                         (LEVER_X + LEVER_WIDTH // 2, lever_y + LEVER_HEIGHT), 4)
        pygame.display.flip()
        time.sleep(0.01)
        lever_y += 1




# Function to check winning combinations
def check_winning(selected_items):
    """
    Check if the selected items match any winning combinations and display the corresponding payout.

    Parameters:
    selected_items (list): A list of selected items.

    Returns:
    None
    """
    if tuple(selected_items) in winning_combinations:
        payout = winning_combinations[tuple(selected_items)]
        print("Congratulations! You won ${}".format(payout))
    else:
        print("Sorry, you didn't win.")

if games_played == 5:
    selected_items = ['7slotmachine.png', '7slotmachine.png', '7slotmachine.png']
else:
    selected_items = random.sample(item_files, 3)

slot_items = [Item(image, SLOTS_X + (SLOT_WIDTH + SLOT_SPACING) * i, SLOTS_Y) for i, image in enumerate(selected_items)]

# Slot machine background
background_color = (200, 200, 200)
slot_machine_rect = pygame.Rect(SLOTS_X, SLOTS_Y, SLOT_WIDTH * 3 + SLOT_SPACING * 2, SLOT_HEIGHT)
pygame.draw.rect(screen, background_color, slot_machine_rect)

for i in range(3):
    x = SLOTS_X + (SLOT_WIDTH + SLOT_SPACING) * i
    reel_rect = pygame.Rect(x, SLOTS_Y, SLOT_WIDTH, SLOT_HEIGHT)
    pygame.draw.rect(screen, (0, 0, 0), reel_rect, 3)

for item in slot_items:
    screen.blit(item.image, item.rect)

# Draw lever
screen.fill((255, 255, 255))
pygame.draw.rect(screen, LEVER_COLOR, LEVER_RECT)
pygame.draw.line(screen, (0, 0, 0), (LEVER_X + LEVER_WIDTH // 2, LEVER_Y),
                 (LEVER_X + LEVER_WIDTH // 2, LEVER_Y + LEVER_HEIGHT), 4)
pygame.display.flip()

# Main game running
def main():
    running = True
    lever_pulled = False
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if LEVER_RECT.collidepoint(event.pos):
                    lever_pulled = True
            elif event.type == pygame.MOUSEBUTTONUP:
                if lever_pulled:
                    handle_lever_pull()
                    lever_pulled = False
    
        # Randomly select 3 items
        if lever_pulled:
            if games_played < 5:
                selected_items = random.sample(item_files, 3)
                games_played += 1
            else:
                selected_items = ['7slotmachine.png', '7slotmachine.png', '7slotmachine.png']
            lever_pulled = False
    
        # Display the 3 random items
        screen.fill((255, 255, 255))
        for i, item_file in enumerate(selected_items):
            image = pygame.image.load(item_file)
            image = pygame.transform.scale(image, (SLOT_WIDTH, SLOT_HEIGHT))
            screen.blit(image, (SLOTS_X + (SLOT_WIDTH + SLOT_SPACING) * i, SLOTS_Y))
    
        # Draw lever
        pygame.draw.rect(screen, LEVER_COLOR, LEVER_RECT)
        pygame.draw.line(screen, (0, 0, 0), (LEVER_X + LEVER_WIDTH // 2, LEVER_Y),
                         (LEVER_X + LEVER_WIDTH // 2, LEVER_Y + LEVER_HEIGHT), 4)
    
        pygame.display.flip()
    
    # Quit Pygame
    pygame.quit()
    
