# tests/test_key_setup.py - Vũ Trung Hiếu
# Test Key Setup: Gồm 2 bộ benchmark (tự tính tay và chuẩn eSTREAM)

import unittest
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from key_setup import dem_khoa, chia_thanh_8_tu, mo_rong_khoa, tao_25_khoa_con, key_setup


class TestKeySetup(unittest.TestCase):

    def test_cac_ham_con(self):
        # 1. Test đệm khóa: 16 byte -> 32 byte (thêm 0x01 rồi các số 0)
        k16 = bytes(range(16))
        pad = dem_khoa(k16)
        self.assertEqual((len(pad), pad[16], pad[17:]), (32, 1, bytes(15)))

        # 2. Test chia 8 từ little-endian: 00 01 02 03 -> 0x03020100
        w8 = chia_thanh_8_tu(pad)
        self.assertEqual(w8[0], 0x03020100)

        # 3. Test mở rộng: w0 = rotl11(w-8 ^ w-5 ^ w-3 ^ w-1 ^ PHI ^ 0, 11)
        # Khớp chính xác với số tính tay 0xdbadac91
        w = mo_rong_khoa(w8)
        self.assertEqual(w[8], 0xDBADAC91)

    def test_benchmark_1_tinh_tay(self):
        # Bộ 1: Nhóm tự tính tay (Key = 00 01 02 ... 0f)
        subkeys = key_setup("000102030405060708090a0b0c0d0e0f")
        self.assertEqual(len(subkeys), 25)
        # K0 tính tay qua hộp S3: [0xd9acacc1, 0xf4b57314, 0x3225025c, 0x103119d9]
        self.assertEqual(subkeys[0], [0xD9ACACC1, 0xF4B57314, 0x3225025C, 0x103119D9])
        print("\n[KEY SETUP] Test tinh tay Key 00..0f -> K0 khop 100%:", [hex(x) for x in subkeys[0]])

    def test_benchmark_2_chuan_estream(self):
        # Bộ 2: Benchmark chuẩn quốc tế của tác giả SOSEMANUK
        subkeys = key_setup("00112233445566778899aabbccddeeff")
        self.assertEqual(subkeys[0], [0x09D8BAF0, 0x7D187FBD, 0xDD4F2B57, 0x7CF49C7D])
        self.assertEqual(subkeys[24], [0xEF48C5A6, 0xA91BD5B5, 0xC003118E, 0x6DB4215C])
        print("[KEY SETUP] Test chuan eSTREAM Key 0011..eeff -> K0 va K24 khop 100%")


if __name__ == "__main__":
    unittest.main()
