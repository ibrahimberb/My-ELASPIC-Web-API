import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "True"
from pygame import mixer  # Load the popular external library
from config import (
    NOTIFY_NETWORK_ERROR_TRY_AUDIO_PATH,
    NOTIFY_PROGRAM_NOT_WORKING_AUDIO_PATH,
)
import time


def notify_error(exception, repeat_inf=False):
    mixer.init()
    if exception == "unexpected-error":
        mixer.music.load(NOTIFY_PROGRAM_NOT_WORKING_AUDIO_PATH)
    elif exception == "network-error-trying":
        mixer.music.load(NOTIFY_NETWORK_ERROR_TRY_AUDIO_PATH)
    else:
        raise ValueError("Unknown error.")

    if repeat_inf:
        while True:
            mixer.music.play()
            time.sleep(3)

    mixer.music.play()




