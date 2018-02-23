#!/usr/bin/env Python
# -*- coding: utf-8 -*-

'''
  Fecha: Febrero 2018
  Licencia: GLP3
  Programa que sirve para cifrar un PDF con caracteres ASCII.
  Las librerías que se necesitan son:
    easygui (para elección del fichero a cifrar y la elección del password)
    unicodecsv (para escribir en unicode en el archivo csv por si el nombre del pdf tiene estos caracteres)
    pypdf2 (para cifrar el documento)
    cx_Freeze para convertir el fichero py en ejecutable y que el usuario utilice un entorno gráfico
  El programa permitiría caracteres unicode pero luego estos caracteres no nos permiten abrir 
  el documento en el visor PDF. Queda pendiente resolver estos
  El programa verifica que la contraseña sea ascii y deja un log en la carpeta donde se 
  ejecuta el programa con un registro de cuando se ha ejecutado el programa, para 
  cifrar el archivo con la contraseña usada.
  Solo se introduce una contraseña (se podría usar dos para abrir el docuemnto con menos permisos)
  El programa genera una copia del documento con el sufijo -SinCifrar para que en ningún caso se pueda perder
  el documento original
  EL programa está testado en entornos Windows y en entornos GNU/Linux  
'''

import easygui as eg
import time

def CopiarFichero(Origen, Destino):
  '''
    Copio un fichero etiquetado como Origen con el nombre Destino
    Devuelvo si se ha hecho cierto o falso si ha sido imposible copiarlo
  '''
  import shutil
  Aux = True
  try:
    shutil.copy(Origen, Destino)
  except IOError, e:
    #print "Unable to copy file. %s" % e
    Aux = False	
  return Aux

def BorrarFichero(archivo):
  '''
    Borro los ficheros que voy generando temporales
    Devuelvo un cierto o falso si se ha podido o no de hacer
  '''
  import os
  Aux = True
  try:
    os.remove(archivo)
  except OSError:
    Aux = False
  return Aux

def ExisteArchivo(fichero):  
  '''
    Verifica si un archivo existe o no
  '''
  import os.path as path
  Aux = False  
  if path.isfile(fichero):
  #if path.exists(fichero): #Devuelve true carpeta y ficheros
   Aux = True
  return Aux
  
def EstaCifrado(Archivo):
  '''
    Nos dice si un archivo pdf está cifrado o no
  '''
  import PyPDF2
  import os  
  PDFCifrado = False
  path, filename = os.path.split(Archivo)
  f = open(Archivo, "rb")
  input_stream = PyPDF2.PdfFileReader(f)
  if input_stream.isEncrypted: 
    PDFCifrado = True
  f.close()
  return PDFCifrado
   
def EscribeLogFicherosProcesados(fichero, texto, debug=False):
  '''
    Escribo en un fichero un log
  '''
  #import csv
  import unicodecsv
  with open(fichero, 'a') as f:
    #writer = csv.writer(f)
    writer = unicodecsv.writer(f)
    writer.writerow([texto])
  if debug:
    print texto.decode('utf-8')
  return texto


def set_password(input_file, user_pass, owner_pass, ArchivoCifrado):
  import PyPDF2
  import os  
  '''
    Function creates new temporary pdf file with same content,
    assigns given password to pdf and rename it with original file.
  '''
  # temporary output file with name same as input file but prepended
  # by "temp_", inside same direcory as input file.
  path, filename = os.path.split(input_file)
  output_file = os.path.join(path, "temp_" + filename)
  # Empezamos el proceso
  output = PyPDF2.PdfFileWriter()
  HemosCifrado = False
  f = open(input_file, "rb")
  #input_stream = PyPDF2.PdfFileReader(open(input_file, "rb"))
  input_stream = PyPDF2.PdfFileReader(f)
  if not input_stream.isEncrypted:
    for i in range(0, input_stream.getNumPages()):
      output.addPage(input_stream.getPage(i))
    outputStream = open(output_file, "wb")
    # Set user and owner password to pdf file
    if type(user_pass) is str:
      salida = output.encrypt(user_pass, owner_pass, use_128bit=True)
      output.write(outputStream)
      outputStream.close()
    else:
      print 'No hemos cifrado el documento porque la clave es unicode'
      HemosCifrado = False
    # Rename temporary output file with original filename, this
    # will automatically delete temporary file
    f.close()
    BorrarFichero(input_file)
    os.rename(output_file, input_file)
    #os.rename(output_file, ArchivoCifrado)
    HemosCifrado = True
  else:
    HemosCifrado = False
  return HemosCifrado

'''
  Inicio del programa como ejemplo
'''
extension = ["*.pdf","*.PDF"]
ficherolog = 'log-pdf-cifrados.csv'
archivo = eg.fileopenbox(msg="Abrir archivo",
                         title="Elige un archivo PDF",
                         default='',
                         filetypes=extension)

if (archivo != None):
  if not EstaCifrado(archivo):
    '''
    paso = eg.passwordbox(msg='Protege el archivo con un password:',
                          title='Pon un password a ' + archivo,
                          default='')
    '''
    paso = eg.enterbox(msg='Protege el archivo con un password:',
                          title='Pon un password a ' + archivo,
                          default='')
    
    if (paso != None):
      if type(paso) is str:
              print 'Copiamos ' + archivo + ' sin cifrar, por si las moscas'
              ArchivoDestino = archivo[:-4] + '-SinCifrar.pdf'
              ArchivoCifrado = archivo[:-4] + '-Cifrado.pdf'
              CopiarFichero(archivo, ArchivoDestino)
              resultado = set_password(archivo, paso, None, ArchivoCifrado)
      else:
              resultado = False
      if not resultado:
        eg.msgbox(msg='ERROR: El fichero ' + archivo.encode('utf-8') + ' no se puede cifrar con ' + paso.encode('utf-8') + ' elige una contraseña sin caracteres especiales',
                  title='Imposible cifrar', 
                  ok_button='Continuar')
      else:
        print 'Ciframos el archivo ' + archivo + ' con el password ' + paso
        eg.msgbox(msg=archivo + ' protegido con ' + paso,
                  title='Archivo cifrado', 
                  ok_button='Continuar')
        FechaActual = time.strftime("%d/%m/%Y %H:%M:%S")
        EscribeLogFicherosProcesados(ficherolog, FechaActual + ';' + archivo.encode('utf-8') + ';' + paso.encode('utf-8'), True)
    else:
      print 'No has puesto una contraseña a ' + archivo.encode('utf-8') + ', No hacemos nada'
  else:
    print 'No podemos cifrar de nuevo el archivo ' + archivo.encode('utf-8') + ' . Ya está cifrado.'
else:
  print 'No hemos elegido ningún archivo, No hacemos nada'
