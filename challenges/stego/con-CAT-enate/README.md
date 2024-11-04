# Prompt

I recently got a new cat named Pearl.

This is a picture of her.

Nothing suspicious about a precious kitten, is there?

# Solution

I have concatenated another image file to the end of the image. Using binwalk to see the offset and dd to create the file works as follows:

```
[root@grasshopper][~/workbench/CC-CTF/challenges/stego/con-CAT-enate]
>> binwalk keht.jpg

DECIMAL       HEXADECIMAL     DESCRIPTION
--------------------------------------------------------------------------------
0             0x0             JPEG image data, JFIF standard 1.01
30            0x1E            TIFF image data, little-endian offset of first image directory: 8
955140        0xE9304         PNG image, 908 x 738, 8-bit/color RGBA, non-interlaced
955204        0xE9344         Zlib compressed data, best compression
958431        0xE9FDF         Zlib compressed data, default compression

[root@grasshopper][~/workbench/CC-CTF/challenges/stego/con-CAT-enate]
>> dd if=./keht.jpg of=./answer.png skip=955140 bs=1
21044+0 records in
21044+0 records out
21044 bytes (21 kB, 21 KiB) copied, 0.011088 s, 1.9 MB/s

[root@grasshopper][~/workbench/CC-CTF/challenges/stego/con-CAT-enate]
>> file answer.png
answer.png: PNG image data, 908 x 738, 8-bit/color RGBA, non-interlaced
```

The PNG file is an image of the flag: `cc_ctf{pearl_is_adorable}`
