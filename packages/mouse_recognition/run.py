from fastai.vision import *
import time
import matplotlib.pyplot as plt
import numpy as np
import PIL
from cycler import cycler
from matplotlib.collections import LineCollection
from pymouse import PyMouse

import terminal_handler.write
from mouse_recognition.config.config import Config

configuration = Config()
configuration.load_yml('config.yml')
terminal_handler.write.clear_all()

colors = configuration.COLORS
plt.rcParams['axes.prop_cycle'] = cycler(color=colors)


def canvas_from_data(delta_batch, dpi, linewidth, cmap, plot_lim):
    fig, ax = plt.subplots(1, figsize=(4, 4), dpi=dpi)
    points = np.array([delta_batch[:, 0], delta_batch[:, 1]]).T.reshape(-1, 1, 2)
    segments = np.concatenate([points[:-1], points[1:]], axis=1)
    lc = LineCollection(segments, cmap=cmap, norm=plt.Normalize(0, 1))
    lc.set_array(np.linspace(0, 1, delta_batch.shape[0])), lc.set_linewidth(linewidth)
    line = ax.add_collection(lc)
    plt.axis('off'), plt.xlim(-plot_lim, plot_lim), plt.ylim(-plot_lim, plot_lim)
    plt.subplots_adjust(top=1, bottom=0, right=1, left=0,
                        hspace=0, wspace=0)
    ax.figure.canvas.draw(), plt.close()
    return ax.figure.canvas


def save_image(canvas, path, img_size):
    pil_image = PIL.Image.frombytes('RGB', canvas.get_width_height(), canvas.tostring_rgb())
    pil_image = pil_image.resize((img_size, img_size), PIL.Image.ANTIALIAS)
    pil_image.save(path)
    #pil_image = None
    #canvas = None


with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    learn = load_learner('ai_models', 'fastai_model01.pkl')

sequence_len = 800
n_max_iteration = 10000000
data = np.zeros([sequence_len, 2])
mouse_position_index = 0
mouse = PyMouse()
x_old, y_old = mouse.position()

for _ in range(n_max_iteration):
    x, y = mouse.position()
    delta_x, x_old = x - x_old, x
    delta_y, y_old = y - y_old, y

    # Discard too small and too big mouse movements
    if (np.abs(delta_x) < 0.5 or np.abs(delta_x) > 100):
        continue
    if (np.abs(delta_y) < 0.5 or np.abs(delta_y) > 100):
        continue

    data[mouse_position_index, 1] = delta_x
    data[mouse_position_index, 0] = delta_y
    mouse_position_index = mouse_position_index + 1
    time.sleep(0.01)
    terminal_handler.write.progress_bar(mouse_position_index, sequence_len)
    if mouse_position_index == sequence_len:
        break

# Create image from mouse position sequence stored in "data"
save_image(canvas_from_data(data, dpi=500, linewidth=0.1, cmap='viridis', plot_lim=10), './temp.png', 224)
img = open_image('./temp.png')
# img = open_image('./test_imgs/giuseppe/delta_00014.png')
# img = open_image('./test_imgs/andrea/delta_00035.png')
# img = open_image('./test_imgs/dario/delta_00015.png')

# Show results
fig, (ax0, ax1, ax2) = plt.subplots(1, 3, figsize=(20, 4))
img.show(ax=ax0)
ax1.plot(data)
[ax.axis('off') for ax in (ax0, ax1, ax2)]
prediction = learn.predict(img)
best_prediction_index = int(prediction[2].argmax())
ax2.text(0, 1.03, f'ANDREA {prediction[2][0]:0.2f}', size=20,
         color=(colors[0] if best_prediction_index == 0 else colors[1]), fontfamily='Impact', va='bottom', ha='center')
ax2.text(-3 ** 0.5 / 2, -0.53, f'GIUSEPPE {prediction[2][1]:0.2f}', size=20,
         color=(colors[0] if best_prediction_index == 1 else colors[1]), fontfamily='Impact', va='top', ha='center')
ax2.text(3 ** 0.5 / 2, -0.53, f'DARIO {prediction[2][2]:0.2f}', size=20,
         color=(colors[0] if best_prediction_index == 2 else colors[1]), fontfamily='Impact', va='top', ha='center')
x = (prediction[2][2] - prediction[2][1]) * 3 ** 0.5 / 2
y = prediction[2][0] - (prediction[2][2] + prediction[2][1]) * 0.5
plt.scatter(x, y, zorder=10, s=300, marker='H')
plt.scatter(0, 0, zorder=10, s=100, marker='+', color=colors[1])
ax2.plot([-3 ** 0.5 / 2, 3 ** 0.5 / 2, 0, -3 ** 0.5 / 2], [-0.5, -0.5, 1, -0.5], color=colors[2])
ax2.set_aspect(1)
plt.savefig('demo.png', bbox_inches='tight')

from kivy.app import App
from kivy.uix.image import Image


class MyApp(App):
    def build(self):
        return Image(source='demo.png')


MyApp().run()
