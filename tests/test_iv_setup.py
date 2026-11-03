# tests/test_iv_setup.py - Vũ Trung Hiếu
# Test IV Setup: Chạy 24 vòng Serpent và gán thanh ghi LFSR/FSM

import unittest
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from key_setup import key_setup
from iv_setup import chuyen_iv_thanh_4_tu, chay_serpent_24_vong, iv_setup


class TestIVSetup(unittest.TestCase):

    def test_cac_ham_con(self):
        # 1. Test chuyển IV 16 byte thành 4 từ little-endian: 00..03 -> 0x03020100
        iv_tu = chuyen_iv_thanh_4_tu(bytes(range(16)))
        self.assertEqual(iv_tu[0], 0x03020100)

        # 2. Test chạy 24 vòng Serpent trả về đủ 3 mốc Y12, Y18, Y24
        subkeys = key_setup("000102030405060708090a0b0c0d0e0f")
        y12, y18, y24 = chay_serpent_24_vong([0, 0, 0, 0], subkeys)
        self.assertEqual((len(y12), len(y18), len(y24)), (4, 4, 4))

    def test_benchmark_1_tinh_tay(self):
        # Bộ 1: Tự tính tay (Key = 00..0f, IV = 00 11..ff)
        subkeys = key_setup("000102030405060708090a0b0c0d0e0f")
        lfsr, fsm = iv_setup("00112233445566778899aabbccddeeff", subkeys)
        # Khớp với FSM tính tay: R1 = y0^18 = 0x57dd3bd8, R2 = y2^18 = 0xe290b929
        self.assertEqual(fsm, [0x57DD3BD8, 0xE290B929])
        # Khớp với LFSR 4 từ đầu (Y24): y3, y2, y1, y0
        self.assertEqual(lfsr[:4], [0xD0A81B26, 0x4AFA6C81, 0xD5789294, 0x6261C4B9])
        print("\n[IV SETUP] Test tinh tay -> FSM khop R1:", hex(fsm[0]), "R2:", hex(fsm[1]))

    def test_benchmark_2_chuan_estream(self):
        # Bộ 2: Benchmark chuẩn quốc tế (Key 0011..eeff, IV 8899..6677)
        subkeys = key_setup("00112233445566778899aabbccddeeff")
        lfsr, fsm = iv_setup("8899aabbccddeeff0011223344556677", subkeys)
        self.assertEqual(fsm, [0x9AB17002, 0x101D095B])
        self.assertEqual(lfsr, [
            0xB3A3B696, 0x4F9F2596, 0x21A53B2B, 0x1BFABB41,
            0xCEC69B9B, 0xDBA99A9F,
            0x6076C06F, 0xC0AE3CD2, 0xABB5043B, 0xA93D885C
        ])
        print("[IV SETUP] Test chuan eSTREAM -> 10 LFSR va 2 FSM khop 100%")


if __name__ == "__main__":
    unittest.main()
