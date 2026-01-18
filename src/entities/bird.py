import pygame
import random
import os
from .spritesheetanim import SpriteStripAnim
from src.data.events import get_random_event, EVENT_HAPPY, EVENT_SAD, EVENT_ANGRY

# States
IDLE = 0
MOVING = 1
# Event States (imported constants would be better but defining here for simplicity/access)
EVENT_HAPPY = 2
EVENT_SAD = 3
EVENT_ANGRY = 4

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
        self.ground_y = world_height * 0.9 # 1/5 up from bottom = 4/5 down
        
        # Snap to ground immediately
        self.position.y = self.ground_y - self.height
        self.rect.y = int(self.position.y)
        
        self.target = None
        self.speed = 2.0
        self.state = IDLE
        self.idle_timer = 0
        self.is_paused = False
        self.current_event = None
        self.event_timer = 0
        self.pick_new_target()

    def load_sprites(self):
        # Determine species from bird_data
        species = "owl" # default
        if self.bird_data and 'species' in self.bird_data:
            s_lower = self.bird_data['species'].lower()
            if "pigeon" in s_lower or "dove" in s_lower:
                species = "pigeon"
            elif "sparrow" in s_lower:
                species = "sparrow"
            # else remains owl/default
        
        # Path relative to where main.py is run (project root)
        sprite_path_right = os.path.join("assets", "sprites", f"{species}_walk.png")
        sprite_path_left = os.path.join("assets", "sprites", f"{species}_walk_left.png")
        idle_path_right = os.path.join("assets", "sprites", f"{species}_stand.PNG")
        idle_path_left = os.path.join("assets", "sprites", f"{species}_stand_left.PNG")
        
        self.anim_right = None
        self.anim_left = None
        self.anim_iter = None
        
        self.anim_mad = None
        self.anim_mad_iter = None
        
        self.image_idle_right = None
        self.image_idle_left = None
        self.overlay_anims = {}
        self.overlay_anim_iter = None
        self.overlay_image = None
        
        # --- Load Mad (Rage Node) Sprites ---
        mad_specs = {
            "owl": {"file": "owl_mad.png", "w": 405, "h": 340},
            "sparrow": {"file": "sparrow_mad.png", "w": 220, "h": 158},
            "pigeon": {"file": "pigeon_mad.png", "w": 240, "h": 206},
        }
        
        if species in mad_specs:
            spec = mad_specs[species]
            mad_path = os.path.join("assets", "sprites", spec["file"])
            if os.path.exists(mad_path):
                try:
                    # 2 Frames, Loop=True, Delay=8 ticks
                    self.anim_mad = SpriteStripAnim(mad_path, (0, 0, spec["w"], spec["h"]), 2, None, True, 8)
                    self.anim_mad_iter = iter(self.anim_mad)
                except Exception as e:
                    print(f"Error loading mad sprite for {species}: {e}")
            else:
                # print(f"Mad sprite not found: {mad_path}")
                pass

        # --- Load Moving Sprites ---
        if os.path.exists(sprite_path_right):
            try:
                temp_surf = pygame.image.load(sprite_path_right)
                w, h = temp_surf.get_size()
                # Assuming 2 frames horizontal strip
                frame_width = w // 2
                frame_height = h
                self.anim_right = SpriteStripAnim(sprite_path_right, (0, 0, frame_width, frame_height), 2, None, True, 8)
                
                # Default to right
                self.anim_iter = iter(self.anim_right)
                self.image = next(self.anim_iter)
                self.width = self.image.get_width()
                self.height = self.image.get_height()
                self.using_sprite = True
            except Exception as e:
                print(f"Error loading right sprite for {species}: {e}")
                self.using_sprite = False
            
            # Load left if available
            if os.path.exists(sprite_path_left):
                try:
                    temp_surf = pygame.image.load(sprite_path_left)
                    w, h = temp_surf.get_size()
                    frame_width = w // 2
                    frame_height = h
                    self.anim_left = SpriteStripAnim(sprite_path_left, (0, 0, frame_width, frame_height), 2, None, True, 8)
                except Exception as e:
                    print(f"Error loading left sprite for {species}: {e}")
                    self.anim_left = self.anim_right # Fallback
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

        # Load Overlay Sprites
        self.overlay_anims = {}
        overlay_map = {'happy': 'happy.png', 'sad': 'sad.png', 'angry': 'mad.png'}
        for evt, filename in overlay_map.items():
            path = os.path.join("assets", "sprites", filename)
            if os.path.exists(path):
                try:
                    surf = pygame.image.load(path)
                    w, h = surf.get_size()
                    # Assuming 2 frames like walk
                    self.overlay_anims[evt] = SpriteStripAnim(path, (0, 0, w//2, h), 2, None, True, 8)
                except: pass

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
        # Only switch to MOVING if not in an event
        if self.state not in [EVENT_HAPPY, EVENT_SAD, EVENT_ANGRY]:
            self.state = MOVING
        
        # Switch animation based on ACTUAL movement direction (after clamping)
        if self.using_sprite and self.anim_left and self.anim_right:
            actual_dx = target_x - self.position.x
            if actual_dx < 0:
                # Moving left
                self.anim_iter = iter(self.anim_left)
                self.facing_right = False
            elif actual_dx > 0:
                # Moving right
                self.anim_iter = iter(self.anim_right)
                self.facing_right = True
            # If actual_dx == 0, no movement - keep current facing direction
            
            # Update image immediately to match direction (only if we have movement)
            if actual_dx != 0:
                try:
                    self.image = next(self.anim_iter)
                except StopIteration:
                    pass

    def update(self, dt):
        # Check for Global CRASHOUT
        from src.data.game_state import GlobalState
        is_crashout = GlobalState.get_instance().is_crashout
        
        if is_crashout:
            # RAGE MODE ANIMATION
            if self.anim_mad_iter:
                try:
                    self.image = next(self.anim_mad_iter)
                    self.width = self.image.get_width()
                    self.height = self.image.get_height()
                except StopIteration:
                     pass
            
            # RAGE MODE: Vibrate violently
            offset_x = random.randint(-5, 5)
            offset_y = random.randint(-5, 5)
            
            # Recalculate base position with new height (so they stay on ground)
            # self.ground_y is fixed. self.position.y should be ground_y - self.height
            base_y = self.ground_y - self.height
            self.position.y = base_y
            
            self.rect.center = (int(self.position.x + offset_x + self.width//2), 
                                int(self.position.y + offset_y + self.height//2))
            return # Skip normal logic

        if self.is_paused:
            return
            
        # Custom sprite setup
        if self.using_sprite:
            if self.state == MOVING or self.state in [EVENT_HAPPY, EVENT_SAD, EVENT_ANGRY]:
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
                     
        # Update Overlay Animation
        if self.overlay_anim_iter:
            try:
                self.overlay_image = next(self.overlay_anim_iter)
            except: pass
        else:
            self.overlay_image = None
            
        if self.state == MOVING and self.target:
            # Ensure Y is correct if height changed back from rage
            self.position.y = self.ground_y - self.height
            
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
            # Fix Y
            self.position.y = self.ground_y - self.height
            
            # Low chance to trigger event if IDLE
            if random.random() < 0.005: 
                self.trigger_random_event()
                
            self.idle_timer -= dt
            if self.idle_timer <= 0:
                self.pick_new_target()
                
        elif self.state in [EVENT_HAPPY, EVENT_SAD, EVENT_ANGRY]:
             # Check Timeout
             self.event_timer -= dt
             # print(f"DEBUG: Bird Event Timer: {self.event_timer:.2f}")
             if self.event_timer <= 0:
                 self.end_event()
                 return

             # In event state, keep moving but slower
             if not self.target:
                 self.pick_new_target()
             
             direction = self.target - self.position
             dist = direction.length()
             
             if dist < 5:
                 self.pick_new_target() # Keep moving
             else:
                 direction.normalize_ip()
                 self.position += direction * (self.speed * 0.5) # Slower
                 
                 # Update facing direction
                 if direction.x > 0: self.facing_right = True
                 elif direction.x < 0: self.facing_right = False
        
        # Update rect for collision detection (in world space)
        self.rect.topleft = (int(self.position.x), int(self.position.y))
        
        if self.overlay_image:
             pass  # Overlay is drawn in draw() method

    def trigger_random_event(self):
        event = get_random_event()
        self.current_event = event
        self.state = event['state']
        self.event_timer = 4.0 # 4 seconds duration
        
        # Setup overlay
        evt_type = event['type']
        if evt_type in self.overlay_anims:
            self.overlay_anim_iter = iter(self.overlay_anims[evt_type])
            try:
                self.overlay_image = next(self.overlay_anim_iter)
            except: pass
        else:
             self.overlay_anim_iter = None
             self.overlay_image = None
             
        # print(f"Bird entered event: {event['type']}")

    def end_event(self):
        """End the current event and return to normal behavior."""
        self.state = 0 # IDLE
        self.current_event = None
        self.overlay_image = None
        self.overlay_anim_iter = None
        self.pick_new_target()

    def update_bounds(self, new_bounds_rect):
        """Update bounds and reposition bird proportionally (size stays fixed)."""
        old_bounds = self.bounds_rect
        old_world_width = old_bounds[2]
        
        new_world_width = new_bounds_rect[2]
        new_world_height = new_bounds_rect[3]
        
        # Calculate relative position (0.0 to 1.0 across the world)
        rel_x = self.position.x / old_world_width if old_world_width > 0 else 0.5
        
        # Update bounds
        self.bounds_rect = new_bounds_rect
        
        # Recalculate ground_y
        self.ground_y = new_world_height * 0.9
        
        # Reposition proportionally (size stays the same)
        self.position.x = rel_x * new_world_width
        self.position.y = self.ground_y - self.height
        
        # Clamp to bounds
        self.position.x = max(0, min(self.position.x, new_world_width - self.width))
        
        # Update rect position (size unchanged)
        self.rect.topleft = (int(self.position.x), int(self.position.y))
        
        # Update target if moving
        if self.target:
            self.target.y = self.ground_y - self.height
            self.target.x = max(0, min(self.target.x, new_world_width - self.width))

    def draw(self, surface, scroll_x):
        # Render Transform: World -> Screen
        screen_pos = (self.rect.x - scroll_x, self.rect.y)
        surface.blit(self.image, screen_pos)
        
        if self.overlay_image:
            surface.blit(self.overlay_image, screen_pos)

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
