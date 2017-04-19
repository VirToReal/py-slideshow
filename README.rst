==============================
py-slideshow - image slideshow
==============================

Random image slideshow in Python with OpenGL pan/zoom effects and a timeray.

.. image:: icon.png

*  Copyright (c) 2015, Jamin W. Collins <jamin.collins@gmail.com>
*  Copyright (c) 2017, Benjamin Hirmer
*  Dev: https://github.com/jamincollins/py-slideshow
*
*  Based on work done by Corey Goldberg
*  Copyright (c) 2013, 2015, Corey Goldberg
*
*  Dev: https://github.com/cgoldberg/py-slideshow
*  License: GPLv3

----

**Requirements**:

* Python 2.7+ or 3.2+
* pyglet

**Command Line Help**::

    $ ./slideshow.py -h
    usage: slideshow.py [-h] [-w WAIT_TIME] [-e] [-t] [dir]

    positional arguments:
      dir                   directory of images

    optional arguments:
     -h, --help            show this help message and exit
     -w WAIT_TIME, --wait WAIT_TIME
                          time between each picture
     -e, --effects         activate pan/zoom effects in slideshow
     -t, --timeray         show timeray


**Example**::

    $ git clone https://github.com/jamincollins/py-slideshow.git
    $ cd py-slideshow
    $ python slideshow.py images/
