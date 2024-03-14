import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Set up screen
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Slot Machine")

# Define parameters
SLOT_WIDTH = 100
SLOT_HEIGHT = 100
SLOT_SPACING = 20
SLOTS_X = (SCREEN_WIDTH - (SLOT_WIDTH * 3 + SLOT_SPACING * 2)) // 2
SLOTS_Y = SCREEN_HEIGHT // 2 - SLOT_HEIGHT // 2

# Define Item class
class Item:
    def __init__(self, image, x, y):
        self.image = image
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

# Winning combinations and payouts
winning_combinations = {
    ('cherryslotmachine.png', 'cherryslotmachine.png', 'cherryslotmachine.png'): 400,  # 3 cherries (second highest)
    ('7slotmachine.png', '7slotmachine.png', '7slotmachine.png'): 500,  # three sevens (highest)
    ('orangeslotmachine.png', 'orangeslotmachine.png', 'orangeslotmachine.png'): 300,  # three oranges
    ('plumslotmachine.png', 'plumslotmachine.png', 'plumslotmachine.png'): 250,  # Three plums
    ('barslotmachine.png', 'barslotmachine.png', 'barslotmachine.png'): 200,  # three bars
    ('lemonslotmachine.png', 'lemonslotmachine.png', 'lemonslotmachine.png'): 150   # three Lemons
}


slot_items = [Item(image, SLOTS_X + (SLOT_WIDTH + SLOT_SPACING) * i, SLOTS_Y) for i, image in enumerate(items)]

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



# Main game running
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

            # Randomly select 3 items
            selected_items = random.sample(item_files, 3)

            # Display the 3 random items
            for i, item_file in enumerate(selected_items):
                image = pygame.image.load(item_file)
                image = pygame.transform.scale(image, (SLOT_WIDTH, SLOT_HEIGHT))
                screen.blit(image, (SLOTS_X + (SLOT_WIDTH + SLOT_SPACING) * i, SLOTS_Y))

            # Check for winning combination
            if tuple(selected_items) in winning_combinations:
                payout = winning_combinations[tuple(selected_items)]
                print("Congratulations! You won ${}".format(payout))
            else:
                print("Sorry, you didn't win this time.")

    # Update display
    pygame.display.flip()

# Quit Pygame
pygame.quit()
