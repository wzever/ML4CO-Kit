# -*- coding: utf-8 -*-
from __future__ import division, print_function

from collections import namedtuple
import os
import shutil
import tempfile
import uuid
import numpy as np

from ._concorde import _CCutil_gettsplib, _CCtsp_solve_dat

ComputedTour = namedtuple(
    "ComputedTour", ["tour", "optimal_value", "success", "found_tour", "hit_timebound"]
)


EDGE_WEIGHT_TYPES = {
    "EXPLICIT",
    "EUC_2D",
    "EUC_3D",
    "MAX_2D",
    "MAN_2D",
    "GEO",
    "GEOM",
    "ATT",
    "CEIL_2D",
    "DSJRAND",
}


def write_tsp_file(fp, xs, ys, norm, name):
    """Write data to a TSPLIB file."""
    if len(xs) != len(ys):
        raise ValueError(
            "x and y coordinate vector must have the "
            "same length ({} != {})".format(len(xs), len(ys))
        )
    if norm not in EDGE_WEIGHT_TYPES:
        raise ValueError(
            "Norm {!r} must be one of {}".format(norm, ", ".join(EDGE_WEIGHT_TYPES))
        )

    fp.write("NAME: {}\n".format(name))
    fp.write("TYPE: TSP\n")
    fp.write("DIMENSION: {}\n".format(len(xs)))
    fp.write("EDGE_WEIGHT_TYPE: {}\n".format(norm))
    fp.write("NODE_COORD_SECTION\n")
    for n, (x, y) in enumerate(zip(xs, ys), start=1):
        fp.write("{} {} {}\n".format(n, x, y))
    fp.write("EOF\n")




class TSPSolver(object):
    def __init__(self):
        self._data = None
        self._ncount = -1

    @classmethod
    def from_tspfile(cls, fname):
        ncount, data = _CCutil_gettsplib(fname)
        if data is None:
            raise RuntimeError("Error in loading {}".format(fname))
        self = cls()
        self._ncount = ncount
        self._data = data
        return self

    @classmethod
    def from_data(cls, xs, ys, norm, name=None):
        """Construct datagroup from given data.

        This routine writes the given data to a temporary file, and then uses
        Concorde's file parser to read from file and do the initialization.
        """
        if norm not in EDGE_WEIGHT_TYPES:
            raise ValueError(
                "norm must be one of {} but got {!r}".format(
                    ", ".join(EDGE_WEIGHT_TYPES), norm
                )
            )

        # TODO: properly figure out Concorde's CCdatagroup format and
        # initialize this object directly instead of going via file.
        if name is None:
            name = uuid.uuid4().hex
        try:
            ccdir = tempfile.mkdtemp()
            ccfile = os.path.join(ccdir, "data.tsp")
            with open(ccfile, "w") as fp:
                write_tsp_file(fp, xs, ys, norm, name)
            return cls.from_tspfile(ccfile)
        finally:
            shutil.rmtree(ccdir)

    @property
    def x(self):
        return self._data.x

    @property
    def y(self):
        return self._data.y

    @property
    def z(self):
        return self._data.z

    def __str__(self):
        if self._data is None:
            return "Uninitialized TSPSolver"
        else:
            return "TSPSolver with {} nodes".format(self._ncount)

    def solve(
        self, 
        name: str, 
        time_bound: int=-1, 
        verbose: bool=True, 
        random_seed: int=0
    ):
        name = name[0:9]
        res = _CCtsp_solve_dat(
            self._ncount, self._data, name, time_bound, not verbose, random_seed
        )
        return ComputedTour(*res)
