import argparse
import sys

from PIL import Image
from bitstring import BitArray

FILENAME_IN = '33.png'


def init_vars():
    parser = argparse.ArgumentParser()
    parser.add_argument('-fin', nargs='?', default=FILENAME_IN)
    parser.add_argument('-mode', nargs='?', default='set')

    return parser.parse_args(sys.argv[1:])


def get_next_pixel(img):
    for i in range(img.width):
        for j in range(img.height):
            yield i, j


def set_bit(value, bit):
    def set(value_, bit_):
        if bit_ == 1:
            return value_ | (1 << 0)
        else:
            return value_ & (~1)

    if type(value) == type(()):
        value = (set(value[0], bit), *value[1:])
        return value
    return set(value, bit)


def get_bit(value):
    def get(value_):
        return value_ & 1

    if type(value) == type(()):
        return get(value[0])
    return get(value)


def set_msg(args):
    text = """Hello darkness, my old friend
I've come to talk with you again
Because a vision softly creeping
Left its seeds while I was sleeping
And the vision that was planted in my brain
Still remains
Within the sound of silence

In restless dreams I walked alone
Narrow streets of cobblestone
'Neath the halo of a streetlamp
I turned my collar to the cold and damp
When my eyes were stabbed by the flash of a neon light
That split the night
And touched the sound of silence

And in the naked light I saw
Ten thousand people, maybe more
People talking without speaking
People hearing without listening
People writing songs that voices never share
No one dare
Disturb the sound of silence

"Fools" said I, "You do not know
Silence like a cancer grows
Hear my words that I might teach you
Take my arms that I might reach you"
But my words like silent raindrops fell
And echoed in the wells of silence

And the people bowed and prayed
To the neon god they made
And the sign flashed out its warning
In the words that it was forming
And the sign said "The words of the prophets
Are written on the subway walls
And tenement halls
And whispered in the sounds of silence""".encode('utf-8')
    container = args
    print("container: " + container)
    img = Image.open(container)

    text = bytes(text)
    c = BitArray(bytes=text)
    text = str(c.bin)
    next_pxl = get_next_pixel(img)
    for bit in text:
        x, y = next(next_pxl)
        w = set_bit(img.getpixel((x, y)), int(bit))
        img.putpixel((x, y), w)

    img.save('withmsg_' + container)


def get_msg(args):
    container = args
    print("container: " + container)
    img = Image.open(container)

    next_pxl = get_next_pixel(img)
    lbit = ""
    for x, y in next_pxl:
        p = img.getpixel((x, y))
        p = get_bit(p)
        lbit += str(p)
    for i in range(0, len(lbit), 8):
        w = lbit[i: i + 8]
        print(chr(int(w, 2)), end='')


def main():
    # args = init_vars()
    file = '44.png'
    #set_msg(file)
    get_msg(file)


if __name__ == '__main__':
    main()
