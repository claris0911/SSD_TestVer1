from flask import Flask, request, redirect, url_for, render_template_string
import re
import logging

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def is_xss_attack(input_str):
    xss_patterns = [
        r"<.*?>", # HTML tags
        r"(&#\d+;)+", # HTML entities
        r"(<|%3C).*script(>|%3E)" # script tags
    ]
    for pattern in xss_patterns:
        if re.search(pattern, input_str, re.IGNORECASE):
            return True
    return False

def is_sql_injection(input_str):
    sql_patterns = [
        r"('|\").*?(\s|--|#|\/\*|;|UNION|SELECT|INSERT|UPDATE|DELETE|DROP|CREATE|ALTER|EXEC|EXECUTE|xp_cmdshell|sp_|OR|AND|HAVING|WAITFOR|GROUP BY|ORDER BY).*?('|\")",
        r"(\s|;|--|#|\/\*).*?(\s|--|#|\/\*)",
        r"(\b(ALTER|CREATE|DELETE|DROP|EXEC|EXECUTE|INSERT|MERGE|SELECT|UPDATE)\b)"
    ]
    for pattern in sql_patterns:
        if re.search(pattern, input_str, re.IGNORECASE):
            return True
    return False

@app.route('/', methods=['GET', 'POST'])
def index():
    error_message = None
    if request.method == 'POST':
        search_term = request.form['search_term']
        if is_xss_attack(search_term):
            error_message = 'XSS Attack Detected. Please enter a valid search term.'
            logging.warning('XSS attack detected with input: %s', search_term)
        elif is_sql_injection(search_term):
            error_message = 'SQL Injection Detected. Please enter a valid search term.'
            logging.warning('SQL injection detected with input: %s', search_term)
        else:
            logging.info('Valid search term entered: %s', search_term)
            return redirect(url_for('result', search_term=search_term))
    return render_template_string('''
                                     {% if error_message %}
                                        <p style="color:red;">{{ error_message }}</p>
                                     {% endif %}
                                     <form method="post">
                                        Search: <input type="text" name="search_term">
                                        <input type="submit" value="Submit">
                                     </form>''', error_message=error_message)

@app.route('/result')
def result():
    search_term = request.args.get('search_term')
    logging.info('Displaying result for search term: %s', search_term)
    return render_template_string(f'''<h1>Search Term: {search_term}</h1>
                                      <a href="/">Go back</a>''')

if __name__ == '__main__':
    app.run(debug=True)
