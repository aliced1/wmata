#!/usr/bin/env python3
import sys
import time
from rgbmatrix import graphics
import rgbmatrix
from samplebase import SampleBase
from PIL import Image
import weather

class Driver():

    def __init__(self) -> None:
        self.current_weather = weather.Weather()
        self.canvas_setup()
    
    def canvas_setup(self) -> None:
        
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
        
        self.double_buffer = self.matrix.CreateFrameCanvas()

    def draw_weather(self):
        if self.current_weather.is_rain_above_percent(30):
            weather_image = Image.open('rain.png').convert('RGB')
        else:
            weather_image = Image.open('sun.png').convert('RGB')
        self.double_buffer.SetImage(weather_image, 0, 0)

    def draw_screen(self):
        
        # DEBUG
        # print('buffer type = ', type(self.double_buffer))
        # print(dir(double_buffer))s

        while True:
            
            # TODO add display for cloud cover, snow, wind, rain depth

            self.draw_weather()
            
            font = graphics.Font()
            font.LoadFont("adafruit_rgb_library/rpi-rgb-led-matrix/fonts/5x8.bdf")
            textColor = graphics.Color(255, 0, 0)
            my_text = '101' + u'\u00B0'
            
            graphics.DrawText(self.double_buffer, font, 20, 10, textColor, my_text)

            # DEBUG
            # double_buffer.SetImage(Image.open('white20x20.png').convert('RGB'), 20)

            self.double_buffer = self.matrix.SwapOnVSync(self.double_buffer)
            time.sleep(0.5)


# Main function
# e.g. call with
#  sudo ./image-scroller.py --chain=4
# if you have a chain of four
if __name__ == "__main__":
    driver = Driver()

    driver.current_weather.print_weather_dict()

    try:
        print("Press CTRL-C to stop sample")
        driver.draw_screen()
    except KeyboardInterrupt:
        print('\nExiting\n')
        sys.exit(0)
        
