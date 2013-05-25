#!/bin/sh

sudo -u postgres dropdb kickpassion
sudo -u postgres createdb kickpassion
python manage.py syncdb --settings kickpassion.localsettings
python manage.py runserver --settings kickpassion.localsettings
