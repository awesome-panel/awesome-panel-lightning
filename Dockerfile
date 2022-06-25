FROM python:3.9.13-slim-bullseye

RUN pip install panel==0.13.1 bokeh==2.4.3 lightning==2022.6.15.post2 holoviews==1.14.9

ADD . .

ENTRYPOINT [ "lightning", "run", "app", "app.py" ]

