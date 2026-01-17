from abc import ABC, abstractmethod
import pygame

class Screen(ABC):
    def __init__(self, screen_manager, manager, window_size):
        self.screen_manager = screen_manager
        self.manager = manager
        self.window_size = window_size

    @abstractmethod
    def setup(self):
        """Initialize screen resources and UI elements."""
        pass
    
    @abstractmethod
    def process_event(self, event):
        """Process local screen events."""
        pass

    @abstractmethod
    def update(self, time_delta):
        """Update screen logic."""
        pass

    @abstractmethod
    def draw(self, surface):
        """Draw screen content to the surface."""
        pass

    @abstractmethod
    def cleanup(self):
        """Clean up screen resources and UI elements."""
        pass
