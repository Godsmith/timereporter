#!/usr/bin/env python

from pycallgraph import PyCallGraph
from pycallgraph import Config
from pycallgraph import GlobbingFilter
from pycallgraph.output import GraphvizOutput

from timereporter.__main__ import main

if __name__ == "__main__":
    config = Config()
    config.trace_filter = GlobbingFilter(
        exclude=[
            "pycallgraph.*",
            "_gcd_import",
            "_lock_unlock_module",
            "_ModuleLock",
            "cb",
            "_sanity_check",
            "*_dump_*",
            "*mydatetime*",
        ]
    )

    graphviz = GraphvizOutput(output_file="pycallgraph.png")
    with PyCallGraph(output=graphviz, config=config):
        main()
