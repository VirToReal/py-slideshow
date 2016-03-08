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


def update_zoom(dt):
    sprite.scale += dt * _zoom_speed


def update_image(dt):
    if not new_pics.empty():
        # if there are images in queue, load the next, and add to known
        filename = new_pics.get()
        image_paths.append(filename)
    elif not image_paths:
        return
    else:
        # otherwise load a random existing image
        filename = random.choice(image_paths)
    try:
        img = pyglet.image.load(filename)
        sprite.image = img
        sprite.scale = get_scale(window, img)
        sprite.x = 0
        sprite.y = 0
        update_pan_zoom_speeds()
        window.clear()
    except FileNotFoundError:
        # remove image from the list
        image_paths.remove(filename)


def get_image_paths(input_dir='.'):
    paths = []
    while not paths:
        for root, dirs, files in os.walk(input_dir, topdown=True):
            for filename in sorted(files):
                if filename.endswith(('jpg', 'png', 'gif')):
                    path = os.path.abspath(os.path.join(root, filename))
                    paths.append(path)
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
        print('%s: %s' % (err.filename, err.strerror), file=sys.stderr)

    poll = select.poll()
    poll.register(w, select.POLLIN)

    timeout = None

    threshold = watcher.Threshold(w, 512)

    while True:
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


def main():
    global sprite
    global image_paths
    global window
    global new_pics

    new_pics = queue.Queue()

    _pan_speed_x, _pan_speed_y, _zoom_speed = update_pan_zoom_speeds()

    parser = argparse.ArgumentParser()
    parser.add_argument('dir', help='directory of images',
                        nargs='?', default=os.getcwd())
    args = parser.parse_args()

    image_paths = get_image_paths(args.dir)
    thread = threading.Thread(target=watch_for_new_images, args=(args.dir,))
    thread.start()

    window = pyglet.window.Window(fullscreen=True)

    @window.event
    def on_draw():
        sprite.draw()

    img = pyglet.image.load(random.choice(image_paths))
    sprite = pyglet.sprite.Sprite(img)
    sprite.scale = get_scale(window, img)

    pyglet.clock.schedule_interval(update_image, 6.0)
    # pyglet.clock.schedule_interval(update_pan, 1/60.0)
    # pyglet.clock.schedule_interval(update_zoom, 1/60.0)

    pyglet.app.run()


if __name__ == '__main__':
    main()
