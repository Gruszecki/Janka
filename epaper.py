# -*-  coding:utf-8 -*-
import time
from PIL import Image, ImageDraw, ImageFont

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

			current_time = time.strftime('%H:%M:%S')
			draw.text((40, 150), current_time, font=font, fill=0)

			epd.displayPart(epd.getbuffer(image))
			time.sleep(1)

	except IOError as e:
		print(e)

if __name__ == '__main__':
    run()


