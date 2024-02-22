# -*-  coding:utf-8 -*-
import time
from PIL import Image, ImageDraw, ImageFont

from waveshare_epd import epd1in54_V2


def run(player) -> None:
	try:
		epd = epd1in54_V2.EPD()
		epd.init(0)
		epd.Clear(0xFF)

		epd.init(1)
		image = Image.new('1', (epd.height, epd.width), 255)
		draw = ImageDraw.Draw(image)
		font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 24)

		curr_station_id = 0
		radio_name_pos = 0
		radio_name_pos_bis = 0

		while True:
			draw.rectangle((0, 0, epd.height, epd.width), fill=255)

			if player.get_curr_station().id != curr_station_id:
				curr_station_id = player.get_curr_station().id 
				radio_name_pos = 0

			logo = Image.open(f'images/radio_{curr_station_id}.bmp')
			
			if curr_station_id:
				image.paste(logo, (50, 0))
	
				draw.text((radio_name_pos, 110), player.get_curr_station().name, font=font, fill=0)
	
				radio_name_width = font.getsize(player.get_curr_station().name)[0]
				
				if radio_name_width > 200:
					if radio_name_pos + int(radio_name_width * 1.5) > 0:
						radio_name_pos -= 10
						radio_name_pos_bis = radio_name_pos + int(radio_name_width * 1.5)
					else:
						radio_name_pos = 0
						radio_name_pos_bis = 0
					
					draw.text((radio_name_pos_bis, 110), player.get_curr_station().name, font=font, fill=0)
			else:
				image.paste(logo, (25, 0))
	
			current_time = time.strftime('%H:%M:%S')
			draw.text((40, 150), current_time, font=font, fill=0)

			epd.displayPart(epd.getbuffer(image))
			time.sleep(0.5)

	except IOError as e:
		print(e)

if __name__ == '__main__':
    run()


