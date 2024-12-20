#!/python-venv/bin/python3
import asyncio
import os
import logging
import socket
from yate.protocol import MessageRequest
from yate.ivr import YateIVR

SOUNDS_PATH = "/usr/local/share/yate/sounds"
UDP_IP = "172.17.0.1"
UDP_PORT = 1234

logger = logging.getLogger(__name__)
ConsoleOutputHandler = logging.StreamHandler()
logger.addHandler(ConsoleOutputHandler)
logging.basicConfig(level=logging.INFO)

async def send_udp_packet(sock, message: str):
    """Sendet ein UDP-Paket an die angegebene IP und den Port."""
    sock.sendto(message.encode(), (UDP_IP, UDP_PORT))

async def main(ivr: YateIVR):
    """Haupt-Logik zur Verarbeitung der Eingabe und zum Senden von UDP-Paketen."""
    
    logger.debug("geht los")
    # Öffne den Socket einmalig und behalte ihn während des Anrufs geöffnet
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    try:
        await ivr.play_soundfile(os.path.join(SOUNDS_PATH, "intro.slin"), complete=True)
        # await asyncio.sleep(0.5)

        # Solange der Anrufer in der Leitung ist, lese DTMF und sende die Daten über UDP
        while True:
            # Warte auf DTMF-Eingabe und sende diese als UDP-Paket
            button = await ivr.read_dtmf_symbols(1, timeout_s=5)
            
            if button:
                await send_udp_packet(sock, button)
                logger.info(f"Sending DTMF {button} to {UDP_IP}:{UDP_PORT}")
            else:
                # Wenn keine Eingabe, kann hier z.B. eine Timeout-Behandlung erfolgen
                logger.info("No input received, waiting for next input...")
            
    finally:
        sock.close()  # Schließe den Socket am Ende des Anrufs

# Initialisiere und starte die Yate IVR Anwendung
logging.info("Starting Yate IVR...")
app = YateIVR(host="127.0.0.1", port=9999)
app.run(main)
