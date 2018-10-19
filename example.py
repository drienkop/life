#!/usr/bin/env python3

from life import Life

# Run a sample simulation with the initial seed from xml/world_real
simulation = Life('xml/world_real.xml')
simulation.run()
