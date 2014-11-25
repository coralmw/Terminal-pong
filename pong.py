from drawille import Canvas
import curses
import numpy as np
import itertools
import time
import os, sys

X = 0
Y = 1
XSEC = 2
YSEC = 3
OUT = open('error', 'w')

def quit():
    OUT.close()
    sys.exit()

class Paddle(object):

    def __init__(self, side, canvas, frame):
        self.side = side
        self.canvas = canvas
        self.size = np.array([5, 2])
        y = 0+self.size[Y] if side == 'left' else frame[YSEC] - self.size[Y]
        x = int(frame[XSEC]/2)
        self.position = np.array([x, y])

        
        print(np.array([x, y]), np.array([5, 1]))
        self.bottom = np.array([x, y]) + np.array([5, 1])

    def draw(self):
        start = self.position
        finish = self.position + self.size    
        for x in range(start[X], finish[X]):
            for y in range(start[Y], finish[Y]):
                self.canvas.set(y, x)


class Ball(object):

    def __init__(self, canvas, frame):
        self.position = np.array([int(frame[XSEC]/2), int(frame[YSEC]/2)])
        self.velocity = np.array([0, -1])
        self.size = np.array([2, 2])
        self.canvas = canvas
        self.bounds = frame

    def update(self):
        self.position += self.velocity

    def _within(self, paddle):
        ybounds = (paddle.position[X]-self.size[0], 
                   paddle.position[X]+paddle.size[X]+self.size[0])
        xcontact = self.position[X] > min(ybounds) and self.position[X] < max(ybounds)
        ycontact = abs(self.position[Y] - paddle.position[Y]) < paddle.size[Y]
        return ycontact and xcontact

    def collide(self, paddle):
        print(self.position[Y], file=OUT)
        if self._within(paddle):
            print(paddle.side, file=OUT)
            print('collide', file=OUT)
            direction = 1 if self.position[Y] < self.bounds[YSEC]/2 else -1
            self.velocity[Y] = direction
        if self.position[Y] < self.bounds[Y] or self.position[Y] > self.bounds[YSEC]:
            quit()




    def draw(self):
        start = self.position
        finish = self.position + self.size  
        for x in range(start[0], finish[0]):
            for y in range(start[1], finish[1]):
                self.canvas.set(y, x)        

def draw_bounds(board, frame):
    top = [(frame[X], y) for y in range(frame[Y], frame[YSEC])]
    left = [(x, frame[Y]) for x in range(frame[X], frame[XSEC])]
    bottom = [(frame[XSEC], y) for y in range(frame[Y], frame[YSEC])]
    right = [(x, frame[YSEC]) for x in range(frame[X], frame[XSEC])]
    for pixel in top+left+right+bottom:
        board.set(*pixel)

def setup():
    # set the size of the board to the size of the terminal at ther start
    width, height = os.popen('stty size', 'r').read().split()
    height, width = 50, 50
    board = Canvas()
    frame = (0, 0, width, height)
    assert(frame[YSEC] == height)
    board.frame(*frame)
    draw_bounds(board, frame)

    # get some paddles
    lpaddle = Paddle('left', board, frame)
    rpaddle = Paddle('right', board, frame)
    ball = Ball(board, frame)

    # get some output!
    stdscr = curses.initscr()
    stdscr.refresh()
    return (lpaddle, rpaddle, ball), board, frame, stdscr

def draw(stuff, board, frame, stdscr):
    #clear the board
    board.clear()
    draw_bounds(board, frame)

    # calculate new ball position
    stuff[2].update()
    # check for collisions
    for paddle in stuff[:2]:
        stuff[2].collide(paddle)
    # draw the objects
    for obj in stuff:
        obj.draw()
    f = board.frame()
    stdscr.addstr(0, 0, '{0}\n'.format(f))
    stdscr.refresh()    

def read(chars, stuff):
    while not chars.empty():
        char = chars.get()
        if char == 'w':
            stuff[0].position[0] -= 1
        elif char == 's':
            stuff[0].position[0] += 1
        elif char == 'i':
            stuff[1].position[0] -= 1
        elif char == 'k':
            stuff[1].position[0] += 1
        elif char == 'q':
            quit()

def main(chars):
    stuff, board, frame, stdscr = setup()
    while True:
        time.sleep(15/1000)
        read(chars, stuff)
        draw(stuff, board, frame, stdscr)





