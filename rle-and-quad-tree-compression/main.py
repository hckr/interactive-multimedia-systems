from PIL import Image
import numpy as np
from glob import glob


def main():
    for path in glob('images/*'):
        if not is_image(path):
            continue
        image = Image.open(path).convert('L')
        image_array, _ = image_to_array(image)
        image_rle_compressed = compressRLE(image_array)
        print(f'Image: {path}')
        print(f'Original size: {len(image_array)}')
        print(f'RLE size: {len(image_rle_compressed)}')
        print(f'RLE decompression equal: {np.array_equal(image_array, decompressRLE(image_rle_compressed))}')
        print(f'RLE compression ratio: {len(image_rle_compressed)/len(image_array)}')


def is_image(path):
    return any(path.endswith(ext) for ext in ('.png', '.jpg'))

def image_to_array(img):
    arr = np.array(img)
    _, width = arr.shape
    return arr.flatten(), width


def image_from_array(np_array, width):
    return Image.fromarray(np_array.reshape(-1, width))


def compressRLE(array):
    result = []
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
    return result


def decompressRLE(compressed_data):
    result = []
    it = iter(compressed_data)
    for (count, p) in zip(it, it):
        for _ in range(count):
            result.append(p)
    return result


def compressQuad(img):
    pass


def decompressQuad(img):
    pass


if __name__ == "__main__":
    main()
