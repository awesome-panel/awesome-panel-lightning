from __future__ import annotations

from typing import Any, Dict

import holoviews as hv
import panel as pn
from bokeh.sampledata import iris
from holoviews import opts

pn.extension()

print("starting cross filter")

ACCENT = "#792EE5"
LIGHTNING_SPINNER_URL = (
    "https://cdn.jsdelivr.net/gh/MarcSkovMadsen/awesome-panel-assets@master/spinners/material/"
    "bar_chart_lightning_purple.svg"
)
LIGHTNING_SPINNER = pn.pane.HTML(
        f"<img src='{LIGHTNING_SPINNER_URL}' style='height:100px;width:100px;'/>"
    )
OPTS: Dict[str, Dict[str, Any]] = {
    "all": {
        "scatter": {"color": ACCENT, "responsive": True, "size": 10},
        "hist": {"color": ACCENT, "responsive": True},
    },
    "bokeh": {
        "scatter": {"tools": ["hover"], "active_tools": ["box_select"]},
        "hist": {"tools": ["hover"], "active_tools": ["box_select"]},
    },
}

MAXIMIZE_FIRST_PANEL = """
.bk-root { height: calc( 100vh - 150px ) !important; }
"""
NO_HEADER_RAW_CSS = """
nav#header {display: None}
"""

pn.config.raw_css.append(NO_HEADER_RAW_CSS)
pn.config.raw_css.append(MAXIMIZE_FIRST_PANEL)


component = pn.Column(LIGHTNING_SPINNER, sizing_mode="stretch_both")

def load(*args):

    pn.extension(sizing_mode="stretch_width")
    hv.extension("bokeh")
    dataset = hv.Dataset(iris.flowers)

    scatter = hv.Scatter(dataset, kdims=["sepal_length"], vdims=["sepal_width"]).opts(
        responsive=True
    )
    hist = hv.operation.histogram(dataset, dimension="petal_width", normed=False)

    selection_linker = hv.selection.link_selections.instance()
    scatter = selection_linker(scatter).opts(
        opts.Scatter(**OPTS["all"]["scatter"], **OPTS["bokeh"]["scatter"])
    )
    hist = selection_linker(hist).opts(
        opts.Histogram(**OPTS["all"]["hist"], **OPTS["bokeh"]["hist"], height=300)
    )
    component[:] = [
        pn.pane.HoloViews(scatter, sizing_mode="stretch_both"),
        hist,
    ]


pn.state.onload(load)

pn.template.FastListTemplate(
    title="Cross Filter", theme="dark", theme_toggle=False, main=[component]
).servable()
