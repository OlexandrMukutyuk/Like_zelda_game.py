import pygame

from obj import *

pygame.init()


class Game:
    def __init__(self):
        self.window = pygame.display.set_mode(SIZE)
        self.command = ["Start menu"]
        self.tick = pygame.time.Clock()
        self.gen = True
        self.rend_list = None
        self.last = ["Start menu"]
        self.step = 5
        self.tex = pygame.font.Font(None, 50).render("Yor DEATH try again", True, (255, 255, 255))
        self.lvl = LVL(self.window, -128 * 3, -128 * 25)
        self.run()

    def run(self):
        while True:
            if self.command[0] == "Start menu":
                self.main_menu()
            elif self.command[0] == "exit":
                exit()
            elif self.command[0] == "Start":
                self.game()
            elif self.command[0] == "death":
                self.death()
            if self.last != self.command[0]:
                self.gen = True
            pygame.display.update()
            self.last = self.command[0]

    def main_menu(self):
        if self.gen:
            self.rend_list = [Button(self.window, SIZE[0] / 2 - 200, 200, 400, 50, (51, 153, 255), "Start", "Start"),
                              Button(self.window, SIZE[0] / 2 - 200, 260, 400, 50, (51, 153, 255), "Settings",
                                     "Start menu"),
                              Button(self.window, SIZE[0] / 2 - 200, 320, 400, 50, (51, 153, 255), "Exit", "exit")]
            self.gen = False
        self.window.fill((20, 255, 20))
        for item in self.rend_list:
            item.rend(pygame.mouse.get_pos())
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONUP:
                for item in self.rend_list:
                    item.detect_clik(pygame.mouse.get_pos(), self.command)
            elif event.type == pygame.QUIT:
                exit()

    def game(self):
        if self.gen:
            self.rend_list = [Button(self.window, 5, 5, 250, 50, (51, 153, 255), "Start menu", "Start menu")]
            self.lvl = LVL(self.window, -128 * 3, -128 * 25)
            self.gen = False
        # self.window.fill((255, 255, 255))
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            for i in range(self.step):
                self.lvl.move_l(1)
        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            for i in range(self.step):
                self.lvl.move_r(-1)
        elif keys[pygame.K_UP] or keys[pygame.K_w]:
            for i in range(self.step):
                self.lvl.move_u(1)
        elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
            for i in range(self.step):
                self.lvl.move_d(-1)
        else:
            self.lvl.stay()
        self.lvl.rend(self.command)
        for items in self.rend_list:
            items.rend(pygame.mouse.get_pos())

        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONUP:
                for item in self.rend_list:
                    item.detect_clik(pygame.mouse.get_pos(), self.command)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.lvl.create_weapon()
                    for item in self.lvl.weapon:
                        item.detect_hit(self.lvl.enemy)

            elif event.type == pygame.QUIT:
                exit()
        self.tick.tick(60)

    def death(self):
        if self.gen:
            self.rend_list = [
                Button(self.window, SIZE[0] / 2 - 125, SIZE[1] / 2 - 25, 250, 50, (51, 153, 255), "Try again", "Start")]
            self.gen = False
        self.window.fill((0, 255, 0))
        for items in self.rend_list:
            items.rend(pygame.mouse.get_pos())
        self.window.blit(self.tex,(SIZE[0] / 2 - 170,SIZE[1] / 2 - 100))
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONUP:
                for item in self.rend_list:
                    item.detect_clik(pygame.mouse.get_pos(), self.command)
            elif event.type == pygame.QUIT:
                exit()


if __name__ == '__main__':
    Game()
