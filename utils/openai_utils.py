import os
import openai

def get_completion_response(prompt):
    openai.api_key = os.getenv('OPENAI_API_KEY')
    prompt += '\n\n###\n\n'
    print('here')
    completion = openai.Completion.create(
        model='curie:ft-personal-2023-03-12-21-37-31',
        prompt=prompt,
        temperature=0.2
    )
    for idx, choice in enumerate(completion.choices):
        print('#{}: {}'.format(idx, choice))
    return completion.choices[0]['text']
