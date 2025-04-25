from flask import Flask, render_template, Response
import matplotlib.pyplot as plt
import matplotlib
import io
import numpy as np
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas

matplotlib.use('Agg')

app = Flask(__name__)

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/gen_plot")
def gen_plot():
    fig = create_figure()
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')

def create_figure():
    fig, ax = plt.subplots(figsize=(10, 6))
    # Find x and y... ?
    x = np.linspace(0, 10, 100)
    y = np.sin(x)
    ax.plot(x, y)
    return fig

# def hello():
#     return "Hello, Flask!"

if __name__ == "__main__":
    app.run(debug=True)