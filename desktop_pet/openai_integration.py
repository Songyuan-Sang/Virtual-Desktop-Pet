from openai import OpenAI

class OpenAIIntegration:
    def __init__(self):
        self.client = OpenAI()

    def openai_query(self, message):
        completion = self.client.chat.completions.create(
            model="gpt-3.5-turbo-1106",
            messages=[
                {"role": "system", "content": "You are a white pomeranian named Kimi, skilled in explaining any kinds of concepts with creative flair."},
                {"role": "user", "content": message}
            ]
        )

        return completion.choices[0].message.content
