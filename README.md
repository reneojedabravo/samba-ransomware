Script en python y bash para detectar encriptación de ransomware desde un cliente hacia nuestro servidor samba


Requerimientos:

Python3

Esto requiere que se haya configurado la auditoría samba.

Los registros de la auditoría samba deberán guardarse en /var/log/samba/audit.log

IPTABLES y fail2ban debidamente configurados en caso de optar por el baneo de la IP atacante.


Funcionamiento:

Se descarga una base de datos de las extensiones y nombres con los que se pueden identificar los archivos encriptados y sus respectivas notas desde https://fsrm.experiant.ca/api/v1/combined

Se formatea y se guarda esa lista en un archivo llamado extensiones.txt que estará en la ruta relativa al "action.py".

Se crea un archivo de log temporal que contendrá las últimas líneas de /var/log/samba/audit.log, esa cantidad de líneas se puede configurar en el action.py, este archivo temporal se llama "temp_log.txt" que estará en la ruta relativa al "Action.py".

En caso de detectar peligro se ejecuta un archivo bash que obtiene el nombre de la PC, nombre del usuario y la IP correspondiente para poder tomar acciones como banear la ip con iptables, detener samba, o lo que se requiera (action.sh o action2.sh).



Notas:

1.- Todavía lo estoy probando.

2.- Tarda algunos segundos en detectar el ataque (5 segundos en mi caso)

3.- Sigo creando los scripts pero ya funciona.

4.- Si alguien sabe de alguna base de datos más completa deje su aporte, mientras más completa mejor para todos >:v

5.- Esto lo estoy haciendo con un sistema Ubuntu Server 22.04 pero se puede adaptar fácilmente a tu sistema.

6.- Debes de ejecutar con permisos de administrador action.py


Fecha de creación: 13/01/24
