# SimpleVideoCombiner
(si sos de boca [clickea aca](#soy-de-boca))

A simple video concatenator / video merger.

As a League of Legends coach I often made 10-15 minute compilation videos of certain game concepts for my players. I made this app to facilitate that process.

[Download for Windows](https://github.com/tomexlol/simplevideocombiner/releases/download/v1.0.0/svc.exe)

[Download for Linux](https://github.com/tomexlol/simplevideocombiner/releases/download/v1.0.0-linux/svc)



**IMPORTANT**: For "Add Clip Number" and "Add File Name" options to work on Windows, you need to install [ImageMagick](https://imagemagick.org/archive/binaries/ImageMagick-7.1.0-62-Q16-HDRI-x64-dll.exe) on the default directory - this file needs to be present here: C:\Program Files\ImageMagick-7.1.0-Q16-HDRI\magick.exe

If you dont have this the program will just crash if you check these options. Leave everything unchecked.



Expected workflow:
* Record your clips using OBS or whatever you prefer. Optional: Name them something descriptive.
* Go to SVC, add your clips by drag and drop or Browse Files button.
* Use the arrows to sort them - descriptive names will come in handy here. Use the X button to discard any unwanted clips.
* Check the settings you want. Adding clip number/name is very useful for visual clarity, otherwise transitions without editing can be a bit jarring.
* Click Generate Video and wait patiently.

## How to Install
Windows: [Download the .exe](https://github.com/tomexlol/simplevideocombiner/releases/download/v1.0.0/svc.exe) and run it, no install needed.

Linux: [Download the executable](https://github.com/tomexlol/simplevideocombiner/releases/download/v1.0.0-linux/svc) and run it, no install needed. You can run svc.py from this source if you don't trust me.



### Settings Explanations

**Add Clip Number**: Adds "Clip 1", "Clip 2", etc to the top left of each clip for 2 seconds at the start.

**Add File Name**: Adds the file name to the top left of each clip for 2 seconds at the start.

![](https://github.com/tomexlol/tomexlol.github.io/blob/master/assets/images/samplesettings)


**Generate timestamps.txt**: Generates a Youtube description friendly timestamps.txt file with the start time of each clip.



# How it Works

SVC is written 100% in Python. Coming soon: a blogpost at tomexlol.com breaking down the sourcecode.

It leverages the power of [MoviePy](https://zulko.github.io/moviepy/) to edit your clips into one and to add the text.

The GUI was made in [Qt Designer](https://doc.qt.io/qt-6/qtdesigner-manual.html) and implemented using [PyQt6](https://www.riverbankcomputing.com/software/pyqt/).

[PyInstaller](https://pyinstaller.org/en/stable/) was used to package the application into a single file. The spec file used is provided in the source (svc.spec)

Icon was made in 5 minutes in [Paint.net](https://www.getpaint.net/)

# Soy de Boca
[Descargar para Windows](https://github.com/tomexlol/simplevideocombiner/releases/download/v1.0.0/svc.exe)

[Descargar para Linux](https://github.com/tomexlol/simplevideocombiner/releases/download/v1.0.0-linux/svc)


Un combinador de videos simple.

Cuando era coach de League of Legends hacía videos compilados de 10-15 minutos de conceptos del juego para mis jugadores. Hice esta aplicación para facilitar ese flujo de trabajo.


Flujo de trabajo esperado:
* Graba tus clips usando OBS o lo que prefieras. Opcional: poneles nombres descriptivos.
* Abrí el SVC, agrega tus clips arrastrandolos o con el botón de Browse Files.
* Usá las flechitas para ordenarlos - acá es donde es útil haberles puesto nombres descriptivos. Usá el botón de la X para descartar los clips que no quieras.
* Tildá las opciones que quieras. Agregar el número de clip o el nombre de archivo es muy útil para la claridad visual, sino las transiciones sin editar pueden ser dificiles de procesar para el cerebro.
* Clickeá Generate Video y esperá pacientemente.


## Cómo Instalar
Windows: [Bajar el .exe](https://github.com/tomexlol/simplevideocombiner/releases/download/v1.0.0/svc.exe) y correrlo, no requiere instalación.

**IMPORTANTE**: Para que funcionen las opciones de "Add Clip Number" y "Add File Name" en Windows, debes instalar [ImageMagick](https://imagemagick.org/archive/binaries/ImageMagick-7.1.0-62-Q16-HDRI-x64-dll.exe) en la carpeta predeterminada - el archivo magick.exe debe estar presente en: C:\Program Files\ImageMagick-7.1.0-Q16-HDRI\magick.exe. Si tu Windows está en español probablemente te de problemas, creá esa carpeta y poné el ImageMagick ahí y debería funcionar. Sino deja estas dos opciones sin tildar. Ya lo voy a arreglar!

Linux: [Bajar el ejecutable](https://github.com/tomexlol/simplevideocombiner/releases/download/v1.0.0-linux/svc) y correrlo, no requiere instalación. O instalar las dependencias y correr svc.py si no confias en mi paquete.


### Opciones - Explicaciones

**Add Clip Number**: Agrega "Clip 1", "Clip 2", etc arriba a la izquierda por 2 segundos al comienzo de cada clip.

**Add File Name**: Agrega el nombre de archivo arriba a la izquierda por 2 segundos al comienzo de cada clip.

![](https://github.com/tomexlol/tomexlol.github.io/blob/master/assets/images/samplesettings)


**Generate timestamps.txt**: Genera un timestamps.txt con el tiempo de inicio de cada clip para linkear en la descripción de Youtube.
