#!/bin/sh
cd $HOME/ical-ufr/
BAK="$HOME/bak-edt-`date -d "last-monday - 3 weeks" +\%Y\%m\%d`.tgz"
test -f $BAK && tar -zxf $BAK -C data.28 --strip-components=1
