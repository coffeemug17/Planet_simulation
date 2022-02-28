#Import the necessary libraries and initialize pygame

import math
import pygame
pygame.init()

WIDTH, HEIGHT = 800, 800
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Solar System Planet Simulation")

#Declaring the RGB values to be used for the planets
WHITE = (255,255,255)
YELLOW = (255,255,0)
BLUE = (100,149,237)
RED = (188, 39, 50)
DARK_GREY = (80, 78, 81)

#Defining a Planet Class which will be used to initialize all the planets and set them in an orbital manner
class Planet:
    #Define constants that we need
    #Astronaumical units
    AU = 149.6e6 * 1000
    G = 6.67423e-11
    SCALE = 250/ AU  #1AU = 100 PIXELS
    TIMESTEP =  3600*24 #1 day timeline

#Initialization
    def __init__(self, x, y, radius, color, mass):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.mass = mass

        self.orbit = []
        self.sun = False
        self.dist_to_sun = 0


        self.x_vel = 0
        self.y_vel = 0

#The draw function is defined withtin the class to draw objects to displace on the window
    def draw(self, win):
        x = self.x * self.SCALE + WIDTH/2
        y = self.y * self.SCALE + HEIGHT/2

        updated_points = []
        if len(self.orbit) > 2:
            for point in self.orbit:
                x, y = point
                x = x*self.SCALE + WIDTH/2
                y = y * self.SCALE + HEIGHT/2
                updated_points.append((x, y))

            pygame.draw.lines(WINDOW, self.color, False, updated_points, 2)
        pygame.draw.circle(WINDOW, self.color, (x,y), self.radius)


        pygame.draw.circle(WINDOW, self.color, (x,y), self.radius)

#This is used to calculate the centrifugal force between the planets and the sun
    def attraction(self,other):
        other_x, other_y = other.x, other.y
        distance_x = other_x - self.x
        distance_y = other_y - self.y
        distance = math.sqrt(distance_x**2 + distance_y**2)

        if other.sun:
            self.dist_to_sun = distance

        force = self.G * self.mass * other.mass/ distance**2
        theta = math.atan2(distance_y, distance_x)

        force_x = math.cos(theta)*force
        force_y = math.sin(theta)*force

        return force_x, force_y

#Constantly update the position to ensure motion
    def update_position(self, Planets):
        total_fx = total_fy = 0
        for planet in Planets:
            if self == planet:
                continue

            fx, fy = self.attraction(planet)
            total_fx += fx
            total_fy += fy

#Defined velocity in the x and y direction
        self.x_vel += total_fx/ self.mass *self.TIMESTEP
        self.y_vel += total_fy/ self.mass *self.TIMESTEP

        self.x += self.x_vel*self.TIMESTEP
        self.y += self.y_vel * self.TIMESTEP
        self.orbit.append((self.x, self.y))


#The main loop
def main():
    loop = True
    clock = pygame.time.Clock() #Running a clock for the program

    sun = Planet(0,0,30, YELLOW, 1.98892*10**30)
    sun.sun = True

    #Upto four planets are defined in the program currently
    earth = Planet(-1*Planet.AU, 0, 16, BLUE, 5.9742*10**24)
    earth.y_vel = 29.783*1000
    mars = Planet(-1.524*Planet.AU, 0, 12, RED, 6.39*10**23)
    mars.y_vel = 24.077*1000
    mercury = Planet(0.387*Planet.AU, 0, 8, DARK_GREY, 3.30*10**23)
    mercury.y_vel = -47.4*1000
    venus = Planet(0.723*Planet.AU, 0, 14, WHITE, 4.8685*10**24)
    venus.y_vel = -35.02*1000

    Planets = [sun, earth, mars, mercury, venus]

    while loop:
        clock.tick(60)
        WINDOW.fill((0,0,0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                loop = False

        for planet in Planets:
            planet.update_position(Planets)
            planet.draw(WINDOW)

        pygame.display.update()

    pygame.quit()

main()
