from flask import Flask, render_template, Response, request, jsonify
import matplotlib.pyplot as plt
import matplotlib
import io
import numpy as np
import math
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
    # slope = 1
    # intercept = 1
    epsilon = 1
    # print(request.method)
    if request.method == 'POST':
        # print("Post???")
        # slope = float(data.get("slope", 1.5))
        # intercept = float(data.get("intercept", 1.5))
        epsilon = float(data.get("epsilon", 1.5))
    print("HEllo!")
    plot_url = f"/plot.png?epsilon={epsilon}"
    return jsonify({'plot_url': plot_url})
    
@app.route('/plot.png')
def plot_png():
    #slope = float(request.args.get("slope", 1.0))
    #intercept = float(request.args.get("intercept", 1.0))
    epsilon = float(request.args.get("epsilon", 1.5))
    
    fig = create_figure(epsilon)
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')


def privacy_risk(epsilon):
    return 1/(1 + math.e**(-1*epsilon))

def create_figure(epsilon):
    plt.close()
    print("Creating figure")
    print(epsilon)
    plt.figure()
    fig, ax = plt.subplots(figsize=(10, 6))
    #if x_range is None:
    x_vals = np.linspace(0, 10, 400)
    y_vals = privacy_risk(x_vals)
    ax.plot(x_vals, y_vals, '--')
    ax.plot([epsilon], [privacy_risk(epsilon)], marker='o', color='red', markersize=10)
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_title(f"Epsilon= {epsilon}; privacy risk={privacy_risk(epsilon)}")
    return fig

# def hello():
#     return "Hello, Flask!"

if __name__ == "__main__":
    app.run(debug=True)