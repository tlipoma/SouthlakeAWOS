from cv2 import imwrite, VideoCapture
import logging

LOGGER = logging.getLogger(__name__)


def caputure():
    # open Camera
    cam = VideoCapture(0)
    if not cam.isOpened():
        LOGGER.debug('FAILED to open camera!!!')
        return None

    # capture image
    status, img = cam.read()
    if not status:
        LOGGER.debug('FAiLED to capture image!!!')
        return None

    cam.release()
    return img


def save_image(img, filename):
    imwrite(filename, img)
    return


def capture_and_save(filename):
    img = caputure()
    if img is not None:
        save_image(img, filename)
