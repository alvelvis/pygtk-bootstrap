# Bootstrapping a new PyGTK application

In order to compile for Windows:

```sh
pyinstaller app.py --add-data "gui.css;." --add-data "gui.glade;." --add-data --noconfirm
```
