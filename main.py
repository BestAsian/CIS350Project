import pygame
import sys
from button import Button
from coinflip import main as coin_flip_game
from Connect4 import main as connect4_game
from Roulette import main as roulette_game
from Bingo import main as bingo_game
from Blackjack import main as blackjack_game
# from Slots import main as slots_game

# Initialize pygame, sets the screen size, screen caption, and background image.
pygame.init()
SCREEN = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("Menu")
BG = pygame.image.load("assets/Background.png")

def get_font(size):
    """
    Returns the font of the given size.
    """
    return pygame.font.Font("assets/font.ttf", size)


def main_menu():
    """
    The main menu loop. Includes the creation of all buttons and action cases.
    """
    while True:
        # Background
        SCREEN.blit(BG, (0, 0))
        # Mouse Position on screen
        MENU_MOUSE_POS = pygame.mouse.get_pos()
        # Sets the main menu title.
        MENU_TEXT = get_font(75).render("CASINO MAIN MENU", True, "#b68f40")
        MENU_RECT = MENU_TEXT.get_rect(center=(640, 100))
        # Initializing the buttons leading to games and options.
        CONNECT4_BUTTON = Button(image=pygame.image.load("assets/Standard Rect.png"), pos=(320, 250),
                                 text_input="CONNECT4", font=get_font(30), base_color="#d7fcd4", hovering_color="White")
        PROFILE_BUTTON = Button(image=pygame.image.load("assets/Standard Rect.png"), pos=(960, 700),
                                text_input="PROFILE", font=get_font(30), base_color="#d7fcd4", hovering_color="White")
        COIN_FLIP_BUTTON = Button(image=pygame.image.load("assets/Standard Rect.png"), pos=(320, 400),
                                  text_input="COIN FLIP", font=get_font(30), base_color="#d7fcd4",
                                  hovering_color="White")
        QUIT_BUTTON = Button(image=pygame.image.load("assets/Standard Rect.png"), pos=(320, 700),
                             text_input="QUIT", font=get_font(30), base_color="#d7fcd4", hovering_color="White")
        ROULETTE_BUTTON = Button(image=pygame.image.load("assets/Standard Rect.png"), pos=(960, 250),
                                 text_input="ROULETTE", font=get_font(30), base_color="#d7fcd4", hovering_color="White")
        BINGO_BUTTON = Button(image=pygame.image.load("assets/Standard Rect.png"), pos=(960, 400),
                              text_input="BINGO", font=get_font(30), base_color="#d7fcd4", hovering_color="White")
        BLACKJACK_BUTTON = Button(image=pygame.image.load("assets/Standard Rect.png"), pos=(960, 550),
                              text_input="BLACKJACK", font=get_font(30), base_color="#d7fcd4", hovering_color="White")
        SLOTS_BUTTON = Button(image=pygame.image.load("assets/Standard Rect.png"), pos=(320, 550),
                                  text_input="SLOTS", font=get_font(30), base_color="#d7fcd4",
                                  hovering_color="White")

        # Loads the Main menu text
        SCREEN.blit(MENU_TEXT, MENU_RECT)

        # Checks if the mouse is hovering an option button.
        for button in [CONNECT4_BUTTON, PROFILE_BUTTON,
                       COIN_FLIP_BUTTON, QUIT_BUTTON,
                       ROULETTE_BUTTON, BINGO_BUTTON,
                       BLACKJACK_BUTTON, SLOTS_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(SCREEN)

        # Handles actions on the main menu screen.
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PROFILE_BUTTON.checkForInput(MENU_MOUSE_POS):
                    Profile()
                elif CONNECT4_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.display.set_caption("Connect4")
                    connect4_game()
                elif COIN_FLIP_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.display.set_caption("Coin Flip")
                    coin_flip_game()
                elif ROULETTE_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.display.set_caption("ROULETTE")
                    roulette_game()
                elif BINGO_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.display.set_caption("BINGO")
                    bingo_game()
                elif BLACKJACK_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.display.set_caption("BLACKJACK")
                    blackjack_game()
                elif BLACKJACK_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.display.set_caption("BLACKJACK")
                    # slots_game()
                elif QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()


def Profile():
    """
    The Profile loop. Creates the screen holding the Profile screen.
    """
    pygame.display.set_caption("Profile")
    while True:
        # Get the mouse position while on the option screen
        OPTIONS_MOUSE_POS = pygame.mouse.get_pos()

        # Fills the screen with a white background
        SCREEN.fill((255,255,0))

        # Draws and loads text onto the profile screen.
        OPTIONS_TEXT = get_font(45).render("This is the PROFILE screen.", True, "Black")
        OPTIONS_RECT = OPTIONS_TEXT.get_rect(center=(640, 260))
        SCREEN.blit(OPTIONS_TEXT, OPTIONS_RECT)

        OPTIONS_BACK = Button(image=None, pos=(640, 460),
                              text_input="BACK", font=get_font(75), base_color="Black", hovering_color="Green")

        OPTIONS_BACK.changeColor(OPTIONS_MOUSE_POS)
        OPTIONS_BACK.update(SCREEN)

        # Handles events on the option screen.
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if OPTIONS_BACK.checkForInput(OPTIONS_MOUSE_POS):
                    pygame.display.set_caption("Menu")
                    main_menu()
        pygame.display.update()


if __name__ == "__main__":
    main_menu()
