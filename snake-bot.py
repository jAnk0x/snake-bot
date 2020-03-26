import pygame
import sys
import random

class Snake:
    def __init__(self):
        self.position = [100, 50]
        self.body = [[100, 50], [90, 50], [80, 50]]
        self.direction = "RIGHT"

    def move(self, food_pos):
        if self.direction == "RIGHT":
            self.position[0] += 10

        if self.direction == "LEFT":
            self.position[0] -= 10

        if self.direction == "UP":
            self.position[1] -= 10

        if self.direction == "DOWN":
            self.position[1] += 10

        if self.position[0] > 490:
            self.position[0] = 0
        elif self.position[0] < 0:
            self.position[0] = 490
        
        if self.position[1] > 490:
            self.position[1] = 0
        elif self.position[1] < 0:
            self.position[1] = 490

        self.body.insert(0, list(self.position))
        if self.position == food_pos:
            return 1
        else:
            self.body.pop()
            return 0

    def check_collision(self):
        for body_part in self.body[1:]:
            if self.position == body_part:
                return 1
        return 0

    def get_head(self):
        return self.position

    def get_body(self):
        return self.body

    def get_direction(self):
        return self.direction

    def find_all_dir(self):
        good_dir = []
        directions = ["RIGHT", "LEFT", "UP", "DOWN"]
        for d in directions:
            test_snake = Snake()
            test_snake.position = self.get_head().copy()
            test_snake.body = self.get_body().copy()
            test_snake.direction = d
            test_snake.move(food_pos)
            if test_snake.check_collision() == 0:
                good_dir.append(d)
            
        return good_dir

    def find_direction(self):
        good_dir = self.find_all_dir()

        if self.get_head()[0] < food_pos[0] and "RIGHT" in good_dir:
            return "RIGHT"
        elif self.get_head()[0] > food_pos[0] and "LEFT" in good_dir:
            return "LEFT"
        else:
            if self.get_head()[1] < food_pos[1] and "DOWN" in good_dir:
                return "DOWN"
            elif self.get_head()[1] > food_pos[1] and "UP" in good_dir:
                return "UP"

        if good_dir:
            return good_dir[0]
        else:
            return "RIGHT"

class Food_spawner:
    def __init__(self):
        self.position = [random.randrange(1, 50) * 10, random.randrange(1, 50) * 10]
        self.isFoodOnScreen = True

    def spawn_food(self):
        if self.isFoodOnScreen is False:
            self.position = [random.randrange(1, 50) * 10, random.randrange(1, 50) * 10]
            self.isFoodOnScreen = True
        return self.position

    def set_food_on_screen(self, b):
        self.isFoodOnScreen = b

windowWidth = 500
windowHeight = windowWidth
window = pygame.display.set_mode((windowWidth, windowHeight))
pygame.display.set_caption("Snake")
fps = pygame.time.Clock()

score = 0
snake = Snake()

food_spawner = Food_spawner()


def game_over():
    print("Score: " + str(score))

    pygame.quit()
    sys.exit()


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over()
        
    food_pos = food_spawner.spawn_food()

    snake.direction = snake.find_direction()

    if snake.move(food_pos) == 1:
        score += 1
        food_spawner.set_food_on_screen(False)

    window.fill(pygame.Color(225, 225, 225))

    for pos in snake.get_body():
        pygame.draw.rect(window, pygame.Color(0, 225, 0), pygame.Rect(pos[0], pos[1], 10, 10))

    pygame.draw.rect(window, pygame.Color(225, 0, 0), pygame.Rect(food_pos[0], food_pos[1], 10, 10))

    if snake.check_collision() == 1:
        game_over()

    pygame.display.flip()
    fps.tick(60)