# tests/test_key_setup.py - Vũ Trung Hiếu
# Kiểm tra các hàm con và toàn bộ quy trình key_setup

import unittest
import sys
import os

# Cho phép import file ở thư mục gốc
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from key_setup import (
    dem_khoa,
    chia_thanh_8_tu,
    mo_rong_khoa,
    tao_25_khoa_con,
    key_setup
)


class TestKeySetup(unittest.TestCase):

    # 1. Kiểm tra hàm đệm khóa
    def test_dem_khoa_128_bit(self):
        # Khóa 16 byte (128 bit) thì phải đệm thành 32 byte
        khoa_16_byte = bytes(range(16))
        khoa_dem = dem_khoa(khoa_16_byte)
        self.assertEqual(len(khoa_dem), 32)
        # Byte thứ 16 phải là 0x01 để đánh dấu
        self.assertEqual(khoa_dem[16], 0x01)
        # Các byte còn lại phải là 0x00
        self.assertEqual(khoa_dem[17:], bytes(15))

    def test_dem_khoa_256_bit(self):
        # Khóa đã đủ 32 byte (256 bit) rồi thì giữ nguyên, không cần đệm
        khoa_32_byte = bytes(range(32))
        khoa_dem = dem_khoa(khoa_32_byte)
        self.assertEqual(khoa_dem, khoa_32_byte)

    def test_dem_khoa_sai_do_dai(self):
        # Không được để khóa rỗng hoặc dài quá 32 byte
        with self.assertRaises(ValueError):
            dem_khoa(b"")
        with self.assertRaises(ValueError):
            dem_khoa(bytes(33))

    # 2. Kiểm tra hàm chia thành 8 từ little-endian
    def test_chia_thanh_8_tu(self):
        # 4 byte đầu: 0x00, 0x01, 0x02, 0x03 -> đảo ngược lại phải ra 0x03020100
        du_lieu_32_byte = bytes(range(32))
        cac_tu = chia_thanh_8_tu(du_lieu_32_byte)
        self.assertEqual(len(cac_tu), 8)
        self.assertEqual(cac_tu[0], 0x03020100)
        self.assertEqual(cac_tu[1], 0x07060504)

    # 3. Kiểm tra hàm mở rộng khóa
    def test_mo_rong_khoa(self):
        # Ban đầu có 8 từ w-8..w-1, mở rộng thêm 100 từ nữa thì tổng phải là 108 từ
        cac_tu_8 = [0] * 8
        w = mo_rong_khoa(cac_tu_8)
        self.assertEqual(len(w), 108)

    # 4. Kiểm tra hàm tạo 25 khóa con
    def test_tao_25_khoa_con(self):
        # Phải sinh đủ 25 khóa con, mỗi khóa con là 1 danh sách 4 từ 32 bit
        cac_tu_8 = [0x12345678] * 8
        w = mo_rong_khoa(cac_tu_8)
        cac_khoa_con = tao_25_khoa_con(w)
        self.assertEqual(len(cac_khoa_con), 25)
        for k in cac_khoa_con:
            self.assertEqual(len(k), 4)

    # 5. Kiểm tra toàn bộ hàm key_setup đối chiếu với test vector chuẩn
    def test_key_setup_vector_chuan(self):
        # Test vector chuẩn của Sosemanuk
        khoa = "00112233445566778899aabbccddeeff"
        cac_khoa_con = key_setup(khoa)
        self.assertEqual(len(cac_khoa_con), 25)

        # Khóa con K0 mong đợi
        k0_mong_doi = [0x9d8baf0, 0x7d187fbd, 0xdd4f2b57, 0x7cf49c7d]
        self.assertEqual(cac_khoa_con[0], k0_mong_doi)

        # Khóa con K24 mong đợi
        k24_mong_doi = [0xef48c5a6, 0xa91bd5b5, 0xc003118e, 0x6db4215c]
        self.assertEqual(cac_khoa_con[24], k24_mong_doi)


if __name__ == "__main__":
    unittest.main()
