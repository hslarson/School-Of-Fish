import pygame
import random
import math

#Initialize Library
pygame.init()

#Title & Icon
pygame.display.set_caption("School of Fish")

icon = pygame.image.load('fish.ico')
pygame.display.set_icon(icon)

#Fish Properties
movement_speed = 1
number_of_fish = 36
fish_push_radius = 20

fish_radius = 4
color_vibrancy = 235

#Environment Properties
cursor_push_radius = 40
row_spacing = cursor_push_radius
column_spacing = row_spacing

rows = math.sqrt(number_of_fish)//1
columns = number_of_fish/rows

SCREENWIDTH = int((columns+6)*column_spacing)
SCREENHEIGHT = int((rows+6)*row_spacing)
screen = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))

start_x = (SCREENWIDTH/2)-((columns-1)*column_spacing)/2
start_y = (SCREENHEIGHT/2)-((rows-1)*row_spacing)/2

#Given 2 points finds angle and distance between them
def triangulate(center, other):
    angle = math.atan2(other[1]-center[1],other[0]-center[0])
    distance = math.sqrt((other[0]-center[0])**2+(other[1]-center[1])**2)
    return (angle, distance)

#Fish Class
class fish():
    def __init__(self, speed, home, position):
        self.speed = speed
        self.home = home
        self.position = position

        #Pick a random color for each fish
        temp_arr = [color_vibrancy,random.randint(0,255),0]
        random.shuffle(temp_arr)
        self.color = tuple(temp_arr)
    
    #Calculate x/y speeds from max speed & angle
    def path(self, angle, distance=movement_speed+1):
        if distance < movement_speed:
            self.position = self.home
            x_speed, y_speed = 0,0
        else:
            x_speed = movement_speed*math.cos(angle)
            y_speed = movement_speed*math.sin(angle)
        self.speed = (x_speed, y_speed)

        #Alters the position of the fish
        new_x = self.position[0]+self.speed[0]
        new_y = self.position[1]+self.speed[1]
        self.position = (new_x,new_y)

    #Detects cursor and/or other fish and navigates away from them
    def flee(self, cursor):
        temp_arr=[] #Stores all sources of danger
        
        #Checks for cursor
        angle, distance = triangulate(cursor,self.position)
        if distance < cursor_push_radius and distance > 0:
            temp_arr.append((angle,distance))
        else:
            #Checks each fish to see if it's too close (needs optimization)
            for f in range(number_of_fish):
                angle, distance = triangulate(school[f].position,self.position)
                if distance < fish_push_radius and distance > 0:
                    temp_arr.append((angle,distance))

        #If there are sources of danger, travel opposite to the sum of their vectors
        if len(temp_arr)>0:
            mean_angle = 0
            for a,d in temp_arr:
                mean_angle+=a
            
            mean_angle/=len(temp_arr)
            fish.path(self,mean_angle)
        
        #If there are no sources of danger, travel back to home position
        else:
            t1,t2 = triangulate(self.position, self.home)
            fish.path(self, t1, t2)

#Generates Fish
school=[]
x_pos = 0
y_pos = 0
for i in range(number_of_fish):
    #Calculate the home position of each fish and create the fish object
    temp_tuple = (int(start_x + x_pos*column_spacing), int(start_y + y_pos*row_spacing))
    school.append(fish((0,0), temp_tuple, temp_tuple))
    
    #Starts the next row 
    if x_pos == columns-1:
        y_pos += 1
        x_pos = 0
    else:
        x_pos += 1

#Main Loop
running = True
x,y=0,0
while running:
    #Draw the Background
    screen.fill((0, 2, 51))

    #Handle Events
    for event in pygame.event.get():
        #If the game is quit, then quit
        if event.type == pygame.QUIT:
            running = False

    #Get the mouse position
    x,y = pygame.mouse.get_pos()

    for i in range(number_of_fish):
        #Draw all of the fish
        pos = (int(school[i].position[0]),int(school[i].position[1]))
        pygame.draw.circle(screen, school[i].color, pos, fish_radius)

        school[i].flee((x,y))
        #school[i].move()
        
    #Update the display
    pygame.display.update()