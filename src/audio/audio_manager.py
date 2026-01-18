import pygame
import random


class AudioManager:
    def __init__(self):
        pygame.mixer.init()
        self.current_music = None
        self.music_volume = 0.7
        self.chirp_timer = 0
        self.next_chirp_interval = random.uniform(5, 15)
        self.chirp_files = [f"assets/audio/chirp_{i}.mp3" for i in range(1, 9)]

    def play_music(self, filepath, loops=-1):
        """
        Play background music.
        loops=-1 means infinite loop.
        """
        try:
            pygame.mixer.music.load(filepath)
            pygame.mixer.music.set_volume(self.music_volume)
            pygame.mixer.music.play(loops)
            self.current_music = filepath
        except pygame.error as e:
            print(f"Could not load music file {filepath}: {e}")

    def stop_music(self):
        """Stop the current music."""
        pygame.mixer.music.stop()
        self.current_music = None

    def play_sfx(self, filepath, volume=None):
        """Play a sound effect (one-off, not looped)."""
        try:
            sound = pygame.mixer.Sound(filepath)
            if volume is not None:
                sound.set_volume(volume)
            sound.play()
        except pygame.error as e:
            print(f"Could not load sound file {filepath}: {e}")

    def set_music_volume(self, volume):
        """Set music volume (0.0 to 1.0)."""
        self.music_volume = max(0.0, min(1.0, volume))
        pygame.mixer.music.set_volume(self.music_volume)

    def update(self, time_delta, current_screen_name=None):
        """Update audio manager (call this every frame)."""
        # Only play chirps on field screen
        if current_screen_name == 'field':
            self.chirp_timer += time_delta
            if self.chirp_timer >= self.next_chirp_interval:
                self.play_random_chirp()
                self.chirp_timer = 0
                self.next_chirp_interval = random.uniform(5, 18)

    def play_random_chirp(self):
        """Play a random chirp sound with random volume."""
        chirp_file = random.choice(self.chirp_files)
        random_volume = random.uniform(0.2, 0.8)
        self.play_sfx(chirp_file, volume=random_volume)

