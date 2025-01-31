import os
from openai import AsyncOpenAI
from dotenv import load_dotenv

load_dotenv()

class GPTHandler:
    def __init__(self):
        self.client = AsyncOpenAI(api_key=os.getenv('OPENAI_API_KEY'))

    async def generate_development_plan(self, skill: str, intensity: str) -> str:
        prompt = self._create_development_prompt(skill, intensity)
        
        try:
            response = await self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "Ты - опытный наставник по развитию навыков"},
                    {"role": "user", "content": prompt}
                ]
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"Ошибка при запросе к GPT: {e}")
            return "Извините, произошла ошибка при генерации плана. Попробуйте позже."

    def _create_development_prompt(self, skill: str, intensity: str) -> str:
        base_prompt = f"""
        Создай план развития навыка: {skill}.
        Интенсивность занятий: {intensity}.
        
        План должен включать:
        1. Краткую оценку выбранного навыка
        2. Конкретные упражнения для развития
        3. Практические задания
        4. Рекомендации по выполнению
        5. Ожидаемые результаты
        
        Формат ответа:
        - Структурированный текст
        - Четкие шаги
        - Конкретные действия
        """
        return base_prompt
