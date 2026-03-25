from pyrogram import Client, filters
from pyrogram.types import Message, BotCommand, InlineKeyboardMarkup, InlineKeyboardButton
from os.path import exists
from json import loads,dumps 
from pathlib import Path
from os import listdir
from os import mkdir
from os import unlink
from os.path import isfile, join
from datetime import timedelta
from random import randint
import re
from re import findall
from bs4 import BeautifulSoup
from py7zr import FILTER_COPY
from multivolumefile import MultiVolume
from io import BufferedReader
from py7zr import SevenZipFile
from move_profile import move_to_profile
from urllib.parse import quote
from time import time, localtime
from yarl import URL
import asyncio
import tgcrypto
import aiohttp_socks
import aiohttp
import requests
import traceback
import time
import os
import ssl
import http.server
import socketserver
import yt_dlp
from uptodl import search, get_info
import psutil
from upload import NextcloudClient
import json
import base64

user_data = {}

ssl._create_default_https_context = ssl._create_unverified_context

def split_file(file_path, chunk_size):
    """Divide un archivo en chunks y los almacena en una lista.

    Args:
        file_path: La ruta del archivo a dividir.
        chunk_size: El tamaño de cada chunk en bytes.

    Returns:
        Una lista de rutas de archivo para cada chunk.
    """
    file_path = Path(file_path)
    file_name = file_path.name
    
    chunks = []
    with open(file_path, 'rb') as file:
        chunk_num = 0
        while True:
            chunk = file.read(chunk_size)
            if not chunk:
                break
            chunk_file_name = f"{file_name}_part{chunk_num}"
            chunk_file_path = file_path.parent / chunk_file_name
            chunks.append(chunk_file_path)
            with open(chunk_file_path, 'wb') as chunk_file:
                chunk_file.write(chunk)
            chunk_num += 1

    return chunks




from pathlib import Path
from os import unlink, walk

def sevenzip(fpath: Path, password: str = None, volume = None):
    filters = [{"id": FILTER_COPY}]
    fpath = Path(fpath)

    if fpath.is_dir():
        
        with MultiVolume(
            fpath.with_name(fpath.name + ".7z"), mode="wb", volume=volume, ext_digits=3
        ) as archive:
            with SevenZipFile(archive, "w", filters=filters, password=password) as archive_writer:
                if password:
                    archive_writer.set_encoded_header_mode(True)
                    archive_writer.set_encrypted_header(True)

                for root, _, files in walk(fpath):
                    for file in files:
                        file_path = os.path.join(root, file)
                        relative_path = os.path.relpath(file_path, str(fpath))
                        archive_writer.write(file_path, relative_path)

    else:
        # If it's a file, use the existing logic
        fsize = fpath.stat().st_size

        if not volume:
            volume = fsize + 1024

        ext_digits = len(str(fsize // volume + 1))
        if ext_digits < 3:
            ext_digits = 3

        with MultiVolume(
            fpath.with_name(fpath.name + ".7z"), mode="wb", volume=volume, ext_digits=ext_digits
        ) as archive:
            with SevenZipFile(archive, "w", filters=filters, password=password) as archive_writer:
                if password:
                    archive_writer.set_encoded_header_mode(True)
                    archive_writer.set_encrypted_header(True)

                archive_writer.write(fpath, fpath.name)

    files = []
    for file in archive._files:
        files.append(file.name)
    # Only unlink the original path if it's a file
    if fpath.is_file(): 
        unlink(fpath)
    return files
	
	

from configs import api_id, api_hash, token
admins = ['Astro_Bots']
bot = Client("client",api_id,api_hash,bot_token=token) 
CONFIG = {}
global_conf = {
       "token": "",
       "host": ""
   }


traffic = {
"downlink":"0",
"uplink":"0"}

traffico = 0

print(global_conf["host"])


stream_sites = ['youtube.com', 'xnxx.com', 'twitch.tv', 'dailymotion.com']



SECOND = 0


def getuser(username):
    try:
        user_info = CONFIG[username]
        return user_info
    except:
        return None

def createuser(username):
    CONFIG[username] = {"username":"","password":"","proxy":"","zips":"99","calidad":"None","automatic":"off","server":"1547","mode":"moodle"}
	
	
def deleteuser(username):
    
    if username in CONFIG:
        del CONFIG[username]
        print(f"Usuario {username} eliminado de la configuración.")
    else:
        print(f"El usuario {username} no existe en la configuración.")


	
@bot.on_message()
async def new_event(client: Client, message: Message):
    global traffico
    await bot.set_bot_commands([
    BotCommand("start","Inicia el Bot"),
    BotCommand("help","Muestra ayuda básica sobre el bot"),
    BotCommand("config","Configurar el host y el token"),
    BotCommand("ls","Listar archivos en la base de datos del bot"),
    BotCommand("up","Subir a moodle EJ /up [Ítem]"),
    BotCommand("cd","Ir a directorio en raiz EJ:/cd [Ítem]"),
    BotCommand("back","Ir a directorio superior"),
    BotCommand("mkdir","Crear directorio en ruta actual"),
    BotCommand("mv","Mover directorio hacia otro existente en ruta actual"),
    BotCommand("rm","Borrar archivo o carpeta almacenada en el bot"),
    BotCommand("del_all","Borrar todos los archivos y carpetas almacenadas en el bot"),
    BotCommand("rename","Renombrar directorios o archivos"),
    BotCommand("seven","Comprimir y cortar directorios antes de suvir a la moodle"),
    BotCommand("auto","Establecer las subidas en automáticas"),
    BotCommand("status","Muestra el estado del server"),
    BotCommand("zips","Tamaño de las partes a subir segun la moodle EJ /zips 99"),
    BotCommand("calidad","Establecer calidad de videos de yt EJ /calidad 480p"),
    BotCommand("upx","Subir a nube despues de configurar con /server"),
    BotCommand("next","Subir a nube despues de configurar con /server"),
    BotCommand("mode","Modo de subida moodle o nube"),
    BotCommand("server","Establecer server a subir [es nube]"),
    BotCommand("add_site","Añadir sitio en caso de que el bot no quiera descargar de el"),
    BotCommand("search","Busca aplicaciones en Uptodown"),
    BotCommand("proxy","Establecer proxy para moodles que lo requieran"),
    BotCommand("off_proxy","Desactivar proxy"),
     BotCommand("del_cloud","borra la nube"),
     BotCommand("add","Añadir usuario al bot"),
    BotCommand("ban","Quitar usuario del bot"),	
  BotCommand("add_days","Añadir usuario por 7 dias")])
  
    msg = message.text
    id = message.from_user.id
    username = message.from_user.username
    @bot.on_callback_query(filters.regex(r"^/download"))
    async def download_callback(client, query):
        url = url_temp["Actual_url"]  # Obtén la URL almacenada en el diccionario
    # Llama a la función download_file() con los parámetros necesarios
        await download_file(url, id, query.message, callback=download_func)  # Usa query.message para el mensaje
        await query.answer("Descargando archivo...")
    if msg is None:
        msg = ""
    
    if getuser(username):
        if exists(str(id)):
            pass
        else:
            mkdir(str(id))
        pass
    else:
        if username in admins:
            createuser(username)
        else:
            await bot.send_message(id,f"❌@{username} 𝘯𝘰 𝘭𝘦 𝘩𝘢𝘯 𝘥𝘢𝘥𝘰 𝘢𝘤𝘤𝘦𝘴𝘰❌")
            return
    if "/start" in msg:
        await message.reply(f"👋𝘏𝘦𝘭𝘭𝘰 😄 @{username} 𝘵𝘦 𝘭𝘭𝘦𝘷𝘰 𝘵𝘪𝘦𝘮𝘱𝘰 𝘦𝘴𝘱𝘦𝘳𝘢𝘯𝘥𝘰. 𝘛𝘦𝘯𝘨𝘰 𝘭𝘢 𝘤𝘢𝘱𝘢𝘤𝘪𝘥𝘢𝘥 𝘥𝘦 ⬆️ 𝘢 𝘭𝘢 ☁️ 𝘚𝘰𝘺 𝘥𝘦 @Astro_Bots")
		
    elif "/calidad" in msg:
        calidad = msg.split(" ")[1]
        CONFIG[username]["calidad"] = calidad
        await bot.send_message(id, "𝘚𝘦 𝘩𝘢 𝘢𝘤𝘵𝘶𝘢𝘭𝘪𝘻𝘢𝘥𝘰 𝘭𝘢 𝘤𝘢𝘭𝘪𝘥𝘢𝘥 𝘳𝘦𝘻𝘢 𝘱𝘰𝘳 𝘲𝘶𝘦 𝘴𝘦𝘢 𝘭𝘢 𝘤𝘰𝘳𝘳𝘦𝘤𝘵𝘢✅")
	    
    elif "/zips" in msg:
        zips = msg.split(" ")[1]
        CONFIG[username]["zips"] = zips
        await bot.send_message(id,"📚𝘏𝘢𝘴 𝘤𝘢𝘮𝘣𝘪𝘢𝘥𝘰 𝘦𝘭 𝘵𝘢𝘮𝘢ñ𝘰 𝘥𝘦 𝘭𝘰𝘴 𝘻𝘪𝘱𝘴 𝘦𝘴 𝘵𝘶 𝘱𝘳𝘰𝘣𝘭𝘦𝘮𝘢 ✅")
    
    elif "/server" in msg:
        server = msg.split(" ")[1]
        CONFIG[username]["server"] = server
        await bot.send_message(id, "📡𝘚𝘦𝘳𝘷𝘦𝘳 𝘤𝘰𝘯𝘧𝘪𝘨𝘶𝘳𝘢𝘥𝘰")
			
    elif "/add_site" in msg:
        site = msg.split()[1]
		
        if site in stream_sites:
            await bot.send_message(id, "𝘠𝘢𝘴 𝘩𝘢𝘴 𝘢𝘤𝘵𝘪𝘷𝘢𝘥𝘰 𝘭𝘢𝘴 𝘥𝘦𝘴𝘤𝘢𝘳𝘨𝘢𝘴 𝘥𝘦 𝘦𝘴𝘵𝘦 𝘴𝘪𝘵𝘪𝘰 🤦‍♂️ 𝘯𝘰 𝘷𝘦𝘴 ?")
        else:
            stream_sites.append(site)
            await bot.send_message(id, f"𝘈𝘩𝘰𝘳𝘢 𝘥𝘦𝘴𝘤𝘢𝘳𝘨𝘰 𝘥𝘦 👉{site} ")
			
    elif "/proxy" in msg:
        zips = msg.split(" ")[1]
        proxy = iprox(zips.replace("socks5://",""))
        CONFIG[username]["proxy"] = f"socks5://{proxy}"
        await bot.send_message(id,"📡𝘚𝘦 𝘨𝘶𝘢𝘳𝘥𝘰 𝘦𝘭 𝘱𝘳𝘰𝘹𝘺 𝘤𝘰𝘳𝘳𝘦𝘤𝘵𝘢𝘮𝘦𝘯𝘵𝘦")
    
    elif "/off_proxy" in msg:
        CONFIG[username]["proxy"] = ""
        await bot.send_message(id,"📡𝘚𝘦 𝘢𝘤𝘢𝘣𝘢 𝘥𝘦 𝘦𝘭𝘪𝘮𝘪𝘯𝘢𝘳 𝘦𝘭 𝘱𝘳𝘰𝘹𝘺 𝘤𝘰𝘳𝘳𝘦𝘤𝘵𝘢𝘮𝘦𝘯𝘵𝘦")
    
    elif "/add" in msg:
        if username in admins:  
            usernames = msg.split(" ")[1]  
            createuser(usernames)  
            await bot.send_message(id, f"𝘏𝘢𝘴 𝘢𝘨𝘳𝘦𝘨𝘢𝘥𝘰 𝘢𝘭 👤 @{usernames} 𝘢𝘭 𝘉𝘰𝘵 😁 𝘮𝘢𝘴 𝘷𝘢𝘭𝘦 𝘲𝘶𝘦 𝘢𝘱𝘳𝘰𝘣𝘦𝘤𝘩𝘦 𝘴𝘶 𝘦𝘴𝘵𝘢𝘯𝘤𝘪𝘢  👌")
        else:
           await bot.send_message(id, "‼️𝘚𝘰𝘭𝘰 𝘱𝘢𝘳𝘢 𝘢𝘥𝘮𝘪‼️")
           return

    elif "/ban" in msg:
        if username in admins:  
            usernames = msg.split(" ")[1]  
            deleteuser(usernames)  
            await bot.send_message(id, f"𝘏𝘢𝘴 𝘩𝘦𝘤𝘩𝘢𝘥𝘰 𝘢 @ {usernames} 𝘥𝘦𝘭 𝘣𝘰𝘵 𝘢 𝘣𝘢𝘴𝘦 𝘥𝘦 𝘱𝘶𝘳𝘢𝘴 𝘱𝘢𝘵𝘢𝘥𝘢𝘴 𝘤𝘳𝘦𝘰 𝘲𝘶𝘦 𝘦𝘴𝘵𝘦 𝘮𝘦𝘯 𝘯𝘰 𝘳𝘦𝘨𝘳𝘦𝘴𝘢𝘳𝘢.🤣")
        else:
            await bot.send_message(id, "‼️𝘚𝘰𝘭𝘰 𝘈𝘥𝘮𝘪‼️")
            return

    elif "/mode" in msg:
        try:
            if CONFIG[username]["mode"] == "moodle":
                CONFIG[username]["mode"] = "uo"
                await bot.send_message(id, "𝕄𝕆𝔻𝕆 𝕌𝕆 ℙ𝕆ℝ ℂ𝕆𝕆𝕂𝕀𝔼𝕊")
            else:
                CONFIG[username]["mode"] = "moodle"
                await bot.send_message(id, "𝕄𝕆𝔻𝕆 𝕄𝕆𝔻𝔻𝕃𝔼")
        except Exception as e:
            await bot.send_message(id, f"𝔼ℝℝ𝕆ℝ 𝔸𝕃 ℂ𝔸𝕄𝔹𝕀𝔸ℝ 𝔼𝕃 𝕄𝕆𝔻𝕆: {e}")	


    elif "/seven" in msg:
        try:
            parts = msg.split()
            if len(parts) >= 2:
                item_name = parts[1]
                volume_size = None  # Default: No volume splitting
                if len(parts) == 3:
                    try:
                        volume_size = int(parts[2]) * 1024 * 1024  # Convert to bytes (MB to bytes)
                    except ValueError:
                        await bot.send_message(id, "Tamaño de volumen inválido. Usa un número entero.")
                        return

                current_directory = user_data.get(id, {}).get('current_directory', os.path.join(str(id)))
                item_path = os.path.join(current_directory, item_name)

                if os.path.exists(item_path):
                    if os.path.isfile(item_path) or os.path.isdir(item_path):
                        try:
                            compressed_files = sevenzip(item_path, volume=volume_size)
                            await bot.send_message(id, f"Archivo/Carpeta '{item_name}' comprimido correctamente.")
                            if len(compressed_files) > 1:
                                await bot.send_message(id, f"Se crearon {len(compressed_files)} archivos comprimidos.")
                                for file_name in compressed_files:
                                    await bot.send_message(id, f" - {file_name}")
                        except Exception as e:
                            await bot.send_message(id, f"Error al comprimir: {e}")
                    else:
                        await bot.send_message(id, f"Error: '{item_name}' no es un archivo o carpeta válido.")
                else:
                    await bot.send_message(id, f"Error: '{item_name}' no existe.") 
            else:
                await bot.send_message(id, "‼️Uso incorrecto del comando‼️. 👀Usa/seven <nombre de archivo/carpeta> [tamaño de volumen en MB]")
        except (IndexError, ValueError):
            await bot.send_message(id, "‼️Uso incorrecto del comando‼️. 👀Usa/seven <nombre de archivo/carpeta> [tamaño de volumen en MB]")
        except Exception as e:
            await bot.send_message(id, f"Error al comprimir: {e}")



			
	    
			
    elif "/auto" in msg:
        try:
            if CONFIG[username]["automatic"] == "off":
                CONFIG[username]["automatic"] = "on"
                await bot.send_message(id, "✅𝘍𝘦𝘭𝘪𝘤𝘪𝘥𝘢𝘥𝘦𝘴 𝘮𝘦 𝘩𝘢𝘴 𝘱𝘶𝘦𝘴𝘵𝘰 𝘦𝘯 𝘮𝘰𝘥𝘰 𝘢𝘶𝘵𝘰𝘮𝘢𝘵𝘪𝘤𝘰 😁✅")
            else:
                CONFIG[username]["automatic"] = "off"
                await bot.send_message(id, "😢❎𝘖𝘺𝘦 𝘮𝘦 𝘩𝘢𝘴 𝘴𝘢𝘤𝘢𝘥𝘰 𝘥𝘦 𝘢𝘶𝘵𝘰𝘮𝘢𝘵𝘪𝘤𝘰 𝘲𝘶𝘦 𝘵𝘦 𝘱𝘢𝘴𝘢❎")
        except Exception as e:
            await bot.send_message(id, f"‼️𝘌𝘳𝘳𝘰𝘳 𝘢𝘭 𝘤𝘢𝘮𝘣𝘪𝘢𝘳 𝘢 𝘢𝘶𝘵𝘰𝘮𝘢𝘵𝘪𝘤𝘰‼️: {e}")			
			
			
			
	
    elif "/config" in msg:
        parts = msg.split(" ", 2)  
        if len(parts) == 3:
            _, host, token = parts  

        
            global_conf["host"] = host
            global_conf["token"] = token 

            await bot.send_message(id, f"✔️𝘊𝘰𝘯𝘧𝘪𝘨𝘶𝘳𝘢𝘤𝘪𝘰𝘯 𝘢𝘭𝘮𝘢𝘤𝘦𝘯𝘢𝘧𝘢 𝘤𝘰𝘳𝘳𝘦𝘤𝘵𝘢𝘮𝘦𝘯𝘵𝘦: \n 👌Host: {host}\n 💪Token: {token}")
        else:
            await bot.send_message(id, "💢𝘌𝘳𝘳𝘰𝘳 𝘢𝘭 𝘨𝘶𝘢𝘳𝘥𝘢𝘳 𝘭𝘢 𝘱𝘪𝘯𝘤𝘩𝘦 𝘤𝘰𝘯𝘧𝘪𝘨𝘶𝘳𝘢𝘤𝘪𝘰𝘯, 𝘍𝘰𝘳𝘮𝘢𝘵𝘰 ✔️𝘊𝘰𝘳𝘳𝘦𝘤𝘵𝘰: /config host token")
						
			
			
    elif "/next" in msg:
        try:
        
            parts = msg.split()  
            if len(parts) >= 2:
                index = int(parts[1])  

                count = 0
                directory = os.path.join(str(id))
                if os.path.exists(directory):
                    for item in listdir(directory):
                        if isfile(join(directory, item)):
                            if count == index:
                                filename = item  # Obtener el nombre del archivo
                                msg = await bot.send_message(id, "Comenzando a subir")
                                await upx(f"{id}/{filename}", msg, username)
                                
                                return  # Termina la ejecución del comando
                            count += 1
                    await bot.send_message(id, f"Índice {index} no encontrado.") 
                else:
                    await bot.send_message(id, f"La ruta {directory} no existe.") 
            else:
                await bot.send_message(id, "‼️Uso incorrecto del comando‼️. 👀Usa/next <índice>")
        except (IndexError, ValueError):
            await bot.send_message(id, "a Occurido un error al subir el archivo o en el comando")
        except Exception as e:
            await bot.send_message(id, f"Error al subir el archivo: {e}")


			
    elif "/up" in msg:
        try:
            parts = msg.split()  
            if len(parts) >= 2:
                file_name = parts[1]  

                current_directory = user_data.get(id, {}).get('current_directory', os.path.join(str(id)))
                if os.path.exists(current_directory):
                    file_path = os.path.join(current_directory, file_name)
                    if os.path.isfile(file_path):
                        msg = await bot.send_message(id, "Comenzando a subir")
                        await uploadfile(file_path, msg, username)  
                        return  # Termina la ejecución del comando
                    else:
                        await bot.send_message(id, f"Error: '{file_name}' no es un archivo válido.")
                else:
                    await bot.send_message(id, f"La ruta {current_directory} no existe.") 
            else:
                await bot.send_message(id, "‼️Uso incorrecto del comando‼️. 👀Usa /up <nombre de archivo>")
        except (IndexError, ValueError):
            await bot.send_message(id, "‼️Uso incorrecto del comando‼️. 👀Usa /up <nombre de archivo>")
        except Exception as e:
            await bot.send_message(id, f"Error al subir el archivo: {e}")      
      


    elif "/rename" in msg:
        try:
            parts = msg.split()
            if len(parts) == 3:
                old_filename = parts[1]
                new_filename = parts[2]

                current_directory = user_data.get(id, {}).get('current_directory', os.path.join(str(id)))
                if os.path.exists(current_directory):
                    old_path = os.path.join(current_directory, old_filename)
                    new_path = os.path.join(current_directory, new_filename)

                    if os.path.isfile(old_path):
                        os.rename(old_path, new_path)
                        await bot.send_message(id, f"Archivo {old_filename} renombrado a {new_filename}.")

                        # Update the folder_indexes dictionary 
                        for index, name in user_data[id]['folder_indexes'].items():
                            if name == old_filename:
                                user_data[id]['folder_indexes'][index] = new_filename
                                break
                        return  # Termina la ejecución del comando
                    else:
                        await bot.send_message(id, f"Error: '{old_filename}' no es un archivo válido.")
                else:
                    await bot.send_message(id, f"La ruta {current_directory} no existe.")
            else:
                await bot.send_message(id, "‼️Uso incorrecto del comando‼️. 👀Usa/rename <Nombreactual> <NombreNuevo>")
        except (IndexError, ValueError):
            await bot.send_message(id, "‼️Uso incorrecto del comando‼️. 👀Usa/rename <Nombreactual> <NombreNuevo>")
        except Exception as e:
            await bot.send_message(id, f"‼️Error al renombrar el archivo‼️: {e}")
			
			
    elif "/del_cloud" in msg:
        filename = msg.split(" ")[1]
        msg = await bot.send_message(id, "Borrando")
        await delcloud(filename, msg, username)
			
    elif "/rm" in msg:
        try:
            parts = msg.split()
            index = int(parts[1])  # Obtiene el índice del archivo a borrar
            
            current_directory = user_data.get(id, {}).get('current_directory', os.path.join(str(id)))
            
            if os.path.exists(current_directory):
                # Get the name of the file/folder from folder_indexes
                file_name = user_data[id].get('folder_indexes', {}).get(index)
                if file_name:
                    file_to_delete = os.path.join(current_directory, file_name)
                    
                    if os.path.isfile(file_to_delete):
                        os.remove(file_to_delete)
                        await bot.send_message(id, f"Archivo {file_name} eliminado correctamente.")
                        # Update folder_indexes after removing the file
                        del user_data[id]['folder_indexes'][index]
                    elif os.path.isdir(file_to_delete):
                        import shutil
                        shutil.rmtree(file_to_delete)
                        await bot.send_message(id, f"Carpeta {file_name} eliminada correctamente.")
                        # Update folder_indexes after removing the folder
                        del user_data[id]['folder_indexes'][index]
                    else:
                        await bot.send_message(id, f"Error: '{file_name}' no es un archivo o carpeta válido.")
                else:
                    await bot.send_message(id, f"Índice {index} no encontrado.") 
            else:
                await bot.send_message(id, f"La ruta {current_directory} no existe.") 
        except (IndexError, ValueError):
            await bot.send_message(id, "‼️Uso incorrecto del comando‼️. 👀Usa /rm <índice>")

    elif "/del_all" in msg:
        try:
            root_directory = os.path.join(str(id))  # Get the user's root directory
            if os.path.exists(root_directory):
                # Clear folder_indexes
                user_data[id]['folder_indexes'] = {} 
                
                for item in os.listdir(root_directory):
                    item_path = os.path.join(root_directory, item)
                    if os.path.isfile(item_path):
                        os.remove(item_path)
                    elif os.path.isdir(item_path):
                        import shutil
                        shutil.rmtree(item_path)
                await bot.send_message(id, "𝕋𝕆𝔻𝕆𝕊 𝔸ℝℂℍ𝕀𝕍𝕆𝕊 𝕐 ℂ𝔸ℝℙ𝔼𝕋𝔸𝕊 ℍ𝔸ℕ 𝕊𝕀𝔻𝕆 𝔼𝕃𝕀𝕄𝕀ℕ𝔸𝔻𝕆")
            else:
                await bot.send_message(id, f"𝕃𝔸 ℝ𝕌𝕋𝔸 {root_directory} ℕ𝕆 𝔼𝕏𝕀𝕊𝕋𝔼") 
        except Exception as e:
            await bot.send_message(id, f"𝔼ℝℝ𝕆ℝ 𝔸𝕃 𝔼𝕃𝕀𝕄𝕀ℕ𝔸ℝ: {e}")	
			
    elif "/help" in msg:
        msg = "ℙ𝕠𝕣𝕗𝕒𝕧𝕠𝕣 𝕝𝕖𝕖𝕣 𝕔𝕠𝕟 𝕒𝕥𝕖𝕟𝕔𝕚𝕠𝕟\n\n"
        msg += "𝔼𝕤𝕥𝕠𝕤 𝕤𝕠𝕟 𝕝𝕠𝕤 𝕡𝕒𝕤𝕠𝕤 𝕢𝕦𝕖 𝕕𝕖𝕧𝕖𝕤 𝕦𝕤𝕒𝕣\n"
        msg += "ℂ𝕠𝕞𝕒𝕞𝕕𝕠 /zips 99\n"
        msg += "ℂ𝕠𝕞𝕒𝕞𝕕𝕠 /calidad 480p\n"
        msg += "ℂ𝕠𝕞𝕒𝕞𝕕𝕠 /auto\n"
        msg += "ℂ𝕠𝕞𝕒𝕟𝕕𝕠 /config\n"
        msg += "𝔼𝕤 𝕖𝕟 𝕖𝕤𝕖 𝕠𝕣𝕕𝕖𝕟 𝕖𝕤𝕡𝕖𝕔𝕚𝕗𝕚𝕔𝕠 𝕔𝕦𝕒𝕝𝕢𝕦𝕚𝕖𝕣 𝕠𝕥𝕣𝕒 𝕕𝕦𝕕𝕒 𝕔𝕠𝕞𝕦𝕟𝕚𝕔𝕒𝕣𝕝𝕠 𝕖𝕟 𝕖𝕝 𝕘𝕣𝕦𝕡𝕠."
        await bot.send_message(id,msg)
		
    elif "/ls" in msg:
        count = 1  # Start index from 1
        msg = f"📔Tu directorio actual ⬇️\n"
    
        # Get the current directory from user data
        current_directory = user_data.get(id, {}).get('current_directory', os.path.join(str(id))) 
    
        msg += f"📘Localización: {current_directory}\n\n"  
    
        if os.path.exists(current_directory):
            # Reset folder_indexes for the user
            user_data[id] = user_data.get(id, {})
            user_data[id]['folder_indexes'] = {}

            for item in os.listdir(current_directory):
                # Check if it's a file or a folder
                item_path = os.path.join(current_directory, item)
                if os.path.isfile(item_path):
                    size = os.path.getsize(item_path)
                    size_str = sizeof_fmt(size)
                    msg += f"{count} 📄 {item} | {size_str}\n"
                    count += 1
                elif os.path.isdir(item_path):
                    msg += f"{count} 📁 {item}\n"
                    user_data[id]['folder_indexes'][count] = item  # Store index-name mapping
                    count += 1
            msg += "/ls Ver\n"
            msg += "/back Subir un nivel\n"
            msg += "/del_all Eliminar directorio raíz"
            await bot.send_message(id, msg)
        else:
            await bot.send_message(id, f"La ruta {current_directory} no existe.")		
		
		
		
		
		
    elif "/mv" in msg:
        current_directory = user_data.get(id, {}).get('current_directory', os.path.join(str(id)))
        parts = msg.split()  
        if len(parts) == 3:
            try:
                source_name = parts[1]
                target_folder = parts[2]

                source_path = os.path.join(current_directory, source_name)
                target_path = os.path.join(current_directory, target_folder)

                if os.path.exists(source_path):
                    if os.path.isfile(source_path):
                        # Move the file
                        os.rename(source_path, os.path.join(target_path, source_name))
                        await bot.send_message(id, f"Archivo '{source_name}' movido a '{target_folder}'.")
                    elif os.path.isdir(source_path):
                        # Move the folder (using shutil for potential conflicts)
                        import shutil
                        shutil.move(source_path, target_path)
                        await bot.send_message(id, f"Carpeta '{source_name}' movida a '{target_folder}'.")
                    else:
                        await bot.send_message(id, f"Error: '{source_name}' no es un archivo o carpeta válido.")
                else:
                    await bot.send_message(id, f"Error: '{source_name}' no existe.")
            except ValueError:
                await bot.send_message(id, "‼️Uso incorrecto del comando‼️. 👀Usa: /mv [nombre archivo/carpeta] [nombre carpeta destino]")
        else:
            await bot.send_message(id, "‼️Uso incorrecto del comando‼️. 👀Usa: /mv [nombre archivo/carpeta] [nombre carpeta destino]")		
		
    elif "/back" in msg:
        current_directory = user_data.get(id, {}).get('current_directory', os.path.join(str(id)))
    
    # Check if we are already in the root directory
        if current_directory == os.path.join(str(id)):
            await bot.send_message(id, "Ya estás en el directorio raíz.")
            return

    # Get the parent directory
        parent_directory = os.path.dirname(current_directory)

    # Update the user's current directory in user_data
        user_data[id] = user_data.get(id, {})
        user_data[id]['current_directory'] = parent_directory

        await bot.send_message(id, f"Directorio cambiado a: {parent_directory}")
    # Automatically execute /ls to show the new directory
        await bot.send_message(id, "/ls") 


		
		

    elif "/cd" in msg:
        current_directory = user_data.get(id, {}).get('current_directory', os.path.join(str(id)))
        try:
            folder_index = int(msg.replace("/cd ", ""))
            # Get folder name from user_data
            target_folder = user_data[id]['folder_indexes'].get(folder_index) 
            if target_folder:
                new_directory = os.path.join(current_directory, target_folder)
                if os.path.isdir(new_directory):
                    # Update the user's current directory in user_data
                    user_data[id] = user_data.get(id, {})
                    user_data[id]['current_directory'] = new_directory
                    await bot.send_message(id, f"Directorio cambiado a: {target_folder}")
                    # Automatically execute /ls to show the new directory
                    await bot.send_message(id, "/ls") 
                else:
                    await bot.send_message(id, f"La carpeta '{target_folder}' no existe.")
            else:
                await bot.send_message(id, "indice de carpeta invalido.")
        except ValueError:
            await bot.send_message(id, "‼️Uso incorrecto del comando‼️. 👀Usa: /cd [numero de carpeta]")


			
		
    elif "/mkdir" in msg:
        folder_name = msg.replace("/mkdir ", "")  # Extract the folder name from the message
        directory = os.path.join(str(id), folder_name)  # Construct the full path

        if os.path.exists(directory):
            await bot.send_message(id, f"La carpeta '{folder_name}' ya existe.")
        else:
            try:
                os.makedirs(directory)  # Create the directory
                await bot.send_message(id, f"Carpeta '{folder_name}' creada correctamente.")
            except OSError as e:
                await bot.send_message(id, f"Error al crear la carpeta: {e}") 		
		
		
			
    elif "/search" in msg:
        parts = msg.split(" ")
        if len(parts) == 3:
            tag = parts[1]
            name = parts[2]
            results = search(name=name, tag=tag)
            item = results[0]
            info = get_info(item, include_down_url=True)
            name = info["name"]
            text = info["text"]
            url = info["url"]
            url_temp["Actual_url"] = url
            msg = f"📃Nombre: {name}\n"
            msg += f"📜Descripcion: {text}\n\n"
            msg += f"🔗Link: {url}"
        
            @Client.on_callback_query(filters.regex(r"^/download"))
            async def download_callback(client, query):
                url = query.data.split(" ")[1]  # Obtén la URL del callback_data
    # Llama a la función download_file() con los parámetros necesarios
                await download_file(url, id, query.message, callback=download_func)  # Usa query.message para el mensaje
                await query.answer("Descargando archivo...")  # Envía una respuesta al usuario 
		

        # Crea un botón con el comando "/download"
            keyboard = InlineKeyboardMarkup([[InlineKeyboardButton("Descargar", callback_data="/download")]])

        # Envía el mensaje con el botón
            msg = await bot.send_message(id, msg, reply_markup=keyboard)
        else:	
            await bot.send_message(id, "Error Debe poner /search android Telegram")
	
    elif message.video or message.audio or message.photo or message.document or message.sticker or message.animation:
        try:
            filename = str(message).split('"file_name": ')[1].split(",")[0].replace('"',"")
            filesize = int(str(message).split('"file_size":')[1].split(",")[0])
        except:
            filename = str(randint(11111,99999))
        msg = await bot.send_message(id,"⬇️Descargando...")
        start = time.time()
        path = await message.download(file_name=f"{id}/{filename}",progress=download_func,progress_args=(filename,start,msg))
        traffico += filesize  
        await msg.edit("✅Archivo descargado.")

    # Comprueba si el modo automático está activado
        if CONFIG[username]["automatic"] == "on":
            if CONFIG[username]["mode"] == "moodle":
                await uploadfile(f"{id}/{filename}", msg, username)
            else:
                await upx(f"{id}/{filename}", msg, username)
				
    elif msg.startswith("https") and not "www.mediafire.com" in msg and not any(site in msg for site in stream_sites):
        url = msg.split(" ")[0]
        msg = await bot.send_message(id, "⬇️Descagrando")
        filename = await download_file(url, id, msg, callback=download_func)
        if filename:
            await msg.edit("Descargado correctamente")
            
            if CONFIG[username]["automatic"] == "on":
                if CONFIG[username]["mode"] == "moodle":
                    await uploadfile(f"{id}/{filename}", msg, username)
                else:
                    await upx(f"{id}/{filename}", msg, username)
        
        

    elif "https://www.mediafire.com/" in msg:
        print("Descargando de MediaFire")
    
        url = msg.split(" ")[0]
        msg = await bot.send_message(id, "Descargando de MediaFire")
        filename = await download_mediafire(url, id, msg, callback=download_func)
        if filename:
            msg.edit(f"Se a descargado el archivo {filename} compruebe usando /ls")
        
        # Comprueba si el modo automático está activado
            if CONFIG[username]["automatic"] == "on":
                if CONFIG[username]["mode"] == "moodle":
                    await uploadfile(f"{id}/{filename}", msg, username)
                else:
                    await upx(f"{id}/{filename}", msg, username)
      
    elif any(site in msg for site in stream_sites):
        url = msg.split(" ")[0]
        msg = await bot.send_message(id, "⬇️ Descargando...")
        quality = CONFIG[username]["calidad"]
        if "None" in quality:
            await bot.send_message(id, "Porfavor configura la calidad a descargar. Ejemplo /calidad 480p")
        else:
            filename = await ytdlp_downloader(url, id, msg, username, lambda data: download_progres(data,msg,format,username), quality)	
            if filename:
                await msg.edit(f"Se a descargado el archivo {filename} use el comando /ls")
            
            # Comprueba si el modo automático está activado
                if CONFIG[username]["automatic"] == "on":
                    if CONFIG[username]["mode"] == "moodle":
                        await uploadfile(f"{filename}", msg, username)
                    else:
                        await upx(f"{filename}", msg, username)
                    
                
            else:
                await bot.send_message("No se a completado la descarga vuelva a intentarlo")

			

			
    elif "/status" in msg:
        system_info = await get_system_info()        	
        cpu = system_info['cpu_percent']
        ram = system_info['ram_total']
        ram_used = system_info['ram_used']
        ram_percent = system_info['ram_percent']
        ram_free = system_info['ram_free']
        Disk = system_info['disk_total']
        Disk_used = system_info['disk_used']
        Disk_free = system_info['disk_free']
        downlink = traffic["downlink"]
        uplink = traffic["uplink"]
        traffics = sizeof_fmt(traffico)
        msg = "📊𝗗𝗮𝘁𝗼𝘀 𝗱𝗲𝗹 𝘀𝗶𝘀𝘁𝗲𝗺𝗮\n\n"
        msg += f"💻𝗖𝗣𝗨: {cpu}%\n"
        msg += f"💾𝗥𝗮𝗺: {ram}\n"
        msg += f"📉𝗨𝘀𝗼 𝗱𝗲 𝗹𝗮 𝗿𝗮𝗺: {ram_used}\n"
        msg += f"💽𝗥𝗮𝗺 𝗱𝗶𝘀𝗽𝗼𝗻𝗶𝗯𝗹𝗲: {ram_free}\n"
        msg += f"📶𝗣𝗼𝗿𝗰𝗲𝗻𝘁𝗮𝗴𝗲 𝗿𝗮𝗺: {ram_percent}%\n"
        msg += f"💿𝗗𝗶𝘀𝗰𝗼 𝘁𝗼𝘁𝗮𝗹: {Disk}\n"
        msg += f"📀𝗗𝗶𝘀𝗰𝗼 𝘂𝘀𝗮𝗱𝗼: {Disk_used}\n"
        msg += f"🗃️𝗗𝗶𝘀𝗰𝗼 𝗹𝗶𝗯𝗿𝗲: {Disk_free}\n"
        msg += "⚡️𝗧𝗿𝗮𝗳𝗶𝗰𝗼 𝗲𝗻 𝗹𝗮 𝗿𝗲𝗱\n\n"
        msg += f"⬇️𝗗𝗲𝘀𝗰𝗮𝗿𝗴𝗮𝗻𝗱𝗼: {downlink}/s\n"
        msg += f"⬆️𝗦𝘂𝗯𝗶𝗲𝗻𝗱𝗼: {uplink}/s\n\n"
        msg += f"𝗧𝗿𝗮𝗳𝗶𝗰𝗼 {traffics}"
        await bot.send_message(id,msg)
		
		
                
import time
from time import localtime

SECOND = None  # Inicializa la variable global

def sizeof_fmt(size):
    """Convierte el tamaño a un formato legible."""
    if size is None:
        return "0 B"  # Manejo de None
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size < 1024:
            return f"{size:.2f} {unit}"
        size /= 1024
    return f"{size:.2f} TB"

def porcent(index, max_value):
    """Calcula el porcentaje."""
    if max_value == 0:  # Para evitar división por cero
        return 0
    porcent = index / max_value
    porcent *= 100
    return round(porcent)

async def download_func(current, total, filename, starttime, msg):
    """Muestra el progreso de la descarga."""

    def text_progress(index, max_value):
        """Genera una representación visual del progreso."""
        try:
            if max_value < 0:
                max_value += 0
            porcent = index / max_value * 100
            porcent = round(porcent)
            make_text = '['
            for index_make in range(1, 15):
                make_text += '■' if porcent >= index_make * 5 else '□'
            make_text += ']'
            return make_text
        except Exception as ex:
            print(f"Error en text_progress: {ex}")
            return ''

    global SECOND
    try:
        speed = (current / (time.time() - starttime)) if starttime else 0  # Calcula la velocidad
        percentage = porcent(current, total)  # Llama a la función porcent

        message = "📥Download File.... \n"
        message += f"{text_progress(current, total)}, {percentage}%\n"
        message += f"📥 Download: {sizeof_fmt(current)}*\n"
        message += f"💾 Total: {sizeof_fmt(total)}\n"
        message += f"🏎️ Velocity: {sizeof_fmt(speed)}\n"

        current_second = localtime().tm_sec
        
        # Actualiza el mensaje solo si ha cambiado el segundo
        if SECOND is None or current_second != SECOND:
            try:
                await msg.edit(message)
            except Exception as ex:
                print(f"Error al actualizar el mensaje: {ex}")
        
        SECOND = current_second

    except Exception as ex:
        print(f"Error en download_func: {ex}")

	
	
def upload_func(current,total,starttime,filename,msg):
    speed = time.time() - starttime  
    if speed > 0:  
        speed = current / speed
    else:
        speed = 0  
    percentage = int((current / total) * 100)

    message = "🔽 𝙎𝙪𝙗𝙞𝙚𝙣𝙙𝙤*\n"
    message += f"🔽 *𝙎𝙪𝙗𝙞𝙙𝙤: {sizeof_fmt(current)}\n"
    message += f"🗃️ 𝙏𝙤𝙩𝙖𝙡: {sizeof_fmt(total)}\n"
    message += f"🐆 𝙑𝙚𝙡𝙤𝙘𝙞𝙙𝙖𝙙: {sizeof_fmt(speed)}\n"
    message += f"📉 𝙋𝙤𝙧𝙘𝙚𝙣𝙩𝙖𝙟𝙚: {percentage}%\n"
    traffic["uplink"] = sizeof_fmt(speed)

    global SECOND
    # Call localtime from the time module
    if SECOND != localtime().tm_sec: 
        try:
            msg.edit(message)
        except Exception as ex:
            print(ex)
            pass
    SECOND = localtime().tm_sec


class UploadProgress(BufferedReader):
    def __init__(self,file,callback):
        f = open(file, "rb")
        self.filename = file.split("/")[-1]
        self.__read_callback = callback
        super().__init__(raw=f)
        self.start = time.time()
        self.length = os.path.getsize(file)
    
    def read(self, size=None):
        calc_sz = size
        if not calc_sz:
            calc_sz = self.length - self.tell()
        self.__read_callback(self.tell(), self.length,self.start,self.filename)
        return super(UploadProgress, self).read(size)
        
async def uploadfile(file, msg, username):
    global global_conf
    original_filename = os.path.basename(file)  # Obtiene el nombre de archivo de la ruta original
    fsize = Path(file).stat().st_size
    zips_size = 1024 * 1024 * int(CONFIG[username]["zips"])


    path = [file]
    if fsize > zips_size:
        await msg.edit("📚𝘾𝙤𝙢𝙥𝙧𝙞𝙢𝙞𝙚𝙣𝙙𝙤 𝙖𝙧𝙘𝙝𝙞𝙫𝙤...")
        path = sevenzip(file, volume=zips_size)

    try:
        if CONFIG[username]["proxy"] == "":
            connector_on = aiohttp.TCPConnector()
        else:
            connector_on = aiohttp_socks.ProxyConnector.from_url(CONFIG[username]["proxy"])
        async with aiohttp.ClientSession(connector=connector_on) as session:
            token = global_conf["token"]
            
            urls = []
            if token:
                for fpath in path:
                    await msg.edit(f"⬆️𝙎𝙪𝙗𝙞𝙚𝙣𝙙𝙤 𝙖𝙧𝙘𝙝𝙞𝙫𝙤𝙨...")
                    file = UploadProgress(
                        fpath,
                        lambda current, total, start, filename: upload_func(
                            current, total, start, filename, msg
                        ),
                    )
                    upload = await uploadtoken(file, token, session)
                    if upload:
                        url = upload
                        await msg.edit(
                            "✅Subida completada. Procediendo a convertir el link a perfil..."
                        )

                        if url:
                            url = url.replace("draftfile.php/", "webservice/draftfile.php/")
                            url = url + "?token=" + token
                            urls.append(url)
                            await msg.edit(f"✅𝗘𝘅𝗶𝘁𝗼 𝗲𝗻 𝗲𝗹 𝗽𝗿𝗼𝗰𝗲𝘀𝗼 𝗱𝗲 𝘀𝘂𝗯𝗶𝗱𝗮✅")
                            

                # Mover la lógica de escritura del archivo fuera del bucle for
                print(urls)
                if urls:
                    with open(f"{original_filename}.txt", "w") as txt:  # Usa original_filename
                        txt.write("\n".join(urls))
                    await bot.send_document(username, f"{original_filename}.txt")
                    os.remove(f"{original_filename}.txt")
                    
                else:
                    await msg.edit(f"❌ 𝗢𝗰𝘂𝗿𝗿𝗶𝗼 𝘂𝗻 𝗲𝗿𝗿𝗼𝗿 𝗮𝗹 𝘀𝘂𝗯𝗶𝗿 𝗲𝗹 𝗮𝗿𝗰𝗵𝗶𝘃𝗼 😢.")
            else:
                await bot.send_message(
                    username,
                    "‼️𝗡𝗼 𝘀𝗲 𝗰𝗼𝗺𝗽𝗹𝗲𝘁𝗼 𝗲𝗹 𝗶𝗻𝗶𝗰𝗶𝗼 𝗱𝗲 𝘀𝗲𝗰𝗰𝗶𝗼𝗻 𝗽𝗼𝘀𝗶𝗯𝗹𝗲𝘀 𝗿𝗮𝘇𝗼𝗻𝗲𝘀: 𝙬𝙚𝙗 𝙘𝙖𝙞𝙙𝙖, 𝙩𝙤𝙠𝙚𝙣 𝙞𝙣𝙘𝙤𝙧𝙧𝙚𝙘𝙩𝙤, 𝙩𝙤𝙠𝙚𝙣 𝙗𝙖𝙣𝙚𝙖𝙙𝙤‼️",
                )
                return
    except Exception as ex:
        traceback.print_exc()
        await bot.send_message(username, f"{ex}")


async def uploadtoken(f, token, session):
    try:
        # Declara global_conf como global
        global global_conf

        # Obtén el host desde el diccionario
        host = global_conf["host"]
        
        

        url = f"{host}webservice/upload.php"
        query = {"token": token, "file": f}
        async with session.post(url, data=query, ssl=True) as response:
            text = await response.text()
            print(text)
            dat = loads(text)[0]
            url = f"{host}draftfile.php/{str(dat['contextid'])}/user/draft/{str(dat['itemid'])}/{str(quote(dat['filename']))}"
            return url
    except:
        traceback.print_exc()
        return None

import yt_dlp
import aiohttp
import time

def download_progres(data,message,format, username):
    global CONFIG
    quality = CONFIG[username]["calidad"]
    if data["status"] == "downloading":
        filename = data["filename"].split("/")[-1]
        _downloaded_bytes_str = data["_downloaded_bytes_str"]
        _total_bytes_str = data["_total_bytes_str"]
        if _total_bytes_str == "N/A":
            _total_bytes_str = data["_total_bytes_estimate_str"]        
        _speed_str = data["_speed_str"].replace(" ","")
        _eta_str = data["_eta_str"]
        _format_str = format        
        msg= f"{filename}\n"
        msg+= f"💾Descargado: {_downloaded_bytes_str}\n"
        msg+= f"📦Total: {_total_bytes_str} \n"
        msg+= f"⚡️Velocidad: {_speed_str}/s \n"
        msg+= f"🎥Calidad: {quality}\n"
        msg+= f"⏰Tiempo restante: {_eta_str}"
        traffic["downlink"] = _speed_str
        global SECOND 
        if SECOND != localtime().tm_sec:
        #if int(localtime().tm_sec) % 2 == 0 :
            try:
                message.edit(msg,reply_markup=message.reply_markup)
            except:
                pass
        SECOND = localtime().tm_sec

		
async def delcloud(filename, msg, username):
        base_url = "https://nube.uo.edu.cu/"  # Reemplaza con tu URL Nextcloud válida
        nextcloud_client = NextcloudClient(base_url)
        v = "1547"
        type = "uo"
        resp = requests.post("http://apiserver.alwaysdata.net/session",json={"type":type,"id":v},headers={'Content-Type':'application/json'})
        data = json.loads(resp.text) 
        await msg.edit("Borrando........")		
        result = nextcloud_client.delete_nexc(url = f'{base_url}remote.php/webdav/?dir=/{filename}', cookies=data)
        await msg.edit(f"{result}")
        return
		
		
		
async def upx(filename, msg, username):
        global server_s
        base_url = "https://nube.uo.edu.cu/"  # Reemplaza con tu URL Nextcloud válida
        nextcloud_client = NextcloudClient(base_url)
        type = "uo"
        v = CONFIG[username]["server"]
        print(v)
        resp = requests.post("http://apiserver.alwaysdata.net/session",json={"type":type,"id":v},headers={'Content-Type':'application/json'})
        data = json.loads(resp.text) 
        await msg.edit(data)		
        result = await nextcloud_client.upload_file(filename, data)
        if "https://nube.uo.edu.cu/" in result:
            await msg.edit(f"✅𝙀𝙭𝙞𝙩𝙤 𝙚𝙣 𝙡𝙖 𝙨𝙪𝙗𝙞𝙙𝙖✅:\n {result}")
        else:
            await msg.edit("‼️𝙊𝙘𝙪𝙧𝙧𝙞𝙤 𝙪𝙣 𝙚𝙧𝙧𝙤𝙧 ‼️")
		
        return
			     
def generate():
    prefix = "web-file-upload-"
    random_string = ''.join(random.choice('abcdefghijklmnopqrstuvwxyz0123456789') for _ in range(32))
    unique_id = str(uuid.uuid4().time_low)

    random_name = f"{prefix}{random_string}-{unique_id}"
    return random_name

	

async def file_renamer(file):
    filename = file.split("/")[-1]
    path = file.split(filename)[0]
    if len(filename)>21:
        p = filename[:10]
        f = filename[-11:]
        filex = p + f
    else:
         filex = filename
    filename = path + re.sub(r'[^A-Za-z0-9.]', '', filex)
    os.rename(file,filename)
    return filename
	

				 
		
async def ytdlp_downloader(url, id, msg, username, callback, format):
    """Descarga un video de YouTube utilizando yt-dlp."""

    class YT_DLP_LOGGER(object):
        def debug(self, msg):
            pass
        def warning(self, msg):
            pass
        def error(self, msg):
            pass

    resolution = str(format)
    dlp = {
        "logger": YT_DLP_LOGGER(),
        "progress_hooks":[callback],
        "outtmpl": f"{id}/%(title)s.%(ext)s",
        "format": f"bestvideo[height<={resolution}]+bestaudio/best[height<={resolution}]"  # Prioritize height first
    }

    downloader = yt_dlp.YoutubeDL(dlp)
    print("Se esta descargando mamawebo")
    loop = asyncio.get_running_loop()

    # Obtén información sobre el video
    filedata = await loop.run_in_executor(None, downloader.extract_info, url)

    # Verifica si la descarga está dividida
    if "entries" in filedata:
        # Descarga dividida
        total_size = 0
        for entry in filedata["entries"]:
            total_size += entry["filesize"]
    else:
        # Descarga completa
        if "filesize" in filedata:
            total_size = filedata["filesize"]
        else:
            # No se puede obtener el tamaño total
            total_size = 0

    # ... (tu código para el progreso de la descarga)
    filepath = downloader.prepare_filename(filedata)
    filename = filedata["requested_downloads"][0]["_filename"]
    return filename

def obtener_ip_publica():
  """Obtiene la IP pública usando la API de icanhazip.com."""
  try:
    response = requests.get("https://icanhazip.com/")
    return response.text.strip()
  except requests.exceptions.RequestException as e:
    print(f"Error al obtener la IP: {e}")
    return None	
	
	
	
	

async def extractDownloadLink(contents):
    for line in contents.splitlines():
        m = re.search(r'href="((http|https)://download[^"]+)', line)
        if m:
            return m.groups()[0]	
	

import asyncio
import aiohttp
import certifi
import ssl	


async def download_file(url, id, msg, callback=None):
    global traffico
    """Downloads a file from MediaFire and saves it to a specified path."""

    # Create a context object
    context = ssl.create_default_context(cafile=certifi.where())  

    # Use the ssl parameter with the context object
    async with aiohttp.ClientSession(
        connector=aiohttp.TCPConnector(
            ssl=context  # Use the SSL context directly 
        )
    ) as session:
        response = await session.get(url)

        response = await session.get(url)
        filename = url.split("/")[-1]

        # Save to {id}/{filename} 
        path = f"{id}/{filename}"
        f = open(path, "wb")

        chunk_ = 0
        total = int(response.headers.get("Content-Length"))
        traffico += total
        start = time.time()  # Llama a la función time.time() para obtener el tiempo actual
        while True:
            chunk = await response.content.read(1024)
            if not chunk:
                break
            chunk_ += len(chunk)
            if callback:
                await callback(chunk_, total, filename, start, msg)
            f.write(chunk)
            f.flush()

        return path

@Client.on_callback_query(filters.regex(r"^download_"))  # Filtra por el prefijo "download_"
async def download_callback(client, query):
    global url_temp
    url = url_temp["Actual_url"]
    await download_file(url, id, query.message, callback=download_func)
    await query.answer("Descargando archivo...")		
		
		


	
async def download_mediafire(url, id, msg, callback=None):
    """Downloads a file from MediaFire and saves it to a specified path."""
    global traffico

    # Create a context object
    context = ssl.create_default_context(cafile=certifi.where())  

    # Use the `ssl` parameter with the context object
    session = aiohttp.ClientSession(
        connector=aiohttp.TCPConnector(
            ssl=context  # Use the SSL context directly 
        )
    )
    
    response = await session.get(url)
    url = await extractDownloadLink(await response.text())
    response = await session.get(url)
    filename = response.content_disposition.filename

    # Save to {id}/{filename} 
    path = f"{id}/{filename}"
    f = open(path, "wb")

    chunk_ = 0
    total = int(response.headers.get("Content-Length"))
    traffico += total
    start = time.time()
    while True:
        chunk = await response.content.read(1024)
        if not chunk:
            break
        chunk_ += len(chunk)
        if callback:
            await callback(chunk_, total, filename, start, msg)
        f.write(chunk)
        f.flush()

    return path

	
        
def sizeof_fmt(num, suffix='B'):
    for unit in ['', 'Ki', 'Mi', 'Gi', 'Ti', 'Pi', 'Ei', 'Zi']:
        if abs(num) < 1024.0:
            return "%3.2f%s%s" % (num, unit, suffix)
        num /= 1024.0
    return "%.2f%s%s" % (num, 'Yi', suffix)

async def get_cpu_percent():
    """Obtiene el porcentaje de uso de la CPU en un hilo separado."""
    loop = asyncio.get_event_loop()
    cpu_percent = await loop.run_in_executor(executor, psutil.cpu_percent)  # No se necesita el argumento 'interval'
    return cpu_percent

import asyncio
import psutil
import os
import time
from concurrent.futures import ThreadPoolExecutor

executor = ThreadPoolExecutor()
	
	
	
	
async def get_system_info():
    """Obtiene información del sistema y la devuelve como un diccionario."""
    
    info = {}

    # Memoria RAM
    ram = psutil.virtual_memory()
    info["ram_total"] = sizeof_fmt(ram.total)
    info["ram_used"] = sizeof_fmt(ram.used)
    info["ram_free"] = sizeof_fmt(ram.free)
    info["ram_percent"] = ram.percent

    # CPU
    info["cpu_percent"] = await get_cpu_percent()

    # Almacenamiento del disco
    disk = psutil.disk_usage('/')  # Obtener información del disco raíz ('/')
    info["disk_total"] = sizeof_fmt(disk.total)  # Convertir a GB
    info["disk_used"] = sizeof_fmt(disk.used)  # Convertir a GB
    info["disk_free"] = sizeof_fmt(disk.free)  # Convertir a GB
    info["disk_percent"] = disk.percent

    return info
   
	
	
	
	
	
def iprox(proxy):
    tr = str.maketrans(
        "@./=#$%&:,;_-|0123456789abcd3fghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ",
        "ZYXWVUTSRQPONMLKJIHGFEDCBAzyIwvutsrqponmlkjihgf3dcba9876543210|-_;,:&%$#=/.@",
    )
    return str.translate(proxy[::2], tr)
	
	
import threading
import http.server
import socketserver
# Asegúrate de importar tu módulo bot

# Función para ejecutar el servidor web
def run_server():
    PORT = 9000
    Handler = http.server.SimpleHTTPRequestHandler
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print(f"Serving at port {PORT}")
        httpd.serve_forever()

# Función para ejecutar el bot
def run_bot():
    bot.run()  # Suponiendo que 'run()' es la función que inicia tu bot

if __name__ == "__main__":
    # Inicia el servidor web en un hilo separado
    server_thread = threading.Thread(target=run_server)
    server_thread.daemon = True
    server_thread.start()

    # Ejecuta el bot en el hilo principal
    run_bot() 





