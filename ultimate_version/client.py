import random
import pygame
from network import Network

width = 540
height = 540
win = pygame.display.set_mode((width, height))
pygame.display.set_caption("Bill vs. Steve")

gates = pygame.image.load('imgs/gates.png')
jobs = pygame.image.load('imgs/jobs.png')
imgs = [gates, jobs]

windows = pygame.image.load('imgs/windows.png')
apple = pygame.image.load('imgs/apple.png')
icons = [windows, apple]

target = pygame.image.load('imgs/target.png')

gwon = pygame.image.load('imgs/gates_won.png')
glost = pygame.image.load('imgs/gates_lost.png')
jwon = pygame.image.load('imgs/jobs_won.png')
jlost = pygame.image.load('imgs/jobs_lost.png')

won_ending = [gwon, jwon]
lost_ending = [glost, jlost]

ending_rect = gwon.get_rect()

bg = pygame.image.load('imgs/bg.jpeg')
bg_rect = bg.get_rect()


clientNumber = 0

class Bean():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.rect = (self.x, self.y )
        self.image = target
    
    def draw(self, win):
        win.blit(self.image, (self.x, self.y))


class Score():
    def __init__(self, x, y, image):
        self.x = x
        self.y = y
        self.image = image

    def draw(self, win):
        win.blit(self.image, (self.x, self.y))


class Player():
    def __init__(self, x, y, width, height, image):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.rect = (x,y,width,height)
        self.vel = 10
        self.image = image

    def draw(self, win):
        win.blit(self.image, (self.x, self.y))


    def move(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            if self.x > 0:
                self.x -= self.vel
        if keys[pygame.K_RIGHT]:
            if self.x < width - 40:
                self.x += self.vel
        if keys[pygame.K_UP]:
            if self.y > 0:
                self.y -= self.vel
        if keys[pygame.K_DOWN]:
            if self.y < height - 60:
                self.y += self.vel
        self.update()

    def update(self):
        self.rect = (self.x, self.y, self.width, self.height)


def read_pos(str):
    str = str.split(",")
    return int(str[0]), int(str[1]), int(str[2])


def make_pos(tup):
    return str(tup[0]) + "," + str(tup[1]) + "," + str(tup[2])


def redrawWindow(win,player, player2, bean, scores, myIndex, wonBool, lostBool):
    win.blit(bg, bg_rect)
    player.draw(win)
    player2.draw(win)
    bean.draw(win)
    for score in scores:
        score.draw(win)
    if wonBool:
        win.blit(won_ending[myIndex], ending_rect)
    if lostBool:
        win.blit(lost_ending[myIndex], ending_rect)
    pygame.display.update()


def main():
    run = True
    n = Network()
    startPos = read_pos(n.getPos())
    myIndex = startPos[2]
    p = Player(startPos[0],startPos[1],100,100, imgs[myIndex])
    p2 = Player(0,0,100,100, imgs[(myIndex+1)%2])
    bean = Bean(100, 100)
    clock = pygame.time.Clock()
    counter = 0
    myScore = 0
    theirScore = 0
    wonBool = False
    lostBool = False
    scores = []


    while run:
        clock.tick(60)
        p2Pos = read_pos(n.send(make_pos((p.x, p.y, myIndex))))
        p2.x = p2Pos[0]
        p2.y = p2Pos[1]
        p2.update()
        x_pool = [168, 267, 89, 476, 424, 415, 428, 362, 148, 363, 386, 46, 138, 496, 236, 399, 161, 310, 327, 375, 294, 75, 95, 259, 232, 486, 122, 370, 329, 53, 335, 423, 391, 171, 182, 164, 122, 167, 188, 167, 305, 117, 139, 149, 93, 320, 243, 318, 113, 223, 423, 61, 303, 146, 74, 237, 366, 496, 487, 265, 158, 338, 419, 81, 167, 311, 140, 185, 299, 474, 324, 389, 289, 226, 87, 434, 256, 148, 47, 374, 217, 199, 72, 446, 318, 447, 317, 471, 63, 473, 362, 238, 354, 123, 107, 221, 56, 135, 94, 86]
        y_pool = [331, 81, 441, 76, 281, 306, 134, 127, 306, 104, 234, 199, 226, 113, 182, 184, 433, 425, 375, 247, 142, 292, 43, 98, 56, 305, 282, 172, 393, 347, 425, 161, 107, 165, 404, 482, 156, 280, 127, 489, 204, 376, 182, 180, 164, 254, 161, 183, 192, 271, 94, 213, 330, 470, 113, 253, 384, 392, 149, 467, 375, 155, 148, 182, 455, 417, 356, 338, 304, 172, 380, 216, 405, 400, 252, 244, 65, 273, 356, 450, 117, 497, 87, 244, 453, 324, 428, 278, 70, 259, 98, 175, 204, 133, 242, 159, 85, 413, 67, 226]

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
        
        thisScored = p.x - 20 < bean.x < p.x + 20 and p.y - 20 < bean.y < p.y + 20
        thatScored = p2.x - 20 < bean.x < p2.x + 20 and p2.y - 20 < bean.y < p2.y + 20

        if thisScored:
            myScore += 1
            scores.append(Score(520 - 20 * myScore, 500, icons[myIndex]))
        
        if thatScored:
            theirScore += 1

        if thisScored or thatScored:
            x = x_pool[counter]
            y = y_pool[counter]
            bean = Bean(x, y)
            print(myScore, theirScore)
            counter += 1
            if myScore == 10:
                print('You won!')
                wonBool = True
            if theirScore == 10:
                print('You lost.')
                lostBool = True

        p.move()
        redrawWindow(win, p, p2, bean, scores, myIndex, wonBool, lostBool)


main()