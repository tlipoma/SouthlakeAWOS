import os

# Change to local folder then take image
os.chdir("/home/pi/SouthlakeAWOS")

# Sent local IP address for logging
import post_ip

# Take Image
os.system("./take_image.sh")

# Send Image
import send_image
