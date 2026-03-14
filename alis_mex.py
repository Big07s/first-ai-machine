import requests
import tempfile
import speech_recognition as sr
from gtts import gTTS
import os
import ollama
import re
import urllib
import webbrowser
import pyautogui

# Ассистент
screen_num = 0
messages = [{'role': 'system', 'content': 'Ты дружелюбный и вежливый ассистент.'}]
os.environ["DISPLAY"] = ":0"
def ans(messages):
    try:
        # Получаем ответ от модели
        res = ollama.chat(model='llama3:latest', messages=messages)
        
       
     
        response = res['message']['content']
                    
        return response
    except Exception as e:
        print(f"Ошибка при получении ответа от Ollama: {e}")
        return "Произошла ошибка при обработке запроса."

# URL потока с аудио
URL = "http://192.168.10.72:8080/audio.wav"  
try:
    r = requests.get(URL, stream=True, timeout=5)
    r.raise_for_status()
except Exception as e:
    print("Не удалось получить звук с камеры:", e)
    exit()

# Запись только первых 3 секунд
while True:
    r = requests.get(URL, stream=True, timeout=5)
    r.raise_for_status()
    with tempfile.NamedTemporaryFile(suffix=".wav") as f:
        chunk_size = 1024
        total_bytes = 0
        max_bytes = 6 * 16000 * 2  # 3 сек * 16kHz * 2 байта (16bit PCM)
        for chunk in r.iter_content(chunk_size=chunk_size):
            f.write(chunk)
            total_bytes += len(chunk)
            if total_bytes >= max_bytes:
                break
        f.flush()

        recognizer = sr.Recognizer()
        with sr.AudioFile(f.name) as source:
            audio = recognizer.record(source)

        try:
            text = recognizer.recognize_google(audio, language="ru-RU")
            print("Распознано:", text)
        
            if "Привет Открой проводник" in text:
                os.system(f'xdg-open "/home"')

            elif "Привет Открой в браузере" in text:
                text = text.replace("Привет Открой в браузере","").replace(" ","")

                webbrowser.open(f"https://{text}.com")
            
            elif "Привет где я" in text:
                z = os.system("ls")
                ttts = gTTS(text=z, lang='en')
                tts.save("response.mp3")
                os.system("mpv response.mp3")
            
            elif "Привет создай тест" in text:
                os.system("touch test.py")

            elif "Привет удали тест" in text:
                os.system("rm -rf test.py")
            
            elif "Привет открой тест" in text:
                os.system("nano test.py")

            elif "Привет закрой тест" in text:
                pyautogui.hotkey('ctrl'+'x')
                pyautogui.press('y')
                pyautogui.press('enter')

            elif "Привет ниже" in text:
                pyautogui.scroll(-100)
            elif "Привет выше" in text:
                pyautogui.scroll(100)

            elif "Привет напиши" in text or "Привет Напиши"  in text:
                text = text.replace("Привет напиши","").replace("Привет Напиши"," ")
                pyautogui.write(text,interval=0.1)

            elif "Привет сделай скриншот" in text:
                screen_num+=1
                pyautogui.screenshot(f"screenshot{screen_num}.png")

            

            elif text == "пока":
                break

            elif "Привет" in text:


                messages.append({'role': 'user', 'content': text})
                response = ans(messages)
                

                
                tts = gTTS(text=response, lang='ru')
                tts.save("response.mp3")
                os.system("mpv response.mp3")  # Воспроизведение аудио с помощью mpv

            elif "дырка" in text:
                messages[:] = [messages[0]]

        except sr.UnknownValueError:
            print("Не удалось распознать речь")
        except sr.RequestError as e:
            print(f"Ошибка сервиса распознавания: {e}")
