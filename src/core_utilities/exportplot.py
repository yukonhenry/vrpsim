# Copyright YukonTR 2015
from bokeh.plotting import figure, output_file, show, gridplot
import numpy as np
class ExportPlot(object):
    def __init__(self, filename_base):
        self.filename_base = filename_base

    def simple_plot(self, data):
        xvec = range(len(data))
        # output to static HTML file
        output_file("out/"+self.filename_base+"_lines.html", title="sample plot")

        p = figure(title="stat example")
        p.line(xvec, data, legend="Arrival Time", x_axis_label='x', y_axis_label='y')

        show(p)

    def hist_plot(self, data):
        hist, edges = np.histogram(data, density=True, bins=50)

        # output to static HTML file
        output_file("out/"+self.filename_base+"_hist.html")

        p = figure(title="Histogram", background_fill="#E8DDCB")
        p.quad(top=hist, bottom=0, left=edges[:-1], right=edges[1:],
               fill_color="#036564", line_color="#033649")

        # customize axes
        xa, ya = p.axis
        xa.axis_label = 'x'
        ya.axis_label = 'Pr(x)'

        show(p)

    def group_plot(self, data_list):
        output_file("out/"+self.filename_base+"_hist.html", title="arrival stats plot")
        gridplot_list = list()
        for data in data_list:
            hist, edges = np.histogram(data, density=True, bins=50)
            s = figure(title="Histogram", background_fill="#E8DDCB")
            s.quad(top=hist, bottom=0, left=edges[:-1], right=edges[1:],
                   fill_color="#036564", line_color="#033649")

            # customize axes
            xa, ya = s.axis
            xa.axis_label = 'x'
            ya.axis_label = 'Pr(x)'
            gridplot_list.append(s)
        p = gridplot([gridplot_list])
        show(p)

