import os
import openai

def get_completion_response(prompt):
    openai.api_key = os.getenv('OPENAI_API_KEY')
    prompt += '\n\n\n###\n\n'
    completion = openai.Completion.create(
        model='curie:ft-personal-2023-03-08-03-46-55',
        prompt=prompt,
    )
    return completion.choices[0]['text']
