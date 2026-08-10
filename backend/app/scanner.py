import asyncio
from app.config import settings
from scapy.all import ARP, Ether, srp

def _sync_arp_scan(subnet: str) -> list[dict]:
    """ Perform a synchronous ARP scan on the given subnet and return a list of discovered devices with their IP and MAC addresses.
    """

    try:
        arp_req = ARP(pdst=subnet)

        broadcast_frame = Ether(dst="ff:ff:ff:ff:ff:ff")

        packet = broadcast_frame / arp_req

        answered, _ = srp(packet, timeout=2, verbose=False)

        discovered_devices = []
        for sent, received in answered:
            discovered_devices.append({"ip": received.psrc, "mac": received.hwsrc})

        return discovered_devices
    except Exception as e:
        print(f"Error during ARP scan: {e}")
        return []

async def scan_network() -> list[dict]:
    """ Asynchronously scan the network for devices using ARP requests and return a list of discovered devices with their IP and MAC addresses.
    """
    return await asyncio.to_thread(_sync_arp_scan, settings.SUBNET_RANGE)