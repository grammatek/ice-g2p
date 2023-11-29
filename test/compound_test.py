import unittest
from ice_g2p import compound_analysis


class CompoundTestCase(unittest.TestCase):
    def test_valid_compound(self):
        comp = 'föðurafi'
        comp_parts = compound_analysis.get_compound_parts(comp)
        self.assertEqual(['föður', 'afi'], comp_parts)

        comp = 'djasstónlistarkennsla'
        comp_parts = compound_analysis.get_compound_parts(comp)
        self.assertEqual(['djass', 'tón', 'listar', 'kennsla'], comp_parts)

    def test_non_compound(self):
        comp = 'föður'
        comp_parts = compound_analysis.get_compound_parts(comp)
        self.assertEqual(['föður'], comp_parts)


if __name__ == '__main__':
    unittest.main()
