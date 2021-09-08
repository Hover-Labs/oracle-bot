build-docker:
	docker build -t kolibri-oraclebot .

bash:
	docker run --rm -it \
	    -v $$(pwd)/:/shared --workdir /shared \
	    kolibri-oraclebot bash

run:
	docker run --rm -it \
	    -v $$(pwd):/shared --workdir /shared \
	    --env-file .env \
	    kolibri-oraclebot \
	    python3 /shared/main.py
