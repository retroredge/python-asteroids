#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

import pygame, sys, os
from pygame.locals import *

class Stage:
    
    # Set up the PyGame surface
    def __init__(self, caption, dimensions=None):
        pygame.init()
        
        # Try for 1024 x 768 like the original game otherwise pick highest resolution available
        if dimensions == None:
            modes = pygame.display.list_modes()
            print(modes)
            if (1024, 768) in modes:
                dimensions = (1024, 768)
            else:
                dimensions = modes[0]

        pygame.display.set_mode(dimensions, FULLSCREEN)
        pygame.mouse.set_visible(False)

        pygame.display.set_caption(caption)
        self.screen = pygame.display.get_surface()
        self.spriteList = []
        self.width = dimensions[0]
        self.height = dimensions[1]
        self.showBoundingBoxes = False
        
    # Add sprite to list then draw it as a easy way to get the bounding rect    
    def add_sprite(self, sprite):
        self.spriteList.append(sprite)    
        sprite.boundingRect = pygame.draw.aalines(self.screen, sprite.color, True, sprite.draw())
                
    def remove_sprite(self, sprite):
        self.spriteList.remove(sprite)
        
    def draw_sprites(self):
        for sprite in self.spriteList:
            sprite.boundingRect = pygame.draw.aalines(self.screen, sprite.color, True, sprite.draw())
            if self.showBoundingBoxes == True:
                pygame.draw.rect(self.screen, (255, 255, 255), sprite.boundingRect, 1)        

    def move_sprites(self):
        for sprite in self.spriteList:
            sprite.move()
     
            if sprite.position.x < 0:
                sprite.position.x = self.width
                
            if sprite.position.x > self.width:
                sprite.position.x = 0
            
            if sprite.position.y < 0:
                sprite.position.y = self.height
                
            if sprite.position.y > self.height:
                sprite.position.y = 0