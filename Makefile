.PHONY: all
all: deps/venv/bin/phony docker_start

deps/venv: 
	python3 -m venv deps/venv 

deps/venv/bin/phony: venv
	git clone https://github.com/Eigenbaukombinat/phony deps/phony
	deps/venv/bin/python3 install -e deps/phony

.PHONY: docker_build
docker_build:
	sudo docker build --tag c3telegaming .

.PHONY: docker_run
docker_start: docker_build

	sudo docker run -ti --rm c3telegaming

.PHONY: clean
clean:
	sudo docker container rm -f $(sudo docker container ls -aq)