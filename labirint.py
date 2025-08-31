# Maze
from pygame import *

class GameSprite(sprite.Sprite):

    def __init__(self, player_image, player_x, player_y, size_x, size_y):
        sprite.Sprite.__init__(self)
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))



class Player(GameSprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_x_speed,player_y_speed):
        GameSprite.__init__(self, player_image, player_x, player_y,size_x, size_y)
        self.x_speed = player_x_speed
        self.y_speed = player_y_speed

    def update(self):
        if  packman.rect.x <= win_width-80 and packman.x_speed > 0 or packman.rect.x >= 0 and packman.x_speed < 0:
            self.rect.x += self.x_speed
      
        platforms_touched = sprite.spritecollide(self, barriers, False)
        if self.x_speed > 0: 
            for p in platforms_touched:
                self.rect.right = min(self.rect.right, p.rect.left) 
        elif self.x_speed < 0:
            for p in platforms_touched:
                self.rect.left = max(self.rect.left, p.rect.right)
        if packman.rect.y <= win_height-80 and packman.y_speed > 0 or packman.rect.y >= 0 and packman.y_speed < 0:
            self.rect.y += self.y_speed
        
        platforms_touched = sprite.spritecollide(self, barriers, False)
        if self.y_speed > 0: 
            for p in platforms_touched:
                self.y_speed = 0
                
                if p.rect.top < self.rect.bottom:
                    self.rect.bottom = p.rect.top
        elif self.y_speed < 0: 
            for p in platforms_touched:
                self.y_speed = 0 
                self.rect.top = max(self.rect.top, p.rect.bottom) 
    
    def fire(self):
        bullet = Bullet('bullet.png', self.rect.right, self.rect.centery, 15, 20, 15)
        bullets.add(bullet)



class Enemy(GameSprite):
    side = "left"
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        GameSprite.__init__(self, player_image, player_x, player_y, size_x, size_y)
        self.speed = player_speed

    def update(self):
        if self.rect.x <= 420: 
            self.side = "right"
        if self.rect.x >= win_width - 85:
            self.side = "left"
        if self.side == "left":
            self.rect.x -= self.speed
        else:
            self.rect.x += self.speed

class Bullet(GameSprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        GameSprite.__init__(self, player_image, player_x, player_y, size_x, size_y)
        self.speed = player_speed

    def update(self):
        self.rect.x += self.speed
        if self.rect.x > win_width+10:
            self.kill()


win_width = 700
win_height = 500
display.set_caption("Maze")
window = display.set_mode((win_width, win_height))
back = (119, 210, 223)

barriers = sprite.Group()

bullets = sprite.Group()

monsters = sprite.Group()

w1 = GameSprite('Wall.png',win_width / 2 - win_width / 3, win_height / 2, 200, 100)
w2 = GameSprite('Wall.png', 340, 130, 50, 300)
w3 = GameSprite('Wall.png', 340, 50, 90, 400)
w4 = GameSprite('Wall.png',win_width / 1 - win_width / -1, win_height / 3, 300, 60)
w5 = GameSprite('Wall.png',win_width / 3 - win_width / 5, win_height / 5, 400, 50)
w6 = GameSprite('Wall.png', 350, 60, 60, 300)
w7 = GameSprite('Wall.png',win_width / 4 - win_width / 6, win_height / 6, 100, 80)
w8 = GameSprite('Wall.png',win_width / 2 - win_width / 5, win_height / 4, 200, 70)
w9 = GameSprite('Wall.png', 300, 100, 10, 100)

barriers.add(w1)
barriers.add(w2)
barriers.add(w3)
barriers.add(w4)
barriers.add(w5)
barriers.add(w6)
barriers.add(w7)
barriers.add(w8)
barriers.add(w9)

packman = Player('Trollface lol.png', 5, win_height - 80, 80, 80, 0, 0)
final_sprite = GameSprite('Exit door no bg.png', win_width - 85, win_height - 100, 80, 80)


monster1 = Enemy('Trollge 1.png', win_width - 80, 150, 80, 80, 5)
monster2 = Enemy('Trollge 2.png', win_width - 80, 230, 80, 80, 5)

monsters.add(monster1)
monsters.add(monster2)

finish = False

run = True
while run:

    time.delay(50)
    for e in event.get():
        if e.type == QUIT:
            run = False
        elif e.type == KEYDOWN:
            if e.key == K_a:
                packman.x_speed = -5
            elif e.key == K_d:
                packman.x_speed = 5
            elif e.key == K_w:
                packman.y_speed = -5
            elif e.key == K_s:
                packman.y_speed = 5
            elif e.key == K_SPACE:
                packman.fire()


        elif e.type == KEYUP:
            if e.key == K_a:
                packman.x_speed = 0
            elif e.key == K_d:
                packman.x_speed = 0
            elif e.key == K_w:
                packman.y_speed = 0
            elif e.key == K_s:
                packman.y_speed = 0

    if not finish:
        window.fill(back)
        packman.update()
        bullets.update()
        packman.reset()

        #drawing the walls 2
        #w1.reset()
        #w2.reset()

        bullets.draw(window)
        barriers.draw(window)
        final_sprite.reset()


        sprite.groupcollide(monsters, bullets, True, True)
        monsters.update()
        monsters.draw(window)
        sprite.groupcollide(bullets, barriers, True, False)

    if sprite.spritecollide(packman, monsters, False):
        finish = True

        img = image.load('GAME OVER.jpg')
        d = img.get_width() // img.get_height()
        window.fill((255, 255, 255))
        window.blit(transform.scale(img, (win_height * d, win_height)), (90, 0))

    if sprite.collide_rect(packman, final_sprite):
        finish = True
        img = image.load('YOU WIN.jpg')
        window.fill((255, 255, 255))
        window.blit(transform.scale(img, (win_width, win_height)), (0, 0))
            
    display.update()
