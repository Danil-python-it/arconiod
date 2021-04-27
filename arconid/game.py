from pygame import *
from random import randint

width = 1000
height = 800
window = display.set_mode((width,height))
display.set_caption("arconoid")
fon = transform.scale(image.load("png/fon.jpg"),(width,height))
win_fon = transform.scale(image.load("png/win_fon.jpg"),(width,height))
pred_win_fon= transform.scale(image.load("png/win_round.png"),(width,height))
game_over_fon = transform.scale(image.load("png/GAME_OVER_FON.png"),(width,height))
menu = transform.scale(image.load("png/menu.jpg"),(width,height))
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
sprite_buff = ["png/buff.png","png/debuff.png"]
init()

mixer.music.load('png/music.mp3')

music_game_over_one = mixer.Sound("png/game_over_one.ogg")
music_game_over_two = mixer.Sound("png/game_over_two.ogg")
collide = mixer.Sound("png/collide.ogg")
bonus = mixer.Sound("png/bonus.ogg")
predwin = mixer.Sound("png/predwin.ogg")



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
        if res != 0 or ros != -1:
            collide.play()
            print(6)
        
        if ros != -1:
            if randint(0,100) >= 80 and player_board.step != 35:
                buff = Up(self.rect.x+15,self.rect.y,75,75,sprite_buff[randint(0,1)],4)
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
            (randint(77,255),randint(77,255),randint(77,255))
        )

class Up(GameSprite):
    def update(self):
        self.rect.y += self.step
        self.y += self.step


        



player_board = platform(400,725,200,50,None,15)
player_boll = bullet(400,500,75,75,"png/boll.png",10)
button = Rect(107,414,191,50)
for i in range(col_block):
    stoyn = block(one_x,one_y,100,50)
    stoyn.coloring()
    one_x += 110
    if one_x == width:
        one_y += 60
        one_x = 10
    all_block.append(stoyn)
    
game = True
win_or_over = True
GameStutus = False

while game:
    for i in event.get():
        if i.type == QUIT:
            game = False

        if i.type == MOUSEBUTTONDOWN:
            x,y = i.pos
            print(x,y)
            
            if GameStutus == False:
                res = button.collidepoint(x,y)
                if res == 1:
                    col_block = 9
                    all_block = list()
                    one_x = 10
                    one_y = 10
                    mixer.music.play()
                    for i in range(col_block):
                        stoyn = block(one_x,one_y,100,50)
                        stoyn.coloring()
                        one_x += 110
                        if one_x == width:
                            one_y += 60
                            one_x = 10
                        all_block.append(stoyn)
                    GameStutus = True
                    win_or_over = True

    going = key.get_pressed()

    if GameStutus == False:
        window.blit(menu,(0,0))
        mixer.music.pause()
        if going[K_SPACE] and GameStutus == False:
            GameStutus = True
            mixer.music.play()
            
    elif GameStutus != False:
        
        if win_or_over == True:
            window.blit(fon,(0,0))
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
                        body = i.body
                        bonus.play()
                        i.kill()
                        stutus_speed_board = True

            if stutus_speed_board != False and deup != False: 
                if body == "png/buff.png":
                    player_board.step += 20
                    timer = 300
                elif body == "png/debuff.png":
                    player_board.step -= 10
                    timer = 100
                deup = False
                
            if timer > 0 and player_board.step != 15 : 
                timer -= 1
                if timer == 0:
                    player_board.step = 15
                    stutus_speed_board = False
                    deup = True
            
            
            if player_boll.rect.y > height-player_boll.l-10 or len(all_block) <= 0:
                win_or_over = False
                if len(all_block) != 0: 
                    mixer.music.pause()
                    if randint(1,2) == 1:
                        music_game_over_one.play()
                    else:
                        music_game_over_two.play()
                elif len(all_block) == 0 and col_block >= 45:
                    mixer.music.load("png/win_fon.ogg")
                    predwin.play()
                    mixer.music.play()


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
            stutus_speed_board = False
            deup = True

            if going[K_ESCAPE]:
                GameStutus = False

            for i in all_buff:
                i.kill()
            
            if len(all_block) <= 0:
                window.blit(pred_win_fon,(0,0))
                if going[K_SPACE]:
                    win_or_over = True
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

            elif len(all_block) == 0 and col_block >= 45:
                window.blit(win_fon,(0,0))
            
            
            else:
                window.blit(game_over_fon,(0,0))
                if going[K_SPACE]:
                    win_or_over = True
                    col_block = 9
                    all_block = list()
                    one_x = 10
                    one_y = 10
                    mixer.music.play()
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