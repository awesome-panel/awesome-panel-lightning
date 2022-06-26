"""A lightning.ai app serving multiple Panel pages"""
from __future__ import annotations

import lightning_app as lapp
import panel as pn

from panel_lightning import LitPanelPage

def introduction():
    ACCENT = "#792EE5"

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
    component = pn.Column(info, lightning, ilightning_string, sizing_mode="stretch_width")

    return pn.template.FastListTemplate(
        site="Panel",
        title="Introduction",
        accent_base_color=ACCENT,
        header_background=ACCENT,
        main=[component],
    )


class LitApp(lapp.LightningFlow):
    def __init__(self):
        super().__init__()
        self.lit_intro = LitPanelPage(page=introduction, parallel=True)
        self.lit_big_data_viz = LitPanelPage(page="pages/big_data_viz.py", parallel=True)
        self.lit_crossfilter = LitPanelPage(page="pages/cross_filter.py", parallel=True)
        self.lit_streaming = LitPanelPage(page="pages/streaming.py", parallel=True)

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



# lightning run app app.py
app = lapp.LightningApp(LitApp())
