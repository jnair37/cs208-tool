from flask import Flask, render_template, Response, request, jsonify
import matplotlib.pyplot as plt
import matplotlib
import io
import numpy as np
import math
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas

# Import the epsilon_optimizer module directly
from epsilon_optimizer import find_optimal_epsilon, calculate_W

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
    
@app.route("/gen_w_plot", methods=['GET', 'POST'])
def gen_w_plot():
    data = request.json
    # slope = 1
    # intercept = 1
    epsilon_a = 1
    epsilon_b = 1
    n = 1
    # print(request.method)
    if request.method == 'POST':
        # print("Post???")
        # slope = float(data.get("slope", 1.5))
        # intercept = float(data.get("intercept", 1.5))
        epsilon_a = float(data.get("epsilon_a", 1.5))
        epsilon_b = float(data.get("epsilon_b", 1.5))
        n = float(data.get("n", 1.5))
    print("W HEllo!")
    plot_url = f"/plot_welfare.png?epsilon_a={epsilon_a}&epsilon_b={epsilon_b}&n={n}"
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

@app.route('/plot_welfare.png')
def plot_welfare_png():
    #slope = float(request.args.get("slope", 1.0))
    #intercept = float(request.args.get("intercept", 1.0))
    epsilon_a = float(request.args.get("epsilon_a", 1.5))
    epsilon_b = float(request.args.get("epsilon_b", 1.5))
    n = float(request.args.get("n", 1))
    
    mx_ep = find_optimal_epsilon(epsilon_a, epsilon_b, n)[0]
    fig = create_w_figure(mx_ep, epsilon_a, epsilon_b, n)
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')

def create_w_figure(max_epsilon, epsilon_a, epsilon_b, n):
    plt.close()
    print("Creating welfare function graph")
    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')
    #if x_range is None:
    x_vals = np.linspace(epsilon_a, epsilon_b, 10000)
    y_vals = np.linspace(0, 10000, 10000) # n range?
    print(len(x_vals))
    print(len(y_vals))
    z_vals = list(map(lambda x, y: calculate_W(x, epsilon_a, epsilon_b, y), x_vals, y_vals))
    ax.scatter(x_vals, y_vals, z_vals)
    tw = calculate_W(max_epsilon, epsilon_a, epsilon_b, n)
    ax.scatter([max_epsilon], [n], [tw], color='red')
    ax.set_xlabel("Epsilon")
    ax.set_ylabel("Number of participants")
    ax.set_zlabel("Total Welfare")
    ax.set_title(f"Epsilon= {max_epsilon}; welfare={tw}")
    return fig

def privacy_risk(epsilon, n=1000):
    return 1/(1 + (n-1)*math.e**(-1*epsilon))

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


@app.route("/calculate_optimal", methods=['POST'])
def calculate_optimal():
    data = request.json
    epsilon_a = float(data.get('epsilon_a', 0.01))
    epsilon_b = float(data.get('epsilon_b', 2.0))
    N = int(data.get('N', 100))
    
    try:
        optimal_epsilon, max_welfare = find_optimal_epsilon(epsilon_a, epsilon_b, N)
        return jsonify({
            'optimal_epsilon': optimal_epsilon,
            'max_welfare': max_welfare
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 400


# def hello():
#     return "Hello, Flask!"

if __name__ == "__main__":
    app.run(debug=True)