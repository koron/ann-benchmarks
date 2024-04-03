FROM ann-benchmarks

RUN apt update && apt install -y python-setuptools python-pip

RUN python3 -m pip install pybind11 numpy numba usearch

RUN python3 -c 'import usearch'
