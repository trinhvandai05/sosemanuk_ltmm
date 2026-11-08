
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
             R1 = 1
        R2 = 2

        # Ket qua mong doi
        R1_mong_doi = 0x9
        R2_mong_doi = 0x328983AA
        f_mong_doi = 0x328983A4

        # Chay ham FSM
        R1_thuc_te, R2_thuc_te, f_thuc_te = fsm_step(
            R1, R2, cac_thanh_ghi
        )

        # Kiem tra ket qua
        self.assertEqual(R1_thuc_te, R1_mong_doi)
        self.assertEqual(R2_thuc_te, R2_mong_doi)
        self.assertEqual(f_thuc_te, f_mong_doi)