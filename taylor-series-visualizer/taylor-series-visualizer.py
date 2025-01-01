import numpy as np # pip install numpy
import sympy as sp # pip install sympy
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
from matplotlib.ticker import MultipleLocator

N_MAX = 10

def calculate_taylor_series(function, n, var, a=0):
    terms = []
    taylor_series = []
    derivative = function

    for i in range(n + 1):
        if i > 0:
            derivative = sp.diff(derivative, var)
        der_a = derivative.evalf(subs={var: a})
        term = sp.Rational(der_a, sp.factorial(i)) * (var - a)**i
        terms.append(term)

        taylor_series.append(sp.sympify(" + ".join([str(term) for term in terms])))
    return taylor_series

if __name__ == "__main__":

    # Parse the function string into a SymPy expression
    user_func = input("Enter a mathematical function in terms of x: ")
    user_func = user_func.replace('e', 'E')
    x = sp.symbols('x')
    try:
        func = sp.sympify(user_func)
    except sp.SympifyError:
        print("Invalid function input.")
        exit(1)

    # Generate list of Taylor Series from T0(x) through Tn(x)
    taylor_series_list = calculate_taylor_series(func, N_MAX, x)

    # Plot the function the user entered
    range_x = np.linspace(-50, 50, 500)
    range_y = [min(func.evalf(subs={x: val}), 100) for val in range_x]
    fig, ax = plt.subplots()
    ax.plot(range_x, range_y, label=f"$f(x) = {sp.latex(func)}$", linestyle='dashed', color='navy')

    # Plot the first Taylor Series function
    taylor_series = taylor_series_list[0]
    ts_range_y = [taylor_series.evalf(subs={x: val}) for val in range_x]
    taylor_series_line, = ax.plot(range_x, ts_range_y, label="Taylor Series", linestyle='solid', color='red')

    # Adding bold lines for the x-axis and y-axis
    ax.axhline(0, color='black', linewidth=1.5)
    ax.axvline(0, color='black', linewidth=1.5)
    
    # Plot settings
    ax.legend()
    ax.grid(True)
    ax.set_xlim(-10, 10)
    ax.set_ylim(-10, 10)
    ax.xaxis.set_major_locator(MultipleLocator(2))
    ax.yaxis.set_major_locator(MultipleLocator(2))
    for spine in ax.spines.values(): spine.set_color(None)
    plt.subplots_adjust(bottom=0.15)

    plt.suptitle(f"Taylor Series for $\\mathbf{{f(x) = {sp.latex(func)}}}$", fontsize=14, fontweight='bold')
    ax.set_title(f"$T_{0}(x) = {sp.latex(taylor_series)}$", fontsize=14)


    # Draw slider to the screen
    n_slider_ax = plt.axes([0.25, 0.05, 0.5, 0.03])
    n_slider = Slider(n_slider_ax, "n", valmin=0, valmax=N_MAX, valinit=0, valstep=1)
    
    # Create notches along the slider
    for notch in range(N_MAX + 1):
        n_slider.ax.axvline(notch, color='black', linewidth=1, alpha=0.5)

    def update_taylor_series(val):
        global range_x, taylor_series, taylor_series_list
        
        # Plot the current Taylor Series
        taylor_series = taylor_series_list[int(n_slider.val)]
        ts_range_y = [taylor_series.evalf(subs={x: val}) for val in range_x]
        taylor_series_line.set_ydata(ts_range_y)

        ax.set_title(f"$T_{{{n_slider.val}}}(x) = {sp.latex(taylor_series)}$", fontsize=14)
        ax.legend()
        fig.canvas.draw_idle()
    
    n_slider.on_changed(update_taylor_series)
    
    plt.show()
