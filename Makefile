all: clean hotels

hotels:
	python3 hotels_db.py

clean:
	rm -rf hotels.db