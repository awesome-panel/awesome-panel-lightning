# Awesome Panel Lightning

Repository showcasing how to combine [Panel](https://panel.holoviz.org) and [lightning.ai](https://lightning.ai/)

![awesome-panel-lightning tour](assets/awesome-panel-lightning.gif)

Check out the [Example App](https://01g6d5mqceawxdbm5epsj7t5xk.litng-ai-03.litng.ai/view?id=01g6d5mqceawxdbm5epsj7t5xk).

## Install Locally

[Create](https://realpython.com/python-virtual-environments-a-primer/#create-it) and [activate](https://realpython.com/python-virtual-environments-a-primer/#activate-it) your local environment. 

Then install the requirements via

```bash
pip install -r requirements.txt
```

## Run Locally

Activate your virtual environment and run

```bash
lightning run app app.py
```

## Run in lightning.ai cloud

DOES NOT WORK YET: See Active Issues below.

Activate your virtual environment and run

```bash
lightning run app app.py --cloud
```

and follow the instructions

## Active issues

- [LightningFlow expects too fast an initial response from other servers](https://github.com/Lightning-AI/lightning/issues/13381)