import speech_recognition as sr
from gtts import gTTS
import tempfile
import pygame
import pafy
import vlc
import requests
import os
import openai
import asyncio

r = sr.Recognizer()
openai.api_key = '***'
api_key = '***'
instance = vlc.Instance()
player = instance.media_player_new()

async def saludo():
    sol = 'Hola'

    stts = gTTS(sol, lang='es')
    with tempfile.NamedTemporaryFile(suffix='.mp3') as f:
        stts.save(os.path.expanduser("C:\\Users\\marwa\\Documents\\temp\\start.mp3"))
        f.seek(0)
        
        # Inicializar Pygame
        pygame.init()
        pygame.mixer.init()

        # Cargar audio en Pygame
        pygame.mixer.music.load(os.path.expanduser("C:\\Users\\marwa\\Documents\\temp\\start.mp3"))

        # Reproducir audio
        pygame.mixer.music.play()

        # Esperar a que el audio termine
        while pygame.mixer.music.get_busy():
            pygame.time.wait(1000)

        # FinalizaPygame
        pygame.mixer.quit()
        pygame.quit()

async def voz():

    # Inicializar Pygame
    pygame.init()
    pygame.mixer.init()

    # Cargar audio en Pygame
    pygame.mixer.music.load(os.path.expanduser("C:\\Users\\marwa\\Documents\\temp\\ex.mp3"))

    # Reproducir audio
    pygame.mixer.music.play()

    # Esperar a que el audio termine
    while pygame.mixer.music.get_busy():
        pygame.time.wait(1000)

    # FinalizaPygame
    pygame.mixer.quit()
    pygame.quit()

async def microfono():    

        with sr.Microphone() as source:
            try:
                r.adjust_for_ambient_noise(source)

                print('Di algo...')
        
                audio = r.listen(source)
            
                frase = r.recognize_google(audio, language='es-ES', show_all=True)
                ffinal = frase["alternative"][0]["transcript"]

            except Exception as e:
                print(f'Error: {e}')

        return str(ffinal).lower()

async def yt_video(query):
    
    try:
        url = f"https://www.googleapis.com/youtube/v3/search?part=snippet&q={query}&type=video&key={api_key}&maxResults=1"
        response = requests.get(url)
        data = response.json()

    except Exception as e:
        print(e)

    global lst
    global name
    lst = dict()
    for item in data["items"]:
        ids = item['id']['videoId']
        name = item['snippet']['title']
        lst[name] = ids

    urlyt = f'https://www.youtube.com/watch?v={lst[name]}'

    return urlyt

# async def yt_duration():
#     url = f'https://www.googleapis.com/youtube/v3/videos?part=contentDetails&id={lst[name]}&key={api_key}'

#     response = requests.get(url)
#     data = response.json()
#     duration = data['items'][0]['contentDetails']['duration']

#     return duration

async def main():

    while True:

        result = await microfono()
        if result.startswith('sol'):

            await saludo()

            with sr.Microphone() as source:
                r.adjust_for_ambient_noise(source)

                sonido = r.listen(source)

                try:
                    resultado = r.recognize_google(sonido, language='es-ES', show_all=True)
                    final = str(resultado["alternative"][0]["transcript"]).capitalize()

                    response = openai.Completion.create(model="text-davinci-003", prompt=final, temperature=0.7, max_tokens=4000)
                    respuesta = response.choices[0].text

                    tts = gTTS(respuesta, lang='es')
                    with tempfile.NamedTemporaryFile(suffix='.mp3') as f:
                        tts.save(os.path.expanduser("C:\\Users\\marwa\\Documents\\temp\\ex.mp3"))
                        f.seek(0)
                        await voz()

                except Exception as e:
                    print(f'Error: {e}')            
                

        elif result.startswith('quiero escuchar música sol'):
            query = 'Qué canción quieres escuchar?'

            mtts = gTTS(query, lang='es')
            with tempfile.NamedTemporaryFile(suffix='.mp3') as f:
                        mtts.save(os.path.expanduser("C:\\Users\\marwa\\Documents\\temp\\ex.mp3"))
                        f.seek(0)
                        await voz()

            with sr.Microphone() as msource:
                r.adjust_for_ambient_noise(msource)

                msonido = r.listen(msource)

                mresultado = r.recognize_google(msonido, language='es-ES', show_all=True)
                mfinal = mresultado["alternative"][0]["transcript"]

                print(f'Lo que quieres escuchar es: {mfinal}')

                url = await yt_video(mfinal)
                video = pafy.new(url)
                b_audio = video.getbestaudio()
                audio_stream = b_audio.url

                # d = await yt_duration()
                # print(d)

                media = instance.media_new(audio_stream)
                player.set_media(media)
                player.play()

    
        else:
            print('...')


if __name__ == '__main__':
    asyncio.run(main())