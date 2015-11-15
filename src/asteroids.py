#! /usr/bin/env python
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
#    Copyright (C) 2008 - 2015  Nick Redshaw
#

import pygame, sys, os, random
from pygame.locals import *  
from util.vectorsprites import *
from ship import *
from stage import *
from badies import *
from shooter import *
from soundManager import *


class Asteroids:
        
    explodingTtl = 180
    
    def __init__(self):        
        self.stage = Stage('Pythentic Asteroids')        
        self.paused = False     
        self.frameAdvance = False   
        self.gameState = "attract_mode"     
        self.rockList = []
        self.create_rocks(8)
        self.saucer = None
        self.secondsCount = 1
        self.score = 0                
        self.ship = None
        self.lives = 0
        
    def initialise_game(self):
        self.gameState = 'playing'
        [self.stage.remove_sprite(sprite) for sprite in self.rockList] # clear old rocks
        if self.saucer is not None: 
            self.kill_saucer()
        self.startLives = 3
        self.create_new_ship()
        self.create_lives_list()
        self.score = 0        
        self.rockList = []
        self.numRocks = 3
        self.nextLife = 10000
        
        self.create_rocks(self.numRocks)
        self.secondsCount = 1

    def create_new_ship(self):
        if self.ship:
            [self.stage.spriteList.remove(debris) for debris in self.ship.shipDebrisList]                                                
        self.ship = Ship(self.stage)                      
        self.stage.add_sprite(self.ship.thrustJet)
        self.stage.add_sprite(self.ship)
        
    def create_lives_list(self):
        self.lives += 1
        self.livesList = []
        for i in range(1, self.startLives):
            self.add_life(i)
            
    def add_life(self, lifeNumber):
        self.lives += 1
        ship = Ship(self.stage)        
        self.stage.add_sprite(ship)
        ship.position.x = self.stage.width - (lifeNumber * ship.boundingRect.width) - 10
        ship.position.y = 0 + ship.boundingRect.height
        self.livesList.append(ship)                                 
        
    def create_rocks(self, numRocks):
        for _ in range(0, numRocks):
            position = Vector2d(random.randrange(-10, 10), random.randrange(-10, 10))
            
            newRock = Rock(self.stage, position, Rock.largeRockType)
            self.stage.add_sprite(newRock)
            self.rockList.append(newRock)

    def play_game(self):

        clock = pygame.time.Clock()        
        
        frameCount = 0.0        
        timePassed = 0.0      
        self.fps = 0.0

        # Main loop                
        while True: 
          
            # fps
            timePassed += clock.tick(60)            
            frameCount += 1            
            if frameCount % 10 == 0:
                self.fps = (frameCount / (timePassed / 1000.0))
                timePassed = 0
                frameCount = 0
          
            self.secondsCount += 1
                                                       
            self.input(pygame.event.get())
            
            if self.paused and not self.frameAdvance:                
                continue
            
            self.stage.screen.fill((0, 0, 0))                                 
            self.stage.move_sprites()
            self.stage.draw_sprites()
            self.do_saucer_logic()
            self.display_score()
            self.check_score()
            # self.displayFps()

            # Process keys
            if self.gameState == 'playing':
                self.playing()                  
            elif self.gameState == 'exploding':
                self.exploding()
            else:
                self.display_text()
                                    
            # Double buffer draw
            pygame.display.flip()     
                                               
    def playing(self):
        if self.lives == 0:
            self.gameState = 'attract_mode'
        else:
            self.process_keys()
            self.check_collisions()
            if len(self.rockList) == 0:
                self.level_up()
            
    def do_saucer_logic(self):
        if self.saucer is not None:            
            if self.saucer.laps >= 2:
                self.kill_saucer()
        
        # Create a saucer
        if self.secondsCount % 2000 == 0 and self.saucer is None:            
            randVal = random.randrange(0,10)
            if randVal <= 3:
                self.saucer = Saucer(self.stage, Saucer.smallSaucerType, self.ship)
            else:
                self.saucer = Saucer(self.stage, Saucer.largeSaucerType, self.ship)
            self.stage.add_sprite(self.saucer)

    def exploding(self):
        self.explodingCount += 1
        if self.explodingCount > self.explodingTtl:
            self.gameState = 'playing'
            [self.stage.spriteList.remove(debris) for debris in self.ship.shipDebrisList]                                        
            self.ship.shipDebrisList = []
                    
            if self.lives == 0:
                self.ship.visible = False
            else:
                self.create_new_ship()
        
    def level_up(self):
        self.numRocks += 1        
        self.create_rocks(self.numRocks)
        
    def display_text(self):
        font1 = pygame.font.Font(None, 50)
        titleText = font1.render('Pythentic Asteroids', True, (255, 255, 255))
        titleTextRect = titleText.get_rect(centerx=self.stage.width/2)        
        titleTextRect.y = self.stage.height/2 - titleTextRect.height*2
        self.stage.screen.blit(titleText, titleTextRect)
                    
        font2 = pygame.font.Font(None, 25)
        keysText = font2.render('Controls: arrow keys rotate left, right and thrust, space to fire, H hyperspace, Esc to quit', True, (255, 255, 255))
        keysTextRect = keysText.get_rect(centerx=self.stage.width/2)        
        keysTextRect.y = self.stage.height/2 - keysTextRect.height/2
        self.stage.screen.blit(keysText, keysTextRect)                

        keysText = font2.render('Alternatively: Z left, X right, M fire, N thrust, H hyperspace, Esc to quit', True, (255, 255, 255))
        keysTextRect = keysText.get_rect(centerx=self.stage.width/2)
        keysTextRect.y = self.stage.height/2 + keysTextRect.height/2
        self.stage.screen.blit(keysText, keysTextRect)

        instructionText = font1.render('Press Enter To Play', True, (255, 255, 255))
        instructionTextRect = instructionText.get_rect(centerx=self.stage.width/2)        
        instructionTextRect.y = self.stage.height/2 + instructionTextRect.height*2
        self.stage.screen.blit(instructionText, instructionTextRect)
                  
    def display_score(self):
        font2 = pygame.font.Font(None, 30)
        scoreStr = str("%06d" % self.score)
        scoreText = font2.render(scoreStr, True, (255, 255, 255))
        scoreTextRect = scoreText.get_rect(centerx=40, centery=15)
        self.stage.screen.blit(scoreText, scoreTextRect)                    

    def display_fps(self):
        font2 = pygame.font.Font(None, 30)
        fpsStr = str(self.fps)
        scoreText = font2.render(fpsStr, True, (255, 255, 255))
        scoreTextRect = scoreText.get_rect(centerx=(self.stage.width/2), centery=15)
        self.stage.screen.blit(scoreText, scoreTextRect)                    
                
    def display_paused(self):
        if self.paused:
            font2 = pygame.font.Font(None, 30)                    
            pausedText = font2.render("Paused", True, (255, 255, 255))
            textRect = pausedText.get_rect(centerx=self.stage.width/2, centery=self.stage.height/2)
            self.stage.screen.blit(pausedText, textRect)
            pygame.display.update()
                    
    # Should move the ship controls into the ship class
    def input(self, events):
        self.frameAdvance = False
        for event in events: 
            if event.type == QUIT: 
                sys.exit(0) 
            elif event.type == KEYDOWN:                
                if event.key == K_ESCAPE:
                    sys.exit(0)
                if self.gameState == 'playing':
                    if event.key == K_SPACE:
                        self.ship.fire_bullet()
                    elif  event.key == K_n:
                        self.ship.fire_bullet()
                    elif event.key == K_h:
                        self.ship.enter_hyper_space()
                elif self.gameState == 'attract_mode':
                    # Start a new game
                    if event.key == K_RETURN:                                                
                        self.initialise_game()
                
                if event.key == K_p:
                    if self.paused:
                        self.paused = False
                    else:
                        self.paused = True                    
                
                if event.key == K_f:
                    pygame.display.toggle_fullscreen()
                    
            elif event.type == KEYUP:
               if event.key == K_o:
                   self.frameAdvance = True                   
                
    def process_keys(self):
        key = pygame.key.get_pressed()
     
        if key[K_LEFT] or key[K_z]:
            self.ship.rotate_left()
        elif key[K_RIGHT] or key[K_x]:
            self.ship.rotate_right()
        
        if key[K_UP] or key[K_m]:
            self.ship.increase_thrust()
            self.ship.thrustJet.accelerating = True
        else:
            self.ship.thrustJet.accelerating = False

    # Check for ship hitting the rocks etc.
    def check_collisions(self):
            
        # Ship bullet hit rock?
        newRocks = []
        shipHit, saucerHit = False, False
        
        # Rocks
        for rock in self.rockList:
            rockHit = False

            if not self.ship.inHyperSpace and rock.collidesWith(self.ship):
                p = rock.check_polygon_collision(self.ship)
                if p is not None:                           
                    shipHit = True
                    rockHit = True
            
            if self.saucer is not None:
                if rock.collidesWith(self.saucer):    
                    saucerHit = True
                    rockHit = True
                
                if self.saucer.bullet_collision(rock):
                    rockHit = True
                    
                if self.ship.bullet_collision(self.saucer):
                    saucerHit = True                    
                    self.score += self.saucer.scoreValue                    
                    
            if self.ship.bullet_collision(rock):
                rockHit = True            
                            
            if rockHit:                
                self.rockList.remove(rock)
                self.stage.spriteList.remove(rock)                
                
                if rock.rockType == Rock.largeRockType:
                    play_sound("explode1")
                    newRockType = Rock.mediumRockType
                    self.score += 50
                elif rock.rockType == Rock.mediumRockType:
                    play_sound("explode2")
                    newRockType = Rock.smallRockType
                    self.score += 100
                else:
                    play_sound("explode3")
                    self.score += 200
                    newRockType = None
                
                if rock.rockType != Rock.smallRockType:
                    # new rocks
                    for _ in range(0, 2):
                        position = Vector2d(rock.position.x, rock.position.y)                  
                        newRock = Rock(self.stage, position, newRockType)
                        self.stage.add_sprite(newRock)
                        self.rockList.append(newRock)
                        
                self.create_debris(rock)

        # Saucer bullets
        if self.saucer is not None:
            if not self.ship.inHyperSpace:
                if self.saucer.bullet_collision(self.ship):
                    shipHit = True            
                    
                if self.saucer.collidesWith(self.ship):
                    shipHit = True            
                    saucerHit = True
                    
            if saucerHit:                
                self.create_debris(self.saucer)
                self.kill_saucer()
                                
        if shipHit:
            self.kill_ship()

    def kill_ship(self):
        stop_sound("thrust")
        play_sound("explode2")
        self.explodingCount = 0
        self.lives -= 1
        if (self.livesList):
            ship = self.livesList.pop()
            self.stage.remove_sprite(ship)
                        
        self.stage.remove_sprite(self.ship)
        self.stage.remove_sprite(self.ship.thrustJet)
        self.gameState = 'exploding'  
        self.ship.explode()    
        
    def kill_saucer(self):
        stop_sound("lsaucer")
        stop_sound("ssaucer")
        play_sound("explode2")
        self.stage.remove_sprite(self.saucer)
        self.saucer = None

    def create_debris(self, sprite):
        for _ in range(0, 25):
            position = Vector2d(sprite.position.x, sprite.position.y)
            debris = Debris(position, self.stage)
            self.stage.add_sprite(debris)

    def check_score(self):
        if self.score > 0 and self.score > self.nextLife:
            play_sound("extralife")
            self.nextLife += 10000
            self.add_life(self.lives)
        
# Script to run the game
if not pygame.font: print 'Warning, fonts disabled'
if not pygame.mixer: print 'Warning, sound disabled'

init_sound_manager()
game = Asteroids()
game.play_game()
