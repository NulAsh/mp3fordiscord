#!/usr/bin/env python3
import os
import sys
#lamefullpath = "E:\\lame\\lame.exe"
lamefullpath = "lame"
maxsize = 8388608
fni = sys.argv[1]
insize = os.stat(fni).st_size
print('Size of input file', insize)
if insize <= maxsize:
    print('No need to recompress')
    sys.exit()
retval = os.spawnl(os.P_WAIT, lamefullpath, lamefullpath, '--mp3input', '-V', '9', '"' + fni + '"', '"' + fni + '_9.mp3"')
if retval != 0:
    sys.exit(retval)
outsize = os.stat(fni + '_9.mp3').st_size
if outsize > maxsize:
    print('Impossible to fit using VBR')
    sys.exit()
if outsize == maxsize:
    print('Done')
    sys.exit()
b = 9
b_ = outsize
retval = os.spawnl(os.P_WAIT, lamefullpath, lamefullpath, '--mp3input', '-V', '0', '"' + fni + '"', '"' + fni + '_0.mp3"')
if retval != 0:
    sys.exit(retval)
outsize = os.stat(fni + '_0.mp3').st_size
if outsize <= maxsize:
    print('Done')
    os.remove(fni + '_9.mp3')
    sys.exit()
a = 0
a_ = outsize
#now: b_ < maxsize < a_
while b != a + 1:
    print('a=',a,'b=',b)
    v = round((a*(maxsize - b_) - b*(maxsize-a_))/(a_ - b_))
    if v == a:
        v += 1
    if v == b:
        v -= 1
    retval = os.spawnl(os.P_WAIT, lamefullpath, lamefullpath, '--mp3input', '-V', str(v), '"' + fni + '"', '"' + fni + '_' + str(v) + '.mp3"')
    if retval != 0:
        sys.exit(retval)
    outsize = os.stat(fni + '_' + str(v) + '.mp3').st_size
    if outsize == maxsize:
        os.remove(fni + '_' + str(a) + '.mp3')
        os.remove(fni + '_' + str(b) + '.mp3')
        print('Done')
        sys.exit()
    if outsize < maxsize:
        os.remove(fni + '_' + str(b) + '.mp3')
        b = v
        b_ = outsize
    else:
        os.remove(fni + '_' + str(a) + '.mp3')
        a = v
        a_ = outsize
os.remove(fni + '_' + str(a) + '.mp3')
a = v
a_ = outsize
print('Done')
