from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/gen-plot")
def gen_plot():
    return

def hello():
    return "Hello, Flask!"

if __name__ == "__main__":
    app.run(debug=True)