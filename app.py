from flask import Flask, render_template, Response, request, jsonify
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

@app.route("/users")
def users():
    return render_template('users.html')

@app.route("/researchers")
def researchers():
    return render_template('researchers.html')

@app.route("/aboutdp")
def aboutdp():
    return render_template('aboutdp.html')

@app.route("/gen_plot", methods=['GET', 'POST'])
def gen_plot():
    data = request.json
    slope = 1
    intercept = 1
    print(request.method)
    if request.method == 'POST':
        print("Post???")
        slope = float(data.get("slope", 1.5))
        intercept = float(data.get("intercept", 1.5))
    print("HEllo!")
    plot_url = f"/plot.png?slope={slope}&intercept={intercept}"
    return jsonify({'plot_url': plot_url})
    
@app.route('/plot.png')
def plot_png():
    slope = float(request.args.get("slope", 1.0))
    intercept = float(request.args.get("intercept", 1.0))
    
    fig = create_figure(slope, intercept)
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')


def create_figure(slope, intercept):
    plt.close()
    print("Creating figure")
    print(slope)
    print(intercept)
    plt.figure()
    fig, ax = plt.subplots(figsize=(10, 6))
    #if x_range is None:
    x_vals = np.array(ax.get_xlim())
    y_vals = intercept + slope * x_vals
    ax.plot(x_vals, y_vals, '--')
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_title(f"Line with slope {slope} and intercept {intercept}")
    return fig

# def hello():
#     return "Hello, Flask!"

if __name__ == "__main__":
    app.run(debug=True)