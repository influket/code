from flask import Flask, jsonify, render_template
import time
import threading

app = Flask(__name__)

# Variables to track progress and scraping status
progress = 0
scraping_thread = None
scraping_active = False

def scrape_nse():
    global progress, scraping_active
    progress = 0
    scraping_active = True

    for i in range(1, 101):
        if not scraping_active:
            break
        time.sleep(0.1)  # Simulate scraping delay
        progress = i

    scraping_active = False

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/start-scraping', methods=['POST'])
def start_scraping():
    global scraping_thread
    if not scraping_thread or not scraping_thread.is_alive():
        scraping_thread = threading.Thread(target=scrape_nse)
        scraping_thread.start()
        return jsonify(status="started")
    return jsonify(status="already running")

@app.route('/stop-scraping', methods=['POST'])
def stop_scraping():
    global scraping_active
    scraping_active = False
    return jsonify(status="stopped")

@app.route('/progress')
def get_progress():
    return jsonify(progress=progress)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
