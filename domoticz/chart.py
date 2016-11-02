import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
import matplotlib.dates as mdates
import matplotlib.ticker as ticks

class Chart:
    def get_x_y(self,data_points):
        log = sorted(data_points, key=lambda x: x['idx'])
        dates = map(lambda x: np.datetime64(x['Date']).astype(datetime), log)
        print(dates)
        x = np.array(dates)
        y = np.array(map(lambda d: d['Level'], log))
        return x, y

    def plot(self, x, y, title):
        plt.step(mdates.date2num(x), y, where='post')
        plt.gcf().autofmt_xdate()
        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d %H:%M'))
        plt.gca().xaxis.set_major_locator(mdates.MinuteLocator(interval=240))
        # plt.gca().yaxis.set_major_locator(ticks.FixedLocator([0,250]))
        # plt.gca().yaxis.set_major_formatter(ticks.FixedFormatter(['Closed', 'Open']))
        plt.title(title)

    def get_y_labels(self, data_points):
        label_map =  dict(map(lambda p: (p['Level'], p['Data']), data_points))

