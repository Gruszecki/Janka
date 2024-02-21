# -*-  coding:utf-8 -*-
import time
from PIL import Image, ImageDraw, ImageFont
import os
from waveshare_epd import epd1in54_V2


def run():
	try:
		epd = epd1in54_V2.EPD()
		epd.init(0)
		epd.Clear(0xFF)

		epd.init(1)
		image = Image.new('1', (epd.height, epd.width), 255)
		draw = ImageDraw.Draw(image)
		font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 24)

		while True:
			draw.rectangle((0, 0, epd.height, epd.width), fill=255)
			if os.path.isfile('images/radio_1.bmp'):
				draw.text((0, 0), 'yes', font=font, fill=0)
			else:
				draw.text((0, 0), 'no', font=font, fill=0)
			# logo = Image.open('images/radio_1.bmp')
			# epd.displayPart(epd.getbuffer(logo))

			current_time = time.strftime('%H:%M:%S')
			draw.text((40, 150), current_time, font=font, fill=0)

			epd.displayPart(epd.getbuffer(image))
			time.sleep(0.5)

	except IOError as e:
		print(e)

if __name__ == '__main__':
    run()


