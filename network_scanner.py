#!/usr/bin/env python3
import nmap
import networkx as nx

class NetworkMapper:
    def __init__(self):
        self.nm = nmap.PortScanner()
        self.network_graph = nx.Graph()
        
    def discover_network(self, network_range="192.168.1.0/24"):
        print(f"🔍 Escaneando red: {network_range}")
        
        try:
            self.nm.scan(hosts=network_range, arguments='-sn -T4')
            
            hosts_list = []
            for host in self.nm.all_hosts():
                if self.nm[host].state() == 'up':
                    # Obtener dirección MAC
                    mac_address = 'Unknown'
                    vendor_info = 'Unknown'
                    
                    addresses = self.nm[host].get('addresses', {})
                    if 'mac' in addresses:
                        mac_address = addresses['mac']
                        vendor_info = self.nm[host].get('vendor', {}).get(mac_address, 'Unknown')
                    
                    # Obtener hostname
                    hostname = self.nm[host].hostname()
                    if not hostname:
                        hostname = host
                    
                    host_info = {
                        'ip': host,
                        'mac': mac_address,
                        'vendor': vendor_info,
                        'hostname': hostname,
                        'os': 'Unknown',  # Se detectará después
                        'ports': [],      # Se llenará con escaneo de puertos
                        'services': []    # Servicios detectados
                    }
                    hosts_list.append(host_info)
                    self.network_graph.add_node(host, **host_info)
                    
            print(f"✅ Encontrados {len(hosts_list)} hosts activos")
            return hosts_list
            
        except nmap.PortScannerError as e:
            print(f"❌ Error de nmap: {e}")
            return []
        except Exception as e:
            print(f"❌ Error inesperado: {e}")
            return []
    
    def scan_ports(self, host):
        """Escaneo de puertos y detección de OS"""
        print(f"🔦 Escaneando puertos y OS en {host}")
        
        try:
            # Escaneo más completo con detección de OS y servicios
            self.nm.scan(hosts=host, arguments='-sT -T4 -F -O --host-timeout 120s')
            
            host_info = {}
            open_ports = []
            os_info = 'Unknown'
            
            if host in self.nm.all_hosts():
                # Detección de Sistema Operativo
                if 'osmatch' in self.nm[host] and self.nm[host]['osmatch']:
                    best_os = self.nm[host]['osmatch'][0]
                    os_info = f"{best_os['name']} ({best_os['accuracy']}%)"
                
                # Escaneo de puertos
                for proto in self.nm[host].all_protocols():
                    ports = self.nm[host][proto].keys()
                    for port in ports:
                        service_info = self.nm[host][proto][port]
                        service_name = service_info.get('name', 'unknown')
                        product = service_info.get('product', '')
                        version = service_info.get('version', '')
                        
                        service_desc = service_name
                        if product:
                            service_desc += f" ({product}"
                            if version:
                                service_desc += f" {version}"
                            service_desc += ")"
                        
                        open_ports.append({
                            'port': port, 
                            'service': service_desc,
                            'protocol': proto
                        })
            
            print(f"   📡 {len(open_ports)} puertos abiertos, OS: {os_info}")
            
            return {
                'ports': open_ports[:10],  # Limitar a 10 puertos
                'os': os_info
            }
            
        except Exception as e:
            print(f"   ❌ Error escaneando {host}: {e}")
            return {'ports': [], 'os': 'Unknown'}
    
    def discover_connections(self, hosts):
        """Descubre conexiones entre hosts (simulado)"""
        print("🔗 Analizando conexiones...")
        
        # Por simplicidad, conectamos hosts basado en subredes comunes
        # En una implementación real usarías traceroute o técnicas similares
        gateway = None
        
        # Identificar gateway (usualmente .1 o .254)
        for host in hosts:
            if host['ip'].endswith('.1') or host['ip'].endswith('.254'):
                gateway = host['ip']
                break
        
        # Conectar todos los hosts al gateway
        if gateway and gateway in self.network_graph:
            for host in hosts:
                if host['ip'] != gateway and host['ip'] in self.network_graph:
                    self.network_graph.add_edge(gateway, host['ip'], 
                                              connection='network', 
                                              weight=1)
        
        return len(self.network_graph.edges())
