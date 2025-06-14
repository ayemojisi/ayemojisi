import pygame
import random

# Initialize Pygame
pygame.init()

# Game constants
WIDTH, HEIGHT = 400, 600
GRAVITY = 0.25
JUMP_STRENGTH = -5
PIPE_GAP = 150
PIPE_FREQUENCY = 1500  # milliseconds

# Setup display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Flappy Bird')
clock = pygame.time.Clock()

# Load images
BIRD_IMG = pygame.Surface((30, 30), pygame.SRCALPHA)
pygame.draw.circle(BIRD_IMG, (255, 255, 0), (15, 15), 15)

PIPE_WIDTH = 60

# Bird class
class Bird:
    def __init__(self):
        self.x = WIDTH // 4
        self.y = HEIGHT // 2
        self.vel = 0
        self.rect = BIRD_IMG.get_rect(center=(self.x, self.y))

    def update(self):
        self.vel += GRAVITY
        self.y += self.vel
        self.rect.centery = int(self.y)

    def jump(self):
        self.vel = JUMP_STRENGTH

    def draw(self, surface):
        surface.blit(BIRD_IMG, self.rect)

# Pipe class
class Pipe:
    def __init__(self):
        self.x = WIDTH
        self.height = random.randint(50, HEIGHT - PIPE_GAP - 50)
        self.top_rect = pygame.Rect(self.x, 0, PIPE_WIDTH, self.height)
        self.bottom_rect = pygame.Rect(self.x, self.height + PIPE_GAP, PIPE_WIDTH, HEIGHT - self.height - PIPE_GAP)

    def update(self):
        self.x -= 3
        self.top_rect.x = int(self.x)
        self.bottom_rect.x = int(self.x)

    def draw(self, surface):
        pygame.draw.rect(surface, (0, 255, 0), self.top_rect)
        pygame.draw.rect(surface, (0, 255, 0), self.bottom_rect)

    def offscreen(self):
        return self.x + PIPE_WIDTH < 0

    def collides_with(self, bird):
        return self.top_rect.colliderect(bird.rect) or self.bottom_rect.colliderect(bird.rect)

# Main function

def main():
    bird = Bird()
    pipes = []
    score = 0

    pygame.time.set_timer(pygame.USEREVENT, PIPE_FREQUENCY)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                bird.jump()
            if event.type == pygame.USEREVENT:
                pipes.append(Pipe())

        bird.update()
        for pipe in pipes:
            pipe.update()
        pipes = [p for p in pipes if not p.offscreen()]

        # Collision detection
        for pipe in pipes:
            if pipe.collides_with(bird):
                running = False
        if bird.rect.top <= 0 or bird.rect.bottom >= HEIGHT:
            running = False

        screen.fill((135, 206, 235))  # Sky blue
        bird.draw(screen)
        for pipe in pipes:
            pipe.draw(screen)
        pygame.display.flip()
        clock.tick(60)

    print('Game Over!')
    pygame.quit()

if __name__ == '__main__':
    main()
