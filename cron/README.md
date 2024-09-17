# Récupération automatique

Cloner le projet sur un serveur, et installer les crontab suivantes

```shell
crontab -e
```

```
### format
## minutes hour dayofmonth month dayofweek action
## ranges allowed
# download from ade every day
0 3 * * * $HOME/ical-ufr/cron/download.sh 2>&1
# then upload
0 4 * * * $HOME/ical-ufr/cron/upload.sh 2>&1
# and backup ics files every week
0 2 * * 1 $HOME/ical-ufr/cron/backup.sh 2>&1
# then restore the anteantepenultimate (four weeks ago) to data.28
10 2 * * 1 $HOME/ical-ufr/cron/restore28.sh 2>&1
# check rss every 10 minutes in weekdays
15 9-18 * * 1-5 $HOME/ical-ufr/cron/update-rss.sh 2>&1
# and build cal from rss at the end of the day
0 19 * * 1-5 $HOME/ical-ufr/cron/buildcalendars-rss.sh
```
