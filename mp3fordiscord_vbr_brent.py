#!/usr/bin/env python3
import os
import sys
#lamefullpath = "E:\\lame\\lame.exe"
lamefullpath = "lame"
maxsize = 8388608
#MachineEpsilon = 2.220446049250313e-16
delta = 1.0e-15
fni = sys.argv[1]
insize = os.stat(fni).st_size
print('Size of input file', insize)
if insize <= maxsize:
    print('No need to recompress')
    sys.exit()
retval = os.spawnl(os.P_WAIT, lamefullpath, lamefullpath, '--mp3input', '-V', '9.999', '"' + fni + '"', '"' + fni + '_9.999.mp3"')
if retval != 0:
    sys.exit(retval)
outsize = os.stat(fni + '_9.999.mp3').st_size
print(outsize)
if outsize > maxsize:
    print('Impossible to fit using VBR')
    sys.exit()
if outsize == maxsize:
    print('Done1')
    sys.exit()
b = 9.999
fb = maxsize - outsize
retval = os.spawnl(os.P_WAIT, lamefullpath, lamefullpath, '--mp3input', '-V', '0', '"' + fni + '"', '"' + fni + '_0.mp3"')
if retval != 0:
    sys.exit(retval)
outsize = os.stat(fni + '_0.mp3').st_size
print(outsize)
if outsize <= maxsize:
    print('Done2')
    os.remove(fni + '_9.999.mp3')
    sys.exit()
a = 0
fa = maxsize - outsize
if abs(fa) < abs(fb):
    a, b, fa, fb = b, a, fb, fa
c = a
fc = fa
mflag = True
while (fb != 0) and (abs(a-b) > delta):
    print('a=',a,'b=',b)
    if (fa != fc) and (fb != fc):
        s = a*fb*fc/((fa-fb)*(fa-fc)) + b*fa*fc/((fb-fa)*(fb-fc)) + c*fa*fb/((fc-fa)*(fc-fb))
    else:
        s = b - fb*(b-a)/(fb-fa)
    tmp2 = (3*a + b)/4
    if ((not(((s > tmp2) and (s < b)) or ((s < tmp2) and (s > b)))) or (mflag and (abs(s - b) >= (abs(b - c) / 2))) or (not mflag and (abs(s - b) >= (abs(c - d) / 2)))):
        s = (a + b) / 2
        mflag = True
    elif (mflag and (abs(b - c) < delta)) or (not mflag and (abs(c - d) < delta)):
        s = (a + b) / 2
        mflag = True
    else:
        mflag = 0
    retval = os.spawnl(os.P_WAIT, lamefullpath, lamefullpath, '--mp3input', '-V', str(s), '"' + fni + '"', '"' + fni + '_' + str(s) + '.mp3"')
    if retval != 0:
        sys.exit(retval)
    outsize = os.stat(fni + '_' + str(s) + '.mp3').st_size
    print(outsize)
    fs = maxsize - outsize
    d = c
    c = b
    fc = fb
    if fs == 0:
        os.remove(fni + '_' + str(a) + '.mp3')
        os.remove(fni + '_' + str(b) + '.mp3')
        print('Done3')
        sys.exit()
    if fa * fs < 0:
        os.remove(fni + '_' + str(b) + '.mp3')
        b = s
        fb = fs
    else:
        os.remove(fni + '_' + str(a) + '.mp3')
        a = s
        fa = fs
    if abs(fa) < abs(fb):
        a, b, fa, fb = b, a, fb, fa
if fb < 0:
    os.remove(fni + '_' + str(b) + '.mp3')
else:
    os.remove(fni + '_' + str(a) + '.mp3')
print('Done4')
