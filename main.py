import datetime as dt
import matplotlib
import matplotlib.pyplot as plt
import netifaces
import numpy as np
import pyvisa
from matplotlib.widgets import RadioButtons


def changewave(label):
    inst.write(f"sens:corr:wav {label}")
    global a
    a = label + '\n'


def animate(i, xs, ys, ys_mean):
    global b
    if a != b:
        xs.clear()
        ys.clear()
        ys_mean.clear()
    xs.append(dt.datetime.now().strftime('%M:%S.%f')[:-3])
    ys.append(float(inst.query("READ?")) * 100000)
    xs, ys = xs[-10:], ys[-10:]
    ys_mean.append(np.average(ys))
    ys_mean = []
    ys_mean = ys_mean[-10:]
    ax1.clear()
    ax2.clear()
    plt.subplots_adjust(left=0.11)
    ax1.set_title(name)
    ax1.set_ylabel('Power, W*10e-6')
    ax2.set_ylabel('Average power, W*10e-6')
    ax1.plot(xs, ys, 'b')
    ax2.plot(xs, ys_mean, 'r')
    b = inst.query("sens:corr:wav?")


if __name__ == '__main__':
    inst = pyvisa.ResourceManager().open_resource('USB0::4883::32886::M00554182::0::INSTR')
    matplotlib.use("webagg")
    matplotlib.rcParams['webagg.port'] = 8080
    matplotlib.rcParams['webagg.open_in_browser'] = False
    matplotlib.rcParams['webagg.address'] = netifaces.ifaddresses('wlan0')[netifaces.AF_INET][0]['addr']
    inst.write(f"sens:corr:wav 400")
    name = inst.query("*IDN?")
    a = '400\n'
    b = '400\n'
    fig = plt.figure(figsize=(13.31, 5.35))
    wave_button = RadioButtons(plt.axes([0.002, 0.845, 0.05, 0.145]), ('400', '500', '633', '800', '1064', '1100'))
    an = wave_button.on_clicked(changewave)
    ax1 = fig.add_subplot(2, 1, 1)
    ax2 = fig.add_subplot(2, 1, 2)
    ani = matplotlib.animation.FuncAnimation(fig, animate, fargs=([], [], []), interval=50)
    plt.show()
