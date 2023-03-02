"""
Module of mixins for agents that range from the sensible to the useless.
These mixins act to fufill the abstract methods of blusky_adaptive.agents.Agent that are relevant to
the decision making, and not the experimental specifics.
    - tell
    - ask
    - report (optional)
    - name (optional)

Children will need to implement the following:
Experiment specific:
    - measurement_plan_name
    - measurement_plan_args
    - measurement_plan_kwargs
    - unpack_run
"""
from abc import ABC
from collections import defaultdict
from logging import getLogger
from typing import Generator, Sequence, Tuple, Union

import numpy as np
import sklearn
from numpy.typing import ArrayLike

from bluesky_adaptive.agents.base import Agent

logger = getLogger("bluesky_adaptive.agents")


class SequentialAgentBase(Agent, ABC):
    """Agent Mixin to take a pre-defined sequence and walk through it on ``ask``.

    Parameters
    ----------
    sequence : Sequence[Union[float, ArrayLike]]
        Sequence of points to be queried
    relative_bounds : Tuple[Union[float, ArrayLike]], optional
        Relative bounds for the members of the sequence to follow, by default None

    Attributes
    ----------
    independent_cache : list
        List of the independent variables at each observed point
    observable_cache : list
        List of all observables corresponding to the points in the independent_cache
    sequence : Sequence[Union[float, ArrayLike]]
        Sequence of points to be queried
    relative_bounds : Tuple[Union[float, ArrayLike]], optional
        Relative bounds for the members of the sequence to follow, by default None
    ask_count : int
        Number of queries this agent has made
    """

    name = "sequential"

    def __init__(
        self,
        *,
        sequence: Sequence[Union[float, ArrayLike]],
        relative_bounds: Tuple[Union[float, ArrayLike]] = None,
        **kwargs,
    ) -> None:
        super().__init__(**kwargs)
        self.independent_cache = []
        self.observable_cache = []
        self.sequence = sequence
        self.relative_bounds = relative_bounds
        self.ask_count = 0
        self._position_generator = self._create_position_generator()

    def _create_position_generator(self) -> Generator:
        """Yield points from sequence if within bounds"""
        for point in self.sequence:
            if self.relative_bounds:
                arr = np.array(point)
                condition = arr <= self.relative_bounds[1] or arr >= self.relative_bounds[0]
                try:
                    if condition:
                        yield point
                        continue
                    else:
                        logger.warning(
                            f"Next point will be skipped.  {point} in sequence for {self.instance_name}, "
                            f"is out of bounds {self.relative_bounds}"
                        )
                except ValueError:  # Array not float
                    if condition.all():
                        yield arr
                        continue
                    else:
                        logger.warning(
                            f"Next point will be skipped.  {point} in sequence for {self.instance_name}, "
                            f"is out of bounds {self.relative_bounds}"
                        )
            else:
                yield point

    def tell(self, x, y) -> dict:
        self.independent_cache.append(x)
        self.observable_cache.append(y)
        return dict(independent_variable=[x], observable=[y], cache_len=[len(self.independent_cache)])

    def ask(self, batch_size: int = 1) -> Tuple[dict, Sequence]:
        doc = defaultdict(list)
        for _ in range(batch_size):
            self.ask_count += 1
            doc["proposal"].append(next(self._position_generator))
        doc["ask_count"] = [self.ask_count]
        return doc, doc["proposal"]

    def report(self, **kwargs) -> dict:
        return dict(percent_completion=[self.ask_count / len(self.sequence)])


class SklearnEstimatorAgentBase(Agent, ABC):
    def __init__(self, *, estimator: sklearn.base.BaseEstimator, **kwargs):
        """Basic functionality for sklearn estimators. Maintains independent and dependent caches.
        Strictly passive agent with do ask mechanism: will raise NotImplementedError

        Parameters
        ----------
        estimator : sklearn.base.TransformerMixin
            Estimator instance that inherits from TransformerMixin and BaseEstimator
            This model will be used to call fit transform.
            Common examples include PCA and NMF.
        """
        super().__init__(**kwargs)
        self.independent_cache = []
        self.observable_cache = []
        self.model = estimator

    def tell(self, x, y):
        self.independent_cache.append(x)
        self.observable_cache.append(y)
        return dict(independent_variable=[x], observable=[y], cache_len=[len(self.independent_cache)])

    def ask(self, batch_size):
        raise NotImplementedError

    def update_model_params(self, params: dict):
        self.model.set_params(**params)

    def server_registrations(self) -> None:
        super().server_registrations()
        self._register_method("update_model_params")


class DecompositionAgentBase(SklearnEstimatorAgentBase, ABC):
    def __init__(self, *, estimator: sklearn.base.TransformerMixin, **kwargs):
        """Passive, report only agent that provide dataset analysis for decomposition.

        Parameters
        ----------
        estimator : sklearn.base.TransformerMixin
            Estimator instance that inherits from TransformerMixin and BaseEstimator
            This model will be used to call fit transform.
            Common examples include PCA and NMF.
        """
        super().__init__(estimator=estimator, **kwargs)

    def report(self, **kwargs):
        weights = self.model.fit_transform(
            np.array([x for _, x in sorted(zip(self.independent_cache, self.observable_cache))])
        )
        try:
            components = self.model.components_
        except AttributeError:
            components = []

        return dict(
            weights=[weights],
            components=[components],
            cache_len=[len(self.independent_cache)],
            latest_data=[self.tell_cache[-1]],
        )


class ClusterAgentBase(SklearnEstimatorAgentBase, ABC):
    def __init__(self, *, estimator: sklearn.base.ClusterMixin, **kwargs):
        """Passive, report only agent that provide dataset analysis for clustering.

        Parameters
        ----------
        estimator : sklearn.base.ClusterMixin
            Estimator instance that inherits from ClusterMixin, TransformerMixin and BaseEstimator
            This model will be used to call fit transform.
            Common examples include kmeans.
        """
        super().__init__(estimator=estimator, **kwargs)

    def report(self, **kwargs):
        arr = np.array([x for _, x in sorted(zip(self.independent_cache, self.observable_cache))])
        self.model.fit(arr)
        clusters = self.model.predict(arr)
        distances = self.model.transform(arr)

        return dict(
            clusters=[clusters],
            distances=[distances],
            cluster_centers=[self.model.cluster_centers_],
            cache_len=[len(self.independent_cache)],
            latest_data=[self.tell_cache[-1]],
        )
