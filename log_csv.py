import csv
import gevent
import io
import time
from datetime import datetime

import emotiv

import numpy as np
import matplotlib.pyplot as plt

plt.ion()
mu, sigma = 100, 15
fig = plt.figure()
x = mu + sigma*np.random.randn(10000)
n, bins, patches = plt.hist(x, 50, normed=1, facecolor='green', alpha=0.75)
for i in range(50):
    x = mu + sigma*np.random.randn(10000)
    n, bins = np.histogram(x, bins, normed=True)
    for rect,h in zip(patches,n):
        rect.set_height(h)
    fig.canvas.draw()


if __name__ == "__main__":
    headset = emotiv.Emotiv()
    gevent.spawn(headset.setup)
    gevent.sleep(1)

    filename = datetime.now().strftime('emotiv_raw_%Y-%m-%d_%H:%M.csv')
    with io.open(filename, 'wb', buffering=1) as fp:
        writer = csv.writer(fp)

        sensors = None

        try:
            while True:
                packet = headset.dequeue()

                if sensors is None:
                    sensors = packet.sensors.keys()
                    writer.writerow(['Timestamp'] + sensors)

                data = [packet.sensors[s]['value'] for s in sensors]
                writer.writerow([time.time()] + data)

                gevent.sleep(0)
        except KeyboardInterrupt:
            headset.close()
        finally:
            headset.close()
