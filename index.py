from flask import Flask, render_template, request, json
from TextSummarization import TextSummarzation

app = Flask(__name__)

@app.route('/')
def main():
    return render_template('login.html')

@app.route('/import', methods=['GET ','POST'])
def import_data():
    _url = request.form['url']
    text = ts.get_text_from_url(_url)
    return render_template('login.html', message=text)


@app.route('/stopwords')
def show_without_stopwords():
    # call get text from url to get text data
    text = ts.remove_stopwords()
    return render_template('login.html', message=text)

@app.route('/tokenize')
def tokenize():
    # call ts function tokenize to create tokens and dispaly it on screen
    tokens = ts.word_tokens()
    return render_template('login.html', message=tokens)

@app.route('/summarize')
def summarize():
    # call ts function summarize to summarize and display it on screen
    data = ts.summarize()
    return render_template('login.html', text=data)

if __name__ == '__main__':
    ts = TextSummarzation()
    app.run()    
