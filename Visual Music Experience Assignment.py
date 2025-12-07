import py5
import py5_tools

py5_tools.processing.download_library("Sound")

from processing.sound import SoundFile
from processing.sound import Amplitude

#variables
rot_x = 0
rot_y = 0
rot_y2 = 0
cam_z = 0

h = 0 #hue

dx = 0 #disco ball x
dy = -150 # disco ball y

#cylinder variables
cone_shape = None
angle = None

#dancer variables
image = None

#text variables
font = None

#sound variables
soundfile = None
waveform = None
amplitude = None

#song variables
playlist = ["disco.wav", "juke_bug.wav", "funkytown.wav", "do_the_bartman.wav"]
current_track = 0
player = None

def setup():
   global image, font, amplitude, player
   py5.size(500,500, py5.P3D)
   py5.color_mode(py5.HSB)
   
   image = py5.load_image("disco.png")
   font = py5.create_font("Party Vibes.otf", 12)

   amplitude = Amplitude(py5.get_current_sketch())
   start_track(0)
   amplitude.input(player)

#music
def start_track(index):
   global player, current_track, amplitude
   current_track = index

   if player is not None and player.isPlaying():
      player.stop()

   print(f"Loading {playlist[current_track]}")
   player = SoundFile(py5.get_current_sketch(), playlist[current_track])
   player.play()
   amplitude.input(player)

def next_track():
   new_index = (current_track + 1) % len(playlist)
   start_track(new_index)

def mouse_pressed():
   next_track()

#visuals
def draw():
   global rot_x, rot_y, rot_y2, r, n, h, amplitude, image, cone_shape, circle_size, i
   global dx, dy
   py5.background(0)
   py5.stroke(h,255,150,100)
   py5.stroke_weight(10)
   py5.no_fill()
   
   #sphere background
   py5.push_matrix()
   py5.rotate_x(rot_x)
   py5.rotate_y(rot_y2)
   py5.sphere(250)
   py5.pop_matrix()
   
   #discoballs
   amp = amplitude.analyze()
   circle_size = py5.remap(amp, 0, 0.5, 50, 400)
   
   py5.push_matrix()
   py5.translate(dx, dy, 0)
   py5.rotate_y(rot_y)
   
   for i in range(0, 4):
      py5.push_matrix()
      
      match i:
         case 0: py5.translate(200, 0, 0)
         case 1: py5.translate(-200, 0, 0)
         case 2: py5.translate(0, 0, -200)
         case 3: py5.translate(0, 0, 200)
      
      py5.sphere(circle_size/10)
      py5.pop_matrix()
   
   py5.pop_matrix()

   #floor
   py5.push_matrix()
   py5.rotate_x(rot_x)
   py5.rotate_y(rot_y)
   py5.stroke(h,255,255)
   py5.fill(0)
   py5.translate(0,125,0)
   py5.box(150)
   py5.pop_matrix()

   #image
   py5.image(image, -25, 50, 50, -100)

   #light
   py5.push_matrix()
   py5.no_stroke()
   py5.fill(h, 100, 255, 100)
   py5.rotate_x(rot_x)
   py5.rotate_y(rot_y)
   py5.translate(0,100,0)
   cylinder(50, 1, -500, 25)
   py5.pop_matrix()

   py5.fill(h % 255, 255, 255)
   py5.scale(-1,1)
   py5.text_font(font)
   py5.text("Click to Play Next Song!", -70, -40, -80)

   #camera 
   #cam_z = - py5.mouse_y * 2 #controllable camera
   cam_z = -200 #set camera
   py5.camera(0, 0, cam_z, 0, 0, 0, 0, 1, 0)
   
   rot_x += 0.0 #rotate x
   rot_y += 0.01 #rotate clockwise
   rot_y2 += - 0.01 #rotate anticlockwise

   #hue change
   h += 1
   if h >= 255: #hue loop
      h = 1

#create cylinder
def cylinder(bottom, top, h, sides):
  py5.push_matrix()
  
  py5.translate(0, h/2, 0)
  
  angle = 0
  x = []
  z = []
  
  x2 = []
  z2 = []
 
  for i in range(0, sides + 1):
    angle = py5.TWO_PI / (sides) * i
    x.append(py5.sin(angle) * bottom)
    z.append(py5.cos(angle) * bottom)
    
  for i in range(0, sides + 1):
    angle = py5.TWO_PI / (sides) * i
    x2.append(py5.sin(angle) * top)
    z2.append(py5.cos(angle) * top)
 
  py5.begin_shape(py5.TRIANGLE_FAN)
 
  py5.vertex(0, -h/2, 0)
 
  for i in range(0, sides + 1):
    py5.vertex(x[i], -h/2, z[i])
 
  py5.end_shape()
 
  py5.begin_shape(py5.QUAD_STRIP) 
 
  for i in range(0, sides + 1):
    py5.vertex(x[i], -h/2, z[i])
    py5.vertex(x2[i], h/2, z2[i])
 
  py5.end_shape()
 
  py5.begin_shape(py5.TRIANGLE_FAN) 
  py5.vertex(0, h/2, 0)
 
  for i in range(0, sides + 1):
    py5.vertex(x2[i], h/2, z2[i])
 
  py5.end_shape()
  py5.pop_matrix()

py5.run_sketch()