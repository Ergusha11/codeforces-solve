import requests
import os
import subprocess
from bs4 import BeautifulSoup

USERNAME = 'Ergusha11'  # Reemplaza con tu usuario de Codeforces

def fetch_solutions(username):
    url = f'https://codeforces.com/api/user.status?handle={username}'
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()['result']
    else:
        print(f'Error fetching solutions: {response.status_code}')
        return []

def fetch_solution_code(contest_id, submission_id):
    url = f'https://codeforces.com/contest/{contest_id}/submission/{submission_id}'
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        code_div = soup.find('pre', {'id': 'program-source-text'})
        if code_div:
            return code_div.text
    return None

def save_solution(solution):
    problem_id = f"{solution['problem']['contestId']}{solution['problem']['index']}"
    language = solution['programmingLanguage'].split()[0].lower()
    file_extension = {'cpp': 'cpp', 'python': 'py', 'java': 'java'}.get(language, 'txt')
    
    dir_path = os.path.join('codeforces', f"{solution['problem']['contestId']}{solution['problem']['index']}")
    os.makedirs(dir_path, exist_ok=True)
    
    code = fetch_solution_code(solution['contestId'], solution['id'])
    if code:
        file_path = os.path.join(dir_path, f'solution.{file_extension}')
        with open(file_path, 'w') as f:
            f.write(solution['programmingLanguage'] + '\n\n' + code)
    else:
        print(f"Error fetching code for problem {problem_id}")

def generate_readme(solutions):
    readme_content = "# Codeforces Solutions\n\n## Estadísticas\n\n"
    readme_content += "| Problema | Lenguaje | Tiempo | Veredicto |\n"
    readme_content += "|----------|----------|--------|-----------|\n"

    for solution in solutions:
        if solution['verdict'] == 'OK':
            problem_id = f"{solution['problem']['contestId']}{solution['problem']['index']}"
            language = solution['programmingLanguage']
            time = solution['creationTimeSeconds']
            verdict = solution['verdict']
            
            readme_content += f"| [{problem_id}](./codeforces/{problem_id}) | {language} | {time} | {verdict} |\n"
    
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
    for solution in solutions:
        if solution['verdict'] == 'OK':
            save_solution(solution)
    generate_readme(solutions)
    git_push()

