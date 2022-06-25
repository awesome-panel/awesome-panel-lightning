# Source: https://github.com/Lightning-AI/lightning/blob/master/docs/source-app/workflows/build_lightning_app/from_scratch.rst
# Source: https://github.com/Lightning-AI/lightning/blob/master/src/lightning_app/frontend/stream_lit.py
# docker run --expose 1-65000 lightning
from __future__ import annotations

import pathlib
from typing import Any, Callable, Dict, Union

import holoviews as hv
import lightning_app as lapp
import numpy as np
import panel as pn
from bokeh.sampledata import iris
from bokeh.server.server import Server
from holoviews import opts
from lightning_app.core import constants
from panel.template.fast.theme import FastDarkTheme, FastDefaultTheme

ACCENT = "#792EE5"
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
Page = Union[Callable[[], pn.viewable.Viewable], str, pathlib.Path]

def get_bokeh_theme(accent, theme="default"):
    if theme=="dark":
        fast_theme = FastDarkTheme()
    else:
        fast_theme = FastDefaultTheme()

    return fast_theme.bokeh_theme

SPINNER_URL = "https://cdn.jsdelivr.net/gh/MarcSkovMadsen/awesome-panel-assets@master/spinners/material/bar_chart_lightning_purple.svg"
LOADING_SPINNER = pn.pane.HTML(f"<img src='{SPINNER_URL}' style='height:100px;width:100px;'/>")

MAXIMIZE_FIRST_PANEL = """
.bk-root { height: calc( 100vh - 150px ) !important; }
"""
NO_HEADER_RAW_CSS = """
nav#header {display: None}
"""
CENTER_ROOT = """
.bk-root {
    margin: auto;
    position: absolute;
}
"""

def page_intro():
    print("starting intro")
    component = pn.Column("Loading ...", sizing_mode="stretch_both")
    
    def load(*args):
        pn.extension(sizing_mode="stretch_width")
        info = """
            **[Panel](https://panel.holoviz.org/)** and the [HoloViz](https://holoviz.org/) ecosystem provides unique and powerful features such as big data viz via [DataShader](https://datashader.org/), easy cross filtering via [HoloViews](https://holoviews.org/), streaming and much more.

            Panel works with the tools you know and love ❤️. Panel ties into the PyData and Jupyter ecosystems as you can develop in notebooks and use ipywidgets. You can also develop in .py files.

            Panel is one of the 4 most popular data app frameworks in Python with [more than 400.000 downloads a month](https://pyviz.org/tools.html#dashboarding). It's especially popular in the scientific community.

            Panel is used by for example Rapids to power [CuxFilter](https://github.com/rapidsai/cuxfilter), a CuDF based big data viz framework.
            
            Panel can be deployed on your favorite server or cloud including **[lightning.ai](https://lightning.ai)**.
            """

        def lightning_string(value):
            return "# " + "⚡" * value

        lightning = pn.widgets.IntSlider(value=5, start=0, end=10, name="⚡")
        ilightning_string = pn.bind(lightning_string, value=lightning)
        component[:]=[
            info,
            lightning,
            ilightning_string,
        ]
    
    pn.state.onload(load)

    template = pn.template.FastListTemplate(
        title="Panel - Introduction",
        accent_base_color=ACCENT,
        header_background=ACCENT,
        main=[component],
    )
    
    return template

def page_big_data_viz():
    return pn.Column(
        "# Example coming up",
        pn.pane.HTML("<img src='https://cdn.jsdelivr.net/gh/MarcSkovMadsen/awesome-panel-assets@master/videos/panel-big-data-viz.gif'/>", sizing_mode="stretch_both"),
        sizing_mode="stretch_both"
    )

def page_crossfilter():
    print("starting cross filter")
    pn.config.raw_css.append(NO_HEADER_RAW_CSS)
    pn.config.raw_css.append(MAXIMIZE_FIRST_PANEL)
    
    component = pn.Column(LOADING_SPINNER, sizing_mode="stretch_both")        
    
    def load(*args):
        
        
        pn.extension(sizing_mode="stretch_width")
        hv.extension("bokeh")
        dataset = hv.Dataset(iris.flowers)

        scatter = hv.Scatter(dataset, kdims=["sepal_length"], vdims=["sepal_width"]).opts(responsive=True)
        hist = hv.operation.histogram(dataset, dimension="petal_width", normed=False)

        selection_linker = hv.selection.link_selections.instance()
        scatter = selection_linker(scatter).opts(
            opts.Scatter(**OPTS["all"]["scatter"], **OPTS["bokeh"]["scatter"])
        )
        hist = selection_linker(hist).opts(
            opts.Histogram(**OPTS["all"]["hist"], **OPTS["bokeh"]["hist"], height=300)
        )
        component[:]=[
            pn.pane.HoloViews(scatter, sizing_mode="stretch_both"), 
            hist,
        ]

    pn.state.onload(load)

    return pn.template.FastListTemplate(
        title="Cross Filter", theme="dark", theme_toggle=False, main=[component]
    )
        

def page_streaming():
    print("starting streaming")
    ncols = 4
    objects = [LOADING_SPINNER]
    grid = pn.layout.GridBox(objects = objects, ncols=ncols)
    
    def load(*args):
        objects = [pn.indicators.Trend(
            title=f"⚡ Panel {index+1}",
            data={"x": np.arange(50), "y": np.random.rand(50).cumsum()},
            plot_type="area",
            sizing_mode="stretch_both",
            plot_color=ACCENT,
        ) for index in range(0,ncols**2)]
    
        grid.objects=objects
    
        def stream_data():
            for trend in objects:
                trend.stream(
                    {"x": [trend.data["x"][-1] + 1], "y": [trend.data["y"][-1] + np.random.randn()]},
                    rollover=50,
                )

        pn.state.add_periodic_callback(stream_data, period=500)
    
    pn.state.onload(load)        
    
    return grid


class LitPanelPage(lapp.LightningWork):
    """Can serve a single page Panel app"""

    def __init__(self, page: Page, **params):
        """_summary_

        Args:
            page (Callable[[], pn.viewable.Viewable]): A function returning a Panel `Viewable`.
                Alternatively a path to a file containing a Panel application.
        """
        if isinstance(page, pathlib.Path):
            page = str(page)
        self._page = page

        self._server: Union[None, Server] = None

        super().__init__(**params)

    def run(self):
        """Starts the server and serves the page"""
        self._server = pn.serve(
            {"/": self._page},
            port=self.port,
            address=self.host,
            websocket_origin=self.websocket_origin,
            show=False,
        )

    def stop(self):
        """Stops the server"""
        if self._server:
            self._server.stop()

    def get_tab(self, name: str) -> Dict[str, str | "LitPanelPage"]:
        """Returns a *tab* definition to be included in the layout of a LightingFlow"""
        return {"name": name, "content": self}

    @property
    def websocket_origin(self) -> str:
        host = constants.APP_SERVER_HOST.replace("http://", "").replace("https://", "")
        return host + ":" + str(self.port)


class LitApp(lapp.LightningFlow):
    def __init__(self):
        super().__init__()
        self.lit_intro = LitPanelPage(page=page_intro, parallel=True)
        self.lit_big_data_viz = LitPanelPage(page=page_big_data_viz, parallel=True)
        self.lit_crossfilter = LitPanelPage(page=page_crossfilter, parallel=True)
        self.lit_streaming = LitPanelPage(page=page_streaming, parallel=True)

    def run(self):
        self.lit_intro.run()
        self.lit_big_data_viz.run()
        self.lit_crossfilter.run()
        self.lit_streaming.run()

    def configure_layout(self):
        return [
            self.lit_intro.get_tab(name="Introduction"),
            self.lit_crossfilter.get_tab(name="Crossfiltering"),
            self.lit_streaming.get_tab(name="Streaming"),
            self.lit_big_data_viz.get_tab(name="Big Data"),
        ]


if __name__.startswith("bokeh"):
    # page_intro().servable()
    # page_crossfilter().servable()
    page_big_data_viz().servable()
    # page_streaming().servable()
    # panel serve app.py --autoreload --show
else:
    # lightning run app app.py
    app = lapp.LightningApp(LitApp())