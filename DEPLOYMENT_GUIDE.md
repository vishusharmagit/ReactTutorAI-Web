# React Tutor AI - Deployment Guide

This guide will help you deploy the React Tutor AI Streamlit app to Streamlit Community Cloud.

## Prerequisites

1. **GitHub Account** - You need a GitHub account (free)
2. **HuggingFace Account** - For API token (free)
3. **Streamlit Cloud Account** - Can sign in with GitHub

---

## Step 1: Get a HuggingFace API Token

The app uses HuggingFace embeddings which may require authentication for rate limiting.

1. Go to [HuggingFace](https://huggingface.co/)
2. Sign up or log in
3. Click on your profile → **Settings** → **Access Tokens**
4. Click **New token**
5. Give it a name (e.g., "React Tutor AI")
6. Select **Read** permission
7. Copy the token (starts with `hf_`)

**Save this token somewhere safe!**

---

## Step 2: Prepare Your Project Files

### 2.1 Create `runtime.txt`

Create a file named `runtime.txt` in the `ReactTutorAI-Web/` folder with this content:

```
python-3.11
```

This tells Streamlit Cloud to use Python 3.11 (more stable than newer versions).

### 2.2 Update `requirements.txt`

Replace the content of `requirements.txt` with:

```txt
streamlit>=1.28.0

langchain>=0.1.0
langchain-core>=0.1.0
langchain-community>=0.0.38
langchain-groq>=0.1.0
langchain-huggingface>=0.0.1

pypdf>=3.15.0
chromadb>=0.4.0
sentence-transformers>=2.7.0

python-dotenv>=1.0.0
requests
cryptography>=3.1
torch
```

### 2.3 Verify `.gitignore`

Make sure `.gitignore` contains:

```gitignore
data/chroma_db/
venv/
__pycache__/
*.pyc
*.pyo
.env
.streamlit/
```

This ensures sensitive files and virtual environments are NOT uploaded to GitHub.

---

## Step 3: GitHub Repository Options

### Option A: Create Your Own Repository

1. Go to [GitHub](https://github.com/)
2. Click the **+** icon → **New repository**
3. Name it (e.g., `react-tutor-ai`)
4. Choose **Public** (Streamlit Cloud works best with public repos)
5. **DO NOT** initialize with README, .gitignore, or license
6. Click **Create repository**

### Option B: Friend Already Pushed Code - Fork It! ✅

**Yes, you can fork your friend's repository and deploy it!** Here's how:

1. **Your friend shares the repository URL** (e.g., `https://github.com/friend-username/react-tutor-ai`)

2. **You fork the repository**:
   - Go to your friend's repository page on GitHub
   - Click the **Fork** button (top right)
   - GitHub will create a copy in your account: `https://github.com/YOUR-USERNAME/react-tutor-ai`

3. **Deploy from your forked repository**:
   - Go to [Streamlit Community Cloud](https://share.streamlit.io)
   - Sign in with GitHub
   - Click **New app**
   - Select **your forked repository** (it will appear in your list)
   - Set main file to `streamlit_app.py`
   - Click **Deploy**

4. **Add your own secrets** (you'll need your own API keys):
   - In Streamlit Cloud settings for your app
   - Add `GROQ_API_KEY` and `HUGGINGFACEHUB_API_TOKEN`

**Important**: 
- Your forked copy is independent - you can modify it without affecting your friend's version
- You'll need your own Groq API key and HuggingFace token for your deployment
- Both you and your friend can have separate deployments running at the same time!

### Option C: Collaborator on Friend's Repository

If you don't want to fork, your friend can add you as a collaborator:
1. Friend goes to repo → Settings → Collaborators → Add people
2. Enter your GitHub username or email
3. You accept the invitation
4. You can then deploy from the same repository

### Pushing Your Local Changes to GitHub (if needed)

If you've made local changes (like the `runtime.txt` and updated `requirements.txt` I created), you'll need to push them:

```bash
# Navigate to your ReactTutorAI-Web folder
cd ReactTutorAI-Web

# If this is a fresh clone/fork, initialize git
git init
git add .
git commit -m "Add deployment files"

# Add your fork as remote (replace with your actual fork URL)
git remote add origin https://github.com/YOUR-USERNAME/react-tutor-ai.git

# Push to your fork
git push -u origin main
```

If you already have a fork and want to update it:
```bash
# Add your fork as remote
git remote add fork https://github.com/YOUR-USERNAME/react-tutor-ai.git

# Push to your fork
git push fork main
```

---

## Step 4: Deploy to Streamlit Cloud

1. Go to [Streamlit Community Cloud](https://share.streamlit.io)
2. Click **Sign in** → **Sign in with GitHub**
3. Authorize Streamlit to access your GitHub
4. Click **New app**
5. Fill in:
   - **GitHub repository**: Select your `react-tutor-ai` repo
   - **Branch**: `main`
   - **Main file path**: `streamlit_app.py`
6. Click **Advanced settings** (optional)
7. Click **Deploy!**

---

## Step 5: Add Secrets to Streamlit Cloud

After deployment starts (or before), you need to add API keys:

1. In your Streamlit Cloud dashboard, find your app
2. Click the **three dots** → **Settings**
3. Scroll down to **Secrets**
4. Click **Add secret**
5. Add your secrets:

```toml
GROQ_API_KEY="your_groq_api_key_here"
HUGGINGFACEHUB_API_TOKEN="your_huggingface_token_here"
```

6. Click **Save**

**Important**: Do NOT commit these secrets to GitHub! Add them only through the Streamlit Cloud interface.

---

## Step 6: Verify Deployment

1. Wait for the deployment to complete (usually 2-5 minutes)
2. Click the link to open your app
3. Test by asking a React question

---

## Troubleshooting

### Build Fails

**Common causes:**

1. **Python version** - Make sure `runtime.txt` exists with `python-3.11`
2. **Missing dependencies** - Check `requirements.txt` is correct
3. **ChromaDB issues** - May need to add `protobuf<5` to requirements.txt

### App Runs but Can't Answer Questions

1. **Check secrets** - Make sure both API keys are added in Streamlit Cloud settings
2. **ChromaDB persistence** - Streamlit Cloud storage is ephemeral. The database may reset between sessions. For a permanent solution, you might need to:
   - Recreate embeddings at startup
   - Use an external vector database service

### Rate Limiting from HuggingFace

If you get rate limit errors, make sure you added `HUGGINGFACEHUB_API_TOKEN` to secrets.

---

## Important Notes

### ChromaDB and Ephemeral Storage

Streamlit Cloud uses temporary storage that resets when the app restarts. This means:

- The `data/chroma_db` folder will be empty on each deployment
- The app will need to recreate the vector database

**Current behavior**: The app expects a pre-built ChromaDB. If it's missing, the app may fail.

**Solutions**:
1. **For testing**: Deploy as-is and see if it works
2. **For production**: Modify the app to rebuild embeddings on startup if the database is missing

If you need help modifying the app for this, let me know!

---

## Quick Checklist

- [ ] Get HuggingFace API token
- [ ] Create `runtime.txt` with `python-3.11`
- [ ] Update `requirements.txt`
- [ ] Verify `.gitignore`
- [ ] Create GitHub repository
- [ ] Push code to GitHub
- [ ] Deploy to Streamlit Cloud
- [ ] Add secrets (GROQ_API_KEY, HUGGINGFACEHUB_API_TOKEN)
- [ ] Test the app

---

## Weekly Reference Guide

If you want to do this deployment next week, just follow these steps:

### Week of Deployment:

1. **Monday**: Get HuggingFace token
2. **Tuesday**: Create runtime.txt and update requirements.txt
3. **Wednesday**: Create GitHub repo and push code
4. **Thursday**: Deploy to Streamlit Cloud
5. **Friday**: Add secrets and test

Good luck with your deployment! 🚀