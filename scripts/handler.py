import asyncio
import logging
import socket

from yate.protocol import MessageRequest
from yate.ivr import YateIVR

import phonyclient

# Initialisiere und starte die Yate IVR Anwendung
logging.info("Starting Yate IVR...")
app = YateIVR()
app.phonyclient.PhonyClient(main)


SOUNDS_PATH = "/usr/local/share/yate/sounds"
UDP_IP = "172.17.0.1"
UDP_PORT = 1234
