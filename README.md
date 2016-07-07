# SouthLake AWOS
This project is meant to run on a raspberry pi, record a picture from a webcam, take data from a weather station, and send it to a remote server for display.

## POST
post.py runs all the commands that are required to update the server. Currently this:
0) post_ip.py    - sends local ip address to server for logging
1) take_image.sh - runs a basic webcam script
2) send_image.py - formats a post using requests to send the image

## CRON
The raspi should be setup to run a cron job that runs the post.py script once every five minutes.

