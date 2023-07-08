#!/usr/bin/env python3
import sys
import time
from rgbmatrix import graphics
import rgbmatrix
from samplebase import SampleBase
from PIL import Image
import weather

class Driver():

    # def __init__(self, *args, **kwargs):
    #     super(Driver, self).__init__(*args, **kwargs)

    def draw_screen(self):
        
        options = rgbmatrix.RGBMatrixOptions()
        
        options.hardware_mapping = 'adafruit-hat'
        options.rows = 32
        options.cols = 64
        options.chain_length = 1
        options.parallel = 1
        options.row_address_type = 0
        options.multiplexing = 0
        options.pwm_bits = 11
        options.brightness = 30
        options.pwm_lsb_nanoseconds = 130
        options.led_rgb_sequence = "RGB"
        options.pixel_mapper_config = ""
        options.panel_type = ""
        options.show_refresh_rate = 1
        options.gpio_slowdown = 2
        options.disable_hardware_pulsing = False
        options.drop_privileges=False
        self.matrix = rgbmatrix.RGBMatrix(options = options)
        
        double_buffer = self.matrix.CreateFrameCanvas()
        current_weather = weather.Weather()

        # print(dir(double_buffer))

        while True:
            
            if current_weather.is_rain_above_percent(30):
                self.image = Image.open('rain.png').convert('RGB')
            else:
                self.image = Image.open('sun.png').convert('RGB')
            
            font = graphics.Font()
            font.LoadFont("adafruit_rgb_library/rpi-rgb-led-matrix/fonts/7x13.bdf")
            textColor = graphics.Color(255, 0, 0)
            my_text = 'sunny'
            
            double_buffer.Clear()
            graphics.DrawText(double_buffer, font, 20, 10, textColor, my_text)
            
            # self.flag = not self.flag
            
            # if self.flag == 0:
            #     self.image = Image.open('sun.png').convert('RGB')
            # else:
            #     self.image = Image.open('rain.png').convert('RGB')

            xpos = 0
            double_buffer.SetImage(self.image, xpos)

            double_buffer = self.matrix.SwapOnVSync(double_buffer)
            time.sleep(0.5)


# Main function
# e.g. call with
#  sudo ./image-scroller.py --chain=4
# if you have a chain of four
if __name__ == "__main__":
    driver = Driver()
    try:
        print("Press CTRL-C to stop sample")
        driver.draw_screen()
    except KeyboardInterrupt:
        print('\nExiting\n')
        sys.exit(0)
        
