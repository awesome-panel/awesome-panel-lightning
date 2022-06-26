import panel as pn

pn.extension()

pn.Column(
    "# Example coming up",
    pn.pane.HTML(
        "<img src='https://cdn.jsdelivr.net/gh/MarcSkovMadsen/awesome-panel-assets@master/videos/panel-big-data-viz.gif'/>",
        sizing_mode="stretch_both",
    ),
    sizing_mode="stretch_both",
).servable()