import requests
import os
import subprocess
from bs4 import BeautifulSoup
import time

USERNAME = 'Ergusha11'  # Reemplaza con tu usuario de Codeforces

def fetch_solutions(username):
    url = f'https://codeforces.com/api/user.status?handle={username}'
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()['result']
    else:
        print(f'Error fetching solutions: {response.status_code}')
        return []

def fetch_solution_code(contest_id, submission_id, is_gym=False, retries=3, delay=5):
    base_url = 'https://codeforces.com/gym' if is_gym else 'https://codeforces.com/contest'
    url = f'{base_url}/{contest_id}/submission/{submission_id}'
    for attempt in range(retries):
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            code_div = soup.find('pre', {'id': 'program-source-text'})
            if code_div:
                return code_div.text
        time.sleep(delay)
    return None

def get_file_extension(language):
    # Mapeo de lenguajes a extensiones de archivo
    extensions = {
        'GNU C++': 'cpp',
        'GNU C++11': 'cpp',
        'GNU C++14': 'cpp',
        'GNU C++17': 'cpp',
        'C++20 (GCC 13-64)': 'cpp',
        'Python 2': 'py',
        'Python 3': 'py',
        'Java': 'java',
        'C': 'c',
        'GNU C': 'c',
        'C#': 'cs',
        'JavaScript': 'js',
        'Ruby': 'rb',
        'PHP': 'php',
        'Haskell': 'hs',
        'Go': 'go',
        'Rust': 'rs',
        # Agregar otros lenguajes según sea necesario
    }
    return extensions.get(language, 'txt')

def save_solution(solution, solutions_dict, is_gym=False):
    contest_id = solution['problem']['contestId']
    index = solution['problem']['index']
    problem_name = solution['problem']['name']
    problem_id = f"{contest_id}{index}-{problem_name}"
    language = solution['programmingLanguage']
    file_extension = get_file_extension(language)
    
    folder_type = 'gym' if is_gym else 'contest'
    dir_path = os.path.join('codeforces', folder_type, f"{contest_id}{index}")
    os.makedirs(dir_path, exist_ok=True)
    
    code = fetch_solution_code(contest_id, solution['id'], is_gym=is_gym)
    if code:
        file_path = os.path.join(dir_path, f'solution.{file_extension}')
        if problem_id not in solutions_dict:
            solutions_dict[problem_id] = {
                'file_path': file_path,
                'contest_id': contest_id,
                'index': index,
                'language': language
            }
            with open(file_path, 'w') as f:
                f.write(solution['programmingLanguage'] + '\n\n' + code)
        else:
            print(f"Skipping duplicate solution for problem {problem_id}")
    else:
        print(f"Error fetching code for problem {problem_id} (is_gym={is_gym})")

def generate_readme(solutions_dict):
    readme_content = "# Codeforces Solutions\n\n## Estadísticas\n\n"
    readme_content += "| Problema | Lenguaje | Enlace a Solución | Enlace a Problema |\n"
    readme_content += "|----------|----------|-------------------|-------------------|\n"

    for problem_id, details in solutions_dict.items():
        contest_id = details['contest_id']
        index = details['index']
        language = details['language'].split()[0].lower()
        problem_url = f"https://codeforces.com/contest/{contest_id}/problem/{index}" if contest_id < 100000 else f"https://codeforces.com/gym/{contest_id}/problem/{index}"
        readme_content += f"| [{problem_id}](./{details['file_path']}) | {language} | [solution]({details['file_path']}) | [problem]({problem_url}) |\n"
    
    with open('README.md', 'w') as f:
        f.write(readme_content)

def git_push():
    try:
        subprocess.check_call(['git', 'add', '.'])
        subprocess.check_call(['git', 'commit', '-m', 'Update Codeforces solutions'])
        subprocess.check_call(['git', 'push', 'origin', 'main'])
    except subprocess.CalledProcessError as e:
        print(f"Error during git operation: {e}")

if __name__ == "__main__":
    solutions = fetch_solutions(USERNAME)
    solutions_dict = {}
    for solution in solutions:
        if solution['verdict'] == 'OK':
            is_gym = solution['problem']['contestId'] >= 100000  # Identifica problemas de Gym
            save_solution(solution, solutions_dict, is_gym=is_gym)
    generate_readme(solutions_dict)
    git_push()  # Descomenta esta línea para hacer push a GitHub automáticamente

