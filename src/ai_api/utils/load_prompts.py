import os

def load_user_prompt(prompt_name):
    with open(f'ai_api/prompts/{prompt_name}/user_prompt.txt', 'r') as file:
        return file.read()

def load_system_prompt(prompt_name):
    with open(f'ai_api/prompts/{prompt_name}/system_prompt.txt', 'r') as file:
        return file.read()
    
def load_all_user_prompts():
    user_prompts = {}
    for dir in os.listdir('ai_api/prompts'):
        if os.path.isdir(f'ai_api/prompts/{dir}'):
            user_prompts[dir] = load_user_prompt(dir)
    return user_prompts

def load_all_system_prompts():
    system_prompts = {}
    for dir in os.listdir('ai_api/prompts'):
        if os.path.isdir(f'ai_api/prompts/{dir}'):
            system_prompts[dir] = load_system_prompt(dir)
    return system_prompts