from pygame import *


#класс-родитель для других спрайтов
class GameSprite(sprite.Sprite):
 # конструктор класса
 def __init__(self, player_image, player_x, player_y, size_x, size_y):
     # Вызываем конструктор класса (Sprite):
     sprite.Sprite.__init__(self)
     # каждый спрайт должен хранить свойство image - изображение
     self.image = transform.scale(image.load(player_image), (size_x, size_y))


     # каждый спрайт должен хранить свойство rect - прямоугольник, в который он вписан
     self.rect = self.image.get_rect()
     self.rect.x = player_x
     self.rect.y = player_y
 # метод, отрисовывающий героя на окне
 def reset(self):
     window.blit(self.image, (self.rect.x, self.rect.y))


#класс главного игрока
class Player(GameSprite):
 #метод, в котором реализовано управление спрайтом по кнопкам стрелкам клавиатуры
 def __init__(self, player_image, player_x, player_y, size_x, size_y, player_x_speed,player_y_speed):
     # Вызываем конструктор класса (Sprite):
     GameSprite.__init__(self, player_image, player_x, player_y,size_x, size_y)


     self.x_speed = player_x_speed
     self.y_speed = player_y_speed


 def update(self):
      
      # сначала движение по горизонтали
      if packman.rect.x <= win_width-80 and packman.x_speed > 0 or packman.rect.x >= 0 and packman.x_speed < 0:
        self.rect.x += self.x_speed
      # если зашли за стенку, то встанем вплотную к стене
      platforms_touched = sprite.spritecollide(self, barriers, False)
      if self.x_speed > 0: # идем направо, правый край персонажа - вплотную к левому краю стены
          for p in platforms_touched:
              self.rect.right = min(self.rect.right, p.rect.left) # если коснулись сразу нескольких, то правый край - минимальный из возможных
      elif self.x_speed < 0: # идем налево, ставим левый край персонажа вплотную к правому краю стены
          for p in platforms_touched:
              self.rect.left = max(self.rect.left, p.rect.right) # если коснулись нескольких стен, то левый край - максимальный
      if packman.rect.y <= win_height-80 and packman.y_speed > 0 or packman.rect.y >= 0 and packman.y_speed < 0:
        self.rect.y += self.y_speed
      # если зашли за стенку, то встанем вплотную к стене
      platforms_touched = sprite.spritecollide(self, barriers, False)
      if self.y_speed > 0: # идем вниз
          for p in platforms_touched:
              self.y_speed = 0
              # Проверяем, какая из платформ снизу самая высокая, выравниваемся по ней, запоминаем её как свою опору:
              if p.rect.top < self.rect.bottom:
                  self.rect.bottom = p.rect.top
      elif self.y_speed < 0: # идем вверх
          for p in platforms_touched:
              self.y_speed = 0  # при столкновении со стеной вертикальная скорость гасится
              self.rect.top = max(self.rect.top, p.rect.bottom) # выравниваем верхний край по нижним краям стенок, на которые наехали
 # метод "выстрел" (используем место игрока, чтобы создать там пулю)
 def fire(self):
     bullet = Bullet('bullet.png', self.rect.right, self.rect.centery, 15, 20, 15)
     bullets.add(bullet)


#класс спрайта-врага   
class Enemy(GameSprite):
 side = "left"
 def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
     # Вызываем конструктор класса (Sprite):
     GameSprite.__init__(self, player_image, player_x, player_y, size_x, size_y)
     self.speed = player_speed


  #движение врага
 def update(self):
     if self.rect.x <= 420: #w1.wall_x + w1.wall_width
         self.side = "right"
     if self.rect.x >= win_width - 85:
         self.side = "left"
     if self.side == "left":
         self.rect.x -= self.speed
     else:
         self.rect.x += self.speed


# класс спрайта-пули  
class Bullet(GameSprite):
 def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
     # Вызываем конструктор класса (Sprite):
     GameSprite.__init__(self, player_image, player_x, player_y, size_x, size_y)
     self.speed = player_speed
 # движение врага
 def update(self):
     self.rect.x += self.speed
     # исчезает, если дойдет до края экрана
     if self.rect.x > win_width+10:
         self.kill()


#Создаем окошко
win_width = 700
win_height = 500
display.set_caption("Лабиринт")
window = display.set_mode((win_width, win_height))
back = (119, 210, 223)#задаем цвет согласно цветовой схеме RGB


#создаем группу для стен
barriers = sprite.Group()


#создаем группу для пуль
bullets = sprite.Group()


#создаем группу для монстров
monsters = sprite.Group()


#создаем стены картинки
w1 = GameSprite('platform2.png',win_width / 2 - win_width / 3, win_height / 2, 300, 50)
w2 = GameSprite('platform2_v.png', 370, 100, 50, 400)


#добавляем стены в группу
barriers.add(w1)
barriers.add(w2)


#создаем спрайты
packman = Player('hero.png', 5, win_height - 80, 80, 80, 0, 0)
final_sprite = GameSprite('pac-1.png', win_width - 85, win_height - 100, 80, 80)


monster1 = Enemy('cyborg.png', win_width - 80, 150, 80, 80, 5)
monster2 = Enemy('cyborg.png', win_width - 80, 230, 80, 80, 5)
#добавляем монстра в группу
monsters.add(monster1)
monsters.add(monster2)


#переменная, отвечающая за то, как кончилась игра
finish = False
#игровой цикл
run = True
while run:
 #цикл срабатывает каждую 0.05 секунд
    time.delay(50)
  #перебираем все события, которые могли произойти
    for e in event.get():
        if e.type == QUIT:
            run = False
        elif e.type == KEYDOWN:
            if e.key == K_LEFT:
                packman.x_speed = -5
            elif e.key == K_RIGHT:
                packman.x_speed = 5
            elif e.key == K_UP:
                packman.y_speed = -5
            elif e.key == K_DOWN:
                packman.y_speed = 5
            elif e.key == K_SPACE:
                packman.fire()


        elif e.type == KEYUP:
            if e.key == K_LEFT:
                packman.x_speed = 0
            elif e.key == K_RIGHT:
                packman.x_speed = 0
            elif e.key == K_UP:
                packman.y_speed = 0
            elif e.key == K_DOWN:
                packman.y_speed = 0


#проверка, что игра еще не завершена
    if not finish:
     #обновляем фон каждую итерацию
        window.fill(back)#закрашиваем окно цветом
    
     #запускаем движения спрайтов
        packman.update()
        bullets.update()


      #обновляем их в новом местоположении при каждой итерации цикла
        packman.reset()
     #рисуем стены 2
     #w1.reset()
     #w2.reset()
        bullets.draw(window)
        barriers.draw(window)
        final_sprite.reset()


        sprite.groupcollide(monsters, bullets, True, True)
        monsters.update()
        monsters.draw(window)
        sprite.groupcollide(bullets, barriers, True, False)


     #Проверка столкновения героя с врагом и стенами
        if sprite.spritecollide(packman, monsters, False):
            finish = True
         #вычисляем отношение
            img = image.load('game-over_1.png')
            d = img.get_width() // img.get_height()
            window.fill((255, 255, 255))
            window.blit(transform.scale(img, (win_height * d, win_height)), (90, 0))


        if sprite.collide_rect(packman, final_sprite):
            finish = True
            img = image.load('thumb.jpg')
            window.fill((255, 255, 255))
            window.blit(transform.scale(img, (win_width, win_height)), (0, 0))
    display.update()

'''# Разработай свою игру в этом файл
from pygame import *

back = (50, 50, 50)
mw = display.set_mode((700, 500))
display.set_caption('Снюс')
run = True
finish = False

class GameSprite(sprite.Sprite):
    def __init__ (self, picture, w, h, x, y):
        super().__init__()
        self.image=transform.scale(image.load(picture),(w,h))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    def reset(self):
        mw.blit(self.image, (self.rect.x,self.rect.y))

class Player(GameSprite):
    def __init__(self, picture, w, h, x, y, x_speed, y_speed):
        GameSprite.__init__(self, picture, w, h, x, y)
        self.x_speed = x_speed
        self.y_speed = y_speed
    def update(self):
        if player.rect.x <= 700-50 and player.x_speed > 0 or player.rect.x >= 0 and player.x_speed < 0:
            self.rect.x += self.x_speed
        platforms_touched = sprite.spritecollide(self, barriers, False)
        if self.x_speed > 0:
            for p in platforms_touched:
                self.rect.right = min(self.rect.right, p.rect.left)
        elif self.x_speed < 0:
            for p in platforms_touched:
                self.rect.left = max(self.rect.left, p.rect.right)
        if player.rect.y <= 500-65 and player.y_speed > 0 or player.rect.y >= 0 and player.y_speed < 0:
            self.rect.y += self.y_speed
        platforms_touched = sprite.spritecollide(self,barriers,False)
        if self.y_speed > 0:
            for p in platforms_touched:
                self.rect.bottom = min(self.rect.bottom, p.rect.top)
        elif self.y_speed < 0:
            for p in platforms_touched:
                self.rect.top = max(self.rect.top, p.rect.bottom)
    def fire(self):
        bullet = Bullet('bullet.png',15,20,self.rect.right, self.rect.centery,15)
        bullets.add(bullet)

class Enemy(GameSprite):
    def __init__(self, picture, w, h, x, y, speed):
        super().__init__(picture, w, h, x, y)
        self.speed = speed
        self.direction = 'left'
    def update(self):
        if self.rect.x <= 400:
            self.direction = 'right'
        if self.rect.x >= 650:
            self.direction = 'left'
        if self.direction == 'left':
            self.rect.x -= self.speed
        else:
            self.rect.x += self.speed

class Bullet(GameSprite):
    def __init__(self, picture, w, h, x, y, speed):
        super().__init__(picture, w, h, x, y)
        self.speed = speed
    def update (self):
        self.rect.x += self.speed
        if self.rect.x > 700 + 10:
            self.kill()


wall_1 = GameSprite('294wabk65pwb.png', 350,50,175,220)
wall_2 = GameSprite('294wabk65pwb.png', 50,350,330,70)
player = Player('pngwing.com.png',50,65,70,210,0,0)
final = GameSprite('egggg.png',50,65,550,210)
enemy = Enemy('pngegg.png',50,65,570,410, 5)
win = transform.scale(image.load('340ada26-49f7-48f1-a572-b27dd6ec766b.jpg'),(700,500))
lose = transform.scale(image.load('EGS_DOOM3_idSoftwarePanicButton_S1_2560x1440-e29ea97ef0c5689b6ee1b5ae12d9a1bb.jpg'),(700,500))

barriers = sprite.Group()
barriers.add(wall_1)
barriers.add(wall_2)

bullets = sprite.Group()

enemies = sprite.Group()
enemies.add(enemy)

while run:
    time.delay(50)
    for e in event.get():
        if e.type == QUIT: 
            run = False
        elif e.type == KEYDOWN:
            if e.key == K_UP:
                player.y_speed = -5
            elif e.key == K_DOWN:
                player.y_speed = 5
            elif e.key == K_LEFT:
                player.x_speed = -5
            elif e.key == K_RIGHT:
                player.x_speed = 5
            elif e.key == K_SPACE:
                player.fire()
        elif e.type == KEYUP:
            if e.key == K_UP:
                player.y_speed = 0
            elif e.key == K_DOWN:
                player.y_speed = 0
            elif e.key == K_LEFT:
                player.x_speed = 0
            elif e.key == K_RIGHT:
                player.x_speed = 0



    if finish != True:
        mw.fill(back)
        player.update()
        bullets.update()
        player.reset()
        bullets.draw(mw)
        barriers.draw(mw)
        final.reset()
        sprite.groupcollide(bullets,enemies,True,True)
        enemies.update()
        enemies.draw(mw)
        sprite.groupcollide(bullets,barriers,True,False)

        if sprite.collide_rect(player, final):
            finish = True
            mw.blit(win,(0,0))
        elif sprite.spritecollide(player, enemies, False):
            finish = True
            mw.blit(lose,(0,0))
        
        
    display.update()'''