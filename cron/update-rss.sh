#!/bin/sh
# peut etre execute plusieurs fois par jours, si nextcloud ou le fichier rss local
# est du jour meme alors cela n'interroge pas ADE.
# sinon on tente une interrogation d'ADE.
cd $HOME/ical-ufr && conda run -n ical python -c 'import rss_to_ical; rss_to_ical.updateall_rss()'
