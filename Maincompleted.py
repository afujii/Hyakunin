# 2023年夏の課題として取り組んでいる。
# 作製開始は、2022年の正月休み、見直しは、2023年の春休み
# 非同期処理による2つのスプライトの生産・消費モデルを実装している。
# observer_async.py -> testloop3.py を参照にしている。
# testloop3.py は未完成
# Scratch の百人一首.sb3 をモデルとして制作中 jissen-scratch
# Messenger は、global
# Sprite.Textarea は、　Sprite.Player と別に定義しないと表示されない。
# つまり、Player の　self.textarea = ScTex
# Main17 の目標は、　Control を　Kami　Simo　と同列で定義して、
# Messenger を　global に設置すること。-> global 失敗
# message に正解を渡す。各Sprite が　自身の正誤を知っている。
# 2023/ 7/19 Last Updated



#!/usr/bin/evn python
# -*- coding:utf-8 -*-
import sys

import pygame
from pygame.locals import *
from collections import deque, defaultdict
from random import randint, sample #重複なし
from time import sleep

SCREEN_WIDTH = 640
SCREEN_HIGHT = 480
SCREEN = Rect(0, 0, SCREEN_WIDTH, SCREEN_HIGHT)
CENTER = (320, 240)
FTCLOR = (200,200,200)# フォントの色
BGCLOR = (50,50,50)# 背景の色
FLAG = True
FONT_PATH = "./aoyagireisyosimo_ttf_2_01.ttf"
TEXT_PATH = "./hyakuninUTF8.txt"
FONT_SIZE = 30
IMAG_SIZE = (90,110)
KAMI_IMG = "./images/kaminoku.png"
SIMO_IMG = "./images/simonoku.png"
CONT_IMG = "./images/control.png" # Cotral は、背景と同じ色の画像
global seikai
global kotae
seikai = 0
kotae = [0,0,0]
##############################################
pygame.init()
FONT = pygame.font.Font(FONT_PATH, FONT_SIZE)
###############################################
class ScrollText(pygame.sprite.Sprite):
    def __init__(self, text, init_position, bgcolor):
        pygame.sprite.Sprite.__init__(self)
        self.font = FONT
        self.bgcolor = bgcolor
        self.image = self.font.render(text,True, bgcolor)
        self.rect  = self.image.get_rect()
        self.rect.topleft = init_position
        
    def set_text(self, text, position):
        self.image = self.font.render(text,True, self.bgcolor)
        self.rect  = self.image.get_rect()
        x, y = position
        self.rect.topleft = (x +50, y)
########################################        
class Player(pygame.sprite.Sprite):
    def __init__(self, filename, id, xy, ScTex):
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load(filename)
        img = pygame.transform.scale(img,IMAG_SIZE)
        self.image = img
        w = self.image.get_width()
        h = self.image.get_height()
        x,y = xy
        self.init_x, self.init_y = xy
        self.rect = Rect(x, y, w, h)
        self.textarea = ScTex
        self.id = id
        self.seikai = False
        ####################       
    def speak(self,text):
        xy = (self.init_x,self.init_y)
        self.textarea.set_text(text,xy)

    def draw(self, surface):
        surface.blit(self.image, self.rect)
###########################################
    
class Messenger(object):
    def __init__(self):
        # News channels
        self.channels = defaultdict(deque)
        self.subscribers = defaultdict(list)
    def register(self, subscriber, channel):
        """ Register a subscriber for a news channel """     
        self.subscribers[channel].append(subscriber)
        
    def add_news(self, channel, message):
        """ Add a news story """
        self.channels[channel].appendleft(message)
    def put_message(self):
        pass
    def get_message(self,channel):
        res = self.channels[channel].pop()
        return res
    def notify(self):
        self.data_null_count = 0         
        for channel in self.channels:
            try:
                data = self.channels[channel].pop()
            except IndexError:
                self.data_null_count += 1
                continue
            subscribers = self.subscribers[channel]
            for sub in subscribers:
                #print('■Notifying',sub.id,'on channel',channel,'with =>',data)
                response = sub.callback(channel, data)
                #print('□Response from',sub.id,'for channel',channel,'=>',response)
            #print('□ Null Count:', self.data_null_count)

#######################################
class Controler(Player):
    def __init__(self, filename, id, xy, ScTex):
        super().__init__(filename, id, xy, ScTex)
        self.tokuten = 0 # 得点の管理はControl で行う
        
    def callback(self, message_type, num):
        #self.speak(message_type+str(num))
        #self.speak("得点：　" + str(tokuten) )
        if message_type == 'answer':
            if num:
                self.tokuten += 1
            else :
                self.tokuten -= 1 # 間違えたら減点
            self.speak("得点：　" + str(self.tokuten) )   
            seikai = randint(1,3)
            kotae = sample([i for i in range(99)],3)
            m.add_news('question', (seikai, kotae))
            
                    
class Kaminoku(Player) :
    """
    def update(self, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONUP:
                if self.rect.collidepoint(event.pos): # 自身のクリック確認
                    self.speak(KamiList[kotae[seikai-1]])
                    #m.add_news('question',num)
    """
    def callback(self,message_type, num):
        if message_type == 'answer':
            if num:
                self.speak('正解')
            else :
                self.speak('まちがい')
        elif message_type == 'question':
            self.speak(KamiList[ num[1][seikai-1] ] )
            
class Simonoku(Player) :
    def update(self, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONUP:
                if self.rect.collidepoint(event.pos): # 自身のクリック確認
                    m.add_news('answer',self.seikai)
    def callback(self,message_type, num):
        if message_type == 'question':
            self.speak(SimoList[ num[1][self.id-1]] )
            if self.id == num[0]: self.seikai = True
            else: self.seikai = False

#####################################################                    
with open(TEXT_PATH,'r',encoding= 'UTF-8') as fp:
    sentences = fp.readlines()
kaminoku = [ s.split(',')[2] for s in sentences]
del kaminoku[0]
simonoku = [ s.split(',')[3] for s in sentences]
del simonoku[0]
KamiList = kaminoku
SimoList = simonoku                    
textarea0 = ScrollText("",(100, 150),FTCLOR)
textarea1 = ScrollText("",(200, 200),FTCLOR)
textarea2 = ScrollText("",(300, 250),FTCLOR)
textarea3 = ScrollText("",(350, 300),FTCLOR)
textarea99 = ScrollText("",(350, 300),FTCLOR)

control = Controler(CONT_IMG, 99 , (0,0), textarea99)
player0 = Kaminoku(KAMI_IMG,0,(50, 100),textarea0)
player1 = Simonoku(SIMO_IMG,1,(100, 250),textarea1)
player2 = Simonoku(SIMO_IMG,2,(200, 300),textarea2)
player3 = Simonoku(SIMO_IMG,3,(300, 350),textarea3)

m = Messenger()

m.register(control, 'question')
m.register(player0, 'question')
m.register(player1, 'question')    
m.register(player2, 'question')   
m.register(player3, 'question')

m.register(control, 'answer')
m.register(player0, 'answer')
m.register(player1, 'answer')    
m.register(player2, 'answer')   
m.register(player3, 'answer')

#members = [player0, player1, player2, player3 ]

###############################################
def initialize():
    global clock, screen, sprite_group, bg

    clock = pygame.time.Clock()

    screen = pygame.display.set_mode( (SCREEN_WIDTH, SCREEN_HIGHT) )
    pygame.display.set_caption('百人一首')
    ##########################################
    seikai = randint(1,3)
    kotae = sample([i for i in range(99)],3)
    m.add_news('question',(seikai,kotae)) # touple = int + list
    ###########################################
    sprite_group = pygame.sprite.Group()
    bg = pygame.Surface(SCREEN.size)
    bg.fill(BGCLOR)  # 画面の背景色
    screen.blit(bg, (0, 0))
    pygame.display.update()# 初回アップデート

    sprite_group.add([player0,player1,player2,player3, control])
    sprite_group.add([textarea0,textarea1,textarea2,textarea3,textarea99])
#############################################
def process( frames, events ):
    FPS = 1 # frame / second
    m.notify() # <- 重要
    ############# 一般的な　pygame 作業　#######
    sprite_group.clear(screen, bg)
    sprite_group.update(events)
    sprite_group.draw(screen)
    pygame.display.update()
    ###########################################
    clock.tick(1)
    sleep(1)
################## main() #####################

def main():
    totalframes = 0
    initialize()

    while FLAG:
        events = pygame.event.get()

        totalframes +=1
        process( totalframes, events ) # process
        for event in events:
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

if __name__ == '__main__':
    main()
