from usearch.index import Index, MetricKind, ScalarKind
from usearch.numba import jit
import numpy as np

from ..base.module import BaseANN

class USearch(BaseANN):

    def __init__(self, metric: str, accuracy: str, method_param: dict):
        assert accuracy in ['f64', 'f32', 'f16', 'f8']
        assert metric in ['angular', 'euclidean']
        assert 'M' in method_param
        assert 'efConstruction' in method_param

        self._method_param = method_param
        self._accuracy = {'f64': ScalarKind.F64, 'f32': ScalarKind.F32, 'f8': ScalarKind.F8}[accuracy]
        self._metric = {'angular': MetricKind.Cos, 'euclidean': MetricKind.L2sq}[metric]

    def __str__(self):
        connectivity = self._method_param['M']
        expansion_add = self._method_param['efConstruction']
        return "usearch (%s, ef: %d)" % (self._method_param, self._index.expansion_search)

    def fit(self, X):
        connectivity = self._method_param['M']
        expansion_add = self._method_param['efConstruction']
        metric = jit(
            X.shape[1],
            self._metric,
            self._accuracy
        )

        self._index = Index(
            ndim=len(X[0]),
            metric=metric,
            dtype=self._accuracy,
            connectivity=connectivity,
            expansion_add=expansion_add
        )

        labels = np.arange(len(X), dtype=np.longlong)
        self._index.add(labels, np.asarray(X))

    def get_memory_usage(self) -> int:
        if not hasattr(self, '_index'):
            return 0

        return self._index.memory_usage / 1024

    def set_query_arguments(self, ef: int):
        self._index.expansion_search = ef

    def freeIndex(self):
        del self._index

    def query(self, v, n):
        return self._index.search(np.expand_dims(v, axis=0), count=n).keys

    def batch_query(self, X, n):
        self._batch_results = self._index.search(np.asarray(X), count=n)

    def get_batch_results(self):
        return self._batch_results
