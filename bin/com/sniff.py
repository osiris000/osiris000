from scapy.all import *

print('Creado módulo-comando sniff y fecha y hora: 2023-10-02 12:00:26.017185')

def main(args):
    print('Args dentro de sniff', args)

    # Verificar si hay argumentos
    if len(args) < 1:
        print("Requiere un argumento ")
        # se sale
        return

    if args[0] == "--interfaces":
        # Obtener interfaces de red disponibles
        interfaces = ifaces
        if not interfaces:
            print("No hay interfaces de red disponibles")
            return

        print("Interfaces disponibles:")
        for iface, details in interfaces.items():
            print(f"Nombre: {iface}, Descripción: {details.description}")
        return

    iface = args[0]  # nombre de tu interfaz de red
    print(f"Monitoreando la red en la interfaz {iface}...\n")
    try:
        sniff(iface=iface, prn=packet_handler)
    except Exception as e:
        print("Error:",e)

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

if __name__ == "__main__":
    main(sys.argv[1:])
