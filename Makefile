.PHONY: clean doc tests

tests:
	./runtests.py
check:
	pychecker2 *.py
clean:
	find . "(" -name "*~" -or -name "*.pyc" ")" -print0 | xargs -0 rm -f
	find . -name '*.pyc' | xargs rm -f
	find . -name '#*' | xargs rm -f
	#rm -rf doc/API
	cd tests ; make clean
doc:
	happydoc -d docs/api *.py
