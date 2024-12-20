#!/usr/bin/env python3
import asyncio
import os
import logging
import socket
from yate.protocol import MessageRequest
from yate.ivr import YateIVR

from filelock import FileLock, Timeout
import time
import atexit

# Pfad zur Lock-Datei und der eigentlichen Datei
lock_file_path = "phonyclient.lock"

# Lock-Objekt erstellen
lock = FileLock(lock_file_path, timeout=-1)  # Timeout nach 5 Sekunden

SOUNDS_PATH = "/usr/local/share/yate/sounds"
UDP_IP = "172.17.0.1"
UDP_PORT = 1234

logger = logging.getLogger(__name__)
ConsoleOutputHandler = logging.StreamHandler()
logger.addHandler(ConsoleOutputHandler)
logging.basicConfig(level=logging.INFO)

def cleanup_lock():
    if lock.is_locked:
        print("Entferne Lock-Datei beim Beenden des Skripts...")
        lock.release()
        if os.path.exists(lock_file_path):
            os.remove(lock_file_path)

async def send_udp_packet(sock, message: str):
    """Sendet ein UDP-Paket an die angegebene IP und den Port."""
    sock.sendto(message.encode(), (UDP_IP, UDP_PORT))

async def main(ivr: YateIVR):
    """Haupt-Logik zur Verarbeitung der Eingabe und zum Senden von UDP-Paketen."""
    
    logger.debug("geht los")
    # Öffne den Socket einmalig und behalte ihn während des Anrufs geöffnet
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    try:
        logger.info("Versuche, die Datei zu sperren...")
        with lock:
            logger.info("Dateilock erstellt")

            try:
                await ivr.play_soundfile(os.path.join(SOUNDS_PATH, "telegaming/intro.slin"), complete=True)
                #await asyncio.sleep(0.5)
        
                #game = await ivr.read_dtmf_symbols(4)
                #if len(game) != 4:
                #    game = "0000"
                #logger.info(game)

                # Solange der Anrufer in der Leitung ist, lese DTMF und sende die Daten über UDP
                while True:
                    # Warte auf DTMF-Eingabe und sende diese als UDP-Paket
                    button = await ivr.read_dtmf_symbols(1, timeout_s=5)
            
                    if button:
                        await send_udp_packet(sock, button)
                        logger.info(f"Sending DTMF {button} to {UDP_IP}:{UDP_PORT}")
                    else:
                        # Wenn keine Eingabe, kann hier z.B. eine Timeout-Behandlung erfolgen
                        await ivr.close
                        logger.info("No input received, waiting for next input...")    
            finally:
                sock.close() # Schließe den Socket am Ende des Anrufs
        logger.info("Datei entsperrt.")
    except Timeout:
        #logger.debug("Script läuft schon (Timeout). ")
        await ivr.play_soundfile(os.path.join(SOUNDS_PATH, "telegaming/intro.slin"), repeat=True, complete=True)
        await ivr.tone("busy")
        logger.info("Timeout")
    except Exception as e:
        print(f"Ein unerwarteter Fehler ist aufgetreten: {e}")
        await ivr.tone("busy")
        await asyncio.sleep(0.2)
    finally:
        cleanup_lock() # Sicherstellen, dass der Lock entfernt wird

# Initialisiere und starte die Yate IVR Anwendung
logging.info("Starting Yate IVR...")
atexit.register(cleanup_lock)
app = YateIVR()
app.run(main)
