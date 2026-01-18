bIrD by Coo Coo Co.

## Inspiration
Sometimes, you just need to stop and watch the birds. This game was originally inspired by the humble hobby of birdwatching, which serves as both a simple method of entertainment and as a potential opportunity for introspection as we observe these incredible animals. We wanted to create a pleasant and calming game with a solid message to take home, and thought that birds would make the perfect muse for our project.  

## What it does
bIrD allows you to take photographs of birds that you see in the real world and keep track of them in your own virtual birdwatching sanctuary.  After photographing a bird that you spot, bIrD will first identify the species of bird, then add a sprite of the bird into your game.  You are able to choose which birds you would like to display and interact with in the sanctuary, while keeping the rest of them archived in your Roost. 

You are able to chat with your birds, who will develop unique personality traits and mannerisms according to how you interact with them. Watch and talk as they experience different events for the first time in their new virtual world, all of which contribute to shape their identities. It's always fun to chat with your birds, and try to consider how they would respond to the way you speak with them!

## How we built it
This game was implemented in Python using Pygame. The music was custom composed using Strudel.cc, and all of the background art and graphical assets were hand-illustrated in Procreate. Hugging Face was used to load models to do 3 tasks: object detection on images to crop the birds in the photos, object classification to classify the bird species, and finally to do sentiment analysis on the conversations that the users had with the birds to develop appropriate responses in the birds' personalities. The Backboard.io API was used to access different models for the birds' chatbots. 

## Challenges we ran into
None of us have any experience with game development, which is why we chose a beginner-friendly format with Python and Pygame. However, we initially tried using a game engine, which proved to be too steep of a learning curve for us to tackle this time. It was also challenging managing all the custom assets for the game and maintaining a clean implementation, there were so many moving parts that it was often difficult to make small edits without creating unwanted changes. 

## Accomplishments that we're proud of
We're super happy with the final aesthetic of the game. It encapsulates a relaxing environment perfect for introspection and reflection, while also being a fun interactive game! We're also proud of our idea generation process and our final execution, since we had to trim down many ideas and prioritize which features we would want to implement. 
