import random 
import pygame
import sys
from os import getcwd
from os.path import join

pygame.init()

WIDTH = 700
HEIGHT = 700
CENTERS = [(150, 150), (350, 150), (550, 150), (150, 350), (350, 350), (550, 350), (150, 550), (350, 550), (550, 550)]
DARK_BLUE = (4, 48, 61)
LIGHT_BLUE = (97, 184, 212)
RED = (255, 64, 85)
QALAY = pygame.font.Font(join(getcwd(), "MAIN_RESOURCES/Fonts/MonkQalayRegular.ttf"), 53)
SAILORETTE = pygame.font.Font(join(getcwd(), "MAIN_RESOURCES/Fonts/Sailorette.ttf"), 35)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
caption = pygame.display.set_caption("Pygame Practice")
clock = pygame.time.Clock()
who_won = "tie"

class Game:
    def __init__(self):
        self.board_values = ["1", "2", "3", "4", "5", "6", "7", "8", "9"] 
        self.whos_turn = "player"
        self.remaining_squares = ["1", "2", "3", "4", "5", "6", "7", "8", "9"]
        self.used_squares = []
        self.player_choice = None
        self.AI_choice = None
        self.has_won = False
        self.diagnol_start_values = [0, 2]
        self.GWLT = False
        self.row = None
        self.column = None
        self.diagnol = None
        self.rows = [0, 0, 0]
        self.columns = [0, 0, 0]
        self.diagnols = [0, 0]
        self.row_problem = False
        self.column_problem = False
        self.diagnol_problem = False
        self.row_values = [[0, 1, 2], [3, 4, 5], [6, 7, 8]]
        self.column_values = [[0, 3, 6], [1, 4, 7], [2, 5, 8]]
        self.diagnol_values = [[0, 4, 8], [2, 4, 6]]
        self.AIhc = False
        self.pos = None
        self.all_clear = False
        self.clicked = False
        self.font_end = None
        self.player_won = "You Won"
        self.AI_Won = "The Computer Beat You"
        self.tie = "You tied with the computer"
        self.text_surface = False
        self.text_rect = False
        self.screen_type = True
        self.in_game = True
        self.text_surface1 = SAILORETTE.render("Play", True, DARK_BLUE)
        self.text_rect1 = self.text_surface1.get_rect()
        self.text_rect1.center = ((WIDTH/2)-self.text_rect1.width/2, (HEIGHT/4)-self.text_rect1.height/2)
        self.text_rect1.center = self.text_rect1.bottomright
        self.ellipse = None
        self.mouse_pos = (0, 0)

    def game_loop(self):
        self.reset_board()
        while True:
            if len(self.remaining_squares) > 0 and self.in_game:
                if self.has_won == False:
                    self.is_won()
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.quit()
                            sys.exit()
                        if event.type == pygame.MOUSEBUTTONDOWN and self.all_clear:
                            self.pos = pygame.mouse.get_pos()
                            self.check_pos(self.pos)
                            self.player_turn()
                            self.clicked = True
                    if self.has_won == False:
                        if self.whos_turn == "player":
                            self.all_clear = True
                            if self.clicked:
                                self.all_clear = False
                                self.whos_turn = "AI"
                        elif self.whos_turn == "AI":
                            self.AI_decision()
                            self.whos_turn = "player"
                            self.clicked = False
                else:
                    if self.has_won == "player":
                        self.screen_type = False
                        self.in_game = False
                    elif self.has_won == "AI":
                        self.screen_type = False
                        self.in_game = False
            if len(self.remaining_squares) == 0 and self.in_game:
                if self.has_won == False:
                    self.GWLT = True
                self.is_won()
                if self.has_won == "player" and self.GWLT:
                    self.screen_type = False
                    self.in_game = False
                elif self.has_won == "AI" and self.GWLT:
                    self.screen_type = False
                    self.in_game = False
                elif self.has_won == "tie":
                    self.screen_type = False
                    self.in_game = False

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.mouse_pos = pygame.mouse.get_pos()
                    if self.ellipse.collidepoint(self.mouse_pos):
                        self.__init__()
                        self.game_loop()

            self.draw()
            clock.tick(60)

    def drawX(self, center):
        pygame.draw.line(screen, LIGHT_BLUE, (center[0]-50, center[1]-50), (center[0]+50, center[1]+50), 10)
        pygame.draw.line(screen, LIGHT_BLUE, (center[0]-50, center[1]+50), (center[0]+50, center[1]-50), 10)

    def drawO(self, center):
        pygame.draw.ellipse(screen, LIGHT_BLUE, [center[0]-50, center[1]-50, 100, 100], 10)

    def draw(self):
        if self.screen_type:
            screen.fill(DARK_BLUE)
            pygame.draw.line(screen, LIGHT_BLUE, (50, 250), (650, 250), 10)
            pygame.draw.line(screen, LIGHT_BLUE, (50, 450), (650, 450), 10)
            pygame.draw.line(screen, LIGHT_BLUE, (250, 50), (250, 650), 10)
            pygame.draw.line(screen, LIGHT_BLUE, (450, 50), (450, 650), 10)
            for i in range(len(self.board_values)):
                if self.board_values[i] == " ":
                    pass
                elif self.board_values[i] == "X":
                    self.drawX(CENTERS[i])
                elif self.board_values[i] == "O":
                    self.drawO(CENTERS[i])
        else:
            screen.fill(DARK_BLUE)
            self.print_win()
            self.ellipse = pygame.draw.ellipse(screen, LIGHT_BLUE, [(WIDTH/2)-63, (HEIGHT/4)-28, 126, 56])
            screen.blit(self.text_surface1, self.text_rect1)
        pygame.display.update()

    def check_pos(self, pos):
        if pos[1] < 250 and pos[1] > 50:
            if pos[0] > 50 and pos[0] < 250:
                self.player_choice = 0
            elif pos[0] > 250 and pos[0] < 450:
                self.player_choice = 1
            elif pos[0] > 450 and pos[0] < 650:
                self.player_choice = 2
        elif pos[1] < 450 and pos[1] > 250:
            if pos[0] > 50 and pos[0] < 250:
                self.player_choice = 3
            elif pos[0] > 250 and pos[0] < 450:
                self.player_choice = 4
            elif pos[0] > 450 and pos[0] < 650:
                self.player_choice = 5
        elif pos[1] < 650 and pos[1] > 450:
            if pos[0] > 50 and pos[0] < 250:
                self.player_choice = 6
            elif pos[0] > 250 and pos[0] < 450:
                self.player_choice = 7
            elif pos[0] > 450 and pos[0] < 650:
                self.player_choice = 8
        
    def AI_decision(self):
        if type(self.row_problem) == int:
            for i in self.row_values[self.row_problem]:
                if self.board_values[i] == "X":
                    pass
                elif self.board_values[i] == " ":
                    self.AI_choice = str(i+1)
                    self.rows[self.row_problem] = 0
                    self.AIhc = True
                    break
        if type(self.column_problem) == int:
            for i in self.column_values[self.column_problem]:
                if self.board_values[i] == "X":
                    pass
                elif self.board_values[i] == " ":
                    self.AI_choice = str(i+1)
                    self.columns[self.column_problem] = 0
                    self.AIhc = True
                    break
        if type(self.diagnol_problem) == int:
            for i in self.diagnol_values[self.diagnol_problem]:
                if self.board_values[i] == "X":
                    pass
                elif self.board_values[i] == " ":
                    self.AI_choice = str(i+1)
                    self.diagnols[self.diagnol_problem] = 0
                    self.AIhc = True 
        if self.AIhc == False:
            self.AI_choice = random.choice(self.remaining_squares)
        self.remaining_squares.remove(str(self.AI_choice))
        self.used_squares.append(str(self.AI_choice))
        self.board_values[int(self.AI_choice) - 1] = "O"
        self.AIhc = False

    def reset_board(self):
        for i in range(len(self.board_values)):
            self.board_values[i] = " "

    def is_won(self):
        if len(self.remaining_squares) == 0:
            self.has_won = "tie"
        for i in range(0, 7, 3):
            if self.board_values[i] == "X" and self.board_values[i+1] == "X" and self.board_values[i+2] == "X":
                self.has_won = "player"
            elif self.board_values[i] == "O" and self.board_values[i+1] == "O" and self.board_values[i+2] == "O":
                self.has_won = "AI"
            else:
                for i in range(0, 3, 1):
                    if self.board_values[i] == "X" and self.board_values[i+3] == "X" and self.board_values[i+6] == "X":
                        self.has_won = "player"
                    elif self.board_values[i] == "O" and self.board_values[i+3] == "O" and self.board_values[i+6] == "O":
                        self.has_won = "AI"
                    else:
                        if self.board_values[4] == "X":
                            for i in range(0, 3, 2):
                                if self.board_values[i] == "X" and self.board_values[(5+(5-(i+1)))-1] == "X":
                                    self.has_won = "player"
                        elif self.board_values[4] == "O":
                            for i in range(0, 3, 2):
                                if self.board_values[i] == "O" and self.board_values[(5+(5-(i+1)))-1] == "O":
                                    self.has_won = "AI"

    def RC_Convert(self, value):
        value = int(value)
        for i in range(0, 3, 1):
            if value == i or value == i+3 or value == i+6:
                self.column = i
            if value >= 0 and value <= 2:
                self.row = 0
            elif value >= 3 and value <= 5:
                self.row = 1
            elif value >= 6 and value <= 8:
                self.row = 2

    def player_turn(self):
        self.remaining_squares.remove(str(self.player_choice+1))
        self.used_squares.append(str(self.player_choice+1))
        self.board_values[self.player_choice] = "X"
        self.RC_Convert(self.player_choice)
        self.rows[self.row] += 1
        self.columns[self.column] += 1
        for i in range(len(self.diagnol_values)):
            for j in range(len(self.diagnol_values[i])):
                if (self.diagnol_values[i][j]) == int(self.player_choice):
                    self.diagnols[i] += 1
        for i in range(len(self.rows)):
            if self.rows[i] == 2:
                self.row_problem = i
        for i in range(len(self.columns)):
            if self.columns[i] == 2:
                self.column_problem = i
        for i in range(len(self.diagnols)):
            if self.diagnols[i] == 2:
                self.diagnol_problem = i

    def print_win(self):
        if self.has_won == "player":
            self.text_surface = QALAY.render(self.player_won, True, LIGHT_BLUE)
        elif self.has_won == "AI":
            self.text_surface = QALAY.render(self.AI_Won, True, LIGHT_BLUE)
        elif self.has_won == "tie":
            self.text_surface = QALAY.render(self.tie, True, LIGHT_BLUE)
        self.text_rect = self.text_surface.get_rect()
        self.text_rect.center = ((WIDTH/2, HEIGHT/2))
        screen.blit(self.text_surface, self.text_rect)
        
game = Game()
game.game_loop()
