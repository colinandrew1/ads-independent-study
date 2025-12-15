import numpy as np
import matplotlib.pyplot as plt
from IPython.display import Markdown, display

def plot_with_reference_curves(x, y, label="measured times", title="", show_linear=True, show_log=True, show_nlogn=True, show_n2=False):
    x = np.array(x)
    y = np.array(y)

    plt.figure()
    plt.plot(x, y, marker='o', label=label)

    # scale reference curves to first data point
    if show_linear:
        k = y[0] / x[0]
        plt.plot(x, k * x, label="scaled linear")
    if show_log:
        c = y[0] / np.log2(x[0])
        plt.plot(x, c * np.log2(x), label="scaled log₂(n)")
    if show_nlogn:
        k_nlogn = y[0] / (x[0] * np.log2(x[0]))
        plt.plot(x, k_nlogn * x * np.log2(x), label="scaled n log₂(n)")
    if show_n2:
        k_n2 = y[0] / (x[0] ** 2)
        plt.plot(x, k_n2 * x**2, label="scaled n²")

    plt.title(title)
    plt.xlabel("n")
    plt.ylabel("time (seconds)")
    plt.legend()
    plt.xticks(x, rotation=90)
    plt.show()



def plot_fpr(x_values, fpr_values, target_fpr=None, title=None, xlabel=None):
    plt.figure()
    plt.plot(x_values, fpr_values, marker='o', label="Measured FPR")

    if target_fpr is not None:
        plt.axhline(y=target_fpr, linestyle='--', label="Target FPR")

    plt.xlabel(xlabel if xlabel else "Number of inserted elements (n)")
    plt.ylabel("False positive rate")
    plt.title(title if title else "False Positive Rate")
    plt.legend()
    plt.grid(True)
    plt.show()


def print_markdown_table(results, columns):
    header_line = "| " + " | ".join([col[0] for col in columns]) + " |"
    separator_line = "| " + " | ".join([":" + "-" * (len(col[0])) + ":" for col in columns]) + " |"
    
    rows = []
    for row in results:
        row_values = []
        for col_name, key in columns:
            val = row.get(key, "")
            if isinstance(val, float):
                val = str(round(val, 4))
            else:
                val = str(val)
            row_values.append(val)
        rows.append("| " + " | ".join(row_values) + " |")
    
    table_md = "\n".join([header_line, separator_line] + rows)
    display(Markdown(table_md))