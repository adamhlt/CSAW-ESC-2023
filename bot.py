import requests
import time
from datetime import datetime

repo_owner = ""  # Remplacez par le propriétaire du référentiel
repo_name = ""    # Remplacez par le nom du référentiel
url = ""
last_commit_info_sha = ""

def get_last_commit(repo_owner, repo_name):
    api_url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/commits"
    
    try:
        response = requests.get(api_url)
        response.raise_for_status()
        commits = response.json()
        if commits:
            last_commit = commits[0]
            return {
                "sha": last_commit["sha"],
                "message": last_commit["commit"]["message"],
                "author": last_commit["commit"]["author"]["name"],
                "date": last_commit["commit"]["author"]["date"]
            }
        else:
            return None
    except requests.exceptions.RequestException as e:
        print(f"Requête API Github Échoué !\n La requête a échoué. (Date : {now.strftime('%d/%m/%Y %H:%M:%S')})")
        return None

if __name__ == "__main__":
    while True:
        now = datetime.now()
        last_commit = get_last_commit(repo_owner, repo_name)
        if last_commit:
            print(f"{last_commit['sha']} Date : {now.strftime('%d/%m/%Y %H:%M:%S')}")
            if last_commit_info_sha == "":
                last_commit_info_sha = last_commit['sha']

            elif last_commit_info_sha != last_commit['sha']:
                last_commit_info_sha = last_commit['sha']
                data = f"Nouveau commit CSAW ! \n {last_commit['message']} \n ({last_commit['sha']})"
                response = requests.post(url, data=data)
                if response.status_code == 200:
                    print(f"La requête a réussi. {now.strftime('%d/%m/%Y %H:%M:%S')}")
                else:
                    print(f"La requête a échoué avec le code d'état {response.status_code} (Date : {now.strftime('%d/%m/%Y %H:%M:%S')}).")
        time.sleep(60)
        
