#!/usr/bin/env python3
import networkx as nx
import matplotlib.pyplot as plt
from network_scanner import NetworkMapper
from datetime import datetime

class SVGGenerator:
    def __init__(self):
        self.mapper = NetworkMapper()
        self.hosts = []  # Guardar hosts como atributo de clase
    
    def generate_text_report(self, network_range, scan_ports=False, output_file="network_report.txt"):
        """Genera un archivo TXT con el resumen completo de la red"""
        
        report_content = []
        report_content.append("=" * 60)
        report_content.append("           INFORME DE RED - NETWORK MAPPER")
        report_content.append("=" * 60)
        report_content.append(f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report_content.append(f"Red escaneada: {network_range}")
        report_content.append(f"Hosts encontrados: {len(self.hosts)}")
        report_content.append(f"Escaneo de puertos: {'SI' if scan_ports else 'NO'}")
        report_content.append("=" * 60)
        report_content.append("")
        
        # Resumen por host
        report_content.append("DETALLE DE HOSTS:")
        report_content.append("-" * 60)
        
        for i, host in enumerate(self.hosts, 1):
            report_content.append(f"\n{i}. {host['hostname']}")
            report_content.append(f"   IP: {host['ip']}")
            report_content.append(f"   MAC: {host['mac']}")
            report_content.append(f"   Fabricante: {host['vendor']}")
            
            if scan_ports:
                report_content.append(f"   Sistema Operativo: {host.get('os', 'Unknown')}")
                
                if host['ports']:
                    report_content.append(f"   PUERTOS ABIERTOS ({len(host['ports'])}):")
                    for port_info in host['ports']:
                        report_content.append(f"      {port_info['port']}/{port_info['protocol']} - {port_info['service']}")
                else:
                    report_content.append("   No se encontraron puertos abiertos")
        
        # Resumen de servicios encontrados
        if scan_ports:
            report_content.append("\n" + "=" * 60)
            report_content.append("RESUMEN DE SERVICIOS ENCONTRADOS:")
            report_content.append("-" * 60)
            
            services_summary = {}
            for host in self.hosts:
                for port in host['ports']:
                    service_key = f"{port['port']}/{port['service']}"
                    if service_key not in services_summary:
                        services_summary[service_key] = []
                    services_summary[service_key].append(host['ip'])
            
            for service, hosts_with_service in services_summary.items():
                report_content.append(f"{service}: {len(hosts_with_service)} hosts")
                for host_ip in hosts_with_service[:3]:  # Mostrar primeros 3 hosts
                    report_content.append(f"  - {host_ip}")
                if len(hosts_with_service) > 3:
                    report_content.append(f"  ... y {len(hosts_with_service) - 3} más")
        
        # Estadísticas generales
        report_content.append("\n" + "=" * 60)
        report_content.append("ESTADÍSTICAS:")
        report_content.append("-" * 60)
        
        total_ports = sum(len(host['ports']) for host in self.hosts)
        report_content.append(f"Total de hosts: {len(self.hosts)}")
        report_content.append(f"Total de puertos abiertos: {total_ports}")
        
        if self.hosts:
            # Hosts con más puertos abiertos
            hosts_sorted = sorted(self.hosts, key=lambda x: len(x['ports']), reverse=True)
            report_content.append(f"Host con más puertos: {hosts_sorted[0]['ip']} ({len(hosts_sorted[0]['ports'])} puertos)")
        
        # Conexiones de red
        report_content.append(f"Conexiones detectadas: {len(self.mapper.network_graph.edges())}")
        
        # Guardar archivo
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write('\n'.join(report_content))
            print(f"📄 Reporte TXT guardado como: {output_file}")
            return output_file
        except Exception as e:
            print(f"❌ Error guardando reporte TXT: {e}")
            return None

    def generate_network_svg(self, network_range="192.168.1.0/24", output_file="network_diagram.svg", scan_ports=False):
        # Descubrir hosts y guardarlos como atributo
        self.hosts = self.mapper.discover_network(network_range)
        
        if not self.hosts:
            print("❌ No se encontraron hosts activos")
            return None
            
        # Escanear puertos y OS si está activado
        if scan_ports:
            print("🔦 Escaneo de puertos y OS activado")
            for host in self.hosts:
                try:
                    scan_result = self.mapper.scan_ports(host['ip'])
                    host['ports'] = scan_result['ports']
                    host['os'] = scan_result['os']
                    host['services'] = scan_result['ports']  # Para compatibilidad
                except Exception as e:
                    print(f"   ⚠️  Error en {host['ip']}: {e}")
                    host['ports'] = []
                    host['os'] = 'Unknown'
                    host['services'] = []
        else:
            print("🔦 Escaneo de puertos desactivado")
            for host in self.hosts:
                host['ports'] = []
                host['os'] = 'Unknown'
                host['services'] = []
        
        # Descubrir conexiones
        connection_count = self.mapper.discover_connections(self.hosts)
        print(f"🔗 {connection_count} conexiones descubiertas")
        
        # Crear gráfico más grande para acomodar más información
        plt.figure(figsize=(16, 12))
        
        # Diseño del gráfico mejorado
        pos = nx.spring_layout(self.mapper.network_graph, k=2, iterations=100)
        
        # Colores y formas por tipo de dispositivo
        node_colors = []
        node_sizes = []
        
        for node in self.mapper.network_graph.nodes():
            host_data = self.mapper.network_graph.nodes[node]
            hostname_lower = host_data.get('hostname', '').lower()
            
            if 'router' in hostname_lower or 'gateway' in hostname_lower:
                node_colors.append('red')
                node_sizes.append(1500)
            elif 'server' in hostname_lower:
                node_colors.append('orange')
                node_sizes.append(1300)
            elif 'switch' in hostname_lower or 'ap' in hostname_lower:
                node_colors.append('green')
                node_sizes.append(1200)
            else:
                node_colors.append('lightblue')
                node_sizes.append(1000)
        
        # Dibujar nodos
        nx.draw_networkx_nodes(self.mapper.network_graph, pos, 
                              node_color=node_colors, 
                              node_size=node_sizes,
                              alpha=0.9,
                              edgecolors='black',
                              linewidths=2)
        
        # Dibujar conexiones con etiquetas
        edge_labels = {}
        for edge in self.mapper.network_graph.edges(data=True):
            edge_labels[(edge[0], edge[1])] = edge[2].get('connection', 'direct')
        
        nx.draw_networkx_edges(self.mapper.network_graph, pos, 
                              alpha=0.6, 
                              width=2,
                              style='solid',
                              edge_color='gray')
        
        nx.draw_networkx_edge_labels(self.mapper.network_graph, pos, 
                                   edge_labels=edge_labels,
                                   font_size=6)
        
        # Etiquetas MEJORADAS con toda la información
        labels = {}
        for node in self.mapper.network_graph.nodes():
            host_data = self.mapper.network_graph.nodes[node]
            
            # Construir etiqueta con toda la información
            label = f"{host_data.get('hostname', node)}\n"
            label += f"IP: {node}\n"
            
            if host_data.get('mac', 'Unknown') != 'Unknown':
                label += f"MAC: {host_data['mac'][:8]}...\n"
            
            if scan_ports and host_data.get('os', 'Unknown') != 'Unknown':
                label += f"OS: {host_data['os']}\n"
            
            if scan_ports and host_data.get('ports'):
                ports_text = ", ".join([str(p['port']) for p in host_data['ports'][:5]])
                if len(host_data['ports']) > 5:
                    ports_text += f"... (+{len(host_data['ports'])-5})"
                label += f"Puertos: {ports_text}"
            
            labels[node] = label
        
        nx.draw_networkx_labels(self.mapper.network_graph, pos, labels, 
                               font_size=6, 
                               font_weight='bold',
                               verticalalignment='top')
        
        # Título informativo
        title = f"Mapa de Red - {network_range}\n"
        title += f"{len(self.hosts)} dispositivos | {connection_count} conexiones"
        if scan_ports:
            title += " | Con escaneo de puertos y OS"
        
        plt.title(title, fontsize=14, pad=20)
        plt.axis('off')
        plt.tight_layout()
        
        # Guardar como SVG
        plt.savefig(output_file, format='svg', bbox_inches='tight', dpi=150)
        print(f"✅ Diagrama SVG guardado como: {output_file}")
        
        # GENERAR ARCHIVO TXT (NUEVO)
        txt_output = output_file.replace('.svg', '_report.txt')
        self.generate_text_report(network_range, scan_ports, txt_output)
        
        # Mostrar información detallada en consola
        print(f"\n📊 RESUMEN DETALLADO:")
        for i, host in enumerate(self.hosts, 1):
            print(f"\n   {i}. {host['ip']} - {host['hostname']}")
            print(f"      MAC: {host['mac']}")
            if scan_ports:
                print(f"      OS: {host['os']}")
                if host['ports']:
                    print(f"      Puertos abiertos:")
                    for port in host['ports'][:8]:
                        print(f"        {port['port']}/{port['protocol']}: {port['service']}")
                else:
                    print(f"      No se encontraron puertos abiertos")
        
        return output_file
