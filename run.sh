#!/bin/sh
killall flask
export FLASK_APP=webapp && export FLASK_ENV=development && flask run
