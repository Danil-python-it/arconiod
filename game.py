from pygame import *
from random import randint

width = 1000
height = 800
window = display.set_mode((width,height))
display.set_caption("arconoid")
window.fill((255,255,255))
clock = time.Clock()
FPS = 60
one_x = 10
one_y = 10
col_block = 9
all_block = list()
all_buff = sprite.Group()
stutus_speed_board = False
deup = True
timer = 0

class GameSprite(sprite.Sprite):
    def __init__(self, x_coor, y_coor, width, length, body=None, step=10):
        super().__init__()
        self.x = x_coor
        self.y = y_coor
        self.w = width
        self.l = length
        self.body = body
        self.step = step
        self.color = (77,77,77)


        self.rect = Rect(x_coor, y_coor, self.w, self.l)
        if self.body != None:
            self.persona = transform.scale(image.load(self.body), (self.w, self.l))
    
    def resert(self):
        
        if self.body != None:
            window.blit(self.persona,(self.x, self.y))
        else:
            draw.rect(window,self.color,self.rect)

class platform(GameSprite):
    def update(self):
        if going[K_a] and self.rect.x > 0:
            self.rect.x -= self.step
        
        if going[K_d] and self.rect.x < width-self.w:
            self.rect.x += self.step



class bullet(GameSprite):
    def __init__(self, x_coor, y_coor, width, length, body, step):
        super().__init__(x_coor, y_coor, width, length, body, step)
        self.stepX = step
        self.stepY = step
    
    def update(self):
        self.rect.x += self.stepX
        self.rect.y += self.stepY
        self.x += self.stepX
        self.y += self.stepY
        res = self.rect.colliderect(player_board.rect)

        ros = self.rect.collidelist(all_block)
        if ros != -1:
            if randint(0,100) >= 80 and player_board.step != 25:
                buff = Up(self.rect.x+15,self.rect.y,75,75,"png/buff.png",4)
                all_buff.add(buff)
            del all_block[ros]
            self.stepY *= -1


        if self.rect.y < 0 or self.rect.y > height-self.l or res == 1:
            self.stepY *= -1
            if self.rect.y > 725:
                self.stepX *= -1

        if self.rect.x < 0 or self.rect.x > width-self.w:
            self.stepX *= -1

class block(GameSprite):
    def coloring(self):
        self.color = (
            (randint(30,255),randint(30,255),randint(30,255))
        )

class Up(GameSprite):
    def update(self):
        self.rect.y += self.step
        self.y += self.step



player_board = platform(400,725,200,50,None,15)
player_boll = bullet(400,500,75,75,"png/boll.png",10)
for i in range(col_block):
    stoyn = block(one_x,one_y,100,50)
    stoyn.coloring()
    one_x += 110
    if one_x == width:
        one_y += 60
        one_x = 10
    all_block.append(stoyn)
    
game = True
Stutus_game = True
while game:
    for i in event.get():
        if i.type == QUIT:
            game = False

        if i.type == MOUSEBUTTONDOWN:
            x,y = i.pos
            print(x,y)
    going = key.get_pressed()

    if Stutus_game == True:
        window.fill((0,0,0))
        player_board.resert()
        player_boll.resert()
        player_board.update()
        player_boll.update()
        for i in all_block:
            i.resert()
        if len(all_buff) > 0:
            for i in all_buff:
                i.resert()
                i.update()
                if i.rect.y > height:
                    i.kill()
    
                ras = player_board.rect.colliderect(i.rect)
                if ras != 0:
                    i.kill()
                    stutus_speed_board = True

        if stutus_speed_board != False and deup != False: 
            player_board.step += 20
            deup = False
            timer = 200
        


        print(player_board.step)
        if timer > 0 and player_board.step != 15 : 
            timer -= 1
            if timer == 0:
                player_board.step -= 20
                stutus_speed_board = False
                deup = True
        
        
        if player_boll.rect.y > height-player_boll.l or len(all_block) <= 0:
            Stutus_game = False
        


    else:
        player_boll.rect.x = 400
        player_boll.rect.y = 650
        player_boll.x = 400
        player_boll.y = 650
        player_board.rect.y = 725
        player_board.rect.x = 300
        player_boll.stepX = -10
        player_boll.stepY = -10
        player_board.step = 15
        for i in all_buff:
            i.kill()
        
        if len(all_block) <= 0:
            window.fill((0,255,0))
            if going[K_SPACE]:
                Stutus_game = True
                col_block += 9
                all_block = list()
                one_x = 10
                one_y = 10
                for i in range(col_block):
                    stoyn = block(one_x,one_y,100,50)
                    stoyn.coloring()
                    one_x += 110
                    if one_x == width:
                        one_y += 60
                        one_x = 10
                    all_block.append(stoyn)

        else:
            window.fill((255,0,0))
            if going[K_SPACE]:
                Stutus_game = True
                col_block = 9
                all_block = list()
                one_x = 10
                one_y = 10
                for i in range(col_block):
                    stoyn = block(one_x,one_y,100,50)
                    stoyn.coloring()
                    one_x += 110
                    if one_x == width:
                        one_y += 60
                        one_x = 10
                    all_block.append(stoyn)
    
    display.update()
    clock.tick(FPS)