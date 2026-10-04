# Step-by-Step Guide: Deploy Dubai Tourism AI Assistant to Render

This guide provides a complete walkthrough for deploying your Dubai Tourism AI Assistant RAG (Retrieval-Augmented Generation) project to Render as a live demo.

## Prerequisites

1. GitHub account with your project pushed (you already have this)
2. Render account (free tier is sufficient)
3. Basic familiarity with Git and command line

## Project Overview

Your Dubai Tourism AI Assistant consists of:
- **main.py**: FastAPI application with chat and evaluation endpoints
- **tourism_graph.py**: LangGraph-based RAG system with TF-IDF retrieval
- **requirements.txt**: Python dependencies
- **Procfile**: Render deployment configuration

## Step 1: Prepare Your Repository

Ensure your GitHub repository has all necessary files committed:

```bash
# Check current status
git status

# Add any missing files
git add main.py requirements.txt tourism_graph.py Procfile

# Commit changes
git commit -m "Prepare for Render deployment"

# Push to GitHub
git push origin main
```

Your repository should contain:
- `main.py` - Main FastAPI application
- `tourism_graph.py` - RAG logic and knowledge base
- `requirements.txt` - Dependencies (fastapi, uvicorn, langgraph, etc.)
- `Procfile` - Tells Render how to run your app

## Step 2: Create Render Account

1. Go to [https://render.com](https://render.com)
2. Sign up using your GitHub account (recommended) or email
3. Verify your email address

## Step 3: Create a New Web Service on Render

1. In your Render dashboard, click **"New +"** → **"Web Service"**
2. Connect your GitHub account if prompted
3. Search for and select your repository: `Dubai-Tourism-AI-Assistant-Multi-Agent-System-`
4. Configure the service:
   - **Name**: `dubai-tourism-ai-assistant` (or similar)
   - **Region**: Choose closest to your users (e.g., US East, EU West)
   - **Branch**: `main`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`
   - **Environment**: Python 3.x (latest stable)

## Step 4: Environment Variables (Optional)

Your current implementation doesn't require API keys (it uses TF-IDF retrieval), so no environment variables are needed. However, if you later add LLM integrations:

1. In your Render service settings, go to **Environment**
2. Add any required variables (e.g., `OPENAI_API_KEY`, `ANTHROPIC_API_KEY`)
3. Click **"Save Changes"**

## Step 5: Deploy Your Service

1. Click **"Create Web Service"**
2. Render will automatically:
   - Clone your repository
   - Install dependencies from `requirements.txt`
   - Start your application using the Procfile/start command
   - Provide a unique URL (e.g., `https://dubai-tourism-ai-assistant.onrender.com`)

## Step 6: Verify Deployment

Once deployment completes (typically 2-5 minutes):

1. Visit your Render service URL
2. You should see a JSON response from the health check endpoint:
   ```json
   {
     "status": "live",
     "service": "Dubai Tourism AI Assistant",
     "version": "1.0.0"
   }
   ```
3. Test the chat endpoint using curl or a browser:
   ```bash
   curl -X POST "https://your-service.onrender.com/chat" \
        -H "Content-Type: application/json" \
        -d '{"query": "What are the best attractions to visit in Dubai?"}'
   ```
4. Expected response format:
   ```json
   {
     "intent": "attractions",
     "response": "Here are the best Dubai attractions matching your query:\n- Burj Khalifa: The tallest building in the world...\n- Dubai Marina: A modern waterfront district...\n- Palm Jumeirah: A man-made island known for luxury resorts..."
   }
   ```

## Step 7: Test Evaluation Endpoint

Verify the evaluation metrics endpoint:
```bash
curl "https://your-service.onrender.com/evaluate"
```
This will return system performance metrics including route accuracy, retrieval hit rate, and latency statistics.

## Step 8: Share Your Live Demo

Your live demo is now available at:
```
https://your-service-name.onrender.com
```

**Key endpoints to showcase:**
- **Health Check**: `GET /` - Confirms service is running
- **Chat**: `POST /chat` - Main RAG functionality 
- **Evaluation**: `GET /evaluate` - System performance metrics

## Troubleshooting

### Common Issues:

1. **Port Binding Error**: Ensure you're using `$PORT` in your start command (Render provides this dynamically)
2. **Module Not Found**: Double-check all dependencies are in `requirements.txt`
3. **Application Errors**: Check Render logs for detailed error messages
4. **Build Failures**: Verify Python version compatibility

### Accessing Logs:
1. In Render dashboard, select your service
2. Click **"Logs"** to view real-time output
3. Use **"View Deploy Log"** for build-specific information

## Next Steps for Enhancement

To make your demo even more impressive for hiring managers:

1. **Add a Simple Frontend**: Create a basic HTML/JavaScript interface
2. **Implement Caching**: Add Redis for faster repeated queries
3. **Enhanced RAG**: Integrate with vector databases like Pinecone or Weaviate
4. **LLM Integration**: Add OpenAI/Anthropic for generative responses
5. **Dockerize**: Create a Dockerfile for more controlled deployment
6. **Monitoring**: Add health checks and performance metrics

## Why This Impresses Hiring Managers

As noted in your context: "A Dubai hiring manager will pick a candidate with a live RAG demo on Render + a GitHub repo over a candidate with an AWS cert and no projects. Every time."

Your deployed demo demonstrates:
- **Practical Implementation**: Working RAG system, not just theory
- **Full-Stack Understanding**: Backend API, deployment knowledge
- **Production Readiness**: Live endpoint handling real requests
- **Git Proficiency**: Proper version control and collaboration
- **Problem Solving**: End-to-end AI application development

## Maintenance Tips

1. **Automatic Deploys**: Render auto-deploys on GitHub pushes (enable in service settings)
2. **Manual Trigger**: Use "Deploy latest commit" button in Render dashboard
3. **Scale Awareness**: Free tier has limitations; consider upgrading for production
4. **Regular Updates**: Keep dependencies current with `pip list --outdated`

---

**Your live RAG demo is now deployed and ready to showcase to potential employers!** Share your Render URL alongside your GitHub repository to maximize your impact in the Dubai job market.