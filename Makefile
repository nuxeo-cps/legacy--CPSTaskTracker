.PHONY: clean doc tests

tests:
	./runtests.py

clean:
	find . -name "*~" -or -name "*.pyc" -print0 | xargs -0 rm -f

doc:
	happydoc -d docs/api *.py
