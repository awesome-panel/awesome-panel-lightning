import panel as pn
import numpy as np

pn.extension()

print("starting streaming")

ACCENT = "#792EE5"
LIGHTNING_SPINNER_URL = (
    "https://cdn.jsdelivr.net/gh/MarcSkovMadsen/awesome-panel-assets@master/spinners/material/"
    "bar_chart_lightning_purple.svg"
)
LIGHTNING_SPINNER = pn.pane.HTML(
    f"<img src='{LIGHTNING_SPINNER_URL}' style='height:100px;width:100px;'/>"
)

ncols = 4
objects = [LIGHTNING_SPINNER]
grid = pn.layout.GridBox(objects=objects, ncols=ncols)


def load(*args):
    objects = [
        pn.indicators.Trend(
            title=f"⚡ Panel {index+1}",
            data={"x": np.arange(50), "y": np.random.rand(50).cumsum()},
            plot_type="area",
            sizing_mode="stretch_both",
            plot_color=ACCENT,
        )
        for index in range(0, ncols**2)
    ]

    grid.objects = objects

    def stream_data():
        for trend in objects:
            trend.stream(
                {
                    "x": [trend.data["x"][-1] + 1],
                    "y": [trend.data["y"][-1] + np.random.randn()],
                },
                rollover=50,
            )

    pn.state.add_periodic_callback(stream_data, period=500)


pn.state.onload(load)

grid.servable()
