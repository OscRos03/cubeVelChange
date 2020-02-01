#Import nessecary modules
import pygame
import time
import random


#Global variables
accelDecel = 1
WHITE = pygame.Color('white')
BLACK = pygame.Color('black')
done = False


#Settings

#Screen settings
screenSize = [500, 500]
# for ball_1 in range(anatl - 1):
#     for ball_2 in range(ball_1+1, antal):
#         hit(ball_1, ball_2) //Olle

#General settings
framerate = 60

#Cube settings
cubeAmount = 50 #Amount of cubes to be drawn
cubeMaxVel = 100 #Cube max speed in px/s at spawn (Min is 1)
cubeSize = 10 #Size of cube in px


#Init
pygame.init()
pygame.joystick.init()
screen = pygame.display.set_mode((screenSize[0], screenSize[1]))
clock = pygame.time.Clock()



class cube(): #Make cube class
    def __init__(self):
        self.side = cubeSize
        self.xpos = random.randint(0, screenSize[0] - self.side)
        self.ypos = random.randint(0, screenSize[1] - self.side)
        self.xvel = random.randint(1, cubeMaxVel)
        self.yvel = random.randint(1, cubeMaxVel)

    
    def updateCube(self, speed, allCubes): #Function for hit detection and drawing the cubes
            pygame.draw.rect(screen, WHITE, (self.xpos, self.ypos, self.side, self.side))

            self.xvel *= accelDecel #Change velocity if button is pressed
            self.yvel *= accelDecel

            if self.xvel * speed >= screenSize[0]: #Set max speed to 1 screen per frame
                self.xvel = screenSize[0]
            
            if self.yvel * speed >= screenSize[1]:
                self.yvel = screenSize[1]


            self.xpos += self.xvel * speed #Change cube position and take time into account
            self.ypos += self.yvel * speed


            if self.xpos + self.side >= screenSize[0] and self.xvel > 0: #Reverse velocity if a side is hit.
                self.xvel = -self.xvel
            elif self.xpos <= 0 and self.xvel < 0:
                self.xvel = -self.xvel

            if self.ypos + self.side >= screenSize[1] and self.yvel > 0:
                self.yvel = -self.yvel
            elif self.ypos <= 0 and self.yvel < 0:
                self.yvel = -self.yvel

            for cubes in allCubes:
                if cubes.xpos < self.xpos < cubes.xpos + cubes.side and cubes.ypos < self.ypos < cubes.ypos + cubes.side: # do big thonk on this one
                    print("inside cube" + str(random.randint(1, 5)))



cubeList = [cube() for i in range(0, cubeAmount)] #Make cube instances

joystick_count = pygame.joystick.get_count() #Get number of joypads
if (joystick_count == 0): #Check if there are 0, warn if so
    print("No joypads found, no accel/decel support")


for i in range(joystick_count): #Make joystick objects
    joystick = pygame.joystick.Joystick(i)
    joystick.init()
    print(joystick.get_name() + "init")

def updateButtons():
    for e in range(joystick_count):
        joystick = pygame.joystick.Joystick(e)
        for i in range(joystick.get_numbuttons()):
            if (joystick.get_button(i) == 1):
                print("Button " + str(i) + " on joypad " + str(e) + ": " + str(pygame.joystick.Joystick(e).get_button(i)))

                

def updateJoystick():
    for e in range(joystick_count):
        joystick = pygame.joystick.Joystick(e)
        for i in range(joystick.get_numaxes()):
            if (round(joystick.get_axis(i)) != 0):
                print("Axis " + str(i) + " on joypad " + str(e) + " is " + str(round(joystick.get_axis(i))))



while not done: #Main game loop
    for event in pygame.event.get(): #Process events
        if event.type == pygame.QUIT:
            done = True
        elif event.type == pygame.JOYBUTTONDOWN:
            updateButtons()
            for e in range(joystick_count):
                joystick = pygame.joystick.Joystick(e)
                if joystick.get_button(0) == 1 and joystick.get_button(1) == 1:
                    accelDecel = 1
                elif joystick.get_button(0) == 1:
                    accelDecel = 0.99
                elif joystick.get_button(1) == 1:
                    accelDecel = 1.01

        elif event.type == pygame.JOYBUTTONUP:
            updateButtons()
            for e in range(joystick_count):
                joystick = pygame.joystick.Joystick(e)
                if joystick.get_button(0) == 0 and joystick.get_button(1) == 0:
                    accelDecel = 1

        elif event.type == pygame.JOYAXISMOTION:
            updateJoystick()

    
    dt = clock.tick(framerate)
    speed = float(dt)/1000

    screen.fill(BLACK)
    
    for i in range(len(cubeList)):
        cubeList[i].updateCube(speed, cubeList)
        
    pygame.display.update()

pygame.quit()