import pygame


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y,couche):
        super().__init__()

        self.all_cheveux = {"bowlhair" : {'tx': 15, 'ty': 19, 'x': 40, 'y': 21}, "mophair":{'tx': 16, 'ty': 20, 'x': 40, 'y': 20},
                       "shorthair":{'tx': 15, 'ty': 19, 'x': 40, 'y': 21},"spikeyhair":{'tx': 15, 'ty': 19, 'x': 40, 'y': 21},
                       "longhair":{'tx': 16, 'ty': 20, 'x': 39, 'y': 20},"curlyhair":{'tx': 18, 'ty': 20, 'x': 39, 'y': 20}}

        self.cheveux = "longhair"
        # chargement image
        self.sprite_sheet_idle = {'body': pygame.image.load('data/assets/charactere/IDLE/base_idle_strip9.png'),
                                  'hair': pygame.image.load(f'data/assets/charactere/IDLE/{self.cheveux}_idle_strip9.png'),
                                  'arm': pygame.image.load('data/assets/charactere/IDLE/tools_idle_strip9.png'),
                                  'pos': self.all_cheveux[self.cheveux]
                                  }

        self.sprite_sheet_walking = {'body': pygame.image.load('data/assets/charactere/WALKING/base_walk_strip8.png'),
                                     'hair': pygame.image.load(
                                         f'data/assets/charactere/WALKING/{self.cheveux}_walk_strip8.png'),
                                     'arm': pygame.image.load('data/assets/charactere/WALKING/tools_walk_strip8.png'),
                                     'pos': self.all_cheveux[self.cheveux]}

        self.all_sprite_sheet = {'idle': self.sprite_sheet_idle, "walking": self.sprite_sheet_walking}

        self.player_speed = 1
        self.type = "idle"
        # direction : false = droite ; true = gauche
        self.direction = False
        self.image = self.get_image(0, 0)
        self.image.set_colorkey([0, 0, 0])
        self.couche = couche

        # rectangle du sprite
        self.rect = self.image.get_rect()
        self.feet_surface = pygame.Surface((self.rect.width, self.rect.height), pygame.SRCALPHA)
        self.feet_rect = pygame.Rect((self.rect.x,self.rect.y+(self.rect.height//3)*2,self.rect.width,(self.rect.height//3)))
        self.mask = pygame.mask.from_surface(self.feet_surface)

        # index pour animation
        self.index = {'image': 0, 'animation': 0}
        self.position = [x, y]

    def update(self):
        self.rect.topleft = self.position
        self.feet_surface = pygame.Surface((self.rect.width, self.rect.height), pygame.SRCALPHA)
        #print(pygame.Rect((self.all_cheveux[self.cheveux]["tx"]-16)/2, (self.rect.height // 3)*2+1+(self.all_cheveux[self.cheveux]["ty"]-19), self.rect.width-(self.all_cheveux[self.cheveux]["tx"]-16), (self.rect.height) // 3))
        pygame.draw.rect(self.feet_surface, (255, 0, 255),
                         pygame.Rect((self.all_cheveux[self.cheveux]["tx"]-16)/2, (self.rect.height // 3)*2+1+(self.all_cheveux[self.cheveux]["ty"]-19), self.rect.width-(self.all_cheveux[self.cheveux]["tx"]-16), (self.rect.height) // 3))
        self.feet_rect = pygame.Rect((self.rect.x+(self.all_cheveux[self.cheveux]["tx"]-16)/2,self.rect.y+(self.rect.height//3)*2+1,self.rect.width,(self.rect.height//3)))
        self.mask = pygame.mask.from_surface(self.feet_surface)



    def mouv(self, vitesse_x, vitesse_y, s1, s2):
        self.position[0] += vitesse_x * s1
        self.position[1] += vitesse_y * s2
        self.update()

    def collision_poly(self, s1, s2, group,all_rect):

        self.mouv(1, 1, s1, s2)

        if (pygame.sprite.spritecollide(self, group[0], False)):
            if (pygame.sprite.spritecollide(self, group[0], False, pygame.sprite.collide_mask)):
                self.mouv(-1, -1, s1, s2)
                return False
        if (pygame.sprite.spritecollide(self, group[self.couche], False)):
            if (pygame.sprite.spritecollide(self, group[self.couche], False, pygame.sprite.collide_mask)):

                self.mouv(-1, -1, s1, s2)
                return False
        for rect in all_rect[0]:
            if(self.feet_rect.colliderect(rect)):
                self.mouv(-1, -1, s1, s2)
                return False
        for rect in all_rect[self.couche]:
            if(self.feet_rect.colliderect(rect)):
                self.mouv(-1, -1, s1, s2)
                return False

        return True

    def move_right(self, group,all_rect):
        return self.collision_poly(1, 0, group,all_rect)

    def move_left(self, group,all_rect):
        return self.collision_poly(-1, 0, group,all_rect)

    def move_up(self, group,all_rect):
        return self.collision_poly(0, -1, group,all_rect)

    def move_down(self, group,all_rect):
        return self.collision_poly(0, 1, group,all_rect)

    def animation_player(self):
        if (self.index['animation'] == 4):
            self.image = self.get_image((96 * self.index['image']), 0)
            self.index['image'] += 1
            if self.index['image'] == 7:
                self.index['image'] = 0
            self.index['animation'] = 0

        self.image.set_colorkey([0, 0, 0])
        self.index['animation'] += 1

    def get_image(self, x, y):
        image = pygame.Surface(
            [self.all_sprite_sheet[self.type]['pos']['tx'], self.all_sprite_sheet[self.type]['pos']['ty']])
        image.blit(self.all_sprite_sheet[self.type]['body'], (0, 0), (
        x + self.all_sprite_sheet[self.type]['pos']['x'], y + self.all_sprite_sheet[self.type]['pos']['y'],
        self.all_sprite_sheet[self.type]['pos']['tx'], self.all_sprite_sheet[self.type]['pos']['ty']))
        image.blit(self.all_sprite_sheet[self.type]['hair'], (0, 0), (
        x + self.all_sprite_sheet[self.type]['pos']['x'], y + self.all_sprite_sheet[self.type]['pos']['y'],
        self.all_sprite_sheet[self.type]['pos']['tx'], self.all_sprite_sheet[self.type]['pos']['ty']))
        image.blit(self.all_sprite_sheet[self.type]['arm'], (0, 0), (
        x + self.all_sprite_sheet[self.type]['pos']['x'], y + self.all_sprite_sheet[self.type]['pos']['y'],
        self.all_sprite_sheet[self.type]['pos']['tx'], self.all_sprite_sheet[self.type]['pos']['ty']))

        return pygame.transform.flip(image, self.direction, False)
