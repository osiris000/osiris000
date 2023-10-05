from scapy.all import *

print('Creado módulo-comando sniff y fecha y hora: 2023-10-02 12:00:26.017185')


def main(args):
    print('Args dentro de sniff', args)
    iface = "wlx0015af36cf55"  # Cambia 'eth0' al nombre de tu interfaz de red
    print(f"Monitoreando la red en la interfaz {iface}...\n")
    sniff(iface=iface, prn=packet_handler);


def packet_handler(packet):
    if packet.haslayer(IP):
        ip_packet = packet[IP]
        print(f"IP Source: {ip_packet.src}, IP Destination: {ip_packet.dst}")

        if packet.haslayer(TCP):
            tcp_packet = packet[TCP]
            print(f"TCP Source Port: {tcp_packet.sport}, TCP Destination Port: {tcp_packet.dport}")

            print("TCP Headers:")
            print(tcp_packet.show())

            print("\n" + "=" * 50 + "\n")

#if __name__ == "__main__":
#    main()
