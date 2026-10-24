# flask-extract-resume
flask-extract-resume

start on windows:

> python -m flask --app main run

> flask --app main run
	- mian -> main.py file name


Resume extracter:
https://github.com/ir-dev/pyresparser/blob/master/OmkarResume.pdf

pip install -r requirements.txt && python -m nltk.downloader words && python -m nltk.downloader stopwords

Python 3.11 only (flask-web/.python-version): pyresparser needs spaCy 2.x, and spaCy 2.3.9 (the last 2.x)
has no wheels past 3.11. Local setup with uv, from flask-web:

> uv venv --python 3.11 && uv pip install -r requirements.txt
> .venv/bin/python -m nltk.downloader words stopwords
> .venv/bin/flask --app main run

requirements.txt is a pinned lock; change requirements.in, then re-lock:

> uv pip compile requirements.in --universal --python-version 3.11 -o requirements.txt