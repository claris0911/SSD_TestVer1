from flask import Flask, request, render_template_string
import re

app = Flask(__name__)

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
            return render_template_string('''<h1>XSS Attack Detected</h1>
                                             <a href="/">Go back</a>''')
        elif is_sql_injection(search_term):
            return render_template_string('''<h1>SQL Injection Detected</h1>
                                             <a href="/">Go back</a>''')
        else:
            return render_template_string(f'''<h1>Search Term: {search_term}</h1>
                                             <a href="/">Go back</a>''')
    return render_template_string('''<form method="post">
                                        Search: <input type="text" name="search_term">
                                        <input type="submit" value="Submit">
                                     </form>''')

if __name__ == '__main__':
    app.run(debug=True)
