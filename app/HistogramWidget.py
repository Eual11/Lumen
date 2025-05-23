from PySide6.QtWidgets import QVBoxLayout, QWidget
from PySide6.QtCharts import QBarSeries, QBarSet, QChart, QChartView, QValueAxis

class HistogramWidget(QWidget):
    def __init__(self, name,bins, x_min, y_min, x_max, y_max):
        super().__init__()

        layout = QVBoxLayout()

        barset = QBarSet(name)
        barset.append(bins)
        
        bar_series = QBarSeries()
        bar_series.append(barset)

        bar_series.setBarWidth(1.0)

        chart = QChart()

        x_axis = QValueAxis()
        y_axis = QValueAxis()
        x_axis.setRange(x_min, x_max)
        y_axis.setRange(y_min, y_max)

        chart.setAxisX(x_axis)
        chart.setAxisY(y_axis)

        bar_series.attachAxis(x_axis)
        bar_series.attachAxis(y_axis)


        chart.addSeries(bar_series)

        chart_view = QChartView(chart)

        layout.addWidget(chart_view)

        self.setLayout(layout)
