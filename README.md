DescargadorS3

Este script en Python permite descargar archivos desde Amazon S3 en función de un rango y tipo especificados.

Detalles del Script
Nombre del Script: cfditoday.py
Descripción: Este script descarga archivos XML y PDF desde un bucket de Amazon S3 en función de un rango proporcionado por el usuario y permite seleccionar qué tipo de archivos descargar (XML, PDF o ambos).
Autor: Jose Alberto Prieto
Fecha de Creación: 13 de octubre de 2023
Versión: 1.0
Requisitos
El script utiliza las siguientes bibliotecas de Python:

boto3: Librería de Amazon Web Services (AWS) para Python.
PySimpleGUI: Librería para crear interfaces gráficas de usuario simples en Python.
Puedes instalar las dependencias utilizando pip:


pip install boto3 PySimpleGUI
Uso
Para ejecutar el script, asegúrate de tener las credenciales de AWS configuradas en tu entorno. Luego, simplemente ejecuta el script y sigue las instrucciones en la interfaz gráfica para descargar los archivos necesarios desde Amazon S3.


python cfditoday.py
Instrucciones de Uso
Ingresa el valor inicial y final del rango que deseas descargar.
Selecciona los tipos de archivos que deseas descargar (XML, PDF o ambos) usando las casillas de verificación.
Haz clic en el botón "Iniciar" para iniciar la descarga.
Una vez completada la descarga, se mostrará una ventana emergente con los archivos descargados.
Estructura del Código
El código está organizado en una clase llamada DescargadorS3 que tiene los siguientes métodos:

__init__(self): Inicializa la clase y crea la interfaz gráfica usando PySimpleGUI.
reset_layout(self): Reinicia el diseño de la ventana.
mostrar_popup(self, mensajes): Muestra una ventana emergente con los mensajes proporcionados.
descargar_archivos_s3(self, tipo, inicio, fin): Descarga archivos desde Amazon S3 en función del tipo y el rango especificado.
ejecutar(self): Función principal para ejecutar la interfaz gráfica.
El script también incluye comentarios detallados en el código para explicar cada parte del programa.