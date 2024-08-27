from flask import Flask, request, render_template
import json
from firecrawl import FirecrawlApp
import google.generativeai as genai
import markdown
import os
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)
genai.configure(api_key=os.getenv('GEMINI_API_KEY'))

model = genai.GenerativeModel('gemini-1.5-flash')

# Initialize Firecrawl
firecrawl = FirecrawlApp(api_key=os.getenv('FIRECRAWL_API_KEY'))

def get_summary(page_content):
    summary = model.generate_content(f'give the summary of the news article within 400 words , the news article is: {page_content}').text
    return summary

@app.route('/', methods=['GET', 'POST'])
def index():
    summary = None
    important_points = None
    url = None

    if request.method == 'POST':
        url = request.form['url']
        print("URL GOT:",url)
        try:
            page_content = firecrawl.scrape_url(url=url, params={"pageOptions": {"onlyMainContent": True}})
            summary = get_summary(page_content)
        except Exception as e:
            summary = "An error occurred: " + str(e)

    return render_template('index.html', summary=summary, url=url)

if __name__ == '__main__':
    app.run(debug=True)
