#!/bin/bash
echo "🔧 Configurando Network Mapper para macOS..."

# Crear y activar entorno virtual
python3 -m venv venv
source venv/bin/activate

# Instalar dependencias
pip install python-nmap networkx matplotlib

echo "✅ Instalación completada"
echo "🎯 Para usar: source venv/bin/activate && python3 auto_network_mapper.py"
