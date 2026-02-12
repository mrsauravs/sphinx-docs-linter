import streamlit as st
import requests
import re
from st_diff_viewer import diff_viewer

st.set_page_config(page_title="Alation AI-Ready Doc Linter", layout="wide")

st.title("Alation AI-Ready Documentation Linter")
st.write("Analyzes and corrects reStructuredText (reST) files for LLM/RAG optimization.")

# GitHub Service Account Configuration
st.sidebar.header("GitHub Connection")
repo = st.sidebar.text_input("Repository", "alation/docs")
branch = st.sidebar.text_input("Branch", "main")
file_path = st.sidebar.text_input("File Path", "docs/connectors/snowflake.rst")

def fetch_from_github(repo, branch, path):
    """Fetches the reST file from GitHub using a Service Account PAT."""
    headers = {}
    # Securely access the GitHub Personal Access Token from Streamlit Cloud Secrets
    if "github_token" in st.secrets:
        headers["Authorization"] = f"token {st.secrets['github_token']}"
    
    url = f"https://raw.githubusercontent.com/{repo}/{branch}/{path}"
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        return response.text
    else:
        st.error(f"Failed to fetch file. HTTP Status: {response.status_code}")
        return None

def apply_ai_ready_corrections(text):
    """Applies 'The Cognitive Interface' style guide rules to the text."""
    issues_flagged =  # Fixed: List is now properly initialized
    corrected_text = text
    
    # Rule 1: Enforce Alation's Specific Metadata Block after the H1 Title
    required_meta_keys = [":deployment_type:", ":user_role:", ":functional_area:", ":topics:", ":keywords:"]
    missing_keys = [key for key in required_meta_keys if key not in corrected_text]
    
    if missing_keys:
        issues_flagged.append("Missing or incomplete Alation Metadata Block injected after page title.")
        meta_template = (
            ".. meta::\n"
            "   :deployment_type: Alation Cloud Service ; Customer Managed\n"
            "   :user_role: Server Admin ; Catalog Admin ; Source Admin ; Viewer\n"
            "   :functional_area: Alation Analytics\n"
            "   :topics: Classic User Experience ; Navigation ; Search ; Access ; Data Source Access ; SCIM ; Email Server\n"
            "   :keywords: BI tool integration ; PostgreSQL ; Tableau workbooks ; alation_analytics database ; analytics data ; authentication ; catalog admin role ; composer role ; content metrics ; data access control ; database roles ; pg_hba.conf ; server admin role ; service user ; source admin role ; steward role ; usage metrics ; user groups ; user permissions ; viewer role\n\n"
        )
        
        # Regex to find the first H1 title (Text followed by a line of ===, ###, or ***)
        h1_pattern = r"^([^\n]+)\n([=#*~^-]{3,})\n"
        match = re.search(h1_pattern, corrected_text, re.MULTILINE)
        
        if match:
            # Insert the meta block immediately after the H1 heading
            insert_pos = match.end()
            corrected_text = corrected_text[:insert_pos] + "\n" + meta_template + corrected_text[insert_pos:]
        else:
            # Fallback: Insert at the very top if no clear H1 is found
            corrected_text = meta_template + corrected_text
        
    # Rule 2: Qualify Generic Headings
    heading_pattern = r"^((?:Setup|Configuration|Prerequisites|Troubleshooting)\n)([-=~]+)$"
    if re.search(heading_pattern, corrected_text, re.MULTILINE):
        issues_flagged.append("Generic headings qualified with feature context.")
        def fix_heading(match):
            # Appends a placeholder feature name and extends the underline
            return f"{match.group(1).strip()}\n{match.group(2)}{'-'*15}"
        corrected_text = re.sub(heading_pattern, fix_heading, corrected_text, flags=re.MULTILINE)
        
    # Rule 3: Correct Ambiguous Terminology
    if re.search(r"\b([Cc]loud [Ii]nstance)\b", corrected_text):
        issues_flagged.append("Ambiguous 'cloud instance' changed to 'Alation Cloud Service (ACS)'.")
        corrected_text = re.sub(r"\b[Cc]loud [Ii]nstance\b", "Alation Cloud Service (ACS)", corrected_text)
        
    if re.search(r"\b(he [Ii]nstance)\b", corrected_text):
        issues_flagged.append("Ambiguous 'the instance' changed to 'the Alation Server'.")
        corrected_text = re.sub(r"\bhe [Ii]nstance\b", "the Alation Server", corrected_text)
        
    # Rule 4: Apply Semantic Roles for UI Elements
    if re.search(r"\*\*(Settings|Data Sources|Save|Cancel|Add Data Source)\*\*", corrected_text):
        issues_flagged.append("Bolded UI elements converted to :guilabel: roles.")
        corrected_text = re.sub(r"\*\*(Settings|Data Sources|Save|Cancel|Add Data Source)\*\*", r":guilabel:`\1`", corrected_text)

    return issues_flagged, corrected_text

# App Execution Flow
if st.sidebar.button("Fetch & Auto-Correct"):
    with st.spinner("Fetching file from GitHub..."):
        raw_content = fetch_from_github(repo, branch, file_path)
        
    if raw_content:
        issues, fixed_content = apply_ai_ready_corrections(raw_content)
        
        if issues:
            st.warning("Violations Found & Corrected:")
            for issue in issues:
                st.write(f"- {issue}")
        else:
            st.success("Perfect Score! No AI-readiness violations found.")
            
        st.subheader("Changes Overview")
        # Render the visual diff viewer component
        diff_viewer(raw_content, fixed_content, lang='none')
        
        # Provide raw text area to copy the final result
        with st.expander("View Raw Corrected Output"):
            st.text_area("Copy your corrected reST here:", fixed_content, height=400)
