import os
from flask import Flask, request, render_template_string
from groq import Groq

app = Flask(__name__)

# --- CONFIGURATION ---
# Paste your NEW Groq API key here
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
client = Groq(api_key=GROQ_API_KEY)

@app.route('/', methods=['GET', 'POST'])
def index():
    report = ""
    scan_data = ""
    
    if request.method == 'POST':
        scan_data = request.form.get('scan_data')
        if scan_data:
            prompt = f"""
            You are a Senior Penetration Tester. 
            Analyze the following raw vulnerability scan data:

            {scan_data}

            Provide a professional report with:
            1. Top Critical Vulnerabilities.
            2. Exploitation Scenario (How a hacker uses this).
            3. Remediation Steps (How to fix it).
            """
            
            try:
                chat_completion = client.chat.completions.create(
                    messages=[{"role": "user", "content": prompt}],
                    model="openai/gpt-oss-20b",
                )
                report = chat_completion.choices[0].message.content
            except Exception as e:
                report = f"Error: {e}"

    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Cloud AI Security Analyst</title>
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
            body { font-family: Arial; padding: 20px; background: #1e1e1e; color: white; }
            textarea { width: 100%; height: 200px; padding: 10px; font-family: monospace; background: #2d2d2d; color: #0f0; border: 1px solid #444; }
            button { padding: 10px 20px; background: #007bff; color: white; border: none; cursor: pointer; font-size: 16px; margin-top: 10px; }
            .report-box { background: #2d2d2d; padding: 20px; border-radius: 8px; margin-top: 20px; white-space: pre-wrap; font-family: monospace; line-height: 1.5; border-left: 4px solid #007bff; }
        </style>
    </head>
    <body>
        <h2>🤖 Cloud AI Security Analyst</h2>
        <p>Paste your raw scanner output below:</p>
        <form method="POST">
            <textarea name="scan_data" placeholder="Paste scanner logs here...">{{ scan_data }}</textarea>
            <button type="submit">Analyze with AI</button>
        </form>

        {% if report %}
        <div class="report-box">
            <h3>AI Report:</h3>
            {{ report }}
        </div>
        {% endif %}
    </body>
    </html>
    """
    return render_template_string(html, report=report, scan_data=scan_data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)