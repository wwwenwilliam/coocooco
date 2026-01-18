import pygame
import pygame_gui
import random
from pygame_gui.elements import UIWindow, UIButton, UITextBox, UITextEntryLine
from src.api.backboard_client import BackboardClient, USE_BACKBOARD_API
from src.data.storage import update_bird_data
from src.ai.sentiment import analyze_text

class TweeterCard(UIWindow):
    def __init__(self, rect, manager, bird_data=None, on_close_callback=None, event_data=None):
        species = bird_data.get('species', 'Bird') if bird_data else 'Bird'
        title = f"Chat with {species}"
        if event_data:
            title = f"{species} is feeling {event_data['type']}!"
            
        super().__init__(rect, manager, title, draggable=False)
        self.bird_data = bird_data
        self.on_close_callback = on_close_callback
        self.species = species
        self.event_data = event_data
        
        # Initialize backboard client
        self.backboard = BackboardClient(bird_data, event_data) if bird_data else None
        
        # Async response handling
        self.waiting_for_response = False
        self.pending_response = None
        
        # Chat history (list of tuples: (sender, message))
        self.chat_history = []
        
        if event_data:
             # Event specific greeting
             self.chat_history.append(("bird", event_data['initial_message']))
        else:
             # Load previous personality or generate greeting
             personality = bird_data.get('personality', '') if bird_data else ''
             if personality:
                 self.chat_history.append(("bird", f"*chirp* Welcome back! I remember you!"))
             else:
                 self.chat_history.append(("bird", f"*chirp* Hello! I'm a {species}. What would you like to talk about?"))

        # Chat Display Area
        self.chat_display = UITextBox(
            html_text=self._format_chat_html(),
            relative_rect=pygame.Rect((10, 10), (rect.width - 20, rect.height - 110)),
            manager=manager,
            container=self
        )
        
        # Text Input
        self.input_line = UITextEntryLine(
            relative_rect=pygame.Rect((10, rect.height - 90), (rect.width - 130, 40)),
            manager=manager,
            container=self,
            placeholder_text="Type a message..."
        )
        
        # Send Button
        self.send_btn = UIButton(
            relative_rect=pygame.Rect((rect.width - 110, rect.height - 90), (100, 40)),
            text='Send',
            manager=manager,
            container=self
        )

    def _format_chat_html(self):
        """Format chat history as HTML for the text box."""
        lines = []
        for sender, message in self.chat_history:
            if sender == "user":
                lines.append(f"<b>You:</b> {message}")
            else:
                lines.append(f"<b>{self.species}:</b> {message}")
        return "<br><br>".join(lines)

    def _get_canned_response(self, user_message):
        """Return a canned placeholder response from the bird."""
        responses = [
            "*chirp chirp* That's very interesting!",
            "*ruffles feathers* Tell me more about that.",
            "*tilts head* I'm just a bird, but I appreciate the thought!",
            "*tweets happily* Thank you for chatting with me!",
            "*hops around* Fascinating!",
        ]
        return random.choice(responses)

    def _get_response_async(self, user_message):
        """Fetch response in background thread."""
        response = None
        
        # Try API first if enabled
        if self.backboard and USE_BACKBOARD_API:
            api_response = self.backboard.send_message(user_message)
            if api_response:
                response = api_response
        
        # Fallback to canned responses
        if not response:
            response = self._get_canned_response(user_message)
        
        self.pending_response = response

    def _send_message(self):
        """Handle sending a message."""
        user_text = self.input_line.get_text().strip()
        if not user_text or self.waiting_for_response:
            return
            
        # Add user message to history and display immediately
        self.chat_history.append(("user", user_text))
        self.chat_display.html_text = self._format_chat_html()
        self.chat_display.rebuild()
        
        # Clear input right away
        self.input_line.set_text("")
        
        # Auto-scroll to show user message
        if self.chat_display.scroll_bar:
            self.chat_display.scroll_bar.set_scroll_from_start_percentage(1.0)
        
        # Start async API call
        self.waiting_for_response = True
        self.pending_response = None
        import threading
        thread = threading.Thread(target=self._get_response_async, args=(user_text,))
        thread.daemon = True
        thread.start()

    def update(self, time_delta):
        """Check for pending responses."""
        if self.waiting_for_response and self.pending_response is not None:
            # Response received
            self.chat_history.append(("bird", self.pending_response))
            self.chat_display.html_text = self._format_chat_html()
            self.chat_display.rebuild()
            
            # Auto-scroll to bottom
            if self.chat_display.scroll_bar:
                self.chat_display.scroll_bar.set_scroll_from_start_percentage(1.0)
            
            self.waiting_for_response = False
            self.pending_response = None

    def _save_chat_data(self):
        """Save chat-related data back to bird_data on close."""
        if not self.bird_data:
            return
            
        updates = {}
        
        # Save backboard IDs if we created them
        if self.backboard:
            backboard_ids = self.backboard.get_ids_for_storage()
            updates.update(backboard_ids)
        
        if updates:
            update_bird_data(self.bird_data['id'], updates)

    def process_event(self, event):
        super().process_event(event)
        
        # Handle Send button click
        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == self.send_btn:
                self._send_message()
        
        # Handle Enter key in text input
        if event.type == pygame_gui.UI_TEXT_ENTRY_FINISHED:
            if event.ui_element == self.input_line:
                self._send_message()
                
    def on_close_window_button_pressed(self):
        self._save_chat_data()
        
        # Trigger sentiment analysis
        if self.event_data and self.bird_data:
             self.analyze_conversation_and_update_trait()
             
        super().on_close_window_button_pressed()
        if self.on_close_callback:
            self.on_close_callback()

    def analyze_conversation_and_update_trait(self):
        # Collect user messages
        user_text = " ".join([msg for sender, msg in self.chat_history if sender == "user"])
        if not user_text: return
        
        print(f"Analyzing traits for: {user_text[:50]}...")
        
        traits = ['Intelligent', 'Curious', 'Brave', 'Lazy', 'Friendly', 'Calm']
        new_scores = analyze_text(user_text, candidate_labels=traits)
        if not new_scores: return
        
        # Load existing scores
        current_scores = self.bird_data.get('trait_scores', {})
        
        # Merge/Init (alpha blending)
        updated_scores = {}
        alpha = 0.5 # 50% update rate
        
        for trait in traits:
            old = current_scores.get(trait, 0.0)
            new = new_scores.get(trait, 0.0)
            updated_scores[trait] = old * (1 - alpha) + new * alpha
            
        # Determine dominant trait
        dominant_trait = max(updated_scores, key=updated_scores.get)
        
        print(f"Updated Composite Traits: {updated_scores}")
        print(f"New Personality: {dominant_trait}")
        
        self.bird_data['trait_scores'] = updated_scores
        self.bird_data['personality'] = dominant_trait
        
        # Clear legacy emotions
        if 'emotion_scores' in self.bird_data:
            del self.bird_data['emotion_scores']
            
        update_bird_data(self.bird_data['id'], self.bird_data)
