NY:clean doc

tests:
	./runtests.py

clean:
	find . -name '*~' | xargs rm -f
	find . -name '*.pyc' | xargs rm -f

doc:
	happydoc -d docs/api *.py
