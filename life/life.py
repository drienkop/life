import xml.etree.ElementTree as ET
import random
from typing import Union


class Organism:
    def __init__(self, y: int, x: int, t: int):
        self.y = y
        self.x = x
        self.type = t


class Life:
    """ Simulates Life based on a seed from an XML file and saves the state into a new XML file.

        :param seed_xml_file: XML filename containing initial life data
        :param output_xml_file: XML filename where the final life data after simulation is saved to
    """

    def __init__(self, seed_xml_file: str ='xml/world_real.xml', output_xml_file: str ='xml/out.xml'):
        self.dimension = None
        self.species_count = None
        self.iterations = None
        self.species_types = None
        self.output_xml_file = output_xml_file

        # 2D world of the life
        self.world = None

        # List of living Organisms only
        self.live_organisms = []

        # List of cells which have already been verified in one iteration
        self.verified_elements = []

        self.load_xml_file(seed_xml_file)

    def load_xml_file(self, xml_source: str):
        """ Load the XML file into class data structures.

        :param xml_source: file name containing XML data
        """

        xml_parsed = ET.parse(xml_source)
        xml_root = xml_parsed.getroot()

        self.dimension = int(xml_root.find('./world/cells').text)
        self.species_types = int(xml_root.find('./world/species').text)
        self.iterations = int(xml_root.find('./world/iterations').text)

        self.world = [[None] * self.dimension for _ in range(self.dimension)]

        # Loading of the actual organisms
        for organism in xml_root.find('./organisms'):
            x = int(organism.find('x_pos').text)
            y = int(organism.find('y_pos').text)
            species_type = int(organism.find('species').text)
            self.live_organisms.append(Organism(y, x, species_type))
            self.world[y][x] = Organism(y, x, species_type)

    def save_xml_file(self, live_organisms: list, destination_xml: str):
        """ Save the state of the world into an XML file.

        :param live_organisms: list of living organisms only
        :param destination_xml: file name location opened for saving the XML data
        """

        # Create the XML tree structure
        life = ET.Element('life')
        world = ET.SubElement(life, 'world')
        ET.SubElement(world, 'cells').text = str(self.dimension)
        ET.SubElement(world, 'species').text = str(self.species_types)
        ET.SubElement(world, 'iterations').text = str(self.iterations)
        organisms = ET.SubElement(life, 'organisms')

        # Create the organisms from the world array
        for organism in live_organisms:
                single_organism = ET.SubElement(organisms, 'organism')
                ET.SubElement(single_organism, 'x_pos').text = str(organism.x)
                ET.SubElement(single_organism, 'y_pos').text = str(organism.y)
                ET.SubElement(single_organism, 'species').text = str(organism.type)

        # Save the XML tree to a file
        ET.ElementTree(life).write(destination_xml, encoding='UTF-8', xml_declaration=True)
        print(f'Simulation done! Results can be found in: {destination_xml}')

    def within_borders(self, y: int, x: int) -> bool:
        """Check if the coordinate is within matrix borders."""

        return {y, x}.issubset(range(len(self.world)))

    def count_neighbour_types(self, y: int, x: int) -> dict:
        """ Return 8 surrounding neighbour types of an element at Y,X.

        :param y: row index in a matrix
        :param x: column index in a matrix
        """

        # Keeps count of each neighbor type
        neighbour_counter = {}

        for yy in range(y - 1, y + 2):
            for xx in range(x - 1, x + 2):
                # Avoid middle element, check border coordinates and empty cells
                if not(yy == y and xx == x) and self.within_borders(yy, xx) and self.world[yy][xx]:
                    neighbour = self.world[yy][xx]
                    if neighbour.type in neighbour_counter:
                        neighbour_counter[neighbour.type] += 1
                    else:
                        neighbour_counter[neighbour.type] = 1
        return neighbour_counter

    def same_type_as_neighbours(self, element: Organism, neighbours_type_count: dict) -> bool:
        return element and element.type in neighbours_type_count

    def get_random_type(self, neighbours_type_count: dict, required_count: list) -> Union[int, None]:
        """ Get a random Organism type from a list of neighbour types with a specific count.

        :param neighbours_type_count: dict of Organism types and its respective count
        :param required_count: list of required counts the randomly selected type has to have
        :return: None if no type has a required count, otherwise Organism type
        """

        try:
            return random.choice([neighbour for neighbour, count in neighbours_type_count.items()
                                  if count in required_count])
        except IndexError:
            return None

    def calculate_organism_with_neighbours(self, current_organism: Organism, new_world: list, new_live_organisms: list):
        """ Iterate over the organism element and its neighbours (9 elements).

        :param current_organism: single living Organism
        :param new_world: N by N matrix with the new state of the world
        :param new_live_organisms: list of new live organisms
        """

        # Go through each of the 9 elements
        for yy in range(current_organism.y - 1, current_organism.y + 2):
            for xx in range(current_organism.x - 1, current_organism.x + 2):

                # Ignore border coordinates and empty cells
                if self.within_borders(yy, xx) and not self.verified_elements[yy * self.dimension + xx]:
                    self.verified_elements[yy * self.dimension + xx] = True

                    neighbours_types = self.count_neighbour_types(yy, xx)
                    element = self.world[yy][xx]

                    # Apply rules of Life - decide on the elements new Organism type
                    if self.same_type_as_neighbours(element, neighbours_types):
                        if 2 <= neighbours_types[element.type] <= 3:
                            if 3 in neighbours_types.values():
                                new_type = self.get_random_type(neighbours_types, required_count=[2, 3])  # Random BIRTH
                            else:
                                new_type = element.type  # Same as old type
                        else:
                            new_type = None  # DIES
                    else:
                        new_type = self.get_random_type(neighbours_types, required_count=[3])  # Random Birth

                    # Save the new type
                    if new_type:
                        new_world[yy][xx] = Organism(yy, xx, new_type)
                        new_live_organisms.append(Organism(yy, xx, new_type))
                    else:
                        new_world[yy][xx] = None

    def evolution_step(self):
        """Single step in in the evolution."""

        self.verified_elements = [False] * (self.dimension * self.dimension)
        new_world = [element for element in self.world]
        new_live_organisms = []

        for live_organism in self.live_organisms:
            self.calculate_organism_with_neighbours(live_organism, new_world, new_live_organisms)

        # Update the data structures with new iteration
        self.live_organisms = [element for element in new_live_organisms]
        self.world = [element for element in new_world]

    def run(self):
        """Run the simulation of Life."""

        print('Starting the simulation.')

        for i in range(self.iterations):
            self.evolution_step()

        self.save_xml_file(self.live_organisms, self.output_xml_file)

        return self.world
