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
   usage: slideshow.py [-h] [-c CHECK_TIME] [-a AGE_OF_FILE] [-w WAIT_TIME] [-r]
                    [-i INSERT INSERT] [-e] [-x] [-t] [-p] [-g]
                    [dir]

    positional arguments:
      dir                   directory of images

    optional arguments:
      -h, --help            show this help message and exit
      -c CHECK_TIME, --checktime CHECK_TIME
                            check every <ms> for new pictures
      -a AGE_OF_FILE, --ageoffile AGE_OF_FILE
                            new pictures have to be at least <ms> old after been
                            created. Depending on your system, pictures will take
                            some time until completly copied/moved
      -w WAIT_TIME, --wait WAIT_TIME
                            time between each picture
      -r, --random          random picture select
      -i INSERT INSERT, --insert INSERT INSERT
                            add every <INSERT> pictures a picture from <INSERT>
                            directory, example: -i 5 /home/user/pictures/
      -e, --effects         activate pan/zoom effects in slideshow
      -x, --eXpand          resize to fit the screen
      -t, --timeray         show timeray
      -p, --picinfo         show filename and date in slideshow
      -g, --raspgpio        reads the GPIO of a raspberry on startup, and executes
                            commands depending on the set of pins. Pin 3 = Random,
                            Pin 5 = Effects, Pin 7 = Expand, Pin 11 = Timeray, Pin
                            12 = Picinfo, Pin 13 = 1. Digit of Time in Binary-
                            Format, Pin 14 = 2. Digit of Time in Binary-Format,
                            Pin 15 = 3. Digit of Time in Binary-Format, Pin 16 =
                            4. Digit of time in Binary-Format

**Example**::

    $ git clone https://github.com/jamincollins/py-slideshow.git
    $ cd py-slideshow
    $ python slideshow.py images/
