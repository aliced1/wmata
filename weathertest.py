#!/usr/bin/env python
import time
from samplebase import SampleBase
from PIL import Image
import json


class ImageScroller(SampleBase):
    def __init__(self, *args, **kwargs):
        super(ImageScroller, self).__init__(*args, **kwargs)
        self.parser.add_argument("-i", "--image", help="The image to display", default="sun.png")

    def run(self):
        # if not 'image' in self.__dict__:
        #     self.image = Image.open(self.args.image).convert('RGB')
        # self.image.resize((20, 20), Image.ANTIALIAS)

        self.image = Image.open('sun.png').convert('RGB')
        # self.image.resize((20, 20), Image.ANTIALIAS)

        double_buffer = self.matrix.CreateFrameCanvas()
        # print(dir(double_buffer))
        img_width, img_height = self.image.size

        # xpos = 10
        # while True:
        #     double_buffer.SetImage(self.image, xpos)
        #     double_buffer = self.matrix.SwapOnVSync(double_buffer)
        #     time.sleep(0.01)

        # let's scroll
        xpos = 0
        while True:
            xpos += 1
            if (xpos > img_width):
                xpos = 0

            double_buffer.SetImage(self.image, -xpos)
            double_buffer.SetImage(self.image, -xpos + 64)

            double_buffer = self.matrix.SwapOnVSync(double_buffer)
            time.sleep(0.05)
    


# Main function
# e.g. call with
#  sudo ./image-scroller.py --chain=4
# if you have a chain of four
if __name__ == "__main__":
    image_scroller = ImageScroller()
    if (not image_scroller.process()):
        image_scroller.print_help()
