import sys
import random
import matplotlib.pyplot as plt     # pip install matplotlib
from matplotlib.animation import FuncAnimation
from matplotlib.widgets import Slider, Button

# Colors
def_color = 'white'
h_red = 'red'
h_green = 'green'
h_yellow = '#ffd500'
h_grey = '#8c8c8c'
button_hover = h_green
bg_color = '#22283e'

def end_animation():
    for i in range (len(colors)): colors[i] = def_color
    yield data[:]
    yield None


# Quadratic

def bubble_sort(data):

    # The two elements in the bubble are RED
    # A GREEN element denotes a swap

    n = len(data)
    for i in range(n):
        for j in range(n - i - 1):
            colors[j] = h_red
            colors[j + 1] = h_red
            yield data[:]

            if data[j] > data[j + 1]:
                data[j], data[j + 1] = data[j + 1], data[j]

                colors[j + 1] = h_red
                colors[j] = h_green
                yield data[:]

            colors[j] = def_color
            colors[j + 1] = def_color

    yield from end_animation()

def insertion_sort(data):

    # The division between sorted and unsorted lists is GREEN
    # The element to be inserted is RED

    n = len(data)
    for i in range(1, n):
        colors[i] = h_green
        j = i
        while j > 0:
            colors[j - 1] = h_red
            if data[j - 1] > data[j]:
                data[j], data[j - 1] = data[j - 1], data[j]
                yield data[:]
            colors[j - 1] = def_color
            j -= 1
        colors[i] = def_color

    yield from end_animation()

def selection_sort(data):

    # The division between sorted and unsorted lists is GREEN
    # The element being looked at is RED
    # The selected minimum element is YELLOW

    n = len(data)
    for i in range(n):
        index = i
        colors[i] = h_green
        for j in range(i + 1, n):
            colors[j] = h_red
            if data[j] < data[index]:
                if index != i: colors[index] = def_color
                index = j
                colors[j] = h_yellow
            else:
                yield data[:]
                colors[j] = def_color

        data[i], data[index] = data[index], data[i]
        colors[i] = def_color
        colors[index] = def_color
    
    yield from end_animation()

def shell_sort(data):

    # The bounds of the gap are GREEN
    # All data in the gap is GREY

    n = len(data)
    gap = n // 2
    while gap > 0:
        for i in range(gap, n):
            j = i

            colors[i] = h_green
            for k in range(j - gap + 1, i): colors[k] = h_grey
            colors[j - gap] = h_green
            yield data[:]

            while j >= gap:
                if data[j - gap] > data[j]:
                    data[j], data[j - gap] = data[j - gap], data[j]
                    yield data[:]
                j -= gap

            colors[i] = def_color
            for k in range(j, i): colors[k] = def_color
        gap = gap // 2
    
    yield from end_animation()

# Divide-and-conquer

def merge_sort(data, start=0, end=None):
    
    # Data starts out GREY
    # Data being merged is highlighted to WHITE (def_color)

    for i in range(len(data)): colors[i] = h_grey
    if end is None: end = len(data)
    if end - start > 1:
        mid = (start + end) // 2

        # Recursively sort the left and right halves
        yield from merge_sort(data, start, mid)
        yield from merge_sort(data, mid, end)

        # Merge
        left = data[start:mid]
        right = data[mid:end]
        i = j = 0
        for k in range(start, end):
            if i < len(left) and (j >= len(right) or left[i] <= right[j]):
                data[k] = left[i]
                i += 1
            else:
                data[k] = right[j]
                j += 1

            colors[k] = def_color
            yield data[:]
    
    if start == 0 and end == len(data): yield from end_animation()

def quick_sort(data, start=0, end=None):
    
    # The pivot element is GREEN
    # The element being looked at is RED
    # The current placement for new pivot is YELLOW
    
    if end is None: end = len(data) - 1
    if start < end:
        pivot = data[end]
        colors[end] = h_green

        # Partition
        j = start - 1
        prev_index = None
        for i in range(start, end):
            colors[i] = h_red
            yield data[:]

            if data[i] < pivot:
                j += 1
                data[i], data[j] = data[j], data[i]

                if prev_index is not None: colors[prev_index] = def_color
                colors[j] = h_yellow
                prev_index = j
                yield data[:]

            colors[i] = def_color

        # Move pivot
        data[j + 1], data[end] = data[end], data[j + 1]
        if prev_index is not None: colors[prev_index] = def_color
        colors[end] = def_color
        yield data[:]

        yield from quick_sort(data, start, j)
        yield from quick_sort(data, j + 2, end)
    
    if start == 0 and end == len(data) - 1: yield from end_animation()


# Heap

def heapify(data, n, root):
    maximum = root
    left = (2 * root) + 1
    right = (2 * root) + 2

    if root != 0: colors[root] = h_red

    # Locate any larger values benneath the root
    if (left < n) and (data[left] > data[maximum]): maximum = left
    if (right < n) and (data[right] > data[maximum]): maximum = right

    # A larger value is deeper than the root -> swap max and root
    if maximum != root:
        colors[maximum] = h_yellow
        data[root], data[maximum] = data[maximum], data[root]
        yield data[:]
        yield from heapify(data, n, maximum)
    
    colors[root] = def_color 

def heap_sort(data):
    
    # The root to be inserted at the end is GREEN
    # The roots for each heapify call are RED
    # The candidate for the new root during heapify is YELLOW

    # Build the initial max heap
    n = len(data)
    for i in range((n // 2) - 1, -1, -1):
        yield from heapify(data, n, i)

    # Move root (largest value) to the end and re-heapify
    for i in range(n - 1, 0, -1):
        colors[0] = colors[i] = h_green
        data[0], data[i] = data[i], data[0]
        yield from heapify(data, i, 0)
        colors[i] = def_color
    
    yield from end_animation()


# Animation

def update(frame):
    if frame is None:
        animate.event_source.stop()
        return
    else:
        global is_paused
        if(is_paused):
            animate.event_source.stop()
            for i in range (len(colors)): colors[i] = def_color

        # The data is plotted as bars to visualize quantity
        ax.clear()
        ax.bar(indices, frame, color=colors)
        ax.set_xticks([])
        ax.set_yticks([])
        ax.set_title(f"{alg.capitalize()} Sort", fontsize=16, color=def_color)


if __name__ == "__main__":

    # Get algorithm from command line
    error = False
    alg = ""
    options=["bubble", "insertion", "selection", "shell", "merge", "quick", "heap"]
    if len(sys.argv) != 2:
        error = True
    else:
        alg = sys.argv[1].lower()
    if alg not in options: error = True
    if error:
        print(f"Select one sorting algorithm from:")
        columns = 4
        for i in range(0, len(options)):
            if i % columns != (columns - 1):
                print(f"  {options[i]:<10}", end="")
            else:
                print(f"  {options[i]:<10}")
        exit(1)

    # Create data
    n = 50
    data = list(range(1, n + 1))
    random.shuffle(data)
    indices = list(range(len(data)))
    sort_generator = eval(f"{alg}_sort(data)")

    # Set up fig and ax objects
    fig, ax = plt.subplots()
    fig.set_facecolor(bg_color)
    ax.set_facecolor('none')
    for spine in ax.spines.values(): spine.set_color(def_color)
    ax.set_title(f"{alg.capitalize()}" + " Sort", fontsize=16, color=def_color)

    colors = [def_color] * n
    ax.bar(indices, data, color=colors)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_title(f"{alg.capitalize()} Sort", fontsize=16, color=def_color)

    # Sliders
    speed_slider_ax = plt.axes([0.35, 0.01, 0.3, 0.05])
    speed_slider = Slider(speed_slider_ax, 'Speed', 1, 1000, valinit=500, valstep=1)
    speed_slider.label.set_color(def_color)
    speed_slider.valtext.set_visible(False)
    speed_slider.ax.set_facecolor(bg_color)

    size_slider_ax = plt.axes([0.35, 0.05, 0.3, 0.05])
    size_slider = Slider(size_slider_ax, 'Size', 10, 75, valinit=50, valstep=1)
    size_slider.label.set_color(def_color)
    size_slider.valtext.set_color(def_color)
    size_slider.ax.set_facecolor(bg_color)

    # Play Button
    play_button_ax = plt.axes([0.8, 0.9, 0.1, 0.05])
    play_button = Button(play_button_ax, 'Play')
    play_button.label.set_color(def_color)
    play_button.color = bg_color
    play_button.hovercolor = button_hover

    # Animation
    is_paused = True
    animate = FuncAnimation(fig, update, frames=sort_generator,
                                interval=speed_slider.valmax - speed_slider.val, blit=False,
                                cache_frame_data=False)

    def reset(val):
        global data, indices, colors, alg, is_paused, animate, sort_generator

        play_button.color = bg_color
        play_button.hover = button_hover

        if animate: animate.event_source.stop()

        # Reinitialize data and variables
        n = int(size_slider.val)
        data = list(range(1, n + 1))
        random.shuffle(data)
        indices = list(range(len(data)))
        colors = [def_color] * n

        # Reset generator and animation
        is_paused = True
        sort_generator = eval(f"{alg}_sort(data)")
        animate = FuncAnimation(fig, update, frames=sort_generator,
                                interval=speed_slider.valmax - speed_slider.val, blit=False,
                                cache_frame_data=False)

    def play(event):
        global is_paused
        if is_paused:
            play_button.color = button_hover
            is_paused = False
            animate.event_source.start()

    speed_slider.on_changed(reset)
    size_slider.on_changed(reset)
    play_button.on_clicked(play)

    plt.show()