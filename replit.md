# PermitPilot

## Overview
PermitPilot is a Flask web application that helps homeowners in Santa Monica, California determine what permits they need for their home improvement projects. The application uses OpenAI's GPT-4 to analyze project descriptions and provide permit recommendations, including estimated fees and requirements.

## Project Structure
- `main.py` - Flask application with routes for home page, processing, and PDF downloads
- `templates/` - HTML templates for the UI
  - `index.html` - Home page with project description form
  - `result.html` - Results page showing permit recommendations
- `static/` - Directory for generated PDF files
- `permits.json` - Database of permit types and requirements for Santa Monica

## Technology Stack
- **Backend**: Python 3.11, Flask
- **AI**: OpenAI GPT-4o-mini for project analysis
- **PDF Generation**: FPDF library
- **Environment**: Replit

## Setup
1. Python 3.11 installed via Replit modules
2. Dependencies managed via pip (requirements.txt)
3. OpenAI API key stored in Replit Secrets as `OPENAI_API_KEY`
4. Flask server runs on port 5000 (0.0.0.0)
5. Deployment configured with Gunicorn for production

## Features
- AI-powered project analysis using OpenAI
- Permit type classification (residential remodel, window replacement)
- Automatic fee estimation
- PDF summary generation for download
- Clean, user-friendly interface

## Recent Changes (October 14, 2025)
- Imported from GitHub
- Fixed file structure (moved result.html to correct templates directory)
- Updated port from 8080 to 5000 for Replit compatibility
- Created .gitignore for Python project
- Installed all dependencies (flask, openai, fpdf, python-dotenv, gunicorn)
- Configured workflow to run Flask development server
- Set up deployment configuration with Gunicorn for production
- Added OpenAI API key via Replit Secrets

## Development
- Run: `python main.py` (via Flask Server workflow)
- Access: View preview on port 5000
- Debug mode enabled for development

## Deployment
- Type: Autoscale
- Server: Gunicorn with port reuse enabled
- Command: `gunicorn --bind=0.0.0.0:5000 --reuse-port main:app`
