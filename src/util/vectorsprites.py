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

import pygame, sys, os, math, random
from math import *
from util.vector2d import *            
from util.geometry import *

class VectorSprite:    
    
    def __init__(self, position, heading, pointlist, angle=0, color=(255, 255, 255)):
        self.position = position
        self.heading = heading        
        self.angle = angle
        self.vAngle = 0
        self.pointlist = pointlist
        self.color = color
        self.ttl = 25        

    # rotate each x,y coord by the angle, then translate it to the x,y position
    def rotate_and_transform(self):
        newPointList = [self.rotate_point(point) for point in self.pointlist]
        self.transformedPointlist = [self.translate_point(point) for point in newPointList]
                
    # draw the sprite            
    def draw(self):
        self.rotate_and_transform()
        return self.transformedPointlist 
                
    # translate each point to the current x, y position     
    def translate_point(self, point):
        newPoint = []
        newPoint.append(point[0] + self.position.x)
        newPoint.append(point[1] + self.position.y)        
        return newPoint
        
    # Move the sprite by the velocity    
    def move(self):                
        # Apply velocity        
        self.position.x = self.position.x + self.heading.x
        self.position.y = self.position.y + self.heading.y
        self.angle = self.angle + self.vAngle

    # Rotate a point by the given angle
    def rotate_point(self, point):
        newPoint = []
        cosVal = math.cos(radians(self.angle))
        sinVal = math.sin(radians(self.angle))
        newPoint.append(point[0] * cosVal + point[1] * sinVal)
        newPoint.append(point[1] * cosVal - point[0] * sinVal)
        
        # Keep points as integers
        newPoint = [int(point) for point in newPoint]                        
        return newPoint
    
    # Scale a point 
    def scale(self, point, scale):
        newPoint = []
        newPoint.append(point[0] * scale)
        newPoint.append(point[1] * scale)
        # Keep points as integers
        newPoint = [int(point) for point in newPoint]                        
        return newPoint

    def collidesWith(self, target):
        if self.boundingRect.colliderect(target.boundingRect):
            return True
        else:
            return False                

    # Check each line from pointlist1 for intersection with the lines in pointlist2
    def check_polygon_collision(self, target):
        for i in range(0, len(self.transformedPointlist)):
            for j in range(0, len(target.transformedPointlist)):                    
                p1 = self.transformedPointlist[i-1]
                p2 = self.transformedPointlist[i]
                p3 = target.transformedPointlist[j-1]
                p4 = target.transformedPointlist[j]                           
                p = calculate_intersect_point(p1, p2, p3, p4)
                if p is not None:
                    return p                
        
        return None

# Used for bullets and debris
class Point(VectorSprite):

    # Class attributes
    pointlist = [(0,0), (1,1), (1,0), (0,1)]
    
    def __init__(self, position, heading, stage):
        VectorSprite.__init__(self, position, heading, self.pointlist)
        self.stage = stage
        self.ttl = 30
        
    def move(self):
        self.ttl -= 1
        if self.ttl <= 0:
            self.stage.remove_sprite(self)
 
        VectorSprite.move(self)
