# **Documentation Linter for AI-Readiness**

A Streamlit web application designed to automatically fetch, analyze, and correct reStructuredText (reST) documentation files from GitHub. This tool enforces Alation's "Cognitive Interface" style guide, ensuring all documentation is optimized for both human readability and Large Language Model (LLM) Retrieval-Augmented Generation (RAG) pipelines.

## **Features**

* **GitHub Integration:** Fetches reST files directly from your repository using a securely stored Personal Access Token (PAT).  
* **Alation Meta Block Injection:** Automatically prepends missing files with Alation's standard Sphinx .. meta:: block (Deployment Type, User Role, Functional Area, Topics, Keywords) for optimal vector filtering.  
* **Semantic Role Enforcement:** Converts generic formatting into strict Sphinx semantic roles (e.g., transforming \*\*Settings\*\* to :guilabel:Settings\`\`).  
* **Terminology Disambiguation:** Upgrades vague terminology to Alation's controlled vocabulary (e.g., converting "cloud instance" to "Alation Cloud Service (ACS)").  
* **Visual Diff Viewer:** Highlights document changes via a side-by-side comparison using the streamlit-diff-viewer component.

## **Repository Structure**

* app.py: The main Streamlit application containing the UI, GitHub fetch logic, and the RegEx-based auto-correction engine.  
* requirements.txt: The dependency list required by Streamlit Cloud to build the environment.

## **Deployment on Streamlit Community Cloud**

This application is designed to be hosted on Streamlit Community Cloud, which allows for seamless deployments directly from GitHub.

1. **Push to GitHub:** Ensure app.py and requirements.txt are pushed to your target GitHub repository.  
2. **Deploy the App:**  
   * Log into([https://share.streamlit.io/](https://share.streamlit.io/)).  
   * Click **New app** and authorize Streamlit to access your GitHub account.  
   * Select your repository, branch, and specify app.py as the main file path.  
   * Click **Deploy**.  
3. **Configure Secrets (Crucial):**  
   * The app requires a GitHub Personal Access Token (PAT) to read files from your Alation repositories.  
   * Go to your deployed app's dashboard, click the vertical **"..."** menu, and select **Settings**.  
   * Navigate to the **Secrets** tab.  
   * Add your service account token using the exact format below:toml  
     github\_token \= "ghp\_your\_actual\_token\_here"  
   * Click **Save**. Streamlit will automatically detect this environment variable and use it for authentication.
