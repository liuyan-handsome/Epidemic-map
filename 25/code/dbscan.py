import numpy as np
from sklearn.base import ClusterMixin, BaseEstimator
from sklearn.cluster._dbscan_inner import dbscan_inner
from sklearn.neighbors import NearestNeighbors

class DBSCAN(ClusterMixin, BaseEstimator):
    def __init__(self, eps, min_samples):
        #eps为半径 min_samples为阈值
        self.eps = eps
        self.min_samples = min_samples

    def fit(self, X, sample_weight=None):

        X = self._validate_data(X)
        # 判断半径eps内对象个数
        neighbors_model = NearestNeighbors(radius=self.eps)
        neighbors_model.fit(X)#判断临近的对象
        neighborhoods = neighbors_model.radius_neighbors(X,return_distance=False)
        # 累加中心点在eps范围的节点数
        if sample_weight is None:
            n_neighbors = np.array([len(neighbors) for neighbors in neighborhoods])
        else:
            n_neighbors = np.array([np.sum(sample_weight[neighbors])
                                    for neighbors in neighborhoods])

        labels = np.full(X.shape[0], -1, dtype=np.intp)#为对象标记
        core_samples = np.asarray(n_neighbors >= self.min_samples,
                                  dtype=np.uint8)                 #如果中心点在eps范围内的节点数大于min_samples
        dbscan_inner(core_samples, neighborhoods, labels)         #则将该点标记为中心点，并继续判断临近点

        self.core_sample_indices_ = np.where(core_samples)[0]     #将两点归于同一簇中
        self.labels_ = labels

        if len(self.core_sample_indices_):
            self.components_ = X[self.core_sample_indices_].copy()
        else:
            self.components_ = np.empty((0, X.shape[1]))

        #返回标签列
        return self

    def fit_predict(self, X):
        self.fit(X)
        return self.labels_
