"""A stub for profiling tools to run one basic simulation."""

import os
import nemo
from nemo import regions
from nemo import polygons
from nemo import utils
import unittest


class TestCoverage(unittest.TestCase):

    """A handful of miscellaneous tests to ensure good coverage."""

    def test_001(self):
        c = nemo.Context()
        c.regions = [regions.nsw, regions.vic, regions.sa]
        c.track_exchanges = True
        c.verbose = 1
        nemo.run(c)

    def test_002(self):
        c = nemo.Context()
        # Make sure there is unserved energy by setting 2nd and
        # subsequent generator capacity to 0.
        for g in c.generators[1:]:
            g.set_capacity(0)
        nemo.run(c)
        utils.plot(c, filename='foo.png')
        os.unlink('foo.png')
        utils.plot(c, filename='foo.png', spills=True)
        os.unlink('foo.png')

        # Test limiting the x-range.
        from datetime import datetime
        xlim = [datetime(2010, 1, 1), datetime(2010, 1, 10)]
        utils.plot(c, filename='foo.png', xlim=xlim)
        os.unlink('foo.png')

    def test_003(self):
        c = nemo.Context()
        # Add 25 DR generators so that the abbreviated legend is used.
        for i in range(25):
            dr = nemo.generators.DemandResponse(polygons.wildcard, 100, 0)
            c.generators += [dr]
        print len(c.generators)
        nemo.run(c)
        utils.plot(c, filename='foo.png')
        os.unlink('foo.png')

    def test_004(self):
        """Test Context.__str__ method."""
        c = nemo.Context()
        print str(c)
        c.regions = [regions.nsw]
        print str(c)

    def test_005(self):
        """Test Context summary with no cost generator."""
        from nemo import costs
        import types
        c = nemo.Context()
        c.costs = costs.NullCosts()
        print str(c)
        c.verbose = True
        print str(c)
        c.regions = [regions.nsw]
        print str(c)

        f = types.MethodType(lambda self, costs: None, c.generators[0], nemo.Context)
        print f
        c.generators[0].summary = f
        print c.generators[0].summary(None)
        print str(c)
