import cv2
import os
import sys
import errno


def generate_jpeg_variants(original_image):
    return [(quality, jpegDecompress(jpegCompress(original_image, quality)))
            for quality in (5, 15, 25, 35, 45, 55, 65, 75, 85, 95)]


def jpegCompress(img, quality):
    encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), quality]
    _, encimg = cv2.imencode('.jpg', img, encode_param)
    return encimg


def jpegDecompress(encimg):
    return cv2.imdecode(encimg, -1)


def save_variants(original_image, dir):
    for quality, image in generate_jpeg_variants(original_image):
        cv2.imwrite(os.path.join(dir, f'{quality}.jpg'), image)


def main():
    original_image = cv2.imread(os.path.join(
        sys.path[0], 'image-grayscale.png'), cv2.IMREAD_UNCHANGED)
    try:
        os.makedirs('images')
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise
    save_variants(original_image, 'images')


if __name__ == "__main__":
    main()
