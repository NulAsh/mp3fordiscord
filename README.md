# mp3fordiscord
Recompress mp3's to fit in 8MB Discord restriction

First program was mp3fordiscord.py. To use it you must have lame installed.

If you are on Windows, edit lamefullpath variable inside program, it should point at lame.exe.
Lame binaries for Windows can be downloaded from here http://www.rarewares.org/mp3-lame-bundle.php

This first version of program picks up INTERGER quality settings for VBR. But later I found out that this number is actually REAL.
So, here's new program, mp3fordiscord_vbr_brent.py. This program works much longer, but gives better results, getting closer to 8MB. If this long work does not suit you, you can use the first program.

Sometimes there is also a rare situation where this program simply cannot compress the big file hard enough, even with the strongest option -V 9.999

For such cases there is mp3fordiscord_abr_brent.py
