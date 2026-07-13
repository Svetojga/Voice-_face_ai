import streamlit as st
import requests

# Настройка страницы приложения
st.set_page_config(page_title="VoiceFace AI", page_icon="🎙️", layout="centered")
st.title("🎙️ Ваш фоторобот по голосу")
st.write("Запишите ваш голос, и ИИ воссоздаст ваш реалистичный портрет.")

# Кнопка записи аудио
audio_value = st.audio_input("Нажмите на микрофон для записи голоса")

# Безопасное чтение ключа из настроек Secrets
FAL_API_KEY = st.secrets["FAL_API_KEY"]

if audio_value:
    st.info("🎙️ Голос успешно записан! Начинаем анализ...")
    
    # Временные параметры для MVP
    gender = "man"
    age = "30-year-old"
    ethnicity = "European"
    
    prompt = f"Hyperrealistic close-up studio photo of a {age} {ethnicity} {gender}, calm expression, high detailed skin texture, 8k resolution, professional lighting, photorealistic"
    
    with st.spinner("🎨 Нейросеть Flux рисует ваш портрет (это займет 5 секунд)..."):
        try:
            # Настройка заголовков авторизации
            headers = {
                "Authorization": f"Key {FAL_API_KEY}",
                "Content-Type": "application/json"
            }
            
            payload = {
                "prompt": prompt,
                "image_size": "square_hd",
                "num_inference_steps": 28,
                "enable_safety_checker": True
            }
            
            # ИСКУССТВЕННЫЙ ИСПРАВЛЕННЫЙ АДРЕС API FLUX DEV
            response = requests.post(
                "https://fal.run/fal-ai/flux/dev", 
                json=payload, 
                headers=headers
            )
            
            if response.status_code == 200:
                result = response.json()
                
                # Достаем ссылку на сгенерированную картинку
                image_url = result["images"][0]["url"]
                
                st.success("✨ Готово! Вот как ИИ видит ваш голос:")
                st.image(image_url, use_column_width=True)
                st.caption(f"Сгенерировано по параметрам: {age}, {gender}")
            else:
                st.error(f"Ошибка API (Код {response.status_code}).")
                st.write("Ответ сервера:", response.text)
                
        except Exception as e:
            st.error(f"Произошла ошибка в коде: {e}")
