#!/bin/bash
# Verifica si se proporcionan los argumentos necesarios
if [ $# -ne 3 ]; then
    echo "Uso: $0 <usuario> <ip> <nombre_equipo>"
    exit 1
fi
# Recibir argumentos
usuario=$1
ip=$2
nombre_equipo=$3
# Ruta del archivo de configuración de Fail2Ban
FAIL2BAN_CONFIG="/etc/fail2ban/jail.local"
# Añadir regla de bloqueo al archivo de configuración
echo -e "\n[$usuario]\nenabled = true\nfilter = %(__name__)s\naction = iptables[name=NOBODY]\nlogpath = /var/log/auth.log\nmaxretry = 1\nbantime = 3600" >> $FAIL2BAN_CONFIG

# Reiniciar Fail2Ban para aplicar los cambios
service fail2ban restart

# Agregar la IP a la lista de direcciones bloqueadas
iptables -A fail2ban-$usuario -s $ip -j DROP

echo "La IP $ip ha sido bloqueada con éxito para el usuario $usuario y el equipo $nombre_equipo."
