__author__ = 'averrin'

import sys
import Image

infile=['tilesets/origin/mchip0.bmp','tilesets/origin/mchip1.bmp','tilesets/origin/mchip2.bmp','tilesets/origin/mchip3.bmp',]
for i,fname in enumerate(infile):
    try:
        im = Image.open(fname)
        xsize,ysize=im.size
        for row in xrange(31):
            for col in xrange(7):
                box = ((xsize/8)*col ,(ysize/32)*row, (xsize/8)*(col+1), (ysize/32)*(row+1))
                region = im.crop(box)
                region.save('tilesets/cutted/%d/%d_%d.png' % (i,col,row), "png")
    except Exception,e:
        print e
try:
    im = Image.open('tilesets/chara_a.png')
    xsize,ysize=im.size
    for row in xrange(31):
        for col in xrange(15):
            box = ((xsize/32)*col ,(ysize/16)*row, (xsize/32)*(col+1), (ysize/16)*(row+1))
            region = im.crop(box)
            region.save('tilesets/cutted/char/%d_%d.png' % (col,row), "png")
except Exception,e:
    print e