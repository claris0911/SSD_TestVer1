from flask import Flask, request, render_template, redirect, url_for, flash
import re
import logging

app = Flask(__name__)
app.secret_key = 'supersecretkey'
logging.basicConfig(filename='app.log', level=logging.INFO)

def is_xss_attack(input_str):
    xss_patterns = ["<.*?>", ".*<.*>.*"]
    for pattern in xss_patterns:
        if re.match(pattern, input_str):
            return True
    return False

def is_sql_injection(input_str):
    sql_patterns = ["' OR '1'='1", "--", ";--", ";", "/*", "*/", "@@", "@", 
                    "char", "nchar", "varchar", "nvarchar", "alter", "begin", 
                    "cast", "create", "cursor", "declare", "delete", "drop", 
                    "end", "exec", "execute", "fetch", "insert", "kill", 
                    "select", "sys", "sysobjects", "syscolumns", "table", 
                    "update"]
    for pattern in sql_patterns:
        if pattern.lower() in input_str.lower():
            return True
    return False

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        search_term = request.form['search_term']
        if is_xss_attack(search_term):
            logging.warning(f'XSS attack detected with input: {search_term}')
            flash('XSS attack detected, please enter a valid search term.')
            return redirect(url_for('index'))
        elif is_sql_injection(search_term):
            logging.warning(f'SQL injection detected with input: {search_term}')
            flash('SQL injection detected, please enter a valid search term.')
            return redirect(url_for('index'))
        else:
            return redirect(url_for('result', search_term=search_term))
    return render_template('index.html')

@app.route('/result')
def result():
    search_term = request.args.get('search_term', '')
    return render_template('result.html', search_term=search_term)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
