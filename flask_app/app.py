from flask import Flask, render_template, request, jsonify, redirect, url_for
import subprocess
import logging
import json
import os


logging.basicConfig(filename="log.log", level=logging.INFO, format='%(asctime)s (%(lineno)d) ---  %(message)s')

app = Flask(__name__)

@app.route('/')
def home_page():
    logging.info("start the server     ")
    return render_template("index.html")

@app.route('/review', methods=['POST'])
def index():
    spider_name = "flipkart_"
    try:
        searchString = request.form['content'].replace(" ","")
        logging.info(f"serach string: {searchString}")
    except Exception as e:
        logging.info(e)
    
    flipkart_url = "https://www.flipkart.com/search?q=" + searchString

    json_data_path = "../flipkart/output.json"
    try:
        if os.path.exists(json_data_path):
            os.remove(json_data_path)
            logging.info("Json file removed!")
    except :
        logging.info("json file not exist")

    try:
        scrapy_project_path = '../flipkart'
        subprocess.check_output(['scrapy','crawl',spider_name,'-a', f'url={flipkart_url}',"-t","json","-o","output.json"], cwd=scrapy_project_path)
        logging.info("subprocess start")
    except Exception as e:
        logging.info(e)

    try:
        with open(json_data_path, "r") as f:
            logging.info("json open")
            reviews = json.load(f)
    except FileNotFoundError as e:
        logging.info(e)
        return redirect(url_for('/review'))    
    return render_template("results.html", reviews=reviews)

if __name__ == '__main__':
    app.run(host="127.0.0.1", debug=True)
