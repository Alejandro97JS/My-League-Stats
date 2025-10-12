from openai import OpenAI

class OpenAIDataAssistant:
    def __init__(self, api_token, open_ai_model="gpt-3.5-turbo"):
        self.open_ai_api_token = api_token
        self.client = OpenAI(api_key=self.open_ai_api_token)
        self.open_ai_model = open_ai_model
        self.role_system = "Eres un asistente que analiza datos y proporciona insights"

    def ask_insight(self, question, temperature=0.4):
        response = self.client.chat.completions.create(
            model=self.open_ai_model,
            messages=[
                {"role": "system", "content": self.role_system},
                {"role": "user", "content": question}
            ],
            temperature=temperature
        )
        return response.choices[0].message.content.strip()
