#!/usr/bin/env python3
import sys
sys.path.append('..')

import unittest  # noqa: E402
import life  # noqa: E402


class BasicTestSuite(unittest.TestCase):

    def test_run(self):
        mock_world_file = """<?xml version="1.0" encoding="UTF-8"?>
            <life>
               <world>
                  <cells>2</cells> // Dimension of the square "world"
                  <species>2</species> // Number of distinct species
                  <iterations>10</iterations> // Number of iterations to be calculated
               </world>
               <organisms>
                  <organism>
                     <x_pos>0</x_pos> // x position
                     <y_pos>0</y_pos> // y position
                     <species>1</species> // Species type
                  </organism>
                  <organism>
                     <x_pos>1</x_pos>
                     <y_pos>0</y_pos>
                     <species>1</species>
                  </organism>
                  <organism>
                     <x_pos>0</x_pos>
                     <y_pos>1</y_pos>
                     <species>1</species>
                  </organism>
                  <organism>
                     <x_pos>1</x_pos>
                     <y_pos>1</y_pos>
                     <species>2</species>
                  </organism>
               </organisms>
            </life>"""

        with open('tmp_seed.xml', 'w') as text_file:
            text_file.write(mock_world_file)

        self.simulation = life.Life('tmp_seed.xml', output_xml_file='xml/out.xml')
        expected_world = [life.Organism(0, 0, 1).type, life.Organism(0, 1, 1).type, life.Organism(1, 0, 1).type,
                          life.Organism(1, 1, 1).type]
        run_world = []

        for x in self.simulation.run():
            for cell in x:
                if cell:
                    run_world.append(cell.type)
                else:
                    run_world.append(None)

        self.assertEqual(run_world, expected_world)

    # TODO: further method tests
