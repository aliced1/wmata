#!/usr/bin/env python3
import sys
import time
import datetime
import pytz
import multiprocessing
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
            weather_image = Image.open('/home/alice/wmata/weather_images/rain.png').convert('RGB')
        else:
            weather_image = Image.open('/home/alice/wmata/weather_images/sun.png').convert('RGB')
        self.double_buffer.SetImage(weather_image, 0, 0)

    def draw_temperatures(self):

        # Set up to draw high temperature
        font = graphics.Font()

        # Letters are 5x8 pixels high, color red, append degree symbol and add to buffer
        font.LoadFont("/home/alice/wmata/adafruit_rgb_library/rpi-rgb-led-matrix/fonts/5x8.bdf")
        
        # draw high
        textColor = graphics.Color(255, 0, 0)
        daily_high = driver.current_weather.get_daily_high_apparent_temp()
        my_text = str(daily_high) + u'\u00B0'
        # x = 20, y = 8
        graphics.DrawText(self.double_buffer, font, 20, 8, textColor, my_text)

        # Draw low temperature
        textColor = graphics.Color(0, 0, 255)
        daily_low = driver.current_weather.get_daily_low_apparent_temp()
        my_text = str(daily_low) + u'\u00B0'
        # x = 20, y = 16, pixels measured from upper left corner
        graphics.DrawText(self.double_buffer, font, 20, 16, textColor, my_text)

    def periodic_refresh_tracker(self, shared_flag):
        current_time = datetime.datetime.now(pytz.timezone('US/Eastern'))
        hour = current_time.hour
        
        while True:
            if current_time.hour != hour:
                print('set flag to update weather!')
                hour = current_time.hour
                shared_flag.value = 1
                time.sleep(60) # Use different sleep times for weather vs metro?


    # @profile
    def draw_screen(self):

        # set buffer initially
        # otherwise won't update until the turn of the hour (for weather)
        self.current_weather.update_weather()
        self.draw_temperatures()
        self.draw_weather()

        # spin off process to track timers with shared state variable "flag" 
        flag = multiprocessing.Value('i', 0)
        t1 = multiprocessing.Process(target=self.periodic_refresh_tracker, args=(flag,))
        t1.start()

        # DEBUG
        # print('buffer type = ', type(self.double_buffer))
        # print(dir(double_buffer))s

        while True:
            
            # TODO add display for cloud cover, snow, wind, rain depth
            # After pulling new data, update images and buffer for loop

            # only update buffer to draw weather and temp after we've pulled new weather data
            if flag.value == 1:
                print('updating weather and buffer in main loop!')
                flag.value = 0
                self.current_weather.update_weather()
                self.draw_temperatures()
                self.draw_weather()

            # self.double_buffer = self.matrix.SwapOnVSync(self.double_buffer)
            self.matrix.SwapOnVSync(self.double_buffer)
            time.sleep(5)


if __name__ == "__main__":
    driver = Driver()

    driver.current_weather.print_weather_dict()
    driver.current_weather.get_daily_high_apparent_temp()

    try:
        print("Press CTRL-C to stop sample")
        driver.draw_screen()
    except KeyboardInterrupt:
        print('\nExiting\n')
        sys.exit(0)
        
