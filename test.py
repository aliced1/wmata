#!/usr/bin/env python3
import time
from rgbmatrix import graphics
import rgbmatrix
from samplebase import SampleBase
from PIL import Image
import schedule
import numpy as np

# When drawing with coordinates, (x, y) is measured from the upper left
# side of the matrix. Whatever is being drawn is measured from the 
# lower left corner of the shape. 

options = rgbmatrix.RGBMatrixOptions()

options.hardware_mapping = 'adafruit-hat'
options.rows = 32
options.cols = 64
options.chain_length = 1
options.parallel = 1
options.row_address_type = 0
options.multiplexing = 0
options.pwm_bits = 10 #default 11
options.brightness = 50 # don't go lower than 30, I think. Max 100
options.pwm_lsb_nanoseconds = 130
options.led_rgb_sequence = "RGB"
options.pixel_mapper_config = ""
options.panel_type = ""
options.show_refresh_rate = 0 #default 1
options.gpio_slowdown = 2 # 2 or 3, 2 seems to work best
options.disable_hardware_pulsing = False
options.drop_privileges=False
matrix = rgbmatrix.RGBMatrix(options = options)
double_buffer = matrix.CreateFrameCanvas()




# draw a black box of size 15 across, 8 high, location measured from top left corner of screen to TOP left corner of black box
image = Image.open('/home/alice/wmata/16x64_pink.png').convert('RGB')
double_buffer.SetImage(image, 0, 0)
double_buffer.SetImage(image, 0, 16)

Canvas = np.full((10, 8), 0)
image = Image.fromarray(Canvas, 'RGB')
double_buffer.SetImage(image, 0, 0)


font = graphics.Font()
# Letters are 5x8 pixels high
font.LoadFont("/home/alice/wmata/adafruit_rgb_library/rpi-rgb-led-matrix/fonts/5x8.bdf")
# graphics.DrawText(double_buffer, font, 0, 8, graphics.Color(255, 255, 255), text)


while True:

    matrix.SwapOnVSync(double_buffer)
    schedule.run_pending()
    time.sleep(0.03)
        
