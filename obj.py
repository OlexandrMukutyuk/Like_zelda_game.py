from Settings import *
from map import lvl_1

import pygame

pygame.init()


class Button:
    def __init__(self, window, x, y, height, weight, color, text_btn, command):
        self.window = window
        self.x = x
        self.y = y
        self.height = height
        self.weight = weight
        self.color = color
        self.color_r = color
        self.command = command
        self.text_t = text_btn
        self.text = pygame.font.Font(None, self.weight).render(text_btn, True, (255, 255, 153))
        self.rect = pygame.Rect(self.x, self.y, self.height, self.weight)

    def rend(self, poz):
        self.detect_mouse(poz)
        pygame.draw.rect(self.window, self.color, self.rect)
        pygame.draw.rect(self.window, (0, 0, 0), self.rect, 2)
        self.window.blit(self.text,
                         (self.x + self.height / 2 - len(self.text_t) * (self.weight / 5), self.y + self.weight / 5))

    def detect_mouse(self, poz):
        if self.rect.collidepoint(poz):
            self.color = (102, 178, 255)
        else:
            self.color = self.color_r

    def detect_clik(self, poz, com):
        if self.rect.collidepoint(poz):
            com[0] = self.command


class LVL:
    def __init__(self, window, x=-128 * 25, y=-128 * 25):
        self.window = window
        self.x = x
        self.y = y
        self.bg_lvl = lvl_1.lvl_1_BG
        self.grass_lvl = lvl_1.lvl_1_Grass
        self.fall_blocks = lvl_1.lvl_1_fall_block
        self.player_side = "down"
        self.anim_player_count = 0
        self.enemy = [self.Enemy(self.window, 10, 9, self.x, self.y),
                      self.Enemy(self.window, 15, 5, self.x, self.y),
                      self.Enemy(self.window, 16, 15, self.x, self.y),
                      self.Enemy(self.window, 26, 7, self.x, self.y),
                      self.Enemy(self.window, 34, 12, self.x, self.y),
                      self.Enemy(self.window, 30, 16, self.x, self.y),
                      self.Enemy(self.window, 23, 23, self.x, self.y),
                      self.Enemy(self.window, 23, 30, self.x, self.y),
                      self.Enemy(self.window, 22, 41, self.x, self.y),
                      self.Enemy(self.window, 17, 41, self.x, self.y),
                      self.Enemy(self.window, 40, 14, self.x, self.y),
                      self.Enemy(self.window, 40, 17, self.x, self.y),
                      self.Enemy(self.window, 38, 22, self.x, self.y),
                      self.Enemy(self.window, 36, 26, self.x, self.y)]
        self.player_img = pygame.image.load("player\player_d_stay.png")
        self.bg_25 = pygame.image.load("img/25.png")
        self.bg_35 = pygame.image.load("img/35.png")
        self.bg_131 = pygame.image.load("img/131.png")
        self.bg_132 = pygame.image.load("img/132.png")
        self.bg_133 = pygame.image.load("img/133.png")
        self.bg_137 = pygame.image.load("img/137.png")
        self.fall_block = []
        self.weapon = []

    def rend(self,command):
        self.rend_bg()
        self.rend_weapon()
        self.rend_enemy(command)
        self.rend_player()

    def rend_bg(self):
        self.window.fill(WATERCOLOR)
        for item in range(len(self.bg_lvl)):
            for items in range(len(self.bg_lvl[item])):
                match self.bg_lvl[item][items]:
                    case 25:
                        self.window.blit(self.bg_25, (items * 128 + self.x, item * 128 + self.y))
                    case 35:
                        self.window.blit(self.bg_35, (items * 128 + self.x, item * 128 + self.y))
        for item in range(len(self.grass_lvl)):
            for items in range(len(self.grass_lvl[item])):
                match self.grass_lvl[item][items]:
                    case 131:
                        self.window.blit(self.bg_131, (items * 128 + self.x, item * 128 + self.y))
                    case 132:
                        self.window.blit(self.bg_132, (items * 128 + self.x, item * 128 + self.y))
                    case 133:
                        self.window.blit(self.bg_133, (items * 128 + self.x, item * 128 + self.y))
                    case 137:
                        self.window.blit(self.bg_137, (items * 128 + self.x, item * 128 + self.y))
        self.gen_fall_block()
        # print([self.fall_block[0].x,self.fall_block[0].y])

    def gen_fall_block(self):
        self.fall_block = []
        for item in range(len(self.fall_blocks)):
            for items in range(len(self.fall_blocks[item])):
                if self.fall_blocks[item][items] == 300:
                    # pygame.draw.rect(self.window,(255,0,0),(items * 128 + self.x, item * 128 + self.y, 128, 128),5)
                    self.fall_block.append(pygame.Rect(items * 128 + self.x, item * 128 + self.y, 128, 128))

    def rend_player(self):
        self.window.blit(self.player_img, (SIZE[0] / 2 - 18, SIZE[1] / 2 - 31))

    def rend_weapon(self):
        for item in self.weapon:
            item.rend(self.enemy)
            if item.time == 25:
                self.weapon = []

    def rend_enemy(self,command):
        for item in self.enemy:
            item.neural_intelegens(pygame.Rect((SIZE[0] / 2 - 18, SIZE[1] / 2, 36, 31)))
            item.move(self.x, self.y)
            item.rend()
            item.hit(pygame.Rect((SIZE[0] / 2 - 18, SIZE[1] / 2, 36, 31)),command)

    def move_r(self, vector):
        self.player_side = "right"
        if self.fall_kol(x=vector):
            self.x += vector
            self.gen_fall_block()
        else:
            print("колізія1")
        if self.anim_player_count <= 60:
            self.player_img = pygame.image.load("player\player_r_1.png")
        elif self.anim_player_count == 120:
            self.anim_player_count = 0
        else:
            self.player_img = pygame.image.load("player\player_r_2.png")
        self.anim_player_count += 1

    def move_l(self, vector):
        self.player_side = "left"
        if self.fall_kol(x=vector):
            self.x += vector
            self.gen_fall_block()
        else:
            print("колізія1")
        if self.anim_player_count <= 60:
            self.player_img = pygame.image.load("player\player_l_1.png")
        elif self.anim_player_count == 120:
            self.anim_player_count = 0
        else:
            self.player_img = pygame.image.load("player\player_l_2.png")
        self.anim_player_count += 1

    def move_u(self, vector):
        self.player_side = "up"
        if self.fall_kol(y=vector):
            self.y += vector
            self.gen_fall_block()
        else:
            print("колізія2")
        if self.anim_player_count <= 60:
            self.player_img = pygame.image.load("player\player_u_1.png")
        elif self.anim_player_count == 120:
            self.anim_player_count = 0
        else:
            self.player_img = pygame.image.load("player\player_u_2.png")
        self.anim_player_count += 1

    def move_d(self, vector):
        self.player_side = "down"
        if self.fall_kol(y=vector):
            self.y += vector
            self.gen_fall_block()
        else:
            print("колізія2")
        if self.anim_player_count <= 60:
            self.player_img = pygame.image.load("player\player_d_1.png")
        elif self.anim_player_count == 120:
            self.anim_player_count = 0
        else:
            self.player_img = pygame.image.load("player\player_d_2.png")
        self.anim_player_count += 1

    def stay(self):
        self.anim_player_count = 0
        if self.player_side == "down":
            self.player_img = pygame.image.load("player\player_d_stay.png")
        elif self.player_side == "up":
            self.player_img = pygame.image.load("player\player_u_stay.png")
        elif self.player_side == "right":
            self.player_img = pygame.image.load("player\player_r_stay.png")
        elif self.player_side == "left":
            self.player_img = pygame.image.load("player\player_l_stay.png")

    def fall_kol(self, x=0, y=0):
        tmp = True

        for item in self.fall_block:
            if item.colliderect(pygame.Rect((SIZE[0] / 2 - 18 - x, SIZE[1] / 2 - y, 36, 31))):
                tmp = False
        return tmp

    def create_weapon(self):
        if not self.weapon:
            self.weapon = [self.Weapon(self.window, self.player_side)]

    class Weapon:
        def __init__(self, window, side):
            self.x = SIZE[0] / 2
            self.y = SIZE[1] / 2
            self.window = window
            self.time = 0
            self.side = side
            if side == "up":
                self.img = pygame.transform.scale(pygame.image.load("player\knife_u.png"), (20, 60))
                self.rec = pygame.Rect(SIZE[0] / 2 - 18, SIZE[1] / 2 - 62, 20, 60)
            elif side == "down":
                self.img = pygame.transform.scale(pygame.image.load("player\knife_d.png"), (20, 60))
                self.rec = pygame.Rect(SIZE[0] / 2 - 18, SIZE[1] / 2 + 21, 20, 60)
            elif side == "left":
                self.img = pygame.transform.scale(pygame.image.load("player\knife_l.png"), (60, 20))
                self.rec = pygame.Rect(SIZE[0] / 2 - 65, SIZE[1] / 2 - 5, 60, 20)
            elif side == "right":
                self.img = pygame.transform.scale(pygame.image.load("player\knife_r.png"), (60, 20))
                self.rec = pygame.Rect(SIZE[0] / 2 + 5, SIZE[1] / 2 - 5, 60, 20)

        def rend(self, enemy):
            self.time += 1
            if self.side == "up":
                self.window.blit(self.img, (SIZE[0] / 2 - 18, SIZE[1] / 2 - 62))
            elif self.side == "down":
                self.window.blit(self.img, (SIZE[0] / 2 - 18, SIZE[1] / 2 + 21))
            elif self.side == "left":
                self.window.blit(self.img, (SIZE[0] / 2 - 65, SIZE[1] / 2 - 5))
            elif self.side == "right":
                self.window.blit(self.img, (SIZE[0] / 2 + 5, SIZE[1] / 2 - 5))

        def detect_hit(self, enemy):
            for item in enemy:
                # print(self.x,self.y)
                # print(item.x,item.y)
                if self.rec.colliderect(item.rec):
                    item.hp -= 2
                    print(item.hp)
            for i in range(len(enemy)):
                if enemy[i].hp <= 0:
                    enemy.pop(i)
                    break

    class Enemy:
        def __init__(self, window, side_map_x, side_map_y, x, y):
            self.window = window
            self.x = x
            self.y = y
            self.x_m = 0
            self.y_m = 0
            self.anim_time = 0
            self.side_map_x = side_map_x
            self.side_map_y = side_map_y
            self.side = "up"
            self.hp = 10
            self.hit_time = 0
            self.img = pygame.image.load("enemy\enemy_u_stay.png")
            self.rec = pygame.Rect(128 * self.side_map_x + self.x + self.x_m, 128 * self.side_map_y + self.y + self.y_m,
                                   32, 50)
            self.agree_rec = pygame.Rect(128 * self.side_map_x + self.x - 400, 128 * self.side_map_y + self.y - 400,
                                         800, 800)

        def neural_intelegens(self, rect):
            if self.agree_rec.colliderect(rect):
                self.move_agree()
                self.move_agree()
                self.move_agree()
            else:
                self.load_stay_picture(self.side[0])

        def move(self, x, y):
            self.x = x
            self.y = y

        def move_agree(self):
            if 128 * self.side_map_x + self.x + self.x_m < SIZE[0] / 2 - 18:
                self.x_m += 1
                if self.side == "right":
                    self.load_picture("r")
                else:
                    self.side = "right"
                    self.anim_time = 0
            elif 128 * self.side_map_x + self.x + self.x_m > SIZE[0] / 2 - 18:
                self.x_m -= 1
                if self.side == "left":
                    self.load_picture("l")
                else:
                    self.side = "left"
                    self.anim_time = 0
            elif 128 * self.side_map_y + self.y + self.y_m < SIZE[1] / 2:
                self.y_m += 1
                if self.side == "down":
                    self.load_picture("d")
                else:
                    self.side = "down"
            elif 128 * self.side_map_y + self.y + self.y_m > SIZE[1] / 2:
                self.y_m -= 1
                if self.side == "up":
                    self.load_picture("u")
                else:
                    self.side = "up"

        def load_picture(self, comm):
            if self.anim_time < 40:
                self.img = pygame.image.load(f"enemy\enemy_{comm}_1.png")
            elif self.anim_time == 80:
                self.anim_time = 0
            else:
                self.img = pygame.image.load(f"enemy\enemy_{comm}_2.png")
            self.anim_time += 1

        def load_stay_picture(self, comm):
            self.img = pygame.image.load(f"enemy\enemy_{comm}_stay.png")

        def rend(self):
            self.rec = pygame.Rect(128 * self.side_map_x + self.x + self.x_m, 128 * self.side_map_y + self.y + self.y_m,
                                   32, 50)
            self.agree_rec = pygame.Rect(128 * self.side_map_x + self.x - 400 + self.x_m,
                                         128 * self.side_map_y + self.y - 400 + self.y_m,
                                         800, 800)
            #pygame.draw.rect(self.window, (255, 0, 0), (
            #    128 * self.side_map_x + self.x - 400 + self.x_m, 128 * self.side_map_y + self.y - 400 + self.y_m, 800,
            #    800),
            #                 5)
            self.window.blit(self.img, (self.rec))

        def hit(self, rec,command):
            if self.rec.colliderect(rec):
                self.hit_time += 1
                if self.hit_time == 30:
                    command[0] = "death"
            else:
                self.hit_time = 0
