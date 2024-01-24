#!/bin/bash
echo "Desconectando servidor..."
systemctl stop smbd
systemctl stop nmbd
