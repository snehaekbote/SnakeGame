import pygame
import random

class SnakeGame:
    def __init__(self):
        pygame.init()
        self.white = (255, 255, 255)
        self.yellow = (255, 255, 102)
        self.black = (0, 0, 0)  # Changed border color to black
        self.red = (213, 50, 80)
        self.green = (0, 255, 0)
        self.blue = (50, 153, 213)
        self.border_color = self.black  # Set border color to black

        self.dis_width = 1000
        self.dis_height = 600
        self.border_size = 50  # Border size around the game area

        self.dis = pygame.display.set_mode((self.dis_width, self.dis_height))
        pygame.display.set_caption('Snake Game')

        self.clock = pygame.time.Clock()
        self.snake_block = 10
        self.snake_speed = 15

        self.font_style = pygame.font.SysFont("bahnschrift", 25)
        self.score_font = pygame.font.SysFont("comicsansms", 35)
        
        self.snake_list = []
        self.length_of_snake = 1

        self.game_over = False
        self.game_close = False

        self.x1 = self.dis_width / 2
        self.y1 = self.dis_height / 2

        self.x1_change = 0
        self.y1_change = 0

        self.foodx = self.random_food_position(self.dis_width, self.border_size, self.snake_block)
        self.foody = self.random_food_position(self.dis_height, self.border_size, self.snake_block)

    def random_food_position(self, max_value, border, block_size):
        return round(random.randrange(border, max_value - border - block_size) / 10.0) * 10.0

    def your_score(self, score):
        value = self.score_font.render("Your Score: " + str(score), True, self.blue)
        self.dis.blit(value, [0, 0])

    def our_snake(self, snake_block, snake_list):
        for x in snake_list:
             pygame.draw.circle(self.dis, self.black, (x[0] + snake_block // 2, x[1] + snake_block // 2), snake_block //2)   #snake = snake_block=10 10/2

    def message(self, msg, color):
        mesg = self.font_style.render(msg, True, color)
        self.dis.blit(mesg, [self.dis_width / 6, self.dis_height / 3])

    def draw_border(self):
        pygame.draw.rect(self.dis, self.border_color, (0, 0, self.dis_width, self.border_size))  # Top border
        pygame.draw.rect(self.dis, self.border_color, (0, self.dis_height - self.border_size, self.dis_width, self.border_size))  # Bottom border
        pygame.draw.rect(self.dis, self.border_color, (0, 0, self.border_size, self.dis_height))  # Left border
        pygame.draw.rect(self.dis, self.border_color, (self.dis_width - self.border_size, 0, self.border_size, self.dis_height))  # Right border

    def game_loop(self):
        while not self.game_over:

            while self.game_close:
                self.dis.fill(self.blue)
                self.message("You Lost! Press Q-Quit or C-Play Again", self.red)
                self.your_score(self.length_of_snake - 1)
                pygame.display.update()

                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_q:
                            self.game_over = True
                            self.game_close = False
                        if event.key == pygame.K_c:
                            self.__init__()
                            self.game_loop()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.game_over = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT and self.x1_change == 0:
                        self.x1_change = -self.snake_block
                        self.y1_change = 0
                    elif event.key == pygame.K_RIGHT and self.x1_change == 0:
                        self.x1_change = self.snake_block
                        self.y1_change = 0
                    elif event.key == pygame.K_UP and self.y1_change == 0:
                        self.y1_change = -self.snake_block
                        self.x1_change = 0
                    elif event.key == pygame.K_DOWN and self.y1_change == 0:
                        self.y1_change = self.snake_block
                        self.x1_change = 0

            if self.x1 >= self.dis_width - self.border_size or self.x1 < self.border_size or self.y1 >= self.dis_height - self.border_size or self.y1 < self.border_size:
                self.game_close = True
            self.x1 += self.x1_change
            self.y1 += self.y1_change
            self.dis.fill(self.green)  # Fill the background with green color
            self.draw_border()  # Draw the border
            pygame.draw.circle(self.dis, self.red, (int(self.foodx + self.snake_block / 2), int(self.foody + self.snake_block / 2)), self.snake_block //1)  # Draw the food with red color
            snake_head = []
            snake_head.append(self.x1)
            snake_head.append(self.y1)
            self.snake_list.append(snake_head)
            if len(self.snake_list) > self.length_of_snake:
                del self.snake_list[0]

            for x in self.snake_list[:-1]:
                if x == snake_head:
                    self.game_close = True

            self.our_snake(self.snake_block, self.snake_list)
            self.your_score(self.length_of_snake - 1)

            pygame.display.update()

            if self.x1 == self.foodx and self.y1 == self.foody:
                self.foodx = self.random_food_position(self.dis_width, self.border_size, self.snake_block)
                self.foody = self.random_food_position(self.dis_height, self.border_size, self.snake_block)
                self.length_of_snake += 1

            self.clock.tick(self.snake_speed)

        pygame.quit()
        quit()

if __name__ == "__main__":
    game = SnakeGame()
    game.game_loop()
