import glob
import os
import sys
from PIL import Image
from functools import reduce

'''Windows is not care if a word is lower() or upper(),so if there have 'JPG' and 'jpg' together,
   we will found that one image was processed twice.'''
EXTS = 'jpeg', 'jpg', 'JPEG', 'gif', 'GIF', 'PNG'


def avhash(im):
    if not isinstance(im, Image.Image):
        im = Image.open(im)
    im = im.resize((8, 8), Image.ANTIALIAS).convert('L')
    avg = reduce(lambda x, y: x + y, im.getdata()) / 64.
    # make 64 compared-values to a 16bit Hexadecimal number that also named  hash-values or image-fingerprint
    return reduce(lambda x, y_z: x | (y_z[1] << y_z[0]), \
                  enumerate(map(lambda i: 0 if i < avg else 1, im.getdata())), 0)  # reduce()'s initial parameter is 0


def hamming(h1, h2):
    h, d = 0, h1 ^ h2
    while d:
        h += 1
        d &= d - 1
    return h


if __name__ == '__main__':
    if len(sys.argv) <= 1 or len(sys.argv) > 3:
        print("Usage: %s " % sys.argv[0])
    else:
        im, wd = sys.argv[1], '.' if len(sys.argv) < 3 else sys.argv[2]
        h = avhash(im)
        # print hash-values or image-fingerprint
        print(h)
        # change the current working-path
        os.chdir(wd)

        images = []
        for ext in EXTS:
            images.extend(glob.glob(r'*.%s' % ext))

        seq = []
        print(len(images))
        # int(true) = 1 and int(false) = 0
        prog = int(len(images) > 50 and sys.stdout.isatty())
        print(prog)
        for f in images:
            seq.append((f, hamming(avhash(f), h)))
            if prog:
                perc = 100 * prog / len(images)
                x = int(2 * perc / 5)
                print('\rCalculating... [' + '#' * x + ' ' * (40 - x) + ']', )
                print('%.2f%%' % perc, '(%d/%d)' % (prog, len(images)), )
                sys.stdout.flush()
                prog += 1

        for f, ham in sorted(seq, key=lambda i: i[1]):
            print("%d\t%s" % (ham, f))

        os.system("pause")
