import json
from scapy.all import *

def packet_handler(pkt):
    if pkt.haslayer(UDP) and pkt[UDP].dport == 1900:
        if pkt.haslayer(UDP) and pkt[UDP].dport == 1900 and pkt.haslayer(Raw):
            if "M-SEARCH" in str(pkt[Raw].load):
                response = build_fake_upnp_response(pkt[IP].src, pkt[Ether].src)
                send(response, verbose=0)

        data = {
            'timestamp': pkt.time,
            'source_ip': pkt[IP].src,
            'packet_details': pkt.summary(),
            'device_info': [],
            'packet_content': str(pkt[Raw].load)
        }
        print("UPnP packet received:")
        print("Timestamp:", data['timestamp'])
        print("Source IP:", data['source_ip'])
        print("Packet details:", data['packet_details'])
        if "M-SEARCH" in str(pkt[Raw].load):
            device_info = extract_device_info(pkt[Raw].load)
            print("Device Information:")
            print("Model:", device_info.get("X-DEVICE-MODEL"))
            print("Version:", device_info.get("X-DEVICE-VERSION"))
            print("Manufacturer:", device_info.get("X-MANUFACTURER"))
            data['device_info'].append({
                'Model': device_info.get("X-DEVICE-MODEL"),
                'Version': device_info.get("X-DEVICE-VERSION"),
                'Manufacturer': device_info.get("X-MANUFACTURER")
            })
        register_data(data)

def register_data(data):
    with open('upnp_data2.json', 'a') as file:
        json.dump(data, file)
        file.write('\n')

def build_fake_upnp_response(destination_ip, source_mac):
    response = Ether(src=source_mac, dst="ff:ff:ff:ff:ff:ff") / IP(dst=destination_ip) / UDP(sport=1900, dport=1900) / \
               Raw(load='HTTP/1.1 200 OK\r\n' +
                         'CACHE-CONTROL: max-age=1800\r\n' +
                         'ST: urn:schemas-upnp-org:device:InternetGatewayDevice:1\r\n' +
                         'EXT:\r\n' +
                         'SERVER: Linux/2.6 UPnP/1.0 MiniUPnPd/2.1\r\n' +
                         'USN: uuid:UPnP-InternetGatewayDevice-1_0-123456789012::urn:schemas-upnp-org:device:InternetGatewayDevice:1\r\n' +
                         'LOCATION: http://' + destination_ip + '/upnp/IGD.xml\r\n' +
                         'OPT: "http://schemas.upnp.org/upnp/1/0/"; ns=01\r\n' +
                         '01-NLS: b9200ebb-736d-4b93-bf03-835149d13983\r\n' +
                         'BOOTID.UPNP.ORG: 1\r\n' +
                         'CONFIGID.UPNP.ORG: 1337\r\n' +
                         'X-DEVICE-MODEL: Security Cam\r\n' +  # Add custom fields and values here
                         'X-DEVICE-VERSION: 1.0\r\n' +
                         'X-MANUFACTURER: Shenzen LTD\r\n' +
                         '\r\n')
    return response

def extract_device_info(raw_load):
    device_info = {}
    lines = raw_load.decode().splitlines()
    for line in lines:
        if ":" in line:
            key, value = line.split(":", 1)
            device_info[key.strip()] = value.strip()
    return device_info
# Port 1900
sniff(filter="udp and port 1900", prn=packet_handler, store=False, iface="eth0")
