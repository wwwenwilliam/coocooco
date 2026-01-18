"""
Event definitions for random bird encounters.
"""

EVENT_HAPPY = 2
EVENT_SAD = 3
EVENT_ANGRY = 4

EVENT_POOL = [
    {
        "type": "happy",
        "state": EVENT_HAPPY,
        "description": "I found a shiny button!",
        "prompt": "You are extremely happy because you found a shiny button on the ground. Act very excited.",
        "initial_message": "*Chirp!* Look what I found! A shiny button! Isn't it amazing?"
    },
    {
        "type": "sad",
        "state": EVENT_SAD,
        "description": "I dropped my worm...",
        "prompt": "You are very sad because you dropped your delicious worm. act depressed and cry a lot.",
        "initial_message": "*Sniff*... my worm... it fell in the dirt..."
    },
    {
        "type": "angry",
        "state": EVENT_ANGRY,
        "description": "A squirrel stole my spot!",
        "prompt": "You are angry because a squirrel took your favorite branch. Rant about squirrels.",
        "initial_message": "*Screech!* That squirrel! He TOOK my spot! Can you believe the nerve?"
    }
]

def get_random_event():
    import random
    return random.choice(EVENT_POOL)
