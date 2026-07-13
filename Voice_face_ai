import streamlit as st
import requests
import os

# 1. Настройка страницы приложения
st.set_page_config(page_title="VoiceFace AI", page_icon="🎙️", layout="centered")
st.title("🎙️ Ваш фоторобот по голосу")
st.write("Запишите ваш голос, и ИИ воссоздаст ваш реалистичный портрет.")

# 2. Кнопка записи аудио (Streamlit сам создаст удобный диктофон для телефона)
audio_value = st.audio_input("Нажмите на микрофон для записи голоса")

# Токен доступа к API (его нужно получить на сайте fal.ai)
FAL_API_KEY = st.secrets["FAL_API_KEY"]

if audio_value:
    st.info("🎙️ Голос успешно записан! Начинаем анализ...")
    
    # --- ЭТАП 1: Имитация анализа аудио (для первой версии MVP) ---
    # В полноценной версии здесь будет отправка audio_value в Hume AI или OpenAI.
    # Для быстрого старта мы временно захардкодим базовые параметры,
    # либо добавим простые переключатели (пол/возраст), чтобы протестировать генерацию.
    
    gender = "man"  # или "woman"
    age = "30-year-old"
    ethnicity = "European"
    
    # --- ЭТАП 2: Автоматическая сборка промпта ---
    prompt = f"Hyperrealistic close-up studio photo of a {age} {ethnicity} {gender}, calm expression, high detailed skin texture, 8k resolution, professional lighting, photorealistic"
    
    st.write("🤖 ИИ сформировал ваш визуальный промпт...")
    
    # --- ЭТАП 3: Отправка запроса в нейросеть Flux.1 через Fal.ai ---
    with st.spinner("🎨 Нейросеть Flux рисует ваш портрет (это займет 5 секунд)..."):
        try:
            headers = {
                "Authorization": f"Key {FAL_API_KEY}",
                "Content-Type": "application/json"
            }
            payload = {
                "prompt": prompt,
                "image_size": "square_hd", # Квадратное фото, идеально для телефонов
                "num_inference_steps": 28,
                "enable_safety_checker": True
            }
            
            # Отправляем запрос на генерацию во Flux.1
            response = requests.post(
                "https://fal.run", 
                json=payload, 
                headers=headers
            )
            
            if response.status_code == 200:
                result = response.json()
                # Получаем ссылку на готовую картинку
                image_url = result["images"][0]["url"]
                
                # --- ЭТАП 4: Вывод результата на экран ---
                st.success("✨ Готово! Вот как ИИ видит ваш голос:")
                st.image(image_url, use_column_width=True)
                st.caption(f"Сгенерировано по параметрам: {age}, {gender}")
            else:
                st.error("Ошибка при генерации изображения. Проверьте API ключ.")
                
        except Exception as e:
            st.error(f"Произошла ошибка: {e}")
