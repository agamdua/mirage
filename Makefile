clean:
	find . -name '*.pyc' -print0 | xargs -0 rm -f
	find . -name '*.pyo' -print0 | xargs -0 rm -f
	find . -name '__pycache__' -type d -print0 | xargs -0 rm -rf

test: clean
	py.test -s
