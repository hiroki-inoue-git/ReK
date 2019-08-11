import pygame
from pygame.locals import *
from define import *
from equipment import Equipment
from listbox import ListBox

class Menu:
    
    def __init__(self, screen, data):
        self.screen = screen
        self.data = data

        self.stage_num = 1
        self.select_num = 0
        self.option_num = 0
        
        StageSelect_font = pygame.font.Font("freesansbold.ttf", 55)
        Arrow_font = pygame.font.Font("freesansbold.ttf", 100)
        Stage_font = pygame.font.Font("freesansbold.ttf", 45)

        self.StageSelect_text = StageSelect_font.render("Stage Select", True, (255,255,255)) 
        self.RightArrow_text = Arrow_font.render(">", True, (255,255,255))
        self.LeftArrow_text = Arrow_font.render("<", True, (255,255,255))
        self.RightArrow_text = pygame.transform.rotate(self.RightArrow_text, 90)
        self.LeftArrow_text = pygame.transform.rotate(self.LeftArrow_text, 90)
        # ステージのテキスト情報をリストにする
        self.stage_text = []
        for i in range(3):
            text = "Stage" + str(i+1)
            self.stage_text.append(Stage_font.render(text, True, (255,255,255)))

        self.option_listbox = ListBox(self.screen, 50, 100, 250, 200, ['Back', 'Shop', 'Equip'], font_size=55)
        self.option_listbox.set_selectable([True, True, True])
        self.file_listbox = ListBox(self.screen, 950, 100, 100, 400, ["Stage1"])
        self.file_listbox.set_selectable([True])
        self.file_listbox()
        self.file_id = None

    def draw(self):

        while True:
            self.option_listbox.draw(False)
            self.file_listbox.draw()
            self.Select_Stage(self.file_id)     #ステージ選択処理
            pygame.display.update()
            for event in pygame.event.get():
                file_id = self.file_listbox.process(event)
                option_num = self.option_listbox.process(event)
                if event.type == KEYDOWN:
                    self.Key_Event(event)       #押されたキーによって異なる処理
                    if event.key == K_RETURN and self.select_num == 1:
                        return self.Return_Stage()
                if event.type == QUIT:
                    return EXIT, None

                if file_id != None:
                    self.file_id = file_id
                    self.select_num += 1
                    self.file_listbox.process(event)

                if option_num != None:
                    if option_num == 0:
                        return None, '0'
                    elif option_num == 1:
                        return None, '1'
                    elif option_num == 2:
                        Equipment(self.screen, self.data).do()
                        break
                
            self.screen.fill((0,0,0))
            
    
    def Select_Stage(self, file_id):
        #選択しているステージを描画
        color = (self.select_num==1)*(255,100,100) or (100,100,100)
        pygame.draw.rect(self.screen,color,Rect(350,100,550,450))
        self.screen.blit(self.StageSelect_text, [105, 5])     #テキストStageSelectを描画
        if file_id != None:
            color = [(0,0,255),(0,255,0), (255,0,0)]
            self.screen.blit(self.stage_text[self.stage_num-1], [410, 210])
            pygame.draw.rect(self.screen,color[self.stage_num-1],Rect(400,200,450,250),5)
            self.screen.blit(self.RightArrow_text, [575, 140])  #テキスト ＞ を描画
            self.screen.blit(self.LeftArrow_text, [575, 450])     #テキスト ＞ を描画
    
    def Key_Event(self,event):
        if event.key == K_RIGHT:
            self.select_num -= 1
        elif event.key == K_LEFT:
            self.select_num += 1
        self.select_num = (self.select_num+3) % 3
        if self.select_num == 0:
            self.file_listbox()
        elif self.select_num == 2:
            self.option_listbox()
        if event.key == K_UP:
            self.stage_num += (self.select_num==1)
        elif event.key == K_DOWN:
            self.stage_num -= (self.select_num==1)
        stage_size = len(self.stage_text)
        self.stage_num = (self.stage_num+stage_size) % stage_size
    
    def Return_Stage(self):
        stage = [Stage1, Stage2, Stage3]
        return self.stage_num, stage[self.stage_num-1]