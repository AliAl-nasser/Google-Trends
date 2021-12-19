#!/bin/bash

#Keep in mind that this overwrites the old images.
#from png to jgp, use this only if you executed the python script file. Otherwise just run make_gif.sh
mogrify -format jpg *.png

