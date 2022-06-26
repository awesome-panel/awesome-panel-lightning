![PyPI - License](https://img.shields.io/pypi/l/panel-highcharts) ![Style Black](https://warehouse-camo.ingress.cmh1.psfhosted.org/fbfdc7754183ecf079bc71ddeabaf88f6cbc5c00/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f636f64652532307374796c652d626c61636b2d3030303030302e737667) [![Follow on Twitter](https://img.shields.io/twitter/follow/MarcSkovMadsen.svg?style=social)](https://twitter.com/MarcSkovMadsen)

# ⚡ Awesome Panel Lightning

Repository demonstrating the power of combining [Panel](https://panel.holoviz.org) and [lightning.ai](https://lightning.ai/).

[![awesome-panel-lightning tour](assets/awesome-panel-lightning.gif)](https://01g6g6axybbecmx47d9m419pe5.litng-ai-03.litng.ai/view?id=01g6g6axybbecmx47d9m419pe5)

Check out the [Example App](https://01g6g6axybbecmx47d9m419pe5.litng-ai-03.litng.ai/view?id=01g6g6axybbecmx47d9m419pe5).

## ⚙️ Install Locally

[Create](https://realpython.com/python-virtual-environments-a-primer/#create-it) and [activate](https://realpython.com/python-virtual-environments-a-primer/#activate-it) your local environment.

Then install the requirements via

```bash
pip install -r requirements.txt
```

Finally you can update the `name` of the app in the [.lightning](.lightning) file.

## 🏃 Run Locally

Activate your virtual environment and run

```bash
lightning run app app.py
```

## ☁️ Run in lightning.ai cloud

Activate your virtual environment and run

```bash
lightning run app app.py --cloud
```

and follow the instructions

## 🐛 Active issues

- [LightningFlow expects too fast an initial response from other servers](https://github.com/Lightning-AI/lightning/issues/13381)