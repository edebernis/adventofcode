#!/usr/bin/python3

from collections import deque


class Image:
    def __init__(self, pixels, width, height):
        self.width = width
        self.height = height
        self.layers = None

        self._load_layers(pixels)

    def _load_layers(self, pixels):
        self.layers = []
        while pixels:
            layer_pixels = pixels[:(self.width * self.height)]
            pixels = pixels[(self.width * self.height):]

            layer = Layer(deque(layer_pixels), self.width, self.height)
            self.layers.append(layer)

    def _combine_pixel(self, pixels):
        for pixel in pixels:
            if pixel == 0:
                return 0
            if pixel == 1:
                return 1
        return 2

    def decode(self):
        for y in range(self.height):
            for x in range(self.width):
                print(' {0} '.format(self._combine_pixel([l.pixels[y][x]
                                     for l in self.layers])), end='')
            print('')


class Layer:
    def __init__(self, pixels, width, height):
        self.width = width
        self.height = height
        self.pixels = None

        self._load_pixels(pixels)

    def _load_pixels(self, pixels):
        self.pixels = [[pixels.popleft() for x in range(self.width)]
                       for y in range(self.height)]

    def count_pixels(self, value):
        count = 0
        for x in range(self.width):
            for y in range(self.height):
                if self.pixels[y][x] == value:
                    count += 1
        return count


def get_layer_with_minimum_zero(image):
    layers = {layer.count_pixels(0): layer for layer in image.layers}
    return layers[min(layers.keys())]


# Part 1 - Test cases
min0_layer = get_layer_with_minimum_zero(
    Image([1, 2, 3, 4, 5, 6, 7, 8, 9, 0, 1, 2], 3, 2))
assert min0_layer.count_pixels(1) * min0_layer.count_pixels(2) == 1

# Part 1 - Main
image = Image(list(map(int, open('input_part1').read().strip())), 25, 6)
min0_layer = get_layer_with_minimum_zero(image)
print('Part 1 answer: {0}'.format(min0_layer.count_pixels(1) *
                                  min0_layer.count_pixels(2)))

# Part 2 - Test cases
Image([0, 2, 2, 2, 1, 1, 2, 2, 2, 2, 1, 2, 0, 0, 0, 0], 2, 2).decode()

# Part 2 - Main
print('Part 2 answer:')
Image(list(map(int, open('input_part1').read().strip())), 25, 6).decode()
