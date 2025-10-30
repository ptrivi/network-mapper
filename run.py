#!/usr/bin/env python3
import subprocess
import sys
import argparse
from pathlib import Path

def check_dependencies():
    """Verifica que todas las dependencias estén instaladas"""
    try:
        import nmap
        import networkx as nx
        import matplotlib.pyplot as plt
        print("✅ Todas las dependencias están instaladas")
        return True
    except ImportError as e:
        print(f"❌ Dependencia faltante: {e}")
        print("💡 Instala las dependencias con:")
        print("   pip install python-nmap networkx matplotlib")
        return False

def main():
    # Configurar argumentos
    parser = argparse.ArgumentParser(description='Network Mapper - Generador de diagramas de red SVG')
    parser.add_argument('network', nargs='?', default='192.168.1.0/24', 
                       help='Rango de red a escanear (ej: 192.168.1.0/24, 10.0.0.0/16)')
    parser.add_argument('--output', '-o', default=None,
                       help='Nombre del archivo SVG de salida')
    parser.add_argument('--scan-ports', '-p', action='store_true',
                       help='Escanear puertos (puede requerir sudo)')
    
    args = parser.parse_args()
    
    print("🚀 Ejecutando Network Mapper...")
    
    # Verificar dependencias primero
    if not check_dependencies():
        return
    
    try:
        # Importar módulos
        from network_scanner import NetworkMapper
        from svg_generator import SVGGenerator
        
        # Usar la red proporcionada como parámetro
        network_range = args.network
        
        # Generar nombre de archivo si no se proporciona
        if not args.output:
            output_file = f"network_map_{network_range.replace('/', '_').replace('.', '_')}.svg"
        else:
            output_file = args.output
        
        print(f"🌐 Escaneando: {network_range}")
        print(f"💾 Salida: {output_file}")
        print(f"🔦 Escaneo de puertos: {'Activado' if args.scan_ports else 'Desactivado'}")
        
        # Generar diagrama
        generator = SVGGenerator()
        output_path = generator.generate_network_svg(network_range, output_file, args.scan_ports)
        
        if output_path and Path(output_path).exists():
            print(f"✅ Diagrama generado: {output_path}")
            # Abrir en macOS
            subprocess.run(['open', output_path])
        else:
            print("❌ No se pudo generar el diagrama")
            
    except KeyboardInterrupt:
        print("\n⏹️  Escaneo cancelado por el usuario")
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
