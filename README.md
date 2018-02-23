# CifrarPDf
Programa que sirve para cifrar un archivo PDF.
El código del programa ejemplo está es el archivo cifrarpdf.py

## Librerías necesarias
El programa usa 4 librerías para su funcionamiento
* esasygui (para la elección del dichero en entorno gráfico)
* unicodecsv (para grabación del log con caracteres unicode en el nombre del fichero)
* pypdf2 (para el cifrado del fichero PDF)
*cx_Freeze (para generar un archivo ejecutable, ver el fichero ejecutar.py)

## Entornos probados
El programa se ha probado en entornos Windows y GNU/Linux. Es posible que los antivirus como Panda cancelen la ejecución del programa.
Hay que parametrizar estos antivirus para que se pueda ejecutar el programa

### Generación de ejecutable en Entornos Windows
En la misma carpeta deben estar el archivo cifrarpdf.py y ejecutar.py
Hay que ejecutar el comando
<code>
python ejecutar.py build
</code>
Su resultado será una carpeta build con el código, dejo un fichero comprimido CifrarPDF.7z con el resultado en una máquina Windows

## Que genera el programa
El programa genera tres ficheros:
1. Un fichero log con el nombre log-pdf-cifrados.csv donde se irán guardando los resultados de los ficheros cifrados con la password usada. Este fichero se genera en la carpeta donde se ejecute el programa
2. Una copia del fichero original para que no se pierda con el mismo nombre que el fichero cifrado añadiendo el sufijo -SinCifrar
3. El fichero con el mismo nombre pero cifrado con la contraseña elegida


