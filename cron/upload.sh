#!/bin/bash
if [ "$HOSTNAME" = "pubmaster" ]; then
    cd $HOME/ical-ufr
    ## no longer on publicence, circular symlink crash lektor
    #rsync -rcuzl --delete data/ $HOME/publicence/lektor/assets/data/
    rsync -rcuzl --delete data/ wwwmaster:licence19-23/data/
else
    >&2 echo "FAIL: run this on deployment machine"
fi
