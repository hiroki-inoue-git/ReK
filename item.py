# coding:utf-8

import pygame
from pygame.locals import *
from machine import Hp

class Item(pygame.sprite.Sprite):
    """アイテム処理の基底となるクラス。継承するクラスは、メソッドeffect(self, machine)を定義する。
    effectメソッドでは、アイテムを取得した機体machineに対して、そのアイテムに応じた処理を行うよう記述する。"""
    def __init__(self, x, y, img, machine):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.image = img
        self.rect = self.image.get_rect()
        self.machine = machine                      # アイテムの効果対象
        self.speed = -1                             # アイテムの移動速度
        self.rect.move_ip(x, y)                     # 引数で指定された初期位置に移動させる

    def update(self):
        self.rect.move_ip(self.speed, 0)            # 移動
        collide_list = pygame.sprite.spritecollide(self, self.machine, False)   # 当たり判定
        if self.checkMachine(collide_list):                            # アイテムを取得した機体があるなら
            self.kill()
            for machine in collide_list:
                if machine.isMachine():             # 当たったのが機体か。シールドなどのアイテムには効果がないから。
                    self.effect(machine)            # アイテムを取得した機体に対して、アイテムに応じた効果を与える

    def checkMachine(self, collide_list):
        """引数collide_listのリスト中に機体があればTrueが返る。ない場合はFalse"""
        if collide_list:
            for x in collide_list:
                if x.isMachine():
                    return True
        return False

class Recovery(Item):
    """取得した機体の体力を1回復するアイテム"""
    def __init__(self, x, y, machine):
        image = pygame.image.load("img/recovery.png").convert_alpha()
        super().__init__(x, y, image, machine)

    def effect(self, machine):
        machine.recover(1)                          # 機体の体力を1回復する

class Shield(pygame.sprite.Sprite):
    """機体を守るシールド"""
    def __init__(self, firmness, machine):
        pygame.sprite.Sprite.__init__(self, machine.containers)
        self.image = pygame.image.load("img/shield.png").convert_alpha()
        self.hp = Hp(firmness)                      # 引数で指定した堅さをhpとして保持
        self.rect = self.image.get_rect()           # 画像からrectを生成
        self.machine = machine                      # このシールドが守る機体の情報を保持
        self.update()                               # 更新する

    def update(self):
        rect = self.machine.rect                    # 機体のrectを取得
        x1, y1 = self.rect.center                   # rectの中心を取得
        x2, y2 = rect.center                        # このシールドのrectの中心を取得
        self.rect.move_ip(x2-x1,y2-y1)              # 機体の移動分シールドを移動

    def hit(self, attack):
        if self.hp.damage(attack):                  # ダメージ計算
            self.kill()

    def isMachine(self):
        # このクラスは機体ではない
        return False

class ShieldItem(Item):
    """取得した機体の体力を1回復するアイテム"""
    def __init__(self, x, y, machine):
        image = pygame.image.load("img/item_shield.png").convert_alpha()
        super().__init__(x, y, image, machine)

    def effect(self, machine):
        Shield(3, machine)          # 堅さ3のシールドを生成