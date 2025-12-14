from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests
import os
from dotenv import load_dotenv

load_dotenv()
print("TOKEN LOADED:", os.getenv("GITHUB_TOKEN") is not None)

app = FastAPI(title="GitHub Repository Intelligence Analyzer")
from fastapi.middleware.cors import CORSMiddleware

# Enable CORS for all origins (for hackathon/demo purposes)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # allow all origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class RepoRequest(BaseModel):
    repo_url: str

GITHUB_API = "https://api.github.com/repos"
TOKEN = os.getenv("GITHUB_TOKEN")

if not TOKEN:
    raise RuntimeError("GITHUB_TOKEN not set in environment variables.")

HEADERS = {
    "Authorization": f"token {TOKEN}",
    "User-Agent": "GitHub-Repo-Analyzer",
    "Accept": "application/vnd.github+json"
}

def parse_repo(url: str):
    try:
        parts = url.rstrip("/").split("/")
        return parts[-2], parts[-1]
    except IndexError:
        return None, None

def github_get(url):
    response = requests.get(url, headers=HEADERS)
    if response.status_code == 403 and "rate limit" in response.text.lower():
        raise HTTPException(status_code=429, detail="GitHub API rate limit exceeded")
    return response

def analyze_repo(owner, repo):
    repo_api = f"{GITHUB_API}/{owner}/{repo}"
    
    r = github_get(repo_api)
    if r.status_code != 200:
        raise HTTPException(status_code=404, detail="Repository not found")
    repo_data = r.json()

    # README
    readme = github_get(f"{repo_api}/readme")
    has_readme = readme.status_code == 200

    # Commits (only first page)
    commits = github_get(f"{repo_api}/commits")
    commit_count = len(commits.json()) if commits.status_code == 200 else 0

    # Languages
    langs = github_get(f"{repo_api}/languages")
    languages = list(langs.json().keys()) if langs.status_code == 200 else []

    return {
        "stars": repo_data.get("stargazers_count", 0),
        "has_readme": has_readme,
        "commit_count": commit_count,
        "languages": languages
    }

def score_repo(data):
    score = 0
    if data["has_readme"]:
        score += 20
    if data["commit_count"] >= 10:
        score += 20
    if data["languages"]:
        score += 20
    if data["commit_count"] >= 30:
        score += 10
    if data["stars"] > 0:
        score += 10
    score = min(score, 100)

    if score < 40:
        level = "Beginner"
    elif score < 70:
        level = "Intermediate"
    else:
        level = "Advanced"
    return score, level

def generate_summary(data, level):
    return (
        f"This repository is rated as {level}. "
        + ("Documentation is present. " if data["has_readme"] else "Documentation is missing. ")
        + ("Commits show reasonable development activity." if data["commit_count"] >= 10 else "Commit history is limited.")
    )

def generate_roadmap(data):
    roadmap = []
    if not data["has_readme"]:
        roadmap.append("Add a detailed README with setup and usage instructions.")
    if data["commit_count"] < 10:
        roadmap.append("Make smaller, frequent commits with clear messages.")
    roadmap.extend([
        "Add unit tests to improve reliability.",
        "Follow consistent code formatting and linting.",
        "Add CI/CD using GitHub Actions."
    ])
    return roadmap

@app.post("/analyze")
def analyze(request: RepoRequest):
    owner, repo = parse_repo(request.repo_url)
    if not owner or not repo:
        raise HTTPException(status_code=400, detail="Invalid GitHub URL")

    data = analyze_repo(owner, repo)
    score, level = score_repo(data)

    return {
        "score": score,
        "level": level,
        "summary": generate_summary(data, level),
        "roadmap": generate_roadmap(data),
        "languages": data["languages"],
        "commit_count": data["commit_count"]
    }
