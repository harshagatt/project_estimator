🚀 DevEstimator AI - AI-Powered Project Estimation Tool
Turn your project requirements into accurate cost and timeline estimates with AI! Built with Python, Flask, MongoDB, and OLAMA.

🌟 Features
AI-generated project estimates (cost, Agile/Waterfall timelines)

History tracking with MongoDB

Clean Bootstrap 5 interface

Easy local deployment

Prompt to get the code from Chatgpt

I would like to create a static page which is connected to my local OLAMA server where I can provide the requirements and it would give me the cost, estimate in AGILE, waterfall model of software development. Create a user guide and code repo so that I can do this on my local machine using python, flask and OLAMA LLM, store the data in mongo db.



Project Folder structure 

/ (root)

│-- app.py
│-- requirements.txt
│-- .env.example

│-- static/
│   │-- index.html
│   │-- css/
│   │-- js/

│-- venv/

│-- .gitignore

🛠️ Installation Guide
1. Prerequisites
macOS (tested on Ventura+)

Python 3.9+

Terminal with sudo access

2. Set Up MongoDB
bash
# 1. Install Homebrew (if you don't have it)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# 2. Add Homebrew to PATH
echo 'eval "$(/opt/homebrew/bin/brew shellenv)"' >> ~/.zshrc
source ~/.zshrc

# 3. Install MongoDB
brew tap mongodb/brew
brew install mongodb-community

# 4. Start MongoDB (keep this running in a separate terminal)
brew services start mongodb-community
3. Set Up Python Environment
bash
# Clone the repository
git clone https://github.com/harshagatt/dev-estimator-ai.git
cd dev-estimator-ai

# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
4. Configure Environment Variables
Create a .env file in the project root with:

env
MONGO_DB_CONNECTION_STRING=mongodb://localhost:27017/
MONGO_DB_NAME=estimator_db
OLAMA_API_URL=http://localhost:11434/api/generate
OLAMA_MODEL_NAME=llama2  # or your preferred model
5. Run the Application
bash
# Start Flask server (default port: 5001)
python app.py
Visit http://localhost:5001 in your browser!

🔍 Troubleshooting
MongoDB not starting?

bash
# Check if MongoDB is running
brew services list

# If port 27017 is blocked:
sudo lsof -i :27017
kill -9 <PID>
Python packages missing?

bash
# Verify installed packages
pip freeze | grep -E "Flask|pymongo|python-dotenv|requests"

# Expected output:
# Flask==2.3.2
# Flask-CORS==3.0.10
# pymongo==4.5.0
# python-dotenv==1.0.0
# requests==2.31.0
UI not loading?

Make sure you have a static folder with index.html

Check browser console for errors (F12)

💡 Pro Tips
For better estimates, customize the AI prompt in app.py

Change the port by running PORT=5002 python app.py

Use ctrl+c to stop the Flask server

📜 License
MIT © Harsha GS
