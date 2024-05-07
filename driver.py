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
import wmata
import numpy as np
import math

class Driver():

    def __init__(self) -> None:
        self.driver_weather = weather.Weather()
        self.driver_wmata = wmata.Wmata()
        self.canvas_setup()
        self.vocab_setup()
        self.set_up_schedules()
        self.refresh_time()
    
    def set_up_schedules(self) -> None:
        # TODO store today's weather and tomorrow's weather in separate vars?
        schedule.every().hour.do(self.driver_weather.update_weather)
        schedule.every().hour.do(self.draw_weather)
        schedule.every().hour.do(self.draw_temperatures)
        schedule.every().hour.do(self.draw_uv_index)
        schedule.every().hour.do(self.draw_current_temperature)
        schedule.every(15).seconds.do(self.draw_train_time)
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

    def draw_weather(self) -> str:

        print('Drawing weather!')
        return_string = ''

        # TODO add night
        # All images are 16x16 pixels
        if self.driver_weather.is_rain_above_percent(30):
            weather_image = Image.open('/home/alice/wmata/weather_images/rain.png').convert('RGB')
            return_string = 'rain'
        elif self.driver_weather.is_snowing():
            weather_image = Image.open('/home/alice/wmata/weather_images/snow.png').convert('RGB')
            return_string = 'snow'
        elif self.driver_weather.get_cloud_cover() > 40:
            weather_image = Image.open('/home/alice/wmata/weather_images/cloudy.png').convert('RGB')
            return_string = 'cloudy'
        elif self.driver_weather.get_cloud_cover() < 40 and self.driver_weather.get_cloud_cover() > 20:
            weather_image = Image.open('/home/alice/wmata/weather_images/partly_cloudy.png').convert('RGB')
            return_string = 'partly_cloudy'
        elif self.driver_weather.is_foggy():
            weather_image = Image.open('/home/alice/wmata/weather_images/fog.png').convert('RGB')
            return_string = 'fog'
        else:
            weather_image = Image.open('/home/alice/wmata/weather_images/sun.png').convert('RGB')
            return_string = 'sun'
        
        self.double_buffer.SetImage(weather_image, 0, 0) # upper left corner of image
        return return_string

    def draw_temperatures(self):

        # Set up to draw high temperature
        font = graphics.Font()
        # Letters are 5x8 pixels high, color red
        font.LoadFont("/home/alice/wmata/adafruit_rgb_library/rpi-rgb-led-matrix/fonts/5x8.bdf")
        
        # draw high
        textColor = graphics.Color(255, 30, 30)
        daily_high = driver.driver_weather.get_daily_apparent_temp_extrema().get('high')
        # Append degree symbol
        temperature_string = str(daily_high) + u'\u00B0'
        # SetImage coordinates are the upper left coordinate of the image 
        self.double_buffer.SetImage(self.black_image(10, 8), 20, 0)
        # x = 20, y = 8, coordinates for DrawText are the lower left corner of the first character
        graphics.DrawText(self.double_buffer, font, 20, 8, textColor, temperature_string)

        # Draw low temperature
        textColor = graphics.Color(128, 214, 242)
        daily_low = driver.driver_weather.get_daily_apparent_temp_extrema().get('low')
        temperature_string = str(daily_low) + u'\u00B0'
        self.double_buffer.SetImage(self.black_image(10, 8), 20, 8)
        # x = 20, y = 16, pixels measured from upper left corner, but coordinates are for lower left corner of first character
        graphics.DrawText(self.double_buffer, font, 20, 16, textColor, temperature_string)

    def black_image(self, width: int, height: int) -> Image:
        # TODO check inputs

        full_array = np.full((height, width), 0)
        return Image.fromarray(full_array, 'RGB')

    def refresh_time(self):
        self.now = datetime.datetime.now(pytz.timezone('US/Eastern'))
    
    def draw_train_time(self):
        # Set up to draw train time
        font = graphics.Font()
        textColor = graphics.Color(0, 255, 0)

        # Letters are 5x8 pixels high, color red, append degree symbol and add to buffer
        font.LoadFont("/home/alice/wmata/adafruit_rgb_library/rpi-rgb-led-matrix/fonts/5x8.bdf")
        
        # draw train time
        incoming_time = self.driver_wmata.get_closest_train('D08', 'SV', 'west')
        display_options = {'ARR':'Now', 'BRD':'NOW', None:'?'}
        display_time = display_options.get(incoming_time, (str(incoming_time) + 'min'))
        train_string = 'Leave'
        # x = 40, y = 8, pixels measured from upper left corner, but coordinates are for lower left corner of first character
        graphics.DrawText(self.double_buffer, font, 40, 8, textColor, train_string)
        self.double_buffer.SetImage(self.black_image(25, 8), 40, 8)
        graphics.DrawText(self.double_buffer, font, 40, 16, textColor, display_time)
    
    def draw_uv_index(self, x: int, y: int) -> None:
        """Draws the current UV index. Color will change according to a mapping between 0 and 11.
        Temperature will be drawn at x and y coordinates provided, measured from the top left corner of the screen.
        Footprint is 25 width, 8 height.

        Args:
            x (int): x coordinate (horizontal distance to upper left starting pixel, exclusive)
            y (int): y coordinate (vertical distance to upper left starting pixel, exclusive)
        """
        uv_index_colors = [[0,255,0], [85,85,0], [170,170,0], [255,255,0], [255,220,0], [255,185,0], [255,150,0], [255,75,0], [255,0,0], [255,0,85], [255,0,170], [255,0,255]]

        # Set up to draw UV index
        font = graphics.Font()

        # Letters are 5x8 pixels high
        font.LoadFont("/home/alice/wmata/adafruit_rgb_library/rpi-rgb-led-matrix/fonts/5x8.bdf")

        # Draw 'UV' on screen
        # draw a black box of size 15 across, 8 high, starting at x, y, measured from top left corner of screen to TOP left corner of black box
        self.double_buffer.SetImage(self.black_image(15, 8), x, y)
        # draw three characters, width 5*3 across, 8 high, starting at x, y, measured from top left corner of screen to BOTTOM left corner of text
        graphics.DrawText(self.double_buffer, font, x, y + 8, graphics.Color(255, 255, 255), 'UV:')
        
        # Draw UV index with color according to UV Index Scale
        uv_index = self.driver_weather.uv_index_list()[self.now.hour]
        uv_index = int(math.ceil(uv_index))
        uv_color = uv_index_colors[uv_index]
        self.double_buffer.SetImage(self.black_image(10, 8), x + 15, y)
        graphics.DrawText(self.double_buffer, font, x + 15, y + 8, graphics.Color(uv_color[0],uv_color[1],uv_color[2]), str(uv_index))
    
    def draw_current_temperature(self, x: int, y: int) -> None:
        """Draws the current apparent temperature (heat index) in Fahrenheit. Color will change according to a mapping between 25 degrees and 110 degrees.
        Temperature will be drawn at x and y coordinates provided, measured from the top left corner of the screen.
        Footprint is 20 width, 8 height.

        Args:
            x (int): x coordinate (horizontal distance to upper left starting pixel, exclusive)
            y (int): y coordinate (vertical distance to upper left starting pixel, exclusive)
        """

        current_temp_colors = {110:[255,0,0],105:[255,0,32],100:[255,0,64],95:[255,0,96],90:[255,0,128],
                               85:[255,0,159],80:[255,0,191],75:[255,0,223],70:[255,0,255],65:[227,0,255],
                               60:[198,0,255],55:[170,0,255],50:[142,0,255],45:[113,0,255],40:[85,0,255],
                               35:[57,0,255],30:[28,0,255],25:[0,0,255]}
        
        current_temp = self.driver_weather.get_current_temperature()
        closest_key_temp = min(current_temp_colors.keys(), key=lambda x:abs(x - current_temp))
        color_list = current_temp_colors.get(closest_key_temp)
        font = graphics.Font()

        # Letters are 5x8 pixels high
        font.LoadFont("/home/alice/wmata/adafruit_rgb_library/rpi-rgb-led-matrix/fonts/5x8.bdf")

        # Draw current temp
        # draw a black box of size 20 across, 8 high, measured from top left corner of screen to TOP left corner of black box
        self.double_buffer.SetImage(self.black_image(20,8), x, y)

        # draw three or four characters (depending on whether temperature is 3 digits)
        # width 5*(3 or 4) across, 8 high, starting at x and y provided, measured from top left corner of screen to BOTTOM left corner of text
        # Add 8 to y value because text is drawn from the bottom left corner and character height is 8
        current_temperature_string = str(round(current_temp)) + u'\u00B0'
        graphics.DrawText(self.double_buffer, font, x, y + 8, graphics.Color(color_list[0],color_list[1],color_list[2]), current_temperature_string)

    def draw_text(self, x: int, y: int, text: str, r: int = 255, g: int = 255, b: int = 255) -> None:
        """Draws generic text at the coordinates specified. x and y coordinates should be the location of the upper left
        corner of the desired text. r, g, b are 8-bit color values between 0 and 255. Default is 255, 255, 255 (white)

        Args:
            x (int): x coordinate
            y (int): y coordinate
            text (str): text to draw
            r (int, optional): Red color value. Defaults to 255.
            g (int, optional): Green color value. Defaults to 255.
            b (int, optional): Blue color value. Defaults to 255.

        Returns:
            _type_: None
        """

        if len(text) == 0: return None

        font = graphics.Font()

        print('LENGTH = {}'.format(len(text)))

        # Letters are 5x8 pixels high
        font.LoadFont("/home/alice/wmata/adafruit_rgb_library/rpi-rgb-led-matrix/fonts/5x8.bdf")

        # draw a black box, location measured from top left corner of screen to TOP left corner of black box
        self.double_buffer.SetImage(self.black_image(5 * len(text), 8), x, y)

        # text starts at x and y provided, measured from top left corner of screen to BOTTOM left corner of text
        # Add 8 to y value because text is drawn from the bottom left corner and character height is 8
        graphics.DrawText(self.double_buffer, font, x, y + 8, graphics.Color(r, g, b), text)


    # @profile
    def draw_screen(self):

        # set buffer initially
        # otherwise won't update until the turn of the hour
        self.driver_weather.update_weather()
        self.draw_temperatures()
        self.draw_weather()
        self.pick_random_word()
        self.refresh_time()
        self.draw_train_time() # TODO make this generic - pass in arguments for station, line, direction
        self.draw_uv_index(20, 16)
        self.draw_current_temperature(20, 24)
        self.draw_text(0, 20, 'Now:', 255, 255, 102)
        
        
        # Set up fonts, text color, and display string for the word of the day
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

            if ((driver.now.hour >= 23) or (driver.now.hour <= 5)):
                sys.exit(0)
            
            if (self.now.hour > 6 and self.now.hour < 9):
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
    # driver.driver_weather.print_weather_dict()
    # print()
    # print('train time:')
    # print(driver.driver_wmata.get_closest_train('D08', 'SV', 'west'))
    # print()

    try:
        print("Press CTRL-C to stop sample")
        driver.draw_screen()
    except KeyboardInterrupt:
        print('\nExiting\n')
        sys.exit(0)
        
