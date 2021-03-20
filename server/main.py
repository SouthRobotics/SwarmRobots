import coms as coms
import time
import camera as cam
import cv2
import pygame as pygame
import pygame.display as display
import pygame.joystick as joystick
import pygame.event as event
from pygame.locals import *
import math
import threading
import matplotlib.pyplot as plt
from matplotlib.colors import Normalize
from matplotlib.cm import ScalarMappable
from gmplot import GoogleMapPlotter
from random import random
import wx


class CustomGoogleMapPlotter(GoogleMapPlotter):
    def __init__(self, center_lat, center_lng, zoom, apikey='',
                 map_type='satellite'):
        if apikey == '':
            try:
                with open('apikey.txt', 'r') as apifile:
                    apikey = apifile.readline()
            except FileNotFoundError:
                pass
        super().__init__(center_lat, center_lng, zoom, apikey)

        self.map_type = map_type
        assert(self.map_type in ['roadmap', 'satellite', 'hybrid', 'terrain'])

    def write_map(self,  f):
        f.write('\t\tvar centerlatlng = new google.maps.LatLng(%f, %f);\n' %
                (self.center[0], self.center[1]))
        f.write('\t\tvar myOptions = {\n')
        f.write('\t\t\tzoom: %d,\n' % (self.zoom))
        f.write('\t\t\tcenter: centerlatlng,\n')
        f.write('\t\t\tmapTypeId: \'{}\'\n'.format(self.map_type))

        f.write('\t\t};\n')
        f.write(
            '\t\tvar map = new google.maps.Map(document.getElementById("map_canvas"), myOptions);\n')
        f.write('\n')

    def color_scatter(self, lats, lngs, colors,
                      size=None, marker=False, s=None, **kwargs):
        def rgb2hex(rgb):
            """ Convert RGBA or RGB to #RRGGBB """
            rgb = list(rgb[0:3]) # remove alpha if present
            rgb = [int(c * 255) for c in rgb]
            hexcolor = '#%02x%02x%02x' % tuple(rgb)
            return hexcolor

        for lat, lon, c in zip(lats, lngs, colors):
            self.scatter(lats=[lat], lngs=[lon], c=c, size=size, marker=marker,
                         s=s, **kwargs)



def truncate(number, digits) -> float:
    stepper = 10.0 ** digits
    return math.trunc(stepper * number) / stepper



#set current operating robot
current_robot = 1




#Subsystem Intilaization

factory = coms.start()
cam.work_addr = "192.168.1.137"
cam.start()





#Intialize GUI
#app = wx.App()

#frm = wx.Frame(None, title="Hello World")
#frm.Show()






#Main Recive/Proccescing loop
def recieveLoop():
    global succesfull
    time.sleep(3)
    initial_zoom = 20
    lats = [41.184546]
    lons = [ -73.99472]
    colors = ["#ff3333"]
    for robot in factory.robots:
        lats.append(robot.coordlat)
        lats.append(robot.coordlat)
        colors.append(robot.robotID)


    gmap = CustomGoogleMapPlotter(lats[current_robot-1], lons[current_robot-1], initial_zoom,
                                map_type='satellite')
    gmap.color_scatter(lats, lons, colors, size=1)

    gmap.draw("mymap.html")
#    frame2.load_file("mymap.html")
#    frame2.pack(fill="both", expand=True)





# Main Controll Sending Loop
def controlLoop():
    pygame.init()
    display.init()

    controller = joystick.Joystick(0)
    controller.init()
    print(joystick.get_count())
    print(controller.get_numaxes())
    while True:
        #time.sleep(3)
        #cam.work_addr = "10.0.0.2"+str(current_robot)
        event.pump()
        #print("i")
        coms.send(factory, current_robot, str(truncate((controller.get_axis(4)+1)/2, 3)) + "--" + str(truncate((controller.get_axis(5)+1)/2,3))  + "--" +  str(truncate(((controller.get_axis(0)+1)*90),3)))
        #print(str(truncate((controller.get_axis(4)+1)/2, 3)) + "--" + str(truncate((controller.get_axis(5)+1)/2,3))  + "--" +  str(truncate(((controller.get_axis(0)+1)*90),3)))
        #print(controller.get_axis(4))
        #coms.send(factory, 1)


#start both loops and gui loop
t2 = threading.Thread(target=recieveLoop)
t2.start()
t1 = threading.Thread(target=controlLoop)
t1.start()


#app.MainLoop()



#print(pygame.joystick.get_count())
#print(controller.get_numaxes())



    
            
