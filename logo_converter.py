from PIL import Image


def convert_to_bw(image_path):
    image = Image.open(image_path)
    bw_image = image.convert('L')
    bw_image = bw_image.point(lambda x: 0 if x < 75 else 255, '1')
    return bw_image


if __name__ == "__main__":
    input_image_path = "Radio_0.jpg"
    output_image_path = "Radio_0.bmp"
    bw_image = convert_to_bw(input_image_path)
    bw_image.save(output_image_path)
