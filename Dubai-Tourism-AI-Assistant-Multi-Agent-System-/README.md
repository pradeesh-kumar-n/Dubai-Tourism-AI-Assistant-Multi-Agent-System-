# Dubai Tourism AI Assistant

A simple multi-agent AI system built with `langgraph` to provide Dubai tourism recommendations.

## Features
- Classifies user queries into attractions, restaurants, or general info
- Provides curated lists of Dubai attractions and restaurants
- Generates contextual responses

## Usage
```bash
python main.py
```

## Live Demo Options

### Option 1: GitHub Actions with ngrok (Original Method)
You can see a live demo of this application via GitHub Actions using ngrok tunneling.

**Note:** This method requires setting up the `NGROK_AUTHTOKEN` secret in your GitHub repository.

1. Ensure the repository secret `NGROK_AUTHTOKEN` is set (get from https://dashboard.ngrok.com/get-started/your-authtoken).
   - Go to Settings → Secrets and variables → Actions → New repository secret.
   - Name: `NGROK_AUTHTOKEN`
   - Value: your authtoken (no spaces).

2. Go to the **Actions** tab, select the **Live Demo** workflow.
3. Click **Run workflow** (or it will run automatically on pushes to `main`).
4. After the job starts, look for the step named "Start demo" in the logs; it will output a public ngrok URL.
5. Click that URL to interact with the live demo.

**Note:** The demo will stay active as long as the workflow run continues (up to 6 hours or until cancelled).

### Option 2: GitHub Codespaces (Recommended Alternative)
If you're having issues with the ngrok secret, you can use GitHub Codespaces as an alternative method to demo the application live. This method doesn't require any additional secrets.

1. Click the green **"Code"** button on your repository page
2. Select the **"Codespaces"** tab
3. Click **"New codespace"**
4. Wait for the environment to be set up (this may take a few minutes)
5. Once the Codespace is ready, the application will automatically start
6. A popup should appear in the bottom-right corner saying "Your application is available at: [URL]" - click this URL to open the demo
7. Alternatively, you can manually open port 8000 by:
   - Opening the PORTS tab in the bottom panel
   - Finding the port 8000 entry
   - Right-clicking it and selecting "Open in Browser"

The Codespace will remain active as long as you keep it open, making it perfect for live demonstrations during interviews or presentations.

## Development
To run the application locally:
```bash
pip install -r requirements.txt
python main.py
```

Then open your browser to http://localhost:8000

## Evaluation
To run system evaluation:
```bash
python main.py
```
Or visit the /evaluate endpoint when the server is running.