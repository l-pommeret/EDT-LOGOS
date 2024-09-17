#!/bin/sh
# fait tout, mais si le fichier rss local est du jour on n'interroge pas ADE
# A executer plutot une fois par jour car en plus (option -M):
# on bouge les anciennes donnees de data vers data.1
cd $HOME/ical-ufr && conda run -n ical python rss_to_ical.py -M
