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
    """Sends a UDP packet to the specified IP and port."""
    sock.sendto(message.encode(), (UDP_IP, UDP_PORT))

async def main(ivr: YateIVR):
    """Main logic to process input and send UDP packets."""
    
    logger.debug("start")
    # Open the socket once and keep it open during the call
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    try:
        await ivr.play_soundfile(os.path.join(SOUNDS_PATH, "intro.slin"), complete=True)
        # await asyncio.sleep(0.5)

        # As long as the caller is on the line, read DTMF and send the data via UDP
        while True:
            # Wait for DTMF input and send it as a UDP packet
            button = await ivr.read_dtmf_symbols(1, timeout_s=5)
            
            if button:
                await send_udp_packet(sock, button)
                logger.info(f"Sending DTMF {button} to {UDP_IP}:{UDP_PORT}")
            else:
                # If no input, a timeout handling can take place here, for example
                logger.info("No input received, waiting for next input...")
            
    finally:
        sock.close() # Close the socket at the end of the call

# Initialize and start the Yate IVR application
logging.info("Starting Yate IVR...")
app = YateIVR()
app.run(main)
