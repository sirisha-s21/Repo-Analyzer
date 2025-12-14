# GitHub Repository Analyzer

## **Project Description**

This project is a web-based tool that analyzes any public GitHub repository and generates:

* **Score** (0–100) and level (Beginner / Intermediate / Advanced)
* **Summary** describing the repository quality
* **Personalized roadmap** for improvement
* **Languages used** in the project
* **Commit count**

It helps students and developers understand the quality of their code, documentation, and project structure from a recruiter or mentor perspective.

---

## **What’s Done**

* FastAPI **backend** to fetch GitHub repository details:

  * Number of commits
  * README presence
  * Languages used
  * Stars
* Analysis & scoring logic implemented
* Personalized roadmap suggestions generated automatically
* Frontend website with simple HTML + JS:

  * Input GitHub repo URL
  * Display score, summary, roadmap, languages, commits
* CORS enabled to allow frontend-backend communication

---

## **Installation & Setup**

### **1. Clone the Repository**

```bash
git clone https://github.com/YOUR_USERNAME/github-analyzer.git
cd github-analyzer
```

---

### **2. Backend Setup**

1. Go to backend folder:

```bash
cd backend
```

2. Create a Python virtual environment:

```bash
python -m venv venv
```

3. Activate the environment:

* **Windows CMD:**

```bash
venv\Scripts\activate
```

* **Mac/Linux:**

```bash
source venv/bin/activate
```

4. Install dependencies:

```bash
pip install -r requirements.txt
```

5. Create `.env` file (copy from `.env.example`) and add your GitHub personal access token:

```
GITHUB_TOKEN=your_personal_github_token_here
```

6. Start the backend server:

```bash
uvicorn main:app --reload
```

* Backend runs at `http://127.0.0.1:8000`

---

### **3. Frontend Setup**

1. Open a new terminal in the `frontend` folder:

```bash
cd frontend
```

2. Start a local server to serve the frontend:

```bash
python -m http.server 3000
```

3. Open browser at:

```
http://localhost:3000
```

---

## **4. How to Use**

1. Enter any **public GitHub repository URL** in the input box.

2. Click **Analyze**.

3. The website will display:

   * Score + Level
   * Summary
   * Personalized roadmap
   * Languages used
   * Total commits

4. Repeat by entering other repo URLs — no backend restart needed.

---

## **5. Approach**

* Backend fetches data from **GitHub REST API** using personal access token
* Scoring based on:

  * README presence
  * Commit history
  * Languages used
  * Stars
* Roadmap suggestions generated dynamically
* Frontend is lightweight HTML + JavaScript using `fetch()` to call backend

---