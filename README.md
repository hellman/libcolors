Python libraries
====================

libcolors.py
---------------------

This module allows to use bash colors.
Example:

<img src="http://dl.dropbox.com/u/8748250/libcolors_screen.png">

<pre>
from libcolors import color
s1 = color("red", "black", "bold underline")
s2 = color()  # Restore default color
print s1 + "Red on black, bold and underlined" + s2
</pre>

Author: hellman ( hellman1908@gmail.com )

License: GNU General Public License v2 (http://opensource.org/licenses/gpl-2.0.php)

libhttp.py
---------------------

Quick http requests with only one call:

<pre>
from libhttp import req
print req("http://www.something.com").data
print req("http://www.google.com").headers

req("http://www.example.com",
    headers=headers     # dict or list of strings
    cookie=cookie       # dict or str like "a=b&c=d"
    data=post_data      # dict or str like "a=b&c=d"
    get=get_data        # dict or str like "a=b&c=d"
    auth=(user, pass)   # tuple (HTTP Basic Auth)
    proxy="host:port"   # both for http and https
    proxy_auth=(u, p)   # tuple for proxy auth
    timeout=10          # 10 seconds
)
</pre>

libnum.py
---------------------

Python library for some numbers functions:

*  working with primes (generating, primality tests)
*  common maths (gcd, lcm, n'th root)
*  modular arithmetics (inverse, Jacobi symbol, square root, solve CRT)
*  converting strings to numbers or binary strings
