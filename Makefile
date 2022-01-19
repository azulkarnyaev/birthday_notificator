virtual_env:
	rm -rf venv
	python3 -m venv venv
	source ./venv/bin/activate && pip3 install -r requirements.txt -r requirements-dev.txt

.PHONY: build
build:
	cd venv/lib/python3.10/site-packages && zip -r ../../../../build/birthday_notifier.zip .
	zip -gr build/birthday_notifier.zip birthday_notificator
	zip -g build/birthday_notifier.zip telegram_notifier.py

clean:
	rm -rf build && mkdir build

deploy:
	aws lambda update-function-code --function-name birthday_notificator --zip-file fileb://build/birthday_notifier.zip

test:
	source ./venv/bin/activate && python3 -m pytest tests
