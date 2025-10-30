#!/usr/bin/env python3
import subprocess
import sys
import os
from pathlib import Path

def check_dependencies():
    """Verifica e instala dependencias en el entorno virtual"""
    try:
        import nmap
        import networkx as nx
        import matplotlib.pyplot as plt
        print("✅ Dependencias ya instaladas")
        return True
    except ImportError as e:
        print(f"📦 Instalando dependencias faltantes: {e}")
        return False

def get_network_range():
    """Obtiene el rango de red automáticamente en macOS"""
    try:
        # Método para macOS
        result = subprocess.run(['ipconfig', 'getifaddr', 'en0'], 
                              capture_output=True, text=True)
        ip = result.stdout.strip()
        if ip and len(ip.split('.')) == 4:
            network_range = '.'.join(ip.split('.')[:3]) + '.0/24'
            print(f"🌐 Rango de red detectado: {network_range}")
            return network_range
    except Exception as e:
        print(f"⚠️  No se pudo detectar red automáticamente: {e}")
    
    # Fallback con opciones comunes
    common_ranges = ["192.168.1.0/24", "192.168.0.0/24", "10.0.0.0/24"]
    
    for range_ip in common_ranges:
        response = input(f"¿Usar rango {range_ip}? (s/n): ").lower()
        if response in ['s', 'si', 'y', 'yes']:
            return range_ip
    
    custom_range = input("Ingresa el rango de red (ej: 192.168.1.0/24): ")
    return custom_range or "192.168.1.0/24"

def main():
    print("🚀 Iniciando Network Mapper para macOS")
    
    # Verificar si estamos en entorno virtual
    if not hasattr(sys, 'real_prefix') and not sys.prefix == sys.base_prefix:
        print("⚠️  No estás en un entorno virtual. Ejecuta:")
        print("   source venv/bin/activate")
        print("   Luego: python3 auto_network_mapper.py")
        return
    
    if not check_dependencies():
        print("❌ Error: Dependencias faltantes. Ejecuta:")
        print("   pip install python-nmap networkx matplotlib")
        return
    
    # Obtener rango de red
    network_range = get_network_range()
    
    # Importar después de verificar dependencias
    from network_scanner import NetworkMapper
    from svg_generator import SVGGenerator
    
    # Generar diagrama
    print("🎨 Generando diagrama de red...")
    generator = SVGGenerator()
    output_file = f"network_diagram_{network_range.replace('/', '_')}.svg"
    output_path = generator.generate_network_svg(network_range, output_file)
    
    # Abrir automáticamente en Mac
    if os.path.exists(output_path):
        subprocess.run(['open', output_path])
        print(f"🎉 Diagrama generado y abierto: {output_path}")
    else:
        print("❌ Error: No se pudo generar el diagrama")

if __name__ == "__main__":
    main()
