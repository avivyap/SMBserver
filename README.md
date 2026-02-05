# Custom SMB Server 

Servidor SMB personalizado en Python construido sobre la librería Impacket.  
Permite levantar rápidamente un recurso compartido SMB configurable por línea de comandos e incluye logging personalizado de conexiones mediante hooks internos.

Proyecto orientado al aprendizaje del funcionamiento interno del servidor SMB de Impacket.


## Características

- Servidor SMB basado en Impacket
- Configuración por argumentos CLI (argparse)
- Definición dinámica de:
  - nombre del recurso compartido
  - ruta a compartir
  - puerto
- Soporte SMB2
- Logging personalizado de conexiones cliente
- Hook interno sobre el motor SMB para capturar IPs
- Control anti-spam de logs (una vez por conexión)
- Salida coloreada en consola
- Manejo limpio de Ctrl+C

---

## Requisitos

- Python 3
- impacket
- termcolor

