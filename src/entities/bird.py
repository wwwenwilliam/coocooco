import pygame
import random
import pygame_gui

# States
IDLE = 0
MOVING = 1

class Bird(pygame.sprite.Sprite):
    def __init__(self, pos, bounds_rect):
        super().__init__()
        self.bounds_rect = bounds_rect # (0, 0, width, height) of the world
        
        # Visuals (Placeholder)
        self.width = 50
        self.height = 50
        self.color = (random.randint(50, 255), random.randint(50, 255), random.randint(50, 255))
        self.image = pygame.Surface((self.width, self.height))
        self.image.fill(self.color)
        self.rect = self.image.get_rect(topleft=pos)
        
        # Movement properties
        self.position = pygame.Vector2(pos)
        self.target = None
        self.speed = 2.0
        self.state = IDLE
        self.idle_timer = 0
        self.pick_new_target()

    def pick_new_target(self):
        """Pick a random target within bounds."""
        x = random.randint(self.bounds_rect[0], self.bounds_rect[2] - self.width)
        y = random.randint(self.bounds_rect[1], self.bounds_rect[3] - self.height)
        self.target = pygame.Vector2(x, y)
        self.state = MOVING

    def update(self, dt):
        if self.state == MOVING and self.target:
            direction = self.target - self.position
            distance = direction.length()
            
            if distance < 5:
                # Reached target
                self.position = self.target
                self.state = IDLE
                self.idle_timer = random.uniform(1.0, 3.0) # Wait 1-3 seconds
            else:
                direction = direction.normalize()
                self.position += direction * self.speed
                
        elif self.state == IDLE:
            self.idle_timer -= dt
            if self.idle_timer <= 0:
                self.pick_new_target()
        
        # Update rect for collision detection (in world space)
        self.rect.topleft = (int(self.position.x), int(self.position.y))

    def draw(self, surface, scroll_x):
        # Render Transform: World -> Screen
        screen_pos = (self.rect.x - scroll_x, self.rect.y)
        surface.blit(self.image, screen_pos)

    def handle_event(self, event, scroll_x):
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            # Check click in World Space
            # Mouse is Screen Space, so add scroll_x to get World X
            world_mouse_pos = (mouse_pos[0] + scroll_x, mouse_pos[1])
            
            if self.rect.collidepoint(world_mouse_pos):
                print(f"Clicked bird at {self.position}! Info card placeholder.")
                return True
        return False
