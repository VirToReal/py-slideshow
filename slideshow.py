#!/usr/bin/env python
#
#  Copyright (c) 2015, Jamin W. Collins <jamin.collins@gmail.com>
#  Dev: https://github.com/jamincollins/py-slideshow
#
#  Based on work done by Corey Goldberg
#  Copyright (c) 2013, 2015, Corey Goldberg
#
#  Dev: https://github.com/cgoldberg/py-slideshow
#  License: GPLv3


import argparse
import os
import queue
import random
import select
import subprocess
import sys
import threading
import time

import inotify  # https://github.com/jamincollins/python-inotify
import pyglet

from inotify import watcher


def update_pan_zoom_speeds():
    global _pan_speed_x
    global _pan_speed_y
    global _zoom_speed
    _pan_speed_x = random.randint(-8, 8)
    _pan_speed_y = random.randint(-8, 8)
    _zoom_speed = random.uniform(-0.02, 0.02)
    return _pan_speed_x, _pan_speed_y, _zoom_speed


def update_pan(dt):
    sprite.x += dt * _pan_speed_x
    sprite.y += dt * _pan_speed_y
    window.clear()


def update_zoom(dt):
    sprite.scale += dt * _zoom_speed
    window.clear()


def generate_timepos(img_time):
    timemax = max(image_paths, key=lambda x:x[1])
    timemin = min(image_paths, key=lambda x:x[1])
    timediff = timemax[1] - timemin[1]
    return int(((window.height-20)*(img_time-timemax[1]))/timediff)*(-1)


def generate_timeray():
    imgF = pyglet.image.load('Timepoint_Inactive.png')
    timesprites = []
    imagecount = len(image_paths)

    for i in range (0, imagecount):
        timesprites.append(pyglet.sprite.Sprite(imgF))
        timesprites[i].x = 5 # Position of Timeline in Picutre from left
        timesprites[i].y = generate_timepos(image_paths[i][1])
    return timesprites


def update_image(dt):
    if not new_pics.empty():
        # if there are images in queue, load the next, and add to known
        filename = new_pics.get()
        filetime = int(os.path.getmtime(filename))
        image_paths.append((filename, filetime))
    elif not image_paths:
        return
    else:
        # otherwise load a existing image
        global image_number
        global images
        #if images > 0:
            #print ("ArgsInsert: " + str(args.insert[0]) + " ImageCount: " + str(images) + " Moduloresult: " + str(images % int(args.insert[0])) + " Total Images: " + str(len(image_paths)) + " Active Image: " + str(image_number) + " Total Insert Images: " + str(len(image_paths2)) + " Activated Insert Image: " + str(image_number2))
        if args.insert and images > 0 and images % int(args.insert[0]) == 0: # select a picture from 'insert' folder each 'n' pictures
            global image_number2
            image_number2 += 1
            images += 1
            image_count2 = len(image_paths2)
            if image_number2 == image_count2:
                image_number2 = 0
            filename = image_paths2[image_number2][0]
        else:
            images += 1
            if args.random: # turn random picture-chooser on/off
                ramdomchoice = random.choice(image_paths)
                filename = ramdomchoice[0]
                filetime = ramdomchoice[1]
            else:
                image_number += 1 # count up the selected image image_number
                image_count = len(image_paths) # count number of avilable images
                if image_number == image_count: # image_number reached its end
                    image_number = 0 # reset image_number
                selectimage = image_paths[image_number]
                filename = selectimage[0]
                filetime = selectimage[1]
    try:
        window.clear()
        img = pyglet.image.load(filename)
        sprite.image = img
        sprite.scale = get_scale(window, img)
        sprite.x = 0
        sprite.y = 0
        update_pan_zoom_speeds()

        if args.timeray and not args.insert: # draw active Point for Timeline
            activetimesprite.x = 5 # Position of Timeline in Picutre from left
            activetimesprite.y = generate_timepos(filetime)

        filenameext = os.path.split(filename)
        filenamevar = os.path.splitext(filenameext[1])
        filenamevar = filenamevar[0].replace('_', ' ')
        if not args.insert:
            filetime = time.localtime(filetime)
            label.text = "<font color='#ffffff' size='5'>%s </font> <font color='#C0C0C0' size='3'> %s.%s.%s %s:%s:%s</font> " % (str(filenamevar), str(filetime[2]),str(filetime[1]), str(filetime[0]), str(filetime[3]), str(filetime[4]), str(filetime[5]))

        window.clear()

    except FileNotFoundError:
        # remove image from the list
        image_paths[0].remove(filename)


def get_image_paths(input_dir='.'):
    paths = []
    while not paths:
        for root, dirs, files in os.walk(input_dir, topdown=True):
            for filename in sorted(files):
                if filename.endswith(('jpg', 'png', 'gif')):
                    path = os.path.abspath(os.path.join(root, filename))
                    filetime = int(os.path.getmtime(path))
                    paths.append((path, filetime))
        time.sleep(.5)
    return paths


def get_scale(window, image):
    if image.width > image.height:
        scale = float(window.width) / image.width
    else:
        scale = float(window.height) / image.height
    return scale


def watch_for_new_images(input_dir):
    w = watcher.AutoWatcher()
    try:
        # Watch all paths recursively, and all events on them.
        w.add_all(input_dir, inotify.IN_ALL_EVENTS)
    except OSError as err:
        print ('%s: %s' % (err.filename, err.strerror), file=sys.stderr)

    poll = select.poll()
    poll.register(w, select.POLLIN)

    timeout = None

    threshold = watcher.Threshold(w, 512)

    while (not threadwhile.is_set()):
        events = poll.poll(timeout)
        nread = 0
        if threshold() or not events:
            print('reading,', threshold.readable(), 'bytes available')
            for evt in w.read(0):
                nread += 1

                events = inotify.decode_mask(evt.mask)
                if 'IN_MOVED_TO' in events:
                    filename = evt.fullpath
                    if filename.endswith(('jpg', 'png', 'gif')):
                        print("adding %s to the queue" % filename)
                        new_pics.put(filename)

        if nread:
            timeout = None
            poll.register(w, select.POLLIN)
        else:
            timeout = 1000
            poll.unregister(w)


def shove_mouse(dt):
    get_vertical = "xdotool getdisplaygeometry | awk '{print $2}'"
    cmd = "xdotool mousemove 0 $({0})".format(get_vertical)
    subprocess.call(cmd, shell=True)


def main():
    global sprite
    global image_paths
    global image_paths2
    global window
    global label
    global new_pics
    global threadwhile
    global args
    global activetimesprite

    new_pics = queue.Queue()
    activetimesprite = None
    _pan_speed_x, _pan_speed_y, _zoom_speed = update_pan_zoom_speeds()

    parser = argparse.ArgumentParser()
    parser.add_argument('dir', help='directory of images', nargs='?', default=os.getcwd())
    parser.add_argument('-w', '--wait', help='time between each picture', type=float, dest='wait_time', default=3.0)
    parser.add_argument('-r', '--random', help='random picture select', dest='random', action='store_true', default=False)
    parser.add_argument('-i', '--insert', help='add every <INSERT> pictures a picture from <INSERT> directory, example: -i 5 /home/user/pictures/', nargs=2)
    parser.add_argument('-e', '--effects', help='activate pan/zoom effects in slideshow', dest='effects', action='store_true', default=False)
    parser.add_argument('-t', '--timeray', help='show timeray', dest='timeray', action='store_true', default=False)
    args = parser.parse_args()

    if args.insert:
        image_paths2 = get_image_paths(args.insert[1])

    image_paths = get_image_paths(args.dir)
    threadwhile = threading.Event()
    thread = threading.Thread(target=watch_for_new_images, args=(args.dir,))
    thread.start()

    window = pyglet.window.Window(fullscreen=True)
    label = pyglet.text.HTMLLabel('', x=window.width//2, y=30, anchor_x='center', anchor_y='center')

    if args.random:
        rndch = random.choice(image_paths)
        img = pyglet.image.load(rndch[0])
        time = rndch[1]
    else:
        slch = image_paths[image_number]
        img = pyglet.image.load(slch[0])
        time = slch[1]

    if args.timeray:
        timesprites = generate_timeray()
        imgT = pyglet.image.load('Timepoint_Active.png')
        activetimesprite = pyglet.sprite.Sprite(imgT)
        activetimesprite.x = 5 # Position of Timeline in Picutre from left
        activetimesprite.y = generate_timepos(time)

    @window.event
    def on_draw():
        sprite.draw()
        label.draw()
        if args.timeray: # draw Points for Timeline
            pyglet.gl.glLineWidth(3)
            pyglet.graphics.draw(2, pyglet.gl.GL_LINES, ("v2f", (15, 10, 15, window.height-10)), ('c3B', (0, 0, 255, 0, 255, 0)))
            for timesprite in timesprites:
                timesprite.draw()
            activetimesprite.draw()

    @window.event
    def on_close():
        print ("closing application...")
        threadwhile.set() #stops 'watcher'-thread

    window.clear()
    sprite = pyglet.sprite.Sprite(img)
    sprite.scale = get_scale(window, img)

    pyglet.clock.schedule_interval(update_image, args.wait_time)
    #pyglet.clock.schedule_interval(shove_mouse, 6.0)

    if args.effects:
        pyglet.clock.schedule_interval(update_pan, 1/60.0)
        pyglet.clock.schedule_interval(update_zoom, 1/60.0)

    pyglet.app.run()


if __name__ == '__main__':
    image_number = 0
    image_number2 = 0
    images = 0
    main()
