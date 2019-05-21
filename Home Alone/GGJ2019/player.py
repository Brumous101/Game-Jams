import pygame
import math
from vector import *


class Player:
    def __init__(self, tile_pos, tile_dim):
        self.mSpeed = 200
        self.default_image= pygame.image.load("images/Eddy.png")
        self.character = {(0,1):[],(-1,0):[],(1,0):[],(0,-1):[],(0,0):[]}
        for i in range(3):
            self.character[(0,1)].append(pygame.image.load("images/Eddy.png"))
            self.character[(-1,0)].append(pygame.image.load("images/Eddy.png"))
            self.character[(1,0)].append(pygame.image.load("images/Eddy.png"))
            self.character[(0,-1)].append(pygame.image.load("images/Eddy.png"))
##        self.mImage = pygame.image.load(image_fname)
        self.mDim = [self.default_image.get_width()-4, self.default_image.get_height()-4]
        self.mPos = Vector(tile_pos[0] * tile_dim[0], tile_pos[1] * tile_dim[1])     # World-space (pixels) of upper-left
        self.mMap = None            # When adding a player to the map, the map should set this reference to itself
        self.dx = 0
        self.dy = 0
        # self.shoot = shoot_time
        self.bspeed = 550
        self.currframe = 0
        self.animationtimer = 0
    def handle_keys(self, keys, dt):
        
        old_pos = self.mPos[:]
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.dx = -1
            self.dy = 0
            self.mPos[0] -= self.mSpeed * dt
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.dx = 1
            self.dy = 0
            self.mPos[0] += self.mSpeed * dt
        if not self.mMap.isWalkable((self.mPos[0], self.mPos[1], self.mDim[0], self.mDim[1])):
            self.mPos[0] = old_pos[0]

        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.dx = 0
            self.dy = -1
            self.mPos[1] -= self.mSpeed * dt
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.dx = 0
            self.dy = 1
            self.mPos[1] += self.mSpeed * dt
        if not self.mMap.isWalkable((self.mPos[0], self.mPos[1], self.mDim[0], self.mDim[1])):
            self.mPos[1] = old_pos[1]
        if keys[pygame.K_LEFT] == False and keys[pygame.K_a] == False and keys[pygame.K_RIGHT] == False and keys[pygame.K_d] == False and keys[pygame.K_UP] == False and keys[pygame.K_w] == False and keys[pygame.K_DOWN] == False and keys[pygame.K_s] == False:
##            self.dx = 0
##            self.dy = 0
            self.animationtimer -= dt
    # def pickup(self, sound):
    #
    #     if not self.mMap.isPickupable((self.mPos[0],self.mPos[1],self.mDim[0],self.mDim[1])):
    #         # pygame.mixer.Sound.play(sound)
    #         # pygame.mixer.music.stop()
    #         # books+=1



            
    def render(self, surf, dt):
        self.animationtimer += dt
        if self.animationtimer > 0.2:
            self.currframe = self.currframe + 1
            if self.currframe == 2:
                self.currframe = 0
            self.animationtimer = 0
        
        if self.dx == 0 and self.dy == 0: 
            surf.blit(self.default_image, self.mMap.get_screen_pos(self.mPos[0], self.mPos[1]))
        else:
            surf.blit(self.character[(self.dx,self.dy)][self.currframe], self.mMap.get_screen_pos(self.mPos[0], self.mPos[1]))

    def draw_bullets(self,book,screen,cam_pos):
        i = 0
        while i < len(book):
            b = book[i]
            bx = int(b[0] - cam_pos[0])
            by = int(b[1] - cam_pos[1])
            bx2 = int(b[2] - cam_pos[0])
            by2 = int(b[3] - cam_pos[1])
            pygame.draw.line(screen, (0, 0, 255), (bx, by), (bx2, by2), 25)
            pygame.draw.line(screen, (255, 255, 255), (bx - 10, by), (bx2 - 10, by2), 2)
            pygame.draw.line(screen, (165, 42, 42), (bx, by), (bx2, by2), 2)
            pygame.draw.line(screen, (165, 42, 42), (bx, by), (bx2, by2), 15)
            i += 1
    def book_update(self,book,dt,win_width,win_height,camera):
        self.shoot -= dt  # shooting cool down
        for b in book:
            if b[4] == 0:
                b[3] += (self.bspeed * dt) * b[5]
                b[1] += (self.bspeed * dt) * b[5]
            if b[5] == 0:
                b[0] += (self.bspeed * dt) * b[4]
                b[2] += (self.bspeed * dt) * b[4]
            if b[1] >= camera[1] + win_height or b[3] >= camera[1] + win_height or b[1] <= camera[1] - win_height or b[3] <= camera[1] - win_height or b[0] >= camera[0] + win_width or b[2] >= camera[0] + win_width or b[0] <= camera[0] - win_width or b[2] <= camera[0] - win_width:
                book.remove(b)
