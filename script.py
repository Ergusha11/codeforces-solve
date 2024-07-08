import requests
import json

def get_solved_problems(user_handle):
    url = f'https://codeforces.com/api/user.status?handle={user_handle}'
    response = requests.get(url)
    data = response.json()

    solved_problems = {}
    if data['status'] == 'OK':
        for result in data['result']:
            if result['verdict'] == 'OK':
                problem = result['problem']
                contest_id = problem['contestId']
                problem_index = problem['index']
                problem_name = problem['name']
                solved_problems[f'{contest_id}-{problem_index}'] = problem_name

    return solved_problems

def generate_markdown(solved_problems):
    markdown_content = "# Codeforces Solved Problems\n\n"
    markdown_content += "## Statistics\n"
    markdown_content += f"**Total Solved Problems**: {len(solved_problems)}\n\n"
    markdown_content += "## Problems\n"
    for problem, name in solved_problems.items():
        markdown_content += f"- [{problem}](https://codeforces.com/contest/{problem.split('-')[0]}/problem/{problem.split('-')[1]}) - {name}\n"
    return markdown_content

def save_to_file(content, file_path):
    with open(file_path, 'w') as file:
        file.write(content)

if __name__ == "__main__":
    user_handle = 'Ergusha11'
    solved_problems = get_solved_problems(user_handle)
    markdown_content = generate_markdown(solved_problems)
    save_to_file(markdown_content, 'README.md')

