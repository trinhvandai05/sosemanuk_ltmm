
import sys
import os
import unittest

sys.path.append(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
)

from LFSR import fsm_step


class TestFSM(unittest.TestCase):

    # Test truong hop R1 co bit cuoi bang 1
    def test_fsm_bit_1(self):

        # Khoi tao cac thanh ghi LFSR
        cac_thanh_ghi = [
            0, 3, 0, 0, 0,
            0, 0, 0, 4, 5
        ]