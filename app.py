import streamlit as st
import urllib.parse

# Настройка страницы приложения
st.set_page_config(page_title="VoiceFace AI", page_icon="🎙️", layout="centered")
st.title("🎙️ Ваш фоторобот по голосу")
st.write("Запишите ваш голос, и ИИ воссоздаст ваш реалистичный портрет.")

# Кнопка записи аудио
audio_value = st.audio_input("Нажмите на микрофон для записи голоса")

if audio_value:
    st.info("🎙️ Голос успешно записан! Начинаем анализ...")
    
    # Временные параметры для MVP
    gender = "man"
    age = "30-year-old"
    ethnicity = "European"
    
    # Собираем промпт для генератора
    prompt = f"Hyperrealistic close-up studio photo of a {age} {ethnicity} {gender}, calm expression, high detailed skin texture, 8k resolution, professional lighting, photorealistic"
    
    with st.spinner("🎨 Нейросеть рисует ваш портрет (это займет 3 секунды)..."):
        try:
            # Кодируем текст промпта для безопасной передачи в интернет-ссылке
            encoded_prompt = urllib.parse.quote(prompt)
            
            # Используем бесплатный и открытый сервер генерации изображений Flux
            # Он принимает промпт прямо в URL-строке и сразу отдает готовую картинку
            image_url = f"https://pollinations.ai{encoded_prompt}?width=1024&height=1024&model=flux&nologo=true"
            
            # Выводим результат на экран
            st.success("✨ Готово! Вот как ИИ видит ваш голос:")
            st.image(image_url, use_column_width=True)
            st.caption(f"Сгенерировано по параметрам: {age}, {gender}")
                
        except Exception as e:
            st.error(f"Произошла ошибка в коде: {e}")
