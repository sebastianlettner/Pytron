import sys, pygame
pygame.init()

size = width, height = 420, 640
speed = [0, 0]
black = 0, 0, 0

screen = pygame.display.set_mode(size)
pygame.display.set_caption("Tron")

ball = pygame.image.load("ball.bmp")
ballrect = ball.get_rect()

class Block(pygame.sprite.Sprite):
    def __init__(self,color,width,height):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.Surface([width, height])
        self.image.fill(color)

        self.rect = self.image.get_rect()

    def set_position(self, x , y):
        self.rect.x = x
        self.rect.y = y


pos_x = 0
pos_y = 0
block1 = Block(pygame.Color("green"), 25 , 25)
block2 = Block(pygame.Color("red"), 25 , 25)
block2.set_position(100,100)
while 1:



    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                speed[1] = 3
                speed[0] = 0
                pos_y += 10
                block1.rect.move(speed)
                block1.set_position(pos_x,pos_y)
                block2.set_position(pos_x+100,pos_y+100)
            if event.key == pygame.K_UP:
                speed[1] = -3
                speed[0] = 0
                pos_y -= 10
                block1.set_position(pos_x,pos_y)
                block2.set_position(pos_x+100,pos_y+100)
            if event.key == pygame.K_RIGHT:
                pos_x += 10
                block1.set_position(pos_x,pos_y)
                block2.set_position(pos_x+100,pos_y+100)
                speed[0] = 3
                speed[1] = 0
            if event.key == pygame.K_LEFT:
                speed[0] = -3
                speed[1] = 0
                pos_x -= 10
                block1.set_position(pos_x,pos_y)
                block2.set_position(pos_x+100,pos_y+100)





    #ballrect = ballrect.move(speed)
    # if ballrect.left < 0 or ballrect.right > width:
    #     speed[0] = -speed[0]
    # if ballrect.top < 0 or ballrect.bottom > height:
    #     speed[1] = -speed[1]

    screen.fill(black)
    screen.blit(block1.image, block1.rect)
    screen.blit(block2.image, block2.rect)
    #screen.blit(ball, ballrect)
    pygame.display.update()
    pygame.display.flip()
