"""Файл, содержащий базовые параметры: \n
-Корневая папка работы скрипта, зависимая от операционной системы"""
import os
import platform

system = platform.system()
if system == "Windows":
    parrent_dir = os.getcwd()
elif system == "Linux":
    parrent_dir = "/var/log/NetologyCursBackup"
