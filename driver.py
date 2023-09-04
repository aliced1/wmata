#!/usr/bin/env python3
import sys
import time
import datetime
import pytz
from rgbmatrix import graphics
import rgbmatrix
from samplebase import SampleBase
from PIL import Image
import weather
import csv
import random
import schedule

class Driver():

    def __init__(self) -> None:
        self.current_weather = weather.Weather()
        self.canvas_setup()
        self.vocab_setup()
        self.set_up_schedules()
    
    def set_up_schedules(self) -> None:
        schedule.every().hour.do(self.current_weather.update_weather)
        schedule.every().hour.do(self.draw_weather)
        schedule.every().hour.do(self.draw_temperatures)
        schedule.every().day.at("02:00", 'US/Eastern').do(self.pick_random_word)
        schedule.every(10).minutes.do(self.refresh_time)

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

    def vocab_setup(self) -> None:
        my_file = open('vocab.csv', 'r')
        reader = csv.reader(my_file)

        next(reader) # skip header
        self.vocab_list = []
        for line in reader:
            self.vocab_list.append(line) # list format is [[word1, definition1], [word2, definition2], ...]
        
        schedule.every().day.at("02:00", 'US/Eastern').do(self.pick_random_word)    

    def pick_random_word(self) -> None:

        # DEBUG
        print('Picking random word!')

        # pick a random word
        word_index = random.randrange(0, len(self.vocab_list))
        self.word_of_day = self.vocab_list[word_index]

    def draw_weather(self):

        print('Drawing weather!')

        if self.current_weather.is_rain_above_percent(30):
            weather_image = Image.open('/home/alice/wmata/weather_images/rain.png').convert('RGB')
        else:
            weather_image = Image.open('/home/alice/wmata/weather_images/sun.png').convert('RGB')
        self.double_buffer.SetImage(weather_image, 0, 0)

    def draw_temperatures(self):

        # DEBUG
        print('Drawing temps!')

        # Set up to draw high temperature
        font = graphics.Font()

        # Letters are 5x8 pixels high, color red, append degree symbol and add to buffer
        font.LoadFont("/home/alice/wmata/adafruit_rgb_library/rpi-rgb-led-matrix/fonts/5x8.bdf")
        
        # draw high
        textColor = graphics.Color(255, 0, 0)
        daily_high = driver.current_weather.get_daily_high_apparent_temp()
        my_text = str(daily_high) + u'\u00B0'
        # x = 20, y = 8, pixels measured from upper left corner, but coordinates are for lower left corner of first character
        graphics.DrawText(self.double_buffer, font, 20, 8, textColor, my_text)

        # Draw low temperature
        textColor = graphics.Color(0, 0, 255)
        daily_low = driver.current_weather.get_daily_low_apparent_temp()
        my_text = str(daily_low) + u'\u00B0'
        # x = 20, y = 16, pixels measured from upper left corner, but coordinates are for lower left corner of first character
        graphics.DrawText(self.double_buffer, font, 20, 16, textColor, my_text)
        my_text = str(999) + u'\u00B0'

    def refresh_time(self):
        self.now = datetime.datetime.now(pytz.timezone('US/Eastern'))


    # @profile
    def draw_screen(self):

        # set buffer initially
        # otherwise won't update until the turn of the hour (for weather)
        self.current_weather.update_weather()
        self.draw_temperatures()
        self.draw_weather()
        self.pick_random_word()
        
        font = graphics.Font()
        font.LoadFont("/home/alice/wmata/adafruit_rgb_library/rpi-rgb-led-matrix/fonts/6x13.bdf")
        font_width = 6
        blackout = Image.open('/home/alice/wmata/16x64_black.png').convert('RGB')
        textColor = graphics.Color(172, 44, 210)
        vocab_display_string = self.word_of_day[0] + ' -- ' + self.word_of_day[1] + '     '
        # graphics.DrawText(self.double_buffer, font, 0, 32, textColor, vocab_display_string)

        xpos = 0
        counter = 0

        while True:
            
            # TODO add display for cloud cover, snow, wind, rain depth
            # After pulling new data, update images and buffer for loop

            self.double_buffer.SetImage(blackout, 0, 16) # upper left corner of image at (0, -16) from upper left corner
            if (self.now.hour in [6, 7, 8, 9]): # TODO only check hour on a schedule?
                self.double_buffer.SetImage(blackout, 0, 16) # upper left corner of image at (0, -16) from upper left corner
                # test = Image.open('/home/alice/wmata/test.png').convert('RGB')
                counter += 1
                if counter > 200:
                    xpos += 1
                if (xpos > len(vocab_display_string) * font_width):
                    xpos = 0
                    counter = 0
                graphics.DrawText(self.double_buffer, font, -xpos, 30, textColor, vocab_display_string) # lower left corner of char at (xpos, y)
                graphics.DrawText(self.double_buffer, font, -xpos + (len(vocab_display_string) * font_width), 30, textColor, vocab_display_string) # lower left corner of char

            # self.double_buffer.SetImage(self.image, -xpos)
            # self.double_buffer.SetImage(self.image, -xpos + img_width)


            self.matrix.SwapOnVSync(self.double_buffer)
            schedule.run_pending()
            # print(schedule.idle_seconds())
            time.sleep(0.03)


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
        
