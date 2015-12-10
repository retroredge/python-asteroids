Pythentic Asteroids
====

A [Python](https://www.python.org/) / [Pygame](http://www.pygame.org/) version of Atari's 1979 classic Asteroids arcade game. 

![Title screen](/../gh-pages/images/title-screen.png?raw=true "Title screen")

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

Pygame page
----
The Pygame project page can be found [here](http://pygame.org/project/977/).

Python and Pygame setup on OSX
----
```
brew install python
pip install --upgrade pip setuptools
pip install hg+http://bitbucket.org/pygame/pygame

Licence
----
```
This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see http://www.gnu.org/licenses/.
```
```