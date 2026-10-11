# Comben

Short for `Com`pute `ben`chmark is a benchmarking suite for evaluating performance among performance and efficent cores in an intel cpu. Currently tested for Ubuntu based distros running on ultra 2 series cpu and an nvidia gpu capable of cuda 12.0.

### Setting up & running
`python -m venv comben-env`<br/>
`source comben-env/bin/activate`<br/>
`pip install -r requirements.txt` <br/>
`just compile-cuda-lib`<br/>
`just wrap`<br/>
`just run-multi`