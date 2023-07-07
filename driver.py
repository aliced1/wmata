#!/usr/bin/env python3
import time
from samplebase import SampleBase
from PIL import Image
import weather

class Driver(SampleBase):

    def __init__(self, *args, **kwargs):
        super(Driver, self).__init__(*args, **kwargs)

    def run(self):
        double_buffer = self.matrix.CreateFrameCanvas()
        current_weather = weather.Weather()

        # print(dir(double_buffer))

        while True:
            
            if current_weather.is_rain_above_percent(30):
                self.image = Image.open('rain.png').convert('RGB')
            else:
                self.image = Image.open('sun.png').convert('RGB')
            
            # self.flag = not self.flag
            
            # if self.flag == 0:
            #     self.image = Image.open('sun.png').convert('RGB')
            # else:
            #     self.image = Image.open('rain.png').convert('RGB')

            xpos = 0
            double_buffer.SetImage(self.image, -xpos)

            double_buffer = self.matrix.SwapOnVSync(double_buffer)
            time.sleep(0.5)
    


# Main function
# e.g. call with
#  sudo ./image-scroller.py --chain=4
# if you have a chain of four
if __name__ == "__main__":
    driver = Driver()
    driver.process()
