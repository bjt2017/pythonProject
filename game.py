import pygame
import pytmx
import pyscroll
from player import Player
from polygone import Polygone
pygame.init()

class Game:
     def __init__(self):
         self.screen = pygame.display.set_mode((900, 600))
         pygame.display.set_caption("Farmer")
         self.running = True
         self.test = False




         #Exemple de chargement de carte
         self.tmx_data = pytmx.util_pygame.load_pygame('data/carte/test2.tmx')
         self.map_data = pyscroll.data.TiledMapData(self.tmx_data)
         self.map_layer = pyscroll.orthographic.BufferedRenderer(self.map_data,self.screen.get_size())
         self.map_layer.zoom = 3

         self.groupe_polygone = []
         self.group_rect = []
         self.group_r_chang = []
         #Ajout des colision
         for i in range(0,int(self.tmx_data.get_object_by_name("player").couche)+1):

             self.groupe_polygone.append(pygame.sprite.Group())
             self.group_rect.append([])



         self.c_rect =""
         for obj in self.tmx_data:
             if obj.name.startswith("changement"):
                 for i in range(0, int(obj.name.split('_')[2]) - len(self.groupe_polygone) + 1):
                     self.groupe_polygone.append(pygame.sprite.Group())
                 for i in range(0,int(obj.name.split('_')[2])-len(self.group_rect)+1):
                     self.group_rect.append([])
                 self.group_r_chang.append([pygame.Rect(obj.x,obj.y,obj.width,obj.height),int(obj.name.split('_')[1]),int(obj.name.split('_')[2]),False])



             if obj.name.startswith("rect"):

                 for i in range(0,int(obj.name.split('_')[len(obj.name.split('_'))-1])-len(self.group_rect)+1):
                     self.group_rect.append([])


                 for i in range(1,len(obj.name.split('_'))):

                    self.group_rect[int(obj.name.split('_')[i])].append(pygame.Rect(obj.x,obj.y,obj.width,obj.height))

             if obj.name.startswith("polygone"):
                 for i in range(0, int(obj.name.split('_')[1]) - len(self.groupe_polygone) + 1):
                     self.groupe_polygone.append(pygame.sprite.Group())
                 list_vertise = []
                 min_x = obj.points[0].x
                 min_y = obj.points[0].y
                 max_x = obj.points[0].x
                 max_y = obj.points[0].y
                 for point in obj.points:
                     if(point.x<min_x):
                         min_x = point.x
                     if (point.x > max_x):
                         max_x = point.x
                     if(point.y<min_y):
                         min_y = point.y
                     if (point.y > max_y):
                         max_y = point.y

                 for point in obj.points:
                    list_vertise.append(((round(point.x)-round(min_x)),(round(point.y)-round(min_y))))


                 polygone = Polygone(round(min_x),round(min_y),max_x-min_x,max_y-min_y,list_vertise)
                 for i in range(1,len(obj.name.split('_'))):

                    self.groupe_polygone[int(obj.name.split('_')[i])].add(polygone)



         player_position = self.tmx_data.get_object_by_name("player")
         self.player = Player(player_position.x,player_position.y,int(player_position.couche))



         #dessiner
         self.group = pyscroll.PyscrollGroup(map_layer=self.map_layer, default_layer=4)

         self.group.add(self.player)

         self.changement_collide = False


         # methode draw
         self.top = [self.screen.get_width()/2, self.screen.get_height()/2]



     def hide_show_couche(self,name,bool):
         for layer in self.tmx_data.layers:
             if layer.name == name and layer.visible!=bool:
                 layer.visible = bool

                 self.map_layer = pyscroll.orthographic.BufferedRenderer(self.map_data, self.screen.get_size())
                 self.map_layer.zoom = 3


         self.group = pyscroll.PyscrollGroup(map_layer=self.map_layer, default_layer=1)
         self.group.add(self.player)




     def handle_input(self):
         pressed = pygame.key.get_pressed()
         move = False
         if pressed[pygame.K_LEFT]:
             self.player.direction = True
             self.player.type = 'walking'
             if self.player.move_left(self.groupe_polygone,self.group_rect):
                 move = True


         elif pressed[pygame.K_RIGHT]:
             self.player.direction = False
             if self.player.move_right(self.groupe_polygone,self.group_rect):
                 move = True
             self.player.type = 'walking'


         if pressed[pygame.K_DOWN]:
             self.player.type = 'walking'
             if self.player.move_down(self.groupe_polygone,self.group_rect):
                move = True

         elif pressed[pygame.K_UP]:
             self.player.type = 'walking'
             if self.player.move_up(self.groupe_polygone,self.group_rect):
                move = True

         if move != True:
             self.player.type = 'idle'

     def update(self):

         self.group.update()
         self.group.center(self.player.rect)

         self.group.draw(self.screen)



         #affichage des colisions
         if self.test:
             for polygone in self.groupe_polygone[0]:
                 self.screen.blit(polygone.surface, polygone.rect)
             for polygone in self.groupe_polygone[self.player.couche]:
                 self.screen.blit(polygone.surface, polygone.rect)

             self.screen.blit(self.player.mask.to_surface(), self.player.rect)
             for rect in self.group_r_chang:
                self.screen.blit(pygame.Surface((rect[0].width, rect[0].height)), rect[0])
             for rect in self.group_rect[0]:

                 self.screen.blit(pygame.Surface((rect.width, rect.height)), rect)
             for rect in self.group_rect[self.player.couche]:
                 self.screen.blit(pygame.Surface((rect.width, rect.height)), rect)






         self.test_rect = pygame.Surface((self.player.rect.width * 3, self.player.rect.height * 3))
         self.test_rect.fill((255, 0, 0))

         #pygame.draw.rect(self.screen, (0, 255, 0), pygame.Rect(self.top[0], self.top[1], self.test_rect.get_width(),self.test_rect.get_height()))
         # test
         #self.screen.blit(self.test_rect, pygame.Rect(self.top[0], self.top[1], self.test_rect.get_width(),self.test_rect.get_height()))

         #mouvement player + animation
         self.player.animation_player()
         self.handle_input()




         #changement de couche
         for collide in self.group_r_chang:
            if (self.player.feet_rect.colliderect(collide[0])):
                collide[3] = True

            elif collide[3]==True:

                if(collide[0].y+collide[0].height==self.player.feet_rect.y):

                    print('show :' + str(collide[1]))
                    self.hide_show_couche("haut_couche_"+str(collide[1]),True)


                    self.player.couche = collide[1]
                else:
                    for i in range(collide[2]-1, 0, -1):
                        print('hide :'+ str(i))

                        self.hide_show_couche("haut_couche_" + str(i), False)
                    self.player.couche = collide[2]
                collide[3] = False








     def run(self):
         clock = pygame.time.Clock()



         while self.running:



             self.update()
             for event in pygame.event.get():
                 if event.type == pygame.QUIT:
                     self.running = False
             clock.tick(60)



             pygame.display.flip()