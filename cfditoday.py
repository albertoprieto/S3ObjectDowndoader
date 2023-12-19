#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Nombre del Script: cfditoday.py
Descripción: Este script descarga archivos desde Amazon S3 en función de un rango y tipo especificados.
Autor: Jose Alberto Prieto
Fecha de Creación: 13 de octubre de 2023
Fecha de modificación: 14 de octubre 2023
    Modificaciones:
        14 de octubre 2023
        -Se agregan parámetros al scroll para mantenerlo fijo:
         keep_on_top=True, no_titlebar=True
        -Se cambia título a 'Amazon S3 cfditoday'
        -El usuario ahora debe seleccionar la carpeta de destino (self.dest_folder)
        -Valida que valor inicial sea menor o igual al final
        -Limita la cantidad de folios por evento a descargar a 5000

Versión: 1.0
"""

import boto3 
import PySimpleGUI as sg
import pathlib
import os

class DescargadorS3:
    """
    Clase para descargar archivos desde Amazon S3.

    Esta clase permite descargar archivos XML y PDF desde un bucket de Amazon S3
    en función de un rango proporcionado por el usuario y permite seleccionar
    qué tipo de archivos descargar (XML, PDF o ambos).

    Attributes:
        path (str): Ruta del bucket en Amazon S3.
        s3 (boto3.resource): Objeto para interactuar con el servicio Amazon S3.
        filecount (int): Contador para el número de archivos descargados.
        ultima_descarga (str): Último archivo descargado.

    Methods:
        reset_layout(): Reinicia el diseño de la ventana.
        mostrar_popup(mensajes): Muestra una ventana emergente con los mensajes proporcionados.
        descargar_archivos_s3(tipo, inicio, fin): Descarga archivos desde Amazon S3
            en función del tipo (FP, GP, AP, NP) y el rango especificado por el usuario.
        ejecutar(): Función principal para ejecutar la interfaz gráfica.
    """

    def __init__(self):
        """
        Inicializa la clase DescargadorS3.

        Inicializa la clase con la ruta del bucket en Amazon S3, crea una interfaz gráfica
        usando PySimpleGUI y establece los contadores de archivos descargados y la última descarga.
        """
        super().__init__()
        self.path = 'CBB_CLONLVSVRAPPS19/C:/cfditoday/'
        self.s3 = boto3.resource('s3')
        self.filecount = 0
        self.ultima_descarga = ''
        self.dest_folder = ''

        sg.theme('BrightColors') 
        self.layout = [
            [sg.Text('Valor inicial ', size=(15, 1))] + [sg.Input(key='inpini')],
            [sg.Text('Valor final  ', size=(15, 1))] + [sg.Input(key='inpfin')],
            [sg.Text('Seleccionar archivos a descargar:', size=(30, 1))],
            [sg.Checkbox('XML', key='xml_checkbox', default=True), sg.Checkbox('PDF', key='pdf_checkbox', default=True)],
            [sg.Button('Iniciar', size=(7, 2), key='ok_button')],
            [sg.Text(size=(200, 1), key='patron_out')],
            [sg.Text(size=(200, 1), key='xmlout')],
            [sg.Text(size=(200, 1), key='pdfout')]
        ]
        self.window = sg.Window('Amazon S3 cfditoday', self.layout, size=(490, 280))

    def reset_layout(self):
        """
        Reinicia el diseño de la ventana.

        Reinicia los contadores, los valores de entrada y las casillas de verificación.
        """
        self.filecount = 0
        self.window['ok_button'].update(disabled=False)
        self.window['inpini'].update('')
        self.window['inpfin'].update('')
        self.window['xml_checkbox'].update(value=True)
        self.window['pdf_checkbox'].update(value=True)

    def mostrar_popup(self, mensajes):
        """
        Muestra una ventana emergente con los mensajes proporcionados.

        Args:
            mensajes (list): Lista de mensajes a mostrar en la ventana emergente.
        """
        mensaje = "\n".join(mensajes)
        #sg.popup_scrolled(f"Archivos Descargados:\n{mensaje}")
        sg.popup_scrolled(f"Archivos Descargados:\n{mensaje}", keep_on_top=True, no_titlebar=True)
        self.window['inpini'].update('')
        self.window['inpfin'].update('')
        self.window['pdfout'].update(f'Última descarga: {str(self.ultima_descarga)}')
        self.filecount = 0
        self.window['ok_button'].update(disabled=False)

    def descargar_archivos_s3(self, tipo, inicio, fin):
        """
        Descarga archivos desde Amazon S3 en función del tipo y el rango especificado.

        Args:
            tipo (str): Tipo de archivos a descargar (FP, GP, AP, NP).
            inicio (str): Valor inicial del rango.
            fin (str): Valor final del rango.
        """
        
        archivos_descargados = []
        errores = []
        for interval in range(int(inicio), int(fin) + 1):
            #patron = f"{tipo}{interval:04d}"
            patron = f"{tipo}{str(interval).zfill(6)}"
            if tipo == 'FP':
                carpeta = 'FACTURA'
                s3xml = f"{self.path}{patron}.xml"
                s3pdf = f"{self.path}{carpeta}-{patron}.pdf"
            elif tipo == 'GP':
                carpeta = 'NCARGO'
                s3xml = f"{self.path}{patron}.xml"
                s3pdf = f"{self.path}{carpeta}-{patron}.pdf"
            elif tipo == 'AP':
                carpeta = 'NCARGO'
                s3xml = f"{self.path}{patron}.xml"
                s3pdf = f"{self.path}{carpeta}-{patron}.pdf"
            elif tipo == 'NP':
                carpeta = 'NCREDITO'
                s3xml = f"{self.path}{patron}.xml"
                s3pdf = f"{self.path}{carpeta}-{patron}.pdf"


            folder_name = carpeta.lower()

            folder_name = os.path.join(self.dest_folder,folder_name)
            if not os.path.isdir(folder_name):
                os.mkdir(folder_name)

            try:
                if self.window['xml_checkbox'].get() and self.window['pdf_checkbox'].get():
                    self.filecount += 1
                    self.s3.Bucket('cfditoday').download_file(s3xml, os.path.join(folder_name, f"{patron}.xml"))
                    self.s3.Bucket('cfditoday').download_file(s3pdf, os.path.join(folder_name, f"{patron}.pdf"))
                    archivos_descargados.append(f"{self.filecount} {patron}.pdf")
                    archivos_descargados.append(f"{self.filecount} {patron}.xml")
                    self.ultima_descarga = patron
                elif self.window['xml_checkbox'].get():
                    self.filecount += 1
                    self.s3.Bucket('cfditoday').download_file(s3xml, os.path.join(folder_name, f"{patron}.xml"))
                    archivos_descargados.append(f"{self.filecount} {patron}.xml")
                    self.ultima_descarga = patron
                elif self.window['pdf_checkbox'].get():
                    self.filecount += 1
                    self.s3.Bucket('cfditoday').download_file(s3pdf, os.path.join(folder_name, f"{patron}.pdf"))
                    archivos_descargados.append(f"{self.filecount} {patron}.pdf")
                    self.ultima_descarga = patron

            except Exception as e:
                errores.append(f"Error al descargar {patron}: {str(e)}")

        if archivos_descargados:
            self.mostrar_popup(archivos_descargados)

        if errores:
            sg.popup_error("\n".join(errores), keep_on_top=True, no_titlebar=True)
            self.filecount = 0
            self.window['ok_button'].update(disabled=False)
            self.window['inpini'].update('')
            self.window['inpfin'].update('')

    def ejecutar(self):
        while True:
            event, values = self.window.read() 
            if event == sg.WIN_CLOSED:
                break

            elif event == 'ok_button':
                if not (values['xml_checkbox'] or values['pdf_checkbox']):
                    sg.popup_error("Selecciona al menos una opción (XML o PDF) antes de iniciar la descarga.")
                else:
                    self.window['ok_button'].update(disabled=True)
                    tipo = values['inpini'][:2].upper()
                    inicio = values['inpini'][2:]
                    fin = values['inpfin'][2:]

                    if tipo in ['FP','GP','NP','AP']:

                        if abs(int(fin) - int(inicio)) > 5000:
                            diferencia = abs(int(fin) - int(inicio))
                            sg.popup_error(f"El límite de descargas por evento es 5000, estás intentando descargar: {diferencia} ")
                            break
                        if inicio <= fin:
                            pass
                        else:
                            sg.popup_error(f'Valor inicial {inicio} es superior al valor final {fin}, verifique')
                            break

                        if len(tipo) != 2:
                            sg.popup_error(f'Tipo " {tipo} " No válido, verifique')
                            self.reset_layout()
                        elif len(inicio) != 6:
                            sg.popup_error(f'Rango inválido " {inicio} " verifique')
                            self.reset_layout()
                        elif len(fin) != 6:
                            sg.popup_error(f'Rango inválido " {fin} " verifique')
                            self.reset_layout()
                        else:
                            self.dest_folder = sg.popup_get_folder("Selecciona la carpeta de destino para los archivos",
                                                          title="Seleccionar carpeta")
                            if not self.dest_folder:
                                sg.popup_error('Se debe seleccionar una carpeta para descargar los archivos')
                                break
                            if not os.path.isdir(self.dest_folder):
                                os.mkdir(self.dest_folder)
                            self.descargar_archivos_s3(tipo, inicio, fin)
                    else:
                        sg.popup_error(f'Tipo " {tipo} " No válido, verifique')
                        self.reset_layout()

        self.window.close()

if __name__ == "__main__":
    descargador = DescargadorS3()
    descargador.ejecutar()
