import google.generativeai as genai
from config import GEMINI_API_KEY, SYSTEM_PROMPT

# ====== НАСТРОЙКА GEMINI ======

genai.configure(api_key=GEMINI_API_KEY)

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash"
)

# ====== ГЕНЕРАЦИЯ ОТВЕТА ======

def get_ai_response(user_text: str, history: list = None) -> str:
    """
    Отправляет запрос в Gemini и возвращает ответ.
    """

    try:
        # формируем контекст
        context = SYSTEM_PROMPT

        if history:
            context += "\n\nИстория диалога:\n"
            for h in history[-10:]:
                context += f"{h}\n"

        full_prompt = context + "\n\nПользователь: " + user_text

        response = model.generate_content(full_prompt)

        return response.text

    except Exception as e:
        return "❌ Ошибка AI. Попробуй ещё раз."
