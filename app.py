import streamlit as st
import urllib.parse
import numpy as np

# Настройка страницы приложения
st.set_page_config(page_title="VoiceFace AI", page_icon="🎙️", layout="centered")
st.title("🎙️ Ваш фоторобот по голосу")
st.write("Запишите ваш голос, и ИИ воссоздаст ваш реалистичный портрет.")

# Кнопка записи аудио
audio_value = st.audio_input("Нажмите на микрофон для записи голоса")

if audio_value:
    st.info("🎙️ Голос успешно записан! Начинаем анализ частот...")
    
    try:
        # --- НАСТОЯЩИЙ АНАЛИЗ ЗВУКА ---
        # Читаем байты записанного аудиофайла
        audio_bytes = audio_value.read()
        
        # Превращаем звук в массив чисел (амплитуду волны)
        audio_data = np.frombuffer(audio_bytes, dtype=np.int16)
        
        # Считаем переходы через ноль, чтобы грубо оценить частоту звука (в Гц)
        zero_crossings = np.nonzero(np.diff(audio_data > 0))[0]
        duration = len(audio_data) / 44100.0  # Базовая длительность при 44.1кГц
        
        # Вычисляем примерную частоту основного тона голоса
        estimated_frequency = len(zero_crossings) / (2 * duration) if duration > 0 else 0
        
        # Классифицируем пол по частоте звука:
        # Мужской голос обычно: 85 - 155 Гц
        # Женский голос обычно: 165 - 255 Гц
        if estimated_frequency > 160:
            gender = "woman"
            detected_sex = "Женский голос"
            age = "25-year-old" # Примерная базовая логика для MVP
        else:
            gender = "man"
            detected_sex = "Мужской голос"
            age = "35-year-old"
            
        st.success(f"📊 Анализ завершен! Оцененная частота: {int(estimated_frequency)} Гц ({detected_sex})")
        
        # --- ФОРМИРОВАНИЕ УМНОГО ПРОМПТА ---
        prompt = f"Hyperrealistic close-up studio photo of a {age} European {gender}, calm expression, highly detailed skin texture, 8k resolution, professional lighting, photorealistic"
        
        with st.spinner("🎨 Нейросеть рисует портрет на основе вашего тембра..."):
            encoded_prompt = urllib.parse.quote(prompt)
            # Добавляем случайный параметр (seed), чтобы картинки всегда были разными при новой записи
            import random
            seed = random.randint(1, 99999)
            image_url = f"https://pollinations.ai{encoded_prompt}?width=1024&height=1024&model=flux&nologo=true&seed={seed}"
            
            # Выводим результат
            st.image(image_url, use_column_width=True)
            st.caption(f"Сгенерировано для: {detected_sex}, {age}")
                
    except Exception as e:
        st.error(f"Произошла ошибка при анализе звука: {e}")
