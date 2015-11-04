Pythentic Asteroids
====

A [Python](https://www.python.org/) / [Pygame](http://www.pygame.org/) version of Atari's 1979 classic Asteroids arcade game. 

Controls
----
- Start game : Enter   
- Rotate Left : Left arrow or Z
- Rotate Right : Right arrow or X
- Thrust : Up arrow or N 
- Fire : Space or M
- Hyperspace : H
- Pause : P
- Frame advance whilst paused : O 
- Quit : Esc

Features
----
- Pixel perfect collision detection. 
- Authentic asteroids shapes 
- Small and large saucers 
- Full screen
- Fading explosion debris 
- Engine thrust jet 
- Extra life at 10,000 
- Hyperspace

Collision Detection
----
If a bounding box collision occurs between the sprites then extra checks are made to determine if there are any intersections 
between line segments that make up each sprite. The intersecting line checks can be found in the geometry.py source file.