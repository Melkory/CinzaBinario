class ImageProcessor:
    def __init__(self, image_path):
        self.image_path = image_path
        self.image = self.load_image()

    def load_image(self):
        with open(self.image_path, 'rb') as f:
            f.seek(18)
            self.width = int.from_bytes(f.read(4), byteorder='little')
            self.height = int.from_bytes(f.read(4), byteorder='little')
            f.seek(10)
            self.data_offset = int.from_bytes(f.read(4), byteorder='little')
            f.seek(self.data_offset)
            image = []
            for _ in range(self.height):
                row = []
                for _ in range(self.width):
                    blue = int.from_bytes(f.read(1), byteorder='little')
                    green = int.from_bytes(f.read(1), byteorder='little')
                    red = int.from_bytes(f.read(1), byteorder='little')
                    row.append((red, green, blue))
                image.append(row)
            return image

    def convert_to_grayscale(self):
        grayscale_image = []
        for row in self.image:
            grayscale_row = []
            for (r, g, b) in row:
                gray = int((0.299 * r) + (0.587 * g) + (0.114 * b))
                grayscale_row.append(gray)
            grayscale_image.append(grayscale_row)
        return grayscale_image

    def binarize_image(self, grayscale_image, threshold=128):
        binary_image = []
        for row in grayscale_image:
            binary_row = []
            for gray in row:
                binary_value = 255 if gray > threshold else 0
                binary_row.append(binary_value)
            binary_image.append(binary_row)
        return binary_image

    def save_image(self, image, filename, mode='L'):
        with open(filename, 'wb') as f:
            f.write(b'BM')
            if mode == 'L':
                file_size = 14 + 40 + 1024 + self.width * self.height
            else:
                file_size = 14 + 40 + self.width * self.height * 3
            f.write(file_size.to_bytes(4, byteorder='little'))
            f.write((0).to_bytes(2, byteorder='little'))
            f.write((0).to_bytes(2, byteorder='little'))
            if mode == 'L':
                f.write((54 + 1024).to_bytes(4, byteorder='little'))
            else:
                f.write((54).to_bytes(4, byteorder='little'))

            f.write((40).to_bytes(4, byteorder='little'))
            f.write(self.width.to_bytes(4, byteorder='little'))
            f.write(self.height.to_bytes(4, byteorder='little'))
            f.write((1).to_bytes(2, byteorder='little'))
            if mode == 'L':
                f.write((8).to_bytes(2, byteorder='little'))
            else:
                f.write((24).to_bytes(2, byteorder='little'))
            f.write((0).to_bytes(4, byteorder='little'))
            if mode == 'L':
                f.write((self.width * self.height).to_bytes(4, byteorder='little'))
            else:
                f.write((self.width * self.height * 3).to_bytes(4, byteorder='little'))
            f.write((0).to_bytes(4, byteorder='little'))
            f.write((0).to_bytes(4, byteorder='little'))
            f.write((0).to_bytes(4, byteorder='little'))
            f.write((0).to_bytes(4, byteorder='little'))

            if mode == 'L':
                for i in range(256):
                    f.write((i).to_bytes(1, byteorder='little') * 3 + (0).to_bytes(1, byteorder='little'))

            for row in reversed(image):
                for value in row:
                    if mode == 'L':
                        f.write((value).to_bytes(1, byteorder='little'))
                    else:
                        f.write((value).to_bytes(1, byteorder='little'))

if __name__ == "__main__":
    image_path = "C:\\Users\\usuario\\Desktop\\ImagemBn\\Lenna.bmp"
    processor = ImageProcessor(image_path)

    grayscale_image = processor.convert_to_grayscale()
    processor.save_image(grayscale_image, "C:\\Users\\usuario\\Desktop\\ImagemBn\\grayscale_image.bmp", mode='L')

    binary_image = processor.binarize_image(grayscale_image)
    processor.save_image(binary_image, "C:\\Users\\usuario\\Desktop\\ImagemBn\\binary_image.bmp", mode='L')
