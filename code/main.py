import pygame
import sys
import os
from settings import *
from level import Level

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption('Our Little Corner')
        self.clock = pygame.time.Clock()
        self.level = None
        self.menu_active = True
        
        # ===== ABSOLUTE PATHS =====
        self.FONT_PATH = r"C:\Users\ketch\Downloads\Sarahdew\Python\LittleCorner\Final\code\font\LycheeSoda.ttf"
        self.BG_PATH = r"C:\Users\ketch\Downloads\Sarahdew\Python\LittleCorner\Final\graphics\menu\tree.png"

        # ===== VERIFY FILES EXIST =====
        self.verify_files_exist()

        # ===== LOAD FONTS =====
        self.title_font = pygame.font.Font(self.FONT_PATH, 74)
        self.menu_font = pygame.font.Font(self.FONT_PATH, 50)

        # ===== MENU SETUP =====
        self.menu_options = [
            {"text": "Start Game", "action": "start"},
            {"text": "Quit", "action": "quit"}
        ]
        self.selected_option = 0

        # ===== LOAD BACKGROUND =====
        self.background = pygame.image.load(self.BG_PATH).convert()
        self.background = pygame.transform.scale(self.background, (SCREEN_WIDTH, SCREEN_HEIGHT))

    def verify_files_exist(self):
        """Ensure critical files exist before proceeding"""
        missing_files = []
        if not os.path.exists(self.FONT_PATH):
            missing_files.append(f"Font: {self.FONT_PATH}")
        if not os.path.exists(self.BG_PATH):
            missing_files.append(f"Background: {self.BG_PATH}")
        
        if missing_files:
            print("CRITICAL ERROR: Missing files:")
            for f in missing_files:
                print(f" - {f}")
            print("\nPlease verify:")
            print("1. File names are EXACTLY as shown (case-sensitive)")
            print("2. Files are in the correct locations")
            pygame.quit()
            sys.exit()

    def draw_menu(self):
        """Draw menu screen with background and text"""
        # Draw background
        self.screen.blit(self.background, (0, 0))
        
        # Draw title
        title_surf = self.title_font.render('Our Little Corner', True, (255, 255, 255))
        title_rect = title_surf.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/4))
        self.screen.blit(title_surf, title_rect)
        
        # Draw menu options
        for index, option in enumerate(self.menu_options):
            color = (255, 215, 0) if index == self.selected_option else (255, 255, 255)
            text_surf = self.menu_font.render(option["text"], True, color)
            text_rect = text_surf.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2 + index * 75))
            self.screen.blit(text_surf, text_rect)

    def handle_menu_input(self):
        """Process menu navigation inputs"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit_game()
                
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    self.selected_option = (self.selected_option + 1) % len(self.menu_options)
                if event.key == pygame.K_UP:
                    self.selected_option = (self.selected_option - 1) % len(self.menu_options)
                if event.key == pygame.K_RETURN:
                    if self.menu_options[self.selected_option]["action"] == "start":
                        self.menu_active = False
                        self.level = Level()
                    else:
                        self.quit_game()

    def quit_game(self):
        """Clean exit procedure"""
        pygame.quit()
        sys.exit()

    def run(self):
        """Main game loop"""
        while True:
            if self.menu_active:
                self.handle_menu_input()
                self.draw_menu()
            else:
                # Run game level
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.quit_game()
                
                dt = self.clock.tick() / 1000
                self.level.run(dt)
            
            pygame.display.update()

if __name__ == '__main__':
    game = Game()
    game.run()