import pygame
import random
from npc import *
class Map:
    def __init__(self, fname, blocking_codes, pickup_codes,dialog_codes, Warp_codes, clock):
        self.mMasterClock = clock
        self.mTileWidth = None           # Width of each tile (in pixels)
        self.mTileHeight = None          # Height of each tile (in pixels)
        self.mMapWidth = 0               # Width of map (in tiles)
        self.mMapHeight = 0              # Height of map (in tiles)
        self.mTileImage = None              # Pygame surface containing all tiles in this map
        self.mTileOffsetX = None            # Number of pixels between each tile horizontally in self.mTileImage
        self.mTileOffsetY = None            # Number of pixels between each tile vertically in self.mTileImage
        self.mTileImageNumX = None          # Number of tiles horizontally in self.mTileImage (I naively assume this is the number of tiles self.mTileWidth goes into the widht of the image
        self.mTileImageNumY = None          # Number of tiles horizontally in self.mTileImage
        self.mLayerCount = 0                # Number of Layers(Alex)
        self.mLayer_data_counter = -3
        self.mDataStart = False
        self.mTileCodes = [[],[],[]]                # Will become a 2d list of tile-codes (I'm currently only supporting one tile layer)
        self.mCamera = [0, 0]
        self.loadFlare(fname)
        self.dialog_codes = dialog_codes
        self.mBlockingCodes = blocking_codes
        self.pickup_codes = pickup_codes
        self.Warp_codes = Warp_codes
        self.mPlayer = None
        self.mFName = fname                 # The filename this map was loaded from.



    def get_tile_dimensions(self):
        return (self.mTileWidth, self.mTileHeight)


    def addPlayer(self, P):
        self.mPlayer = P
        P.mMap = self

    def addnpc(self,npc):
        npc.mMap = self

    def setCamera(self, cpos, screen_dim):
        maxi = [self.mMapWidth * self.mTileWidth - screen_dim[0], self.mMapHeight * self.mTileHeight - screen_dim[1]]
        for i in range(2):
            self.mCamera[i] = cpos[i]
            if self.mCamera[i] < 0:
                self.mCamera[i] = 0
            if self.mCamera[i] > maxi[i]:
                self.mCamera[i] = maxi[i]


    def loadFlare(self, fname):
        self.mFName = fname
        self.mTileWidth = None  # Width of each tile (in pixels)
        self.mTileHeight = None  # Height of each tile (in pixels)
        self.mMapWidth = 0  # Width of map (in tiles)
        self.mMapHeight = 0  # Height of map (in tiles)
        self.mTileImage = None  # Pygame surface containing all tiles in this map
        self.mTileOffsetX = None  # Number of pixels between each tile horizontally in self.mTileImage
        self.mTileOffsetY = None  # Number of pixels between each tile vertically in self.mTileImage
        self.mTileImageNumX = None  # Number of tiles horizontally in self.mTileImage (I naively assume this is the number of tiles self.mTileWidth goes into the widht of the image
        self.mTileImageNumY = None  # Number of tiles horizontally in self.mTileImage
        self.mLayerCount = 0  # Number of Layers(Alex)
        section = None
        self.mTileCodes = [[], [], []]
        self.mCamera = [0, 0]
        fp = open(fname, "r")
        self.mLayerCount = 0
        self.mLayer_data_counter = -3
        self.mFName = fname
        self.mDataStart = False

        for line in fp:
            line = line.strip()

            if len(line) == 0:
                continue

            if '[layer]' in line:
                self.mLayerCount += 1

            if len(line) > 2 and line[0] == "[" and line[-1] == "]":
                section = line[1:-1]
            elif section == "header" and line.count("=") == 1:
                parts = line.split("=")
                parts[0] = parts[0].strip()
                if parts[0] == "width":         self.mMapWidth = int(parts[1])
                elif parts[0] == "height":      self.mMapHeight = int(parts[1])
                elif parts[0] == "tilewidth":   self.mTileWidth = int(parts[1])
                elif parts[0] == "tileheight":  self.mTileHeight = int(parts[1])
            elif section == "tilesets" and line.count("=") == 1:
                image_info = line.split("=")[1]
                img_fname, tile_w, tile_h, offset_x, offset_y = image_info.split(",")
                self.mTileOffsetX = int(offset_x)
                self.mTileOffsetY = int(offset_y)
                self.mTileImage = pygame.image.load("images\\" + img_fname).convert_alpha()
                self.mTileImageNumX = self.mTileImage.get_width() // (self.mTileWidth + self.mTileOffsetX)
                self.mTileImageNumY = self.mTileImage.get_height() // (self.mTileHeight + self.mTileOffsetY)
            # elif section == "layer":
            #     #for layer in range(self.mLayerCount):          # Note, this is hardcoded to work with only 3 layers right now(Alex)
            #         if line.count(",") >= self.mMapWidth - 1:
            #             codes = line.split(",")
            #             if len(codes) > self.mMapWidth:
            #                 codes = codes[:-1]
            #             row = []
            #             for c in codes:
            #                 row.append(int(c))
            #             self.mTileCodes[layer].append(row)
            if self.mDataStart:
                if '[layer]' in line:
                    self.mLayer_data_counter += 1
                    self.mDataStart = False
                    continue

                codes = line.split(",")
                if len(codes) >= self.mMapWidth:
                    if codes[-1]is"":
                        codes = codes[:-1]
                    row = []
                    for c in codes:
                        row.append(int(c))
                    self.mTileCodes[self.mLayer_data_counter].append(row)


            if "=" in line:
                left, right = line.split("=")
                if left == "data":
                    self.mDataStart = True

        self.mMasterClock.tick()




    def rect_collides(self, r1, r2):
        return not (r1[0] > r2[0] + r2[2] or r2[0] > r1[0] + r1[2] or
                    r1[1] > r2[1] + r2[3] or r2[1] > r1[1] + r1[3])


    def isWalkable(self, rect):
        """ Returns true if rect (x, y, w, h) overlaps any tiles """
        min_tx = int(rect[0]) // self.mTileWidth
        if min_tx < 0:
            min_tx = 0
        min_ty = int(rect[1]) // self.mTileHeight
        if min_ty < 0:
            min_ty = 0
        max_tx = min_tx + rect[2] // self.mTileWidth + 1
        max_ty = min_ty + rect[3] // self.mTileHeight + 1

        for i in range(min_ty, max_ty + 1):
            y = i * self.mTileHeight
            for j in range(min_tx, max_tx + 1):
                if self.mTileCodes[0][i][j] in self.mBlockingCodes:
                    x = j * self.mTileWidth
                    trect = (x, y, self.mTileWidth, self.mTileHeight)
                    if self.rect_collides(trect, rect):
                        return False
        return True
    def Warpable(self, rect):
        min_tx = int(rect[0]) // self.mTileWidth
        if min_tx < 0:
            min_tx = 0
        min_ty = int(rect[1]) // self.mTileHeight
        if min_ty < 0:
            min_ty = 0
        max_tx = min_tx + rect[2] // self.mTileWidth + 1
        max_ty = min_ty + rect[3] // self.mTileHeight + 1

        for i in range(min_ty, max_ty + 1):
            y = i * self.mTileHeight
            for j in range(min_tx, max_tx + 1):
                if self.mTileCodes[0][i][j] in self.Warp_codes or self.mTileCodes[1][i][j] in self.Warp_codes:
                    x = j * self.mTileWidth
                    trect = (x, y, self.mTileWidth, self.mTileHeight)
                    if self.rect_collides(trect, rect):

                        return False
        return True
    def Warp(self, player):
        playerx = int(player.mPos[0] // self.mMapWidth)
        playery = int(player.mPos[1] // self.mMapHeight)
        if self.mFName == ("maps\\School_Test_Map.txt"):

            if playerx == 28 and playery == 7:
                self.loadFlare("maps\\ATCfirstfloor.txt")
                player.mPos[0] = 132 * self.mTileWidth
                player.mPos[1] = 177 * self.mTileHeight
            elif playerx == 29 and playery == 7:
                self.loadFlare("maps\\ATCfirstfloor.txt")
                player.mPos[0] = 132 * self.mTileWidth
                player.mPos[1] = 177 * self.mTileHeight
            elif playerx == 30 and playery == 7:
                self.loadFlare("maps\\ATCfirstfloor.txt")
                player.mPos[0] = 132 * self.mTileWidth
                player.mPos[1] = 177 * self.mTileHeight

        elif self.mFName == ("maps\\ATCfirstfloor.txt"):

            if playerx == 21 and playery == 28:
                self.loadFlare("maps\\School_Test_Map.txt")
                player.mPos[0] = 69 * self.mTileWidth
                player.mPos[1] = 20 * self.mTileHeight
            elif playerx == 19 and playery == 20:
                self.loadFlare("maps\\School_Test_Map.txt")
                player.mPos[0] = 69 * self.mTileWidth
                player.mPos[1] = 20 * self.mTileHeight
            elif playerx == 20 and playery == 28:
                self.loadFlare("maps\\ATCsecondfloor.txt")
                player.mPos[0] = 46 * self.mTileWidth
                player.mPos[1] = 165 * self.mTileHeight
            elif playerx == 31 and playery == 26:
                self.loadFlare("maps\\ATCsecondfloor.txt")
                player.mPos[0] = 69 * self.mTileWidth
                player.mPos[1] = 39 * self.mTileHeight
            elif playerx == 29 and playery == 15:
                player.mPos[0] = 69 * self.mTileWidth
                player.mPos[1] = 20 * self.mTileHeight
        elif self.mFName == ("maps\\ATCsecondfloor.txt"):

            if playerx == 7 and playery == 26:
                self.loadFlare("maps\\ATCfirstfloor.txt")
                player.mPos[0] = 129 * self.mTileWidth
                player.mPos[1] = 177 * self.mTileHeight
            if playerx == 10 and playery == 15 or playerx == 10 and playery == 16:
                self.loadFlare("maps\\ATCfirstfloor.txt")
                player.mPos[0] = 129 * self.mTileWidth
                player.mPos[1] = 176 * self.mTileHeight






    def isPickupable(self, rect):
        """ Returns true if rect (x, y, w, h) overlaps any tiles """
        min_tx = int(rect[0]) // self.mTileWidth
        if min_tx < 0:
            min_tx = 0
        min_ty = int(rect[1]) // self.mTileHeight
        if min_ty < 0:
            min_ty = 0
        max_tx = min_tx + rect[2] // self.mTileWidth + 1
        max_ty = min_ty + rect[3] // self.mTileHeight + 1

        for i in range(min_ty, max_ty + 1):
           y = i * self.mTileHeight
           for j in range(min_tx, max_tx + 1):
               if self.mTileCodes[1][i][j] in self.pickup_codes:
                    x = j * self.mTileWidth
                    trect = (x, y, self.mTileWidth, self.mTileHeight)
                    if self.rect_collides(trect, rect):
                        self.mTileCodes[1][i][j] = 0

                        return False

        return True


    def __str__(self):
        s = ""
        s += "self.mTileWidth = " + str(self.mTileWidth) + "\n"
        s += "self.mTileHeight = " + str(self.mTileHeight) + "\n"
        s += "self.mMapWidth = " + str(self.mMapWidth) + "\n"
        s += "self.mMapHeight = " + str(self.mMapHeight) + "\n"
        s += "self.mTileImage = " + str(self.mTileImage) + "\n"
        s += "self.mTileOffsetX = " + str(self.mTileOffsetX) + "\n"
        s += "self.mTileOffsetY = " + str(self.mTileOffsetY) + "\n"
        s += "self.mTileImageNumX = " + str(self.mTileImageNumX) + "\n"
        s += "self.mTileImageNumY = " + str(self.mTileImageNumY) + "\n"
        s += "self.mTileCodes =\n"
        for row in self.mTileCodes:
            s += "   " + str(row) + "\n"
        return s


    def draw(self, surf):

        # Draw the map (only the portion we need)
        offsetx = int(self.mCamera[0]) % self.mTileWidth
        offsety = int(self.mCamera[1]) % self.mTileHeight
        sx = int(self.mCamera[0]) // self.mTileWidth
        sy = int(self.mCamera[1]) // self.mTileHeight
        sw = surf.get_width() // self.mTileWidth + 2
        sh = surf.get_height() // self.mTileHeight + 2

        for layer_num in range(self.mLayerCount):
            y = -offsety
            #y = 0
            for row_num in range(sy, sy + sh):
                if row_num < 0 or row_num >= self.mMapHeight:
                    continue
                
                row = self.mTileCodes[layer_num][row_num]
                x = -offsetx
                #x = 0
                for col_num in range(sx, sx + sw):
                    if col_num < 0 or col_num >= self.mMapWidth:
                        continue
                    code = row[col_num]
                    if code != 0:
                        tile_row = (code - 1) // self.mTileImageNumX
                        tile_col = (code - 1) % self.mTileImageNumX
                        tile_x = tile_col * (self.mTileWidth + self.mTileOffsetX)
                        tile_y = tile_row * (self.mTileHeight + self.mTileOffsetY)
                        surf.blit(self.mTileImage, (x, y), (tile_x, tile_y, self.mTileWidth, self.mTileHeight))
                    x += self.mTileWidth
                y += self.mTileHeight

        # Draw those coins that are partially on screen
        # for c in self.mCoins:
        #     if sx <= c[0] <= sx + sw + 1 and sy <= c[1] <= sy + sh:
        #         x = (c[0] + 0.5) * self.mTileWidth - self.mCoinImage.get_width() // 2 - self.mCamera[0]
        #         y = (c[1] + 0.5) * self.mTileHeight - self.mCoinImage.get_height() // 2 - self.mCamera[1]
        #         surf.blit(self.mCoinImage, (x, y))

    def get_screen_pos(self, wx, wy):
        return (wx - self.mCamera[0], wy - self.mCamera[1])


##if __name__ == "__main__":
##    M = Map("maps\\Multi-Layer-Test.txt", (1033, 1165))
##    print(M.mLayerCount)
##    print(M.mTileCodes)
