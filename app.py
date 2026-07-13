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
    
    # Временные параметры для MVP (пока без интеграции аудио-анализатора)
    gender = "man"
    age = "30-year-old"
    ethnicity = "European"
    
    prompt = f"Hyperrealistic close-up studio photo of a {age} {ethnicity} {gender}, calm expression, high detailed skin texture, 8k resolution, professional lighting, photorealistic"
    
    with st.spinner("🎨 Нейросеть Flux рисует ваш портрет (это займет 5 секунд)..."):
        try:
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
            
            # Отправка запроса во Flux.1
            response = requests.post(
                "https://fal.run", 
                json=payload, 
                headers=headers
            )
            
            if response.status_code == 200:
                result = response.json()
                
                # Извлекаем ссылку на изображение из корректной структуры ответа fal.ai
                image_url = result["images"][0]["url"]
                
                st.success("✨ Готово! Вот как ИИ видит ваш голос:")
                st.image(image_url, use_column_width=True)
                st.caption(f"Сгенерировано по параметрам: {age}, {gender}")
            else:
                st.error(f"Ошибка API (Код {response.status_code}). Проверьте правильность ключа в Secrets.")
                st.write(response.text) # Поможет увидеть точную причину ошибки
                
        except Exception as e:
            st.error(f"Произошла ошибка: {e}")
