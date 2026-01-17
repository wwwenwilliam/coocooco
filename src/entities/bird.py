import pygame
import random
import pygame_gui
import os
from .spritesheetanim import SpriteStripAnim

# States
IDLE = 0
MOVING = 1

class Bird(pygame.sprite.Sprite):
    def __init__(self, pos, bounds_rect, bird_data=None):
        super().__init__()
        self.bounds_rect = bounds_rect # (0, 0, width, height) of the world
        self.bird_data = bird_data
        
        # Visuals
        self.width = 100
        self.height = 100
        self.facing_right = True # Track direction for idle state
        
        self.load_sprites()
            
        self.rect = self.image.get_rect(topleft=pos)
        
        # Movement properties
        self.position = pygame.Vector2(pos)
        
        # Constrain Y to "ground" (1/5 up from bottom)
        # bounds_rect is (x, y, w, h)
        world_height = self.bounds_rect[3]
        self.ground_y = world_height * 0.8 # 1/5 up from bottom = 4/5 down
        
        # Snap to ground immediately
        self.position.y = self.ground_y - self.height
        self.rect.y = int(self.position.y)
        
        self.target = None
        self.speed = 2.0
        self.state = IDLE
        self.idle_timer = 0
        self.is_paused = False
        self.pick_new_target()

    def load_sprites(self):
        # Path relative to where main.py is run (project root)
        sprite_path_right = os.path.join("assets", "sprites", "owl_walk.png")
        sprite_path_left = os.path.join("assets", "sprites", "owl_walk_left.png")
        idle_path_right = os.path.join("assets", "sprites", "owl_stand.PNG")
        idle_path_left = os.path.join("assets", "sprites", "owl_stand_left.PNG")
        
        self.anim_right = None
        self.anim_left = None
        self.anim_iter = None
        self.image_idle_right = None
        self.image_idle_left = None
        
        # Load Moving Sprites
        if os.path.exists(sprite_path_right):
            # OWL: (0, 0, 261, 340), count=2, loop=True, frames=8
            self.anim_right = SpriteStripAnim(sprite_path_right, (0, 0, 261, 340), 2, None, True, 8)
            # Default to right
            self.anim_iter = iter(self.anim_right)
            self.image = next(self.anim_iter)
            self.width = self.image.get_width()
            self.height = self.image.get_height()
            self.using_sprite = True
            
            # Load left if available
            if os.path.exists(sprite_path_left):
                self.anim_left = SpriteStripAnim(sprite_path_left, (0, 0, 261, 340), 2, None, True, 8)
            else:
                self.anim_left = self.anim_right # Fallback
        else:
            self.using_sprite = False
            
        # Load Idle Sprite Right
        if os.path.exists(idle_path_right):
             try:
                self.image_idle_right = pygame.image.load(idle_path_right).convert_alpha()
             except Exception as e:
                print(f"Failed to load idle sprite right: {e}")
        else:
             print(f"Warning: Idle sprite not found at {idle_path_right}")

        # Load Idle Sprite Left
        if os.path.exists(idle_path_left):
             try:
                self.image_idle_left = pygame.image.load(idle_path_left).convert_alpha()
             except Exception as e:
                print(f"Failed to load idle sprite left: {e}")
        else:
             print(f"Warning: Idle sprite not found at {idle_path_left}")
             self.image_idle_left = self.image_idle_right # Fallback

        # Fallback visuals if no sprite at all
        if not self.using_sprite and not self.image_idle_right:
             self.color = (random.randint(50, 255), random.randint(50, 255), random.randint(50, 255))
             self.image = pygame.Surface((self.width, self.height))
             self.image.fill(self.color)
        elif not self.using_sprite and self.image_idle_right:
             self.image = self.image_idle_right
             self.width = self.image.get_width()
             self.height = self.image.get_height()
        elif self.using_sprite and not self.image_idle_right: 
             # Use first frame as idle if no dedicated idle
             pass

    def pick_new_target(self):
        """Pick a random target within bounds, but with short hops."""
        # Short hop distance
        hop_min = 100
        hop_max = 300
        
        direction = random.choice([-1, 1])
        distance = random.randint(hop_min, hop_max)
        dx = direction * distance
        
        target_x = self.position.x + dx
        
        # Clamp to bounds
        target_x = max(self.bounds_rect[0], min(target_x, self.bounds_rect[2] - self.width))
        
        # Constrain target Y to same ground level
        y = self.ground_y - self.height
        self.target = pygame.Vector2(target_x, y)
        self.state = MOVING
        
        # Switch animation based on direction
        if self.using_sprite and self.anim_left and self.anim_right:
            if target_x < self.position.x:
                self.anim_iter = iter(self.anim_left)
                self.facing_right = False
            else:
                self.anim_iter = iter(self.anim_right)
                self.facing_right = True

    def update(self, dt):
        if self.is_paused:
            return
            
        # Custom sprite setup
        if self.using_sprite:
            if self.state == MOVING:
                try:
                    self.image = next(self.anim_iter)
                    # Update dimensions to match the current sprite frame
                    self.width = self.image.get_width()
                    self.height = self.image.get_height()
                except StopIteration:
                    pass # Should loop
            elif self.state == IDLE:
                idle_img = self.image_idle_right if self.facing_right else self.image_idle_left
                # Fallback to right if left missing, handled in load but double check
                if not idle_img and self.image_idle_right: idle_img = self.image_idle_right
                
                if idle_img:
                     self.image = idle_img
                     self.width = self.image.get_width()
                     self.height = self.image.get_height()

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
                species = self.bird_data.get('species', 'Unknown') if self.bird_data else 'Unknown'
                print(f"Clicked bird: {species} at {self.position}! Info card placeholder.")
                return True
        return False
