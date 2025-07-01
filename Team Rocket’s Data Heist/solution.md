# Team Rocket’s Secret QR Code Transmission — Direct Writeup

## Overview

- You receive a CSV file named `rocket_pokedex.csv` containing a grid of 0s and 1s.
- Interpret each `0` as a black pixel and each `1` as a white pixel to reconstruct an image.
- The resulting image is a QR code.

## Steps to Solve

1. Convert the CSV data into a black-and-white image.
2. Scan the QR code using any QR code reader.
3. The QR code reveals multiple lines of text, including a URL:  https://hacktest-taupe.vercel.app/
4. The text indicates the flag is **not** the URL itself.
5. Visit the URL and inspect the HTML source code.
6. Find a hidden HTML comment containing the real flag:  hackemon{QR_PIKACHU}


