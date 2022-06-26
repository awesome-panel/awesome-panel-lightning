import panel as pn

LIGHTNING_PURPLE = "#792EE5"

LIGHTNING_SPINNER_URL = (
    "https://cdn.jsdelivr.net/gh/MarcSkovMadsen/awesome-panel-assets@master/spinners/material/"
    "bar_chart_lightning_purple.svg"
)

def get_lightning_spinner(url=LIGHTNING_SPINNER_URL, **params) -> pn.pane.HTML:
    """Returns a loding spinner for your lightning.ai app"""
    return pn.pane.HTML(
        f"<img src='{url}' style='height:100%;width:100%;'/>", **params
    )

LIGHTNING_SPINNER = get_lightning_spinner(sizing_mode="fixed", width=100, height=100)
