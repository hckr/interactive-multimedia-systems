from PIL import Image
import numpy as np
from glob import glob


def main():
    for path in glob('images/*'):
        if not is_image(path):
            continue
        image = Image.open(path).convert('L')
        image_array = np.array(image)
        image_rle_compressed = compressRLE(image_array)
        assert np.array_equal(image_array, decompressRLE(image_rle_compressed))
        print(f'Image: {path}')
        print(f'Original size: {image_array.size}')
        print(f'RLE size: {image_rle_compressed.size}')
        print(f'RLE compression ratio: {image_rle_compressed.size / image_array.size}')
        print()


def is_image(path):
    return any(path.endswith(ext) for ext in ('.png', '.jpg'))


def compressRLE(array):
    _, width = array.shape
    array = array.flatten()
    result = [width]
    if (len(array) == 0):
        return result
    prev = array[0]
    count = 1
    for p in array[1:]:
        if prev != p:
            result.append(count)
            result.append(prev)
            prev = p
            count = 1
        else:
            count += 1
    else:
        result.append(count)
        result.append(prev)
    return np.array(result)


def decompressRLE(compressed_data):
    result = []
    width, *data = compressed_data
    it = iter(data)
    for (count, p) in zip(it, it):
        for _ in range(count):
            result.append(p)
    return np.array(result).reshape(-1, width)


def compressQuad(img):
    pass


def decompressQuad(img):
    pass


if __name__ == "__main__":
    main()
