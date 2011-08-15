libcolors.py
====================

This small script allows to use bash colors.

<img src="http://dl.dropbox.com/u/8748250/libcolors_screen.png">

Usage
---------------------

<pre>
from libcolors import color
s1 = color("red", "black", "bold underline")
s2 = color()  # Restore default color
print s1 + "Red on black, bold and underlined" + s2
</pre>

<b>Available colors and background colors:</b>

black, white, red, green, blue, yellow, purple, cyan

<b>Available colors and background colors:</b>

regular, bold (light), underline, strike, dark, invert

About
---------------------

Author: hellman ( hellman1908@gmail.com )

License: GNU General Public License v2 (http://opensource.org/licenses/gpl-2.0.php)
