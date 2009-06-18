#!/usr/bin/env python
# Brian Cottingham
# 2009-06-17
# Takes a directory of mp3 files and organizes them (quite unorderedly) into audio-cd-sized groups
# Licensed under the GNU GPLv3 (http://www.gnu.org/copyleft/gpl.html)

import os
import sys

try:
    import mad
except:
    print "You must have the pymad library to use this script!"
    exit()


CD_LENGTH = 80 * 60 * 1000
destdir = "dest"

cds = []
files = []


def main():
    if len(sys.argv) < 2:
        print "You must specify a directory containing your music!"
        exit()

    # Find all mp3 files and store their track lengths
    for f in os.popen("find %s -iname '*.mp3'" % sys.argv[1]).read().split("\n"):
        if f == '':
            break
        length = int(mad.MadFile(f).total_time())
        files.append((f, length))

    if len(files) == 0:
        print "No files to handle!"
        exit()

    # Find a CD for each track to belong to 
    cds.append([])  # Without this, the inner loop will never trigger, so we'll never have cds appended to the list, and the script will do nothing
    for track in files:
        for cd in range(len(cds)):  # Check every CD to see if we have room for this track
            if track[1] + timeOnCD(cd) < CD_LENGTH:
                # Add the track to the current CD and move on to the next track
                cds[cd].append(track)
                break
            if cd == len(cds)-1:  # Searched all CDs but couldn't find a place to insert this track
                cds.append([])
                cds[len(cds)-1].append(track)

    # Now that we've figured out how to organize everything, organize the actual files
    if not os.path.exists(destdir):
        os.mkdir(destdir)
    for cd in range(len(cds)):
        destination = os.path.join(destdir, str(cd))
        if not os.path.exists(destination):
            os.mkdir(destination)

        for track in cds[cd]:
            os.popen("cp %s %s" % (sh_escape(track[0]), sh_escape(destination)))  # Really, Python doesn't have a decent cp command built into the os module?



def sh_escape(s):
    return "'" + s.replace("'", "'\\''") + "'"



def timeOnCD(cd):
    used = 0
    for track in cds[cd]:
        used += track[1]
    return used



if __name__ == "__main__":
    main()
