import streamlit as st
import urllib.parse
import speech_recognition as sr
import io

# Настройка страницы приложения
st.set_page_config(page_title="VoiceFace AI", page_icon="🎙️", layout="centered")
st.title("🎙️ Ваш фоторобот по голосу")
st.write("Назовите в микрофон свой пол, примерный возраст или просто скажите пару фраз (например: 'Я парень, мне 25 лет'). ИИ воссоздаст ваш портрет!")

# Кнопка записи аудио
audio_value = st.audio_input("Нажмите на микрофон для записи голоса")

if audio_value:
    st.info("🎙️ Голос успешно записан! Начинаем распознавание речи...")
    
    try:
        # Читаем аудиофайл из интерфейса
        audio_bytes = audio_value.read()
        
        # Настраиваем инструмент распознавания речи
        recognizer = sr.Recognizer()
        audio_file = io.BytesIO(audio_bytes)
        
        with sr.AudioFile(audio_file) as source:
            audio_data = recognizer.record(source)
            
        with st.spinner("🧠 Расшифровываем вашу речь..."):
            # Бесплатное распознавание русского текста без всяких API-ключей
            text_result = recognizer.recognize_google(audio_data, language="ru-RU")
            st.success(f"🗣️ ИИ услышал фразу: «{text_result}»")
            
        # Базовые параметры по умолчанию
        gender = "man"
        age = "30-year-old"
        detected_info = "Мужчина, 30 лет (по умолчанию)"
        
        # Простая умная логика: ищем маркеры пола и возраста в тексте речи
        text_lower = text_result.lower()
        
        if "девушка" in text_lower or "женщина" in text_lower or "пала" in text_lower or "слышала" in text_lower:
            gender = "woman"
            detected_info = "Женщина"
            
        if "парень" in text_lower or "мужчина" in text_lower or "слышал" in text_lower:
            gender = "man"
            detected_info = "Мужчина"
            
        # Ищем упоминание примерного возраста
        if "20" in text_lower or "двадцать" in text_lower:
            age = "20-year-old"
            detected_info += ", 20 лет"
        elif "40" in text_lower or "сорок" in text_lower:
            age = "40-year-old"
            detected_info += ", 40 лет"
        else:
            age = "30-year-old"
            detected_info += ", 30 лет"

        # --- ГЕНЕРАЦИЯ КАРТИНКИ ---
        with st.spinner("🎨 Нейросеть рисует ваш портрет..."):
            prompt = f"Hyperrealistic close-up studio photo of a {age} European {gender}, calm expression, highly detailed skin texture, 8k resolution, professional lighting, photorealistic"
            encoded_prompt = urllib.parse.quote(prompt)
            
            import random
            seed = random.randint(1, 99999)
            image_url = f"https://pollinations.ai{encoded_prompt}?width=1024&height=1024&model=flux&nologo=true&seed={seed}"
            
            # Выводим результат
            st.image(image_url, use_column_width=True)
            st.caption(f"Профиль построен по распознанному маркеру: {detected_info}")
                
    except sr.UnknownValueError:
        st.warning("🤖 ИИ не смог разобрать слова. Попробуйте надиктовать текст погромче и почетче!")
    except Exception as e:
        st.error(f"Произошла ошибка в коде: {e}")
