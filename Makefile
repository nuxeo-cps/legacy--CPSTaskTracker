NY: tests clean doc

tests:
	./runtests.py

clean:
	find . -name '*~' | xargs rm -f
	find . -name '*.pyc' | xargs rm -f
	rm -rf docs/api

doc:
	happydoc -d docs/api *.py
