#---套件模組載入---
import pygame as pg
import random
import os  #方便存取路徑
#---套件模組載入---

#---遊戲環境基本設定---
FPS = 60
WIDTH = 1200
HEIGHT = 800
#---遊戲環境基本設定---

#---顏色---
WHITE = (255,255,255)
BLACK = (0,0,0)
GREEN = (0,255,0)
RED = (255,0,0)
YELLOW = (255,255,0) #Bullet的顏色
ROCK = (112,66,20) #Rock的顏色
SKY_BLUE = (135,206,235)
BABY_PINK = (255,217,230)
#---顏色---


#---遊戲初始化 與 創建視窗---
pg.init()
pg.mixer.init() #音效模組初始化
screen = pg.display.set_mode((WIDTH,HEIGHT))  #設置遊戲視窗寬度及高度 (turple)
pg.display.set_caption("狗狗可以吃什麼？")  #修改遊戲視窗標題
game_icon = pg.image.load(os.path.join("image", "maru0.png")).convert()
pg.display.set_icon(game_icon)  #修改遊戲視窗標題圖示
clock = pg.time.Clock() #設置遊戲迴圈執行的速度
#---遊戲初始化 與 創建視窗---


#---載入圖片---
background_img = pg.image.load(os.path.join("image", "background_dog.png")).convert()  #convert函式可將圖片轉換為pygame方便讀取的格式
background_img = pg.transform.scale(background_img, (WIDTH,HEIGHT))
background_gameover_img = pg.image.load(os.path.join("image", "background_gameover.png")).convert()
background_gameover_img = pg.transform.scale(background_gameover_img, (WIDTH,HEIGHT))
player_img = pg.image.load(os.path.join("image", "dog.png")).convert()
player_life_img = pg.image.load(os.path.join("image", "heart.png")).convert() #玩家的生命數
water_img = pg.image.load(os.path.join("image", "water.png")).convert()
dog_img = pg.image.load(os.path.join("image", "dog5.png")).convert()  
#可以吃的
food_imgs = []
for i in range(3):
    food_imgs.append(pg.image.load(os.path.join("image", "food{i}.png".format(i=i))).convert())

#不可以吃的
not_food_imgs = []
for i in range(3):
    not_food_imgs.append(pg.image.load(os.path.join("image", "not_food{i}.png".format(i=i))).convert())

#---爆炸動畫---
explore_animation = [] #字典存放爆炸動畫
for i in range(9):
    explore_img = pg.image.load(os.path.join("image", "player_expl{i}.png".format(i=i) )).convert()
    explore_img.set_colorkey(BLACK)
    explore_animation.append(explore_img)
#---爆炸動畫---

#---載入圖片---


#---載入字體---
font_name = os.path.join("font","General_Art.ttf") #綜藝字體

#---載入音樂---
eat_sound = pg.mixer.Sound(os.path.join("sound", "eat.mp3"))
wrong_eat_sound = pg.mixer.Sound(os.path.join("sound", "wrong_eat.mp3"))
bark_sound = pg.mixer.Sound(os.path.join("sound", "bark.mp3"))
water_sound = pg.mixer.Sound(os.path.join("sound", "water.mp3"))
fail_sound = pg.mixer.Sound(os.path.join("sound", "fail.mp3"))
#背景音樂要持續播放，所以載入的方法有所不同
pg.mixer.music.load(os.path.join("sound", "background.mp3"))
pg.mixer.music.set_volume(0.5) #背景音樂音量
#---載入音樂---


#此方法用來處理把文字寫到畫面上的動作
def draw_text(surf, color, text, size, x, y): #(寫在什麼平面上, 文字內容, 文字大小, x座標, y座標)
    font = pg.font.Font(font_name, size)
    text_surface = font.render(text, True, color) #渲染(要渲染的文字, 是否反鋸齒(antialias), 文字顏色)
    text_rect = text_surface.get_rect()
    text_rect.centerx = x
    text_rect.top = y
    surf.blit(text_surface, text_rect) #畫出來(要畫的東西, 畫的位置)

#此方法用來處理把圖片放到畫面上的動作
def draw_image(surf, img, size, x, y):
    image_surface = pg.transform.scale(img, size)
    image_surface.set_colorkey(BLACK)
    image_rect = image_surface.get_rect()
    image_rect.centerx = x
    image_rect.top = y
    surf.blit(image_surface, image_rect)


#此方法用來畫生命條
def draw_health_bar(surf, hp, x, y): #(畫在哪裡？, 生命量, 座標x, 座標y)
    if hp < 0: #檢查生命值是否為零
        hp = 0
    BAR_LENGTH = 100
    BAR_HEIGHT = 10
    fill =( hp / 100) * BAR_LENGTH
    #生命條外框
    outline_rect = pg.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    pg.draw.rect(surf, WHITE, outline_rect, 2) #生命條外框 2 = 2像素
    #生命條內部
    fill_rect = pg.Rect(x, y, fill, BAR_HEIGHT)
    pg.draw.rect(surf, GREEN, fill_rect) #生命條填滿
    

def newFood(): #新增可以吃的
    food = Food()
    all_sprites.add(food)
    foods.add(food) #將food加進foods群組

def newNot_food(): #新增不能吃的
    not_food = Not_food()
    not_food.speedx = random.randrange(-3, 3) #左右移動
    not_food.speedy = 10 #落下 
    all_sprites.add(not_food)
    not_foods.add(not_food) #將Not_food加進Not_foods群組

def newWater():
    water = Water()
    all_sprites.add(water)
    waters.add(water) 



#此方法用來畫剩幾條命
def draw_lifes(surf, lifes, img, x, y):
    for i in range(lifes): #看還剩幾條命
        image_surface = pg.transform.scale(img, (20, 20))
        image_surface.set_colorkey(BLACK) 
        img_life = image_surface.get_rect()
        img_life.x = x - 30 * i #從傳入的位置開始畫，要間隔大於圖片寬度再畫一個
        img_life.y = y
        surf.blit(image_surface, img_life)

#此方法用來畫遊戲初始畫面
def draw_init():
    screen.fill(WHITE) #(R,G,B)
    draw_text(screen, BLACK, '狗狗可以吃什麼？', 64, WIDTH/2, HEIGHT/4)
    draw_text(screen, BLACK,'鍵盤 ← → 移動狗狗', 42, WIDTH/2, HEIGHT/4+100)
    draw_text(screen, GREEN,'狗狗可以吃：', 32, WIDTH/2 - 150, HEIGHT/2)
    for i in range(len(food_imgs)):
        draw_image(screen, food_imgs[i], (70,70), (WIDTH/2) + i * 90, HEIGHT/2 - 25)

    draw_text(screen, RED,'狗狗不能吃：', 32, WIDTH/2 - 150, HEIGHT/2 + 100)   
    for i in range(len(not_food_imgs)):
        draw_image(screen, not_food_imgs[i], (70,70), (WIDTH/2) + i * 90, HEIGHT/2 + 75)     
    
    draw_text(screen, BLACK,'按任意鍵開始遊戲!', 18, WIDTH/2, HEIGHT/ 1.35 )
    draw_image(screen, dog_img, (450,210), 225, HEIGHT-210)

    pg.display.update() #更新遊戲畫面
    waiting_key_press = True
    while waiting_key_press:
        clock.tick(FPS)  #一秒鐘內最多被執行60次（FPS）
        #---取得遊戲中的輸入--
        for event in pg.event.get():  #回傳發生的事件（列表形式）
            if event.type == pg.QUIT: #當按下視窗左上 X ，遊戲結束
                pg.quit()
                exit()
            elif event.type == pg.KEYUP: #當按下任意按鍵，跳出此迴圈，回到遊戲迴圈
                waiting_key_press = False

#此方法用來畫遊戲結束畫面        
def draw_gameover():
    screen.blit(background_gameover_img,(0,0))
    draw_text(screen, WHITE,'', 36, WIDTH/2, 250 )
    draw_text(screen, WHITE,'按空白鍵重新開始遊戲!', 28, WIDTH/2, 300  )
    pg.display.update()
    waiting_key_press = True
    while waiting_key_press:
        clock.tick(FPS)  #一秒鐘內最多被執行60次（FPS）
        #---取得遊戲中的輸入--
        for event in pg.event.get():  #回傳發生的事件（列表形式）
            if event.type == pg.QUIT: #當按下視窗左上 X ，遊戲結束
                pg.quit()
                exit()
            elif event.type == pg.KEYUP: #當按下任意按鍵，跳出此迴圈，回到遊戲迴圈
                if event.key == pg.K_SPACE:
                    waiting_key_press = False
    
#---玩家---
class Player(pg.sprite.Sprite):
    #遊戲初始的設定
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        #self.image = pg.Surface((100, 40)) #建立一個Surface，有圖片就不需要
        self.image = pg.transform.scale(player_img, (100, 100)) #transform.scale 函式可以把圖片調整成需要的大小
        self.image.set_colorkey(BLACK) #set_colorkey 設定顏色透明度，傳入參數(RGB值)
        #self.image.fill(GREEN) #有圖片就不需要填滿
        self.rect = self.image.get_rect() #把image框起來
        self.radius = self.rect.width / 2 - 5
        #circle:畫圓(畫在哪裡？image, 顏色？RED, 中心點位置？rect, 圓的半徑？radius)
        #pg.draw.circle(self.image, RED, self.rect.center, self.radius)
        #玩家出現位置
        self.rect.centerx = (WIDTH/2)
        self.rect.bottom = (HEIGHT - 10)
        self.speedx = 8
        self.health = 100 #Player的生命值
        self.lifes = 3
        self.hidden = False #判斷玩家是否正在隱藏
        self.hide_time = 0
        
    #不斷地更新遊戲中的動作    
    def update(self):
        now = pg.time.get_ticks()
        #把Player重新顯示
        #如果Player正在隱藏，而且當update被呼叫時的時間 - 隱藏時間，已經大於1秒鐘
        if self.hidden and (now - self.hide_time) > 1000:  
            self.hidden = False
            #傳回初始位置
            self.rect.centerx = (WIDTH / 2)
            self.rect.bottom = (HEIGHT - 10)

        
        #會回傳布林值，判斷鍵盤是否有被按下去 有：True 沒有：False
        key_pressed = pg.key.get_pressed() 
        if key_pressed[pg.K_RIGHT]:
            self.rect.x += self.speedx
        if key_pressed[pg.K_LEFT]:
            self.rect.x -= self.speedx
        '''
        if key_pressed[pg.K_UP]:
            self.rect.y -= self.speedx
        if key_pressed[pg.K_DOWN]:
            self.rect.y += self.speedx
        '''
        #self.rect.x += 2  #image向右移動 (x:左右, y:上下)
        #self.rect.y += 2  #image向下移動 (x:左右, y:上下)
        
        #使物件不超出視窗
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        
        if self.rect.top < 0 and not(self.hidden):
            self.rect.top = 0
        if self.rect.bottom > HEIGHT and not(self.hidden):
            self.rect.bottom = HEIGHT
        
        #判斷物件是否已超出視窗
        '''
        if self.rect.left > WIDTH:  
            self.rect.x = 0
        if self.rect.right < 0:
            self.rect.x = WIDTH
        if self.rect.top > HEIGHT:  
            self.rect.y = 0
        if self.rect.bottom < 0:
            self.rect.y = HEIGHT
        '''
    def hide(self): #玩家隱藏
        self.hidden = True
        self.hide_time = pg.time.get_ticks()
        self.rect.center = (WIDTH / 2, HEIGHT + 200) #定位到視窗以外
#---玩家---        
        

#---可以吃的食物---            
class Food(pg.sprite.Sprite):
    #遊戲初始的設定
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        #self.image = pg.Surface((30, 30)) #建立一個Surface
        #self.image_ori = pg.transform.scale(rock_img, (30, 30)) #transform.scale 函式可以把圖片調整成需要的大小
        self.image_ori = random.choice(food_imgs)
        self.image_ori = pg.transform.scale(self.image_ori, (70, 70))
        self.image_ori.set_colorkey(BLACK) #set_colorkey 設定顏色透明度，傳入參數(RGB值)
        self.image = self.image_ori.copy()
    
        
        self.rect = self.image.get_rect() #把image框起來
        self.radius = self.rect.width / 2
        #circle:畫圓(畫在哪裡？image, 顏色？RED, 中心點位置？rect, 圓的半徑？radius)
        #pg.draw.circle(self.image, RED, self.rect.center, self.radius) 
        
        #Food位置隨機出現
        self.rect.x = random.randrange(0, (WIDTH - self.rect.width))
        self.rect.y = random.randrange(-130, -80)
        #Food落下的時間也是隨機的
        self.speedx = random.randrange(-3, 3) #左右移動
        self.speedy = random.randrange(2, 6) #落下
        
        #圖片旋轉設定
        self.total_degree = 0
        self.rotate_degree = random.randrange(-6, 6)
     
     #圖片旋轉動作
    def rotate(self):
        self.total_degree += self.rotate_degree
        self.total_degree = self.total_degree % 360
        self.image = pg.transform.rotate(self.image_ori, self.total_degree) #(要旋轉的圖片, 轉動幾度？)   
        #self.image = pg.transform.rotate(self.image, self.rotate_degree) #(要旋轉的圖片, 轉動幾度？)
        image_center = self.rect.center #記錄原先定位的中心點
        self.rect = self.image.get_rect() #對轉動過的圖片(Food)重新框起來
        self.rect.center = image_center   

        
    #不斷地更新遊戲中的動作    
    def update(self):
        self.rotate() #旋轉
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        
        #當Food超出視窗，再掉一次
        if self.rect.top > HEIGHT or self.rect.left > WIDTH or self.rect.right < 0:
            #Food位置隨機出現
            self.rect.x = random.randrange(0, (WIDTH - self.rect.width))
            self.rect.y = random.randrange(-100, -40)
            #Food落下的時間也是隨機的
            self.speedx = random.randrange(-3, 3) #左右移動
            self.speedy = random.randrange(2, 6) #落下
    
#---可以吃的食物---


#---不可以吃的食物--- 
class Not_food(pg.sprite.Sprite):
    #遊戲初始的設定
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.image_ori = random.choice(not_food_imgs)
        self.image_ori = pg.transform.scale(self.image_ori, (70, 70))
        self.image_ori.set_colorkey(BLACK) #set_colorkey 設定顏色透明度，傳入參數(RGB值)
        self.image = self.image_ori.copy()
    
        
        self.rect = self.image.get_rect() #把image框起來
        self.radius = self.rect.width / 2
        #circle:畫圓(畫在哪裡？image, 顏色？RED, 中心點位置？rect, 圓的半徑？radius)
        #pg.draw.circle(self.image, RED, self.rect.center, self.radius) 
        
        #Food位置隨機出現
        self.rect.x = random.randrange(0, (WIDTH - self.rect.width))
        self.rect.y = random.randrange(-130, -80)
        #Food落下的時間也是隨機的
        self.speedx = random.randrange(-3, 3) #左右移動
        self.speedy = random.randrange(6,10) #落下
        
        #圖片旋轉設定
        self.total_degree = 0
        self.rotate_degree = random.randrange(-6, 6)
     
     #圖片旋轉動作
    def rotate(self):
        self.total_degree += self.rotate_degree
        self.total_degree = self.total_degree % 360
        self.image = pg.transform.rotate(self.image_ori, self.total_degree) #(要旋轉的圖片, 轉動幾度？)   
        #self.image = pg.transform.rotate(self.image, self.rotate_degree) #(要旋轉的圖片, 轉動幾度？)
        image_center = self.rect.center #記錄原先定位的中心點
        self.rect = self.image.get_rect() #對轉動過的圖片(Food)重新框起來
        self.rect.center = image_center   

        
    #不斷地更新遊戲中的動作    
    def update(self):
        self.rotate() #旋轉
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        
        #當Food超出視窗，再掉一次
        if self.rect.top > HEIGHT or self.rect.left > WIDTH or self.rect.right < 0:
            #Food位置隨機出現
            self.rect.x = random.randrange(0, (WIDTH - self.rect.width))
            self.rect.y = random.randrange(-100, -40)
            #Food落下的時間也是隨機的
            self.speedx = random.randrange(-3, 3) #左右移動
            self.speedy = random.randrange(6, 10) #落下
                

#---爆炸動畫---        
class Explosion(pg.sprite.Sprite):
    def __init__(self, center): #(爆炸中心點)
        pg.sprite.Sprite.__init__(self)
        self.image = explore_animation[0]  #爆炸的第一張圖片
        self.rect = self.image.get_rect()
        self.rect.center = center  #中心點定位在傳進來的中心點
        self.frame = 0 #代表已經更新到第幾張圖片了
        self.last_update = pg.time.get_ticks()  #記錄最後一次更新圖片的時間，get_ticks()會回傳從初始化到現在經過的毫秒數
        self.frame_rate = 50  #frame_rate代表至少要經過幾毫秒才會更新到下一張圖片
        
        '''
        為什麼要記錄最後一次圖片更新的時間及至少要過多久才要更新到下一張？
        因為如果用update方法來更新會太快(FPS為60)
        所以要用frame_rate來判斷上一次圖片更新的時間和現在時間是否已經過了50毫秒(frame_rate值)？
        如果經過了frame_rate才讓它更新
        '''
    def update(self): 
        now = pg.time.get_ticks() #代表update被執行當下的時間
        if (now - self.last_update) > self.frame_rate: #now - 上一次圖片更新的時間
            self.last_update = now
            self.frame += 1  #到第幾張圖片了？
            if self.frame == len(explore_animation): #判斷目前的frame有沒有到最後一張了？
                self.kill()
            else:
                self.image = explore_animation[self.frame]  #如果沒有，則更新到下一張
                center = self.rect.center 
                self.rect = self.image.get_rect() #對爆炸圖片重新定位
                self.rect.center = center  #定位在原先的中心點
#---爆炸動畫---


#---補生命值---
class Water(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.image = water_img
        self.image = pg.transform.scale(water_img, (30, 75))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        #self.rect.center = center
        #位置隨機出現
        self.rect.x = random.randrange(0, (WIDTH - self.rect.width))
        self.rect.y = random.randrange(-100, -40)
        #落下的時間也是隨機的
        self.speedx = random.randrange(-3, 3) #左右移動
        self.speedy = random.randrange(2, 6) #落下    
        self.speedy = 3 #寶物是向下掉落，所以正數，y軸移動，

    def update(self):
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT:
            self.kill()
#---補生命值---        
    
pg.mixer.music.play(-1) #(參數)音樂要重複播放幾次？

#---遊戲迴圈---
show_init = True #遊戲初始畫面
running = True #控制遊戲啓閉
while running:
    if show_init:
        draw_init()
        show_init = False

        #---sprite群組，可以放sprite的物件---
        all_sprites = pg.sprite.Group()
        foods = pg.sprite.Group()
        not_foods = pg.sprite.Group()
        waters = pg.sprite.Group()
        player = Player()
        all_sprites.add(player)
        for i in range(5): #Food出現次數
            newFood()
        for i in range(5): #Not_food出現次數
            newNot_food()
        score = 0 #記錄分數

    clock.tick(FPS)  #一秒鐘內最多被執行60次（FPS）
    #---取得遊戲中的輸入--
    for event in pg.event.get():  #回傳發生的事件（列表形式）
        if event.type == pg.QUIT:
            running = False
                
    #---更新遊戲---
    all_sprites.update() #去執行all_sprites 每一個物件(sprite)的update函式
        
    #處理Player吃到Food，若吃到要刪除則為True    
    foodsHitPlayer = pg.sprite.spritecollide(player, foods, True, pg.sprite.collide_circle) 
    for hit in foodsHitPlayer:
        eat_sound.play()
        score += int(hit.radius - 20)
        newFood() #每吃一個就再新增加一個，否則Foodk會被吃完
    
    #處理Player吃到Not_Food，若吃到要刪除則為True    
    notFoodsHitPlayer = pg.sprite.spritecollide(player, not_foods, True, pg.sprite.collide_circle) 
    for hit in notFoodsHitPlayer:
        player.health -= 35
        wrong_eat_sound.play()
        newNot_food() #每吃一個就再新增加一個，否則Foodk會被吃完
        newWater() #每吃一個Not_Food給一個Wate可以補充生命值
        if player.health <= 0:
            player_die = Explosion(player.rect.center)
            all_sprites.add(player_die)
            player.lifes -= 1
            player.health = 100
            player.hide()

    #處理Player吃到water
    waterHitPlayer = pg.sprite.spritecollide(player, waters, True)
    for hit in waterHitPlayer:
        water_sound.play()
        player.health += 20
        if player.health > 100:
            player.health = 100

    if player.lifes == 0 and not(player_die.alive()) : #如果playerLife為0，player_die物件不存在，遊戲結束
        fail_sound.play()
        draw_text(screen, BLACK, 'GG', 64, WIDTH/2, HEIGHT/4)
        pg.time.wait(3000)
        draw_gameover()
        show_init = True
    #---更新遊戲---
    
    #---畫面顯示---
    screen.fill((BLACK)) #(R,G,B)
    screen.blit(background_img,(0,0))  #把圖片'畫'在視窗上 (0,0) 為該圖片的x,y座標
    all_sprites.draw(screen)
    draw_text(screen, WHITE, str(score), 25, WIDTH/2, 20) #分數字體顯示
    draw_health_bar(screen, player.health, 5, 15)
    draw_lifes(screen, player.lifes, player_life_img, WIDTH - 40, 15)
    
    pg.display.update()

    #---畫面顯示---
    
pg.quit()
#---遊戲迴圈---
