# -*-  coding:utf-8 -*-
import time
from PIL import Image, ImageDraw, ImageFont

from waveshare_epd import epd1in54_V2

import weather

def get_weather() -> str:
	return f'{weather.get_current_weather_full_deccription()}{weather.get_daily_forecast()}'

def run(player) -> None:
	try:
		epd = epd1in54_V2.EPD()
		epd.init(0)
		epd.Clear(0xFF)

		epd.init(1)
		image = Image.new('1', (epd.height, epd.width), 255)
		draw = ImageDraw.Draw(image)
		font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 24)
		font_weather = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 16)
		current_weather = get_weather()

		curr_station_id = 0
		radio_name_pos = 0
		radio_name_pos_bis = 0
		weather_pos = 0
		weather_pos_bis = font_weather.getsize(current_weather)[0]

		while True:
			draw.rectangle((0, 0, epd.height, epd.width), fill=255)

			# Draw radio station's logo
			if player.get_curr_station().id != curr_station_id:
				curr_station_id = player.get_curr_station().id
				radio_name_pos = 0

			logo = Image.open(f'images/radio_{curr_station_id}.bmp')

			# Write radio station's name
			if curr_station_id:
				image.paste(logo, (50, 0))

				draw.text((radio_name_pos, 110), player.get_curr_station().name, font=font, fill=0)

				radio_name_width = font.getsize(player.get_curr_station().name)[0]

				if radio_name_width > 200:
					radio_name_pos -= 10
					radio_name_pos_bis = radio_name_pos + radio_name_width + 100

					if radio_name_pos_bis <= 0:
						radio_name_pos = 0
						radio_name_pos_bis = 0

					draw.text((radio_name_pos_bis, 110), player.get_curr_station().name, font=font, fill=0)
			else:
				image.paste(logo, (25, 0))

			# Write time
			draw.text((40, 150), time.strftime('%H:%M:%S'), font=font, fill=0)

			# Write weather
			if int(time.strftime('%M')) % 15 == 0:
				current_weather = get_weather()

			draw.text((weather_pos, 180), current_weather, font=font_weather, fill=0)
			draw.text((weather_pos_bis, 180), current_weather, font=font_weather, fill=0)

			weather_pos -= 50
			weather_pos_bis -= 50

			if weather_pos_bis <= 0:
				weather_pos = 0
				weather_pos_bis = font_weather.getsize(current_weather)[0]

			# Display iamge
			epd.displayPart(epd.getbuffer(image))
			time.sleep(0.9)

	except IOError as e:
		print(e)
