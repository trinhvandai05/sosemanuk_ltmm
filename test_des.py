# test_des.py - test thuat toan des

import unittest
from des import (
    hoan_vi,
    dich_vong_trai,
    sinh_16_khoa_con,
    ma_hoa_khoi_des,
    giai_ma_khoi_des
)


class TestDES(unittest.TestCase):

    def test_dich_vong_trai(self):
        bits = [1, 2, 3, 4]
        self.assertEqual(dich_vong_trai(bits, 1), [2, 3, 4, 1])
        self.assertEqual(dich_vong_trai(bits, 2), [3, 4, 1, 2])

    def test_sinh_khoa(self):
        khoa_bits = [0]* 64
        cac_khoa = sinh_16_khoa_con(khoa_bits)
        self.assertEqual(len(cac_khoa), 16)
        for k in cac_khoa:
            self.assertEqual(len(k), 48)

    def test_vi_du_1(self):
        khoa= "133457799BBCDFF1"
        ban_ro = "0123456789ABCDEF"
        ban_ma_mong_doi= "85E813540F0AB405"

        ban_ma_thuc_te= ma_hoa_khoi_des(ban_ro, khoa)
        self.assertEqual(ban_ma_thuc_te, ban_ma_mong_doi)

        ban_ro_giai_ma= giai_ma_khoi_des(ban_ma_thuc_te, khoa)
        self.assertEqual(ban_ro_giai_ma, ban_ro)

    def test_in_tung_vong(self):
        # in thu cac vong
        khoa= "133457799BBCDFF1"
        ban_ro = "0123456789ABCDEF"
        ban_ma= ma_hoa_khoi_des(ban_ro, khoa, in_trang_thai=True)
        self.assertEqual(ban_ma, "85E813540F0AB405")

    def test_thuan_nghich(self):
        khoa = "AABBCCDDEEFF0011"
        cac_ban_ro= [
            "0000000000000000",
            "FFFFFFFFFFFFFFFF",
            "123456789ABCDEF0"
        ]
        for p in cac_ban_ro:
            c= ma_hoa_khoi_des(p, khoa)
            p_giai_ma = giai_ma_khoi_des(c, khoa)
            self.assertEqual(p_giai_ma, p)


if __name__ == "__main__":
    unittest.main()
