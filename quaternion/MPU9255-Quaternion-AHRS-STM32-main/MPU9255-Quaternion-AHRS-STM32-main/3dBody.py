import pygame
import math
from OpenGL.GL import *
from OpenGL.GLU import *
from pygame.locals import *
from threading import Thread
import threading

#useSerial = True # set true for using serial for data transmission, false for wifi
useQuat = False   # set true for using quaternions, false for using y,p,r angles


import serial
#ser = serial.Serial('COM3', 115200)
ser = serial.Serial(port="COM3", baudrate=115200, bytesize=8, timeout=1, stopbits=serial.STOPBITS_ONE)

def main():
    video_flags = OPENGL | DOUBLEBUF
    pygame.init()
    screen = pygame.display.set_mode((600,500), video_flags)
    pygame.display.set_caption("Aldebaran Core AHRS - MPU9255 QUATERNION")
    resizewin(600,500)
    init()
    frames = 0
    ticks = pygame.time.get_ticks()
    global b,d
    b=0
    d=0
    while 1:
        event = pygame.event.poll()
        
        if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
            break

        #line = ser.readline().decode('UTF-8').replace('\n', '')
        
        yaw = 0
        pitch = 89-d
        roll = b-84
        #yaw = float(line.split()[0])
        #pitch = float(line.split()[1])
        #roll = -float(line.split()[2])

        pitch = pitch - 0
        roll = roll - 0

        draw(1, yaw, pitch, roll)
        pygame.display.flip()


    #if(useSerial):
    #    ser.close()


def resizewin(width, height):
    """
    For resizing window
    """
    if height == 0:
        height = 1
    glViewport(0, 0, width, height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45, 1.0*width/height, 0.1, 100.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()


def init():
    glShadeModel(GL_SMOOTH)
    glClearColor(0.0, 0.0, 0.0, 0.0)
    glClearDepth(1.0)
    glEnable(GL_DEPTH_TEST)
    glDepthFunc(GL_LEQUAL)
    glHint(GL_PERSPECTIVE_CORRECTION_HINT, GL_NICEST)

def draw(w, nx, ny, nz):
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    glTranslatef(0, 0.0, -7.0)

    yaw = nx
    pitch = ny
    roll = nz
    drawText((-3,2.5,0), "Yaw: %f, Pitch: %f, Roll: %f" %(yaw, pitch, roll), 15)
    glRotatef(-roll, 0.00, 0.00, 1.00)
    glRotatef(pitch, 1.00, 0.00, 0.00)
    glRotatef(yaw, 0.00, 1.00, 0.00)

    glBegin(GL_QUADS)
    glColor3f(0.0, 1.0, 0.0)
    glVertex3f(1.0, 0.2, -1.0)
    glVertex3f(-1.0, 0.2, -1.0)
    glVertex3f(-1.0, 0.2, 1.0)
    glVertex3f(1.0, 0.2, 1.0)

    glColor3f(1.0, 0.5, 0.0)
    glVertex3f(1.0, -0.2, 1.0)
    glVertex3f(-1.0, -0.2, 1.0)
    glVertex3f(-1.0, -0.2, -1.0)
    glVertex3f(1.0, -0.2, -1.0)

    glColor3f(1.0, 0.0, 0.0)
    glVertex3f(1.0, 0.2, 1.0)
    glVertex3f(-1.0, 0.2, 1.0)
    glVertex3f(-1.0, -0.2, 1.0)
    glVertex3f(1.0, -0.2, 1.0)

    glColor3f(1.0, 1.0, 0.0)
    glVertex3f(1.0, -0.2, -1.0)
    glVertex3f(-1.0, -0.2, -1.0)
    glVertex3f(-1.0, 0.2, -1.0)
    glVertex3f(1.0, 0.2, -1.0)

    glColor3f(0.0, 0.0, 1.0)
    glVertex3f(-1.0, 0.2, 1.0)
    glVertex3f(-1.0, 0.2, -1.0)
    glVertex3f(-1.0, -0.2, -1.0)
    glVertex3f(-1.0, -0.2, 1.0)

    glColor3f(1.0, 0.0, 1.0)
    glVertex3f(1.0, 0.2, -1.0)
    glVertex3f(1.0, 0.2, 1.0)
    glVertex3f(1.0, -0.2, 1.0)
    glVertex3f(1.0, -0.2, -1.0)
    glEnd()


def drawText(position, textString, size):
    font = pygame.font.SysFont("Courier", size, True)
    textSurface = font.render(textString, True, (255, 255, 255, 255), (0, 0, 0, 255))
    textData = pygame.image.tostring(textSurface, "RGBA", True)
    glRasterPos3d(*position)
    glDrawPixels(textSurface.get_width(), textSurface.get_height(), GL_RGBA, GL_UNSIGNED_BYTE, textData)


def text():
    global a,b,c,d
    a=0
    b=0
    c=0
    d=0
    while True:
        s = ser.readline(2)
        a=s[0]
        b=0.95*b+0.05*a

        c=s[1]
        d=d*0.95+0.05*c

    print(s[0],"  ",s[1])


t1 = threading.Thread(target=main)
t2 = threading.Thread(target=text)
t1.start()
t2.start()

'''
if __name__ == '__main__':
    main()
'''