from flask import Flask, request, render_template_string, redirect, url_for
import re

app = Flask(__name__)

# Define a pattern to detect XSS attacks 
def is_xss_attack(input_str):
    xss_patterns = [r"<.*?>", r".*<.*>.*"]
    for pattern in xss_patterns:
        if re.search(pattern, input_str, re.IGNORECASE):
            return True
    return False

# Define a pattern to detect SQL injection attacks
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

# Home page route
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        search_term = request.form['search_term']
        
        if is_xss_attack(search_term):
            return redirect(url_for('index', message="XSS Attack Detected"))
        
        elif is_sql_injection(search_term):
            return redirect(url_for('index', message="SQL Injection Detected"))
        
        return render_template_string('''<h1>Search Term: {{ search_term }}</h1>
                                         <a href="{{ url_for('index') }}">Go back</a>''', search_term=search_term)
    
    message = request.args.get('message')
    return render_template_string('''<form method="post">
                                        Search: <input type="text" name="search_term">
                                        <input type="submit" value="Submit">
                                     </form>
                                     {% if message %}
                                         <p>{{ message }}</p>
                                     {% endif %}''')

if __name__ == '__main__':
    app.run(debug=True)
