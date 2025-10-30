# Network Mapper 🔍

Herramienta casera para diagramar redes de datos con descubrimiento automático y generación de gráficos SVG.

## Características

- ✅ Descubrimiento automático de hosts en la red
- ✅ Generación de diagramas SVG automáticos
- ✅ Escaneo de puertos y detección de OS
- ✅ Reporte TXT con resumen completo
- ✅ Conexiones entre dispositivos
- ✅ Información de servicios y versiones
- ✅ Múltiples modos de uso

## Instalación Rápida

```bash
# Clonar repositorio
git clone https://github.com/tu-usuario/network-mapper.git
cd network-mapper

# Opción 1: Setup automático
chmod +x setup.sh
./setup.sh

# Opción 2: Manual
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Uso

### 🔧 Opción 1: Script Automático (Recomendado para empezar)
```bash
# Setup y ejecución automática
./setup.sh
python3 auto_network_mapper.py
```

### 🎯 Opción 2: Script Principal con Parámetros
```bash
# Escaneo básico
python3 run.py 192.168.1.0/24

# Escaneo completo (puertos y OS)
sudo python3 run.py 192.168.1.0/24 --scan-ports

# Con archivo de salida personalizado
python3 run.py 192.168.1.0/24 -o mi_red.svg
```

## Scripts Disponibles

- **`setup.sh`** - Instalación automática y configuración
- **`auto_network_mapper.py`** - Ejecución automática con detección de red
- **`run.py`** - Script principal con parámetros personalizables
- **`network_scanner.py`** - Lógica de descubrimiento y escaneo
- **`svg_generator.py`** - Generación de diagramas y reportes

## Ejemplos

```bash
# Escaneo automático con detección de red
python3 auto_network_mapper.py

# Escanear subred completa
python3 run.py 10.0.0.0/24

# Escanear rango específico con puertos
sudo python3 run.py 192.168.1.1-50 --scan-ports

# Escanear con nombre personalizado
python3 run.py 192.168.68.0/24 -o oficina.svg
```

## Archivos generados

- `network_map_[RED].svg` - Diagrama visual de la red
- `network_map_[RED]_report.txt` - Reporte detallado en texto

## Requisitos

- Python 3.6+
- nmap instalado en el sistema
- Privilegios de root para escaneo de puertos

## Estructura del Proyecto

```
network-mapper/
├── run.py                 # Script principal con parámetros
├── auto_network_mapper.py # Ejecución automática
├── setup.sh              # Instalación automática
├── network_scanner.py    # Lógica de descubrimiento
├── svg_generator.py      # Generación de diagramas
├── requirements.txt      # Dependencias
└── README.md            # Esta documentación
```

## Licencia

MIT
