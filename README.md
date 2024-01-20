# WMATA and Weather
### A weather and DC metro train time driver for Adafruit's LED matrix board

Displays today's weather or tomorrow's weather depending on the time of day, and upcoming train times for the line and station selected. Also displays a word of the day between 6AM and 9AM local time, chosen from a 3k+ GRE word list. Tested to run on a Raspberry Pi 3 Model B, on Ubuntu and Raspberry Pi OS. Uses the Adafruit 64x32 LED Matrix with 4mm pitch, and the RGB [Matrix HAT + RTC](https://learn.adafruit.com/adafruit-rgb-matrix-plus-real-time-clock-hat-for-raspberry-pi)



## Installation
In your project directory, run curl to grab the rgb matrix installation script, according to Adafruit's guide [here](). This should create a folder called `adafruit_rgb_library` with the required library
`curl https://raw.githubusercontent.com/adafruit/Raspberry-Pi-Installer-Scripts/main/rgb-matrix.sh >rgb-matrix.sh`
`sudo bash rgb-matrix.sh`

Install pip
`sudo apt-get pip`

Install the following packages using pip
`sudo pip install pytz`
`sudo pip install pandas`
`sudo pip install schedule`

Run the script using
`sudo python driver.py`
