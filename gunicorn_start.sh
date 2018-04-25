#!/bin/bash
#nohup gunicorn -w 10 --worker-class=gevent MyLofter.wsgi:application &
gunicorn --workers 10 --daemon --worker-class=gevent MyLofter.wsgi:application 
