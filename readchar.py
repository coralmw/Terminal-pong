import sys, os, tty, termios

def read(stdin):
    try:
        tty.setraw(stdin.fileno())
        ch = stdin.read(1)
    except Exception as e:
        print(e)
    else:
        return ch

def main(queue, fileno):
    stdin = os.fdopen(fileno)
    while True:
        ch = read(stdin) # blocking
        queue.put(ch)