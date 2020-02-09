#! /bin/sh

#Configure camera
v4l2-ctl -d 0 -c exposure_auto=1 -c exposure_absolute=5 -c brightness=30
