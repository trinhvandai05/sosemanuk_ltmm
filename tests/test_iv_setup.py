# tests/test_iv_setup.py - Vũ Trung Hiếu
# Kiểm tra các hàm con và toàn bộ quy trình iv_setup

import unittest
import sys
import os

# Cho phép import file ở thư mục gốc
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from key_setup import key_setup
from iv_setup import (
    chuyen_iv_thanh_4_tu,
    chay_serpent_24_vong,
    iv_setup
)


class TestIVSetup(unittest.TestCase):

    # 1. Kiểm tra chuyển IV 16 byte thành 4 từ 32 bit
    def test_chuyen_iv_thanh_4_tu(self):
        # IV 16 byte đầu vào phải đổi ra đúng 4 từ theo little-endian
        iv_16_byte = bytes(range(16))
        cac_tu = chuyen_iv_thanh_4_tu(iv_16_byte)
        self.assertEqual(len(cac_tu), 4)
        # 4 byte đầu 0, 1, 2, 3 đảo ngược lại phải ra 0x03020100
        self.assertEqual(cac_tu[0], 0x03020100)

    def test_chuyen_iv_sai_kich_thuoc(self):
        # IV bắt buộc phải đúng 16 byte, thừa hay thiếu đều phải báo lỗi
        with self.assertRaises(ValueError):
            chuyen_iv_thanh_4_tu(bytes(15))
        with self.assertRaises(ValueError):
            chuyen_iv_thanh_4_tu(bytes(17))

    # 2. Kiểm tra chạy Serpent 24 vòng
    def test_chay_serpent_24_vong(self):
        # Chạy thử 24 vòng xem có trả về đủ 3 mốc vòng 12, 18, 24 không
        khoa = "00112233445566778899aabbccddeeff"
        cac_khoa_con = key_setup(khoa)
        iv_4_tu = [0, 0, 0, 0]

        y12, y18, y24 = chay_serpent_24_vong(iv_4_tu, cac_khoa_con)
        self.assertEqual(len(y12), 4)
        self.assertEqual(len(y18), 4)
        self.assertEqual(len(y24), 4)

    # 3. Kiểm tra gán đúng thanh ghi LFSR và FSM theo vector chuẩn
    def test_iv_setup_vector_chuan(self):
        khoa = "00112233445566778899aabbccddeeff"
        iv = "8899aabbccddeeff0011223344556677"

        cac_khoa_con = key_setup(khoa)
        lfsr, fsm = iv_setup(iv, cac_khoa_con)

        # Kiểm tra 10 thanh ghi LFSR (s1 đến s10)
        self.assertEqual(len(lfsr), 10)
        lfsr_mong_doi = [
            0xb3a3b696, 0x4f9f2596, 0x21a53b2b, 0x1bfabb41,
            0xcec69b9b, 0xdba99a9f,
            0x6076c06f, 0xc0ae3cd2, 0xabb5043b, 0xa93d885c
        ]
        self.assertEqual(lfsr, lfsr_mong_doi)

        # Kiểm tra 2 thanh ghi FSM (R1, R2)
        self.assertEqual(len(fsm), 2)
        fsm_mong_doi = [0x9ab17002, 0x101d095b]
        self.assertEqual(fsm, fsm_mong_doi)


if __name__ == "__main__":
    unittest.main()
