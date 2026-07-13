import streamlit as st
import requests
import urllib.parse
import base64
from openai import OpenAI

# Настройка страницы приложения
st.set_page_config(page_title="VoiceFace AI", page_icon="🎙️", layout="centered")
st.title("🎙️ Ваш фоторобот по голосу")
st.write("Запишите ваш голос (не менее 5 секунд), и искусственный интеллект воссоздаст ваш реалистичный портрет.")

# Кнопка записи аудио
audio_value = st.audio_input("Нажмите на микрофон для записи голоса")

if audio_value:
    st.info("🎙️ Голос успешно записан! Нейросеть OpenAI начинает глубокий анализ биомаркеров речи...")
    
    try:
        # Инициализируем клиента OpenAI с настройками из Secrets
        client = OpenAI(
            api_key=st.secrets["OPENAI_API_KEY"],
            base_url=st.secrets["OPENAI_BASE_URL"]
        )
        
        # Читаем аудио и кодируем его в base64 для безопасной передачи по API
        audio_bytes = audio_value.read()
        audio_base64 = base64.b64encode(audio_bytes).decode("utf-8")
        
        with st.spinner("🧠 ИИ вслушивается в тембр, интонации и дыхание..."):
            # Просим модель GPT-4o проанализировать аудио и выдать строгие параметры
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": "Прослушай аудиозапись речи человека. Оцени его биологический пол (man или woman), примерный возраст (например: 25-year-old, 50-year-old), расу/этническую принадлежность на английском и эмоцию голоса. Ответь строго в формате JSON, без лишнего текста, вот так: {\"gender\": \"man\", \"age\": \"30-year-old\", \"ethnicity\": \"European\", \"emotion\": \"calm\", \"ru_desc\": \"Мужчина, около 30 лет, спокойный тембр\"}"},
                            {"type": "input_audio", "input_audio": {"data": audio_base64, "format": "wav"}}
                        ]
                    }
                ],
                response_format={"type": "json_object"}
            )
            
            # Разбираем ответ от аналитической нейросети
            ai_analysis = eval(response.choices[0].message.content)
            
            gender = ai_analysis.get("gender", "man")
            age = ai_analysis.get("age", "30-year-old")
            ethnicity = ai_analysis.get("ethnicity", "European")
            emotion = ai_analysis.get("emotion", "calm")
            ru_desc = ai_analysis.get("ru_desc", "Голос проанализирован")
            
            st.success(f"📊 Результат анализа голоса: {ru_desc} (настроение: {emotion})")
            
        # --- ГЕНЕРАЦИЯ ПОРТРЕТА НА ОСНОВЕ РЕАЛЬНЫХ ДАННЫХ ---
        with st.spinner("🎨 Передаем фоторобот художнику..."):
            prompt = f"Hyperrealistic close-up studio photo of a {age} {ethnicity} {gender}, {emotion} facial expression, high detailed skin texture, 8k resolution, professional lighting, photorealistic"
            
            encoded_prompt = urllib.parse.quote(prompt)
            
            # Используем надежный и быстрый публичный шлюз картинок Flux
            import random
            seed = random.randint(1, 99999)
            image_url = f"https://pollinations.ai{encoded_prompt}?width=1024&height=1024&model=flux&nologo=true&seed={seed}"
            
            # Выводим готовую картинку на экран
            st.image(image_url, use_column_width=True)
            st.caption(f"Визуальный профиль ИИ собран по параметрам вашей речи.")
                
    except Exception as e:
        st.error(f"Произошла ошибка при анализе ИИ: {e}")
        st.write("Пожалуйста, убедитесь, что вы записали четкую речь и правильно настроили ключи в Secrets.")
