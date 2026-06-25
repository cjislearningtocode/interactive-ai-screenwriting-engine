\# Interactive AI Screenwriting Engine

An interactive, terminal-based screenwriting assistant and project blueprint manager built in Python. This engine leverages the Google GenAI SDK to collaboratively outline, structure, and develop script concepts, plot architectures, and character arcs in real time.

\#\# Features

\* \*\*Interactive Terminal Interface:\*\* A clean command-line menu system to start fresh script projects or load existing blueprints.  
\* \*\*Core AI Screenwriting Architecture:\*\* Deep integration with generative models to assist with narrative pacing, scene outlines, and structural breakdowns.  
\* \*\*Secure Key Management:\*\* Fully integrated with system environment variables to protect API credentials during development and deployment.

\#\# Installation & Setup

\#\#\# 1\. Clone the Repository  
\`\`\`bash  
git clone \[https://github.com/cjislearningtocode/interactive-ai-screenwriting-engine.git\](https://github.com/cjislearningtocode/interactive-ai-screenwriting-engine.git)  
cd interactive-ai-screenwriting-engine 

echo 'export GEMINI\_API\_KEY="your\_api\_key\_here"' \>\> \~/.zshrc  
source \~/.zshrc

python3 [screenwrite.py](http://screenwrite.py) 

\#\# Technical Foundations  
\* \*\*Languages:\*\* Python 3  
\* \*\*Concepts:\*\* Google GENAI SDK (google-genai), OS Environment Management

\--- \#\#\# How to push this to GitHub:   
Once you have saved the file, go back to your terminal window and run these final three commands one by one to send it live:   
\`\`\`bash git add README.md   
git commit \-m "Docs: Add project README with setup instructions"   
git push origin main