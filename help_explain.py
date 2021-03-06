import pygame
from pygame.locals import *
from help_print import *
from define import EXIT

class Help_a: 
    def __init__(self, screen):
        self.screen = screen
        self.select_num = 0
        self.back_num = 0
        pygame.font.init()
        explain_font = pygame.font.Font("font/freesansbold.ttf", 25)
        
        with open('testa/test.txt', 'r', encoding="utf-8") as fp:   # ファイルを読み取り専用で開く]
            self.dic_data = [0, 1, 2, 3, 4, 5, 6]
            for (line, data) in zip(fp.readlines(), range(len(self.dic_data))):                 # ファイルを一行ごとに読み取り、変数lineに文字列として格納する
                self.dic_data[data] = line.strip('\n')       # 改行コード'\n'を取り除き、タブ区切りでリストに分割する
                self.dic_data[data] = explain_font.render(self.dic_data[data], True, (255,255,255))
                
        
    def draw(self):
        
        while True:
            self.screen.blit(self.dic_data[0], [430, 50]) 
            self.screen.blit(self.dic_data[1], [0, 80]) 
            self.screen.blit(self.dic_data[2], [430, 120]) 
            self.screen.blit(self.dic_data[3], [430, 160]) 
            self.screen.blit(self.dic_data[4], [430, 200]) 
            self.screen.blit(self.dic_data[5], [430, 240]) 
            self.Draw_key(self.screen)

            
            pygame.display.update()
           
            for event in pygame.event.get():   
                if event.type == KEYDOWN:
                    self.Key_Event(event)
                    if event.key == K_RETURN:
                        if self.back_num == 1:
                            return "0"
                        else :
                            help_print = Help_print(self.screen, self.select_num)
                            help_print1 = help_print.draw()
                    
                elif event.type == QUIT:
                    return EXIT
            
           
            self.screen.fill((0,0,0))


    def Key_Event(self, event):
        
        if event.key == K_DOWN:
            if self.select_num == 0:
                self.select_num = 1
            elif self.select_num == 1:
                self.select_num = 2
            elif self.select_num == 2:
                self.select_num = 3
                self.back_num = 1
            else :
                self.select_num = 0

        if event.key == K_UP:
            if self.select_num == 3:
                self.select_num = 2
            elif self.select_num == 2:
                self.select_num = 1
            elif self.select_num == 1:
                self.select_num = 0
            else :
                self.select_num = 3
                self.back_num = 1                

    def Draw_key(self, screen):
        if self.select_num == 0:
            self.screen.blit(self.dic_data[6], [400, 120]) 
        if self.select_num == 1:
            self.screen.blit(self.dic_data[6], [400, 160])
        if self.select_num == 2:
            self.screen.blit(self.dic_data[6], [400, 200])
        if self.select_num == 3:
            self.screen.blit(self.dic_data[6], [400, 240])       

    