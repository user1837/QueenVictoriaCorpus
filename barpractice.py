import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
import numpy as np
import tkinter

def show_barchart():
    plt.switch_backend('TkAgg')
    freqs = {'1837': 3, '1838': 6, '1839': 10}
    x_locs = np.arange(len(freqs))
    bar_heights = list(freqs.values())
    fig, ax = plt.subplots()
    bars = ax.bar(x_locs, bar_heights, width=0.5, color='r')
    ax.set_ylabel('Frequency')
    ax.set_title('Word frequency by year')
    ax.set_xticks(x_locs)
    ax.set_xticklabels(list(freqs.keys()))
    for b in bars:
        height = b.get_height()
        ax.annotate('{}'.format(height), xy=(b.get_x() + b.get_width() / 2, height), xytext=(0,3), textcoords='offset points', ha='center', va='bottom')
    plt.show()

def show_in_window():
    freqs = {'1837': 3, '1838': 6, '1839': 10}
    x_locs = np.arange(len(freqs))
    bar_heights = list(freqs.values())

    root = tkinter.Tk()
    root.title('Bar Chart')

    fig = Figure(figsize=(5,4), dpi=100)
    ax = fig.add_subplot(111)
    bars = ax.bar(x_locs, bar_heights, width=0.5, color='r')
    ax.set_ylabel('Frequency')
    ax.set_title('Word frequency by year')
    ax.set_xticks(x_locs)
    ax.set_xticklabels(list(freqs.keys()))
    for b in bars:
        height = b.get_height()
        ax.annotate('{}'.format(height), xy=(b.get_x() + b.get_width() / 2, height), xytext=(0, 3),
                    textcoords='offset points', ha='center', va='bottom')

    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.draw()
    canvas.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)

    tkinter.mainloop()

# show_in_window()
def sort_dictionary():
    freqs = {'1840': 3, '1838': 6, '1839': 10}
    itemz = sorted([i for i in freqs.items()], key=lambda x:x[0])
    category, freq = zip(*itemz)
    print(category)
    print(freq)


sort_dictionary()

