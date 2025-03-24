# app.py
from flask import Flask, render_template, request, redirect, url_for, flash
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Use a secure key for production

def get_job_listings(keyword, location):
    params = {
        'q': keyword,
        'l': location
    }
    response = requests.get('https://www.indeed.com/jobs', params=params)
    soup = BeautifulSoup(response.content, 'html.parser')

    jobs = []
    for listing in soup.find_all('div', {'class': 'jobsearch-SerpJobCard'}):
        title = listing.find('a', {'data-tn-element': 'jobTitle'})['title']
        link = listing.find('a', {'data-tn-element': 'jobTitle'})['href']
        jobs.append({'title': title, 'link': f'https://www.indeed.com{link}'})

    return jobs

@app.route('/')
def index():
    keyword = request.args.get('keyword', '')
    location = request.args.get('location', '')

    if not keyword:
        flash("Please enter a job keyword.", "warning")
        return redirect(url_for('index'))

    jobs = get_job_listings(keyword, location)

    return render_template('index.html', jobs=jobs)

@app.route('/apply/<int:job_id>', methods=['GET'])
def apply(job_id):
    flash("Application submitted successfully!", "success")
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
