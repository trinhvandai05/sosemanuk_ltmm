
import unittest
from smath import rotl32, sbox, LT, mul_alpha, div_alpha


class TestMath(unittest.TestCase):

    # 1. Kiem tra ROTL32
    def test_rotl32_vi_du(self):
        self.assertEqual(rotl32(0x923B75B5, 11), 0xDBADAC91)
        self.assertEqual(rotl32(0x12345678, 8), 0x34567812)
        self.assertEqual(rotl32(0x80000001, 1), 0x00000003)

    def test_rotl32_bien(self):
        self.assertEqual(rotl32(0, 13), 0)
        self.assertEqual(rotl32(0x12345678, 0), 0x12345678)
        self.assertEqual(rotl32(0x12345678, 32), 0x12345678)
        self.assertEqual(rotl32(0xFFFFFFFF, 17), 0xFFFFFFFF)

    # 2. Kiem tra S-box
    def test_sbox_s2(self):
        dau_vao = [
            0x9A72177D, 0x6E9BD691,
            0x92CCAD70, 0x49CF5598
        ]

        mong_doi = [
            0x27D82B09, 0x6661ED94,
            0xFFAB50E4, 0xD351C3E3
        ]

        self.assertEqual(sbox(2, dau_vao), mong_doi)

    def test_sbox_day_du(self):
        # Bang S-box Serpent dung de doi chieu
        cac_bang = [
            [3, 8, 15, 1, 10, 6, 5, 11, 14, 13, 4, 2, 7, 0, 9, 12],
            [15, 12, 2, 7, 9, 0, 5, 10, 1, 11, 14, 8, 6, 13, 3, 4],
            [8, 6, 7, 9, 3, 12, 10, 15, 13, 1, 14, 4, 0, 11, 5, 2],
            [0, 15, 11, 8, 12, 9, 6, 3, 13, 1, 2, 4, 10, 7, 5, 14],
            [1, 15, 8, 3, 12, 0, 11, 6, 2, 5, 4, 10, 9, 14, 7, 13],
            [15, 5, 2, 11, 4, 10, 9, 12, 0, 3, 14, 8, 13, 6, 7, 1],
            [7, 2, 12, 5, 8, 4, 6, 11, 14, 9, 1, 15, 13, 3, 10, 0],
            [1, 13, 15, 0, 14, 8, 2, 11, 7, 4, 12, 10, 9, 3, 5, 6]
        ]

        for chi_so in range(8):
            for gia_tri in range(16):
                dau_vao = [
                    0xFFFFFFFF if (gia_tri >> i) & 1 else 0
                    for i in range(4)
                ]

                gia_tri_ra = cac_bang[chi_so][gia_tri]

                mong_doi = [
                    0xFFFFFFFF if (gia_tri_ra >> i) & 1 else 0
                    for i in range(4)
                ]

                with self.subTest(sbox=chi_so, gia_tri=gia_tri):
                    self.assertEqual(
                        sbox(chi_so, dau_vao), mong_doi
                    )

    def test_sbox_du_lieu_sai(self):
        for chi_so in [-1, 8]:
            with self.assertRaises(ValueError):
                sbox(chi_so, [0, 0, 0, 0])

        with self.assertRaises(ValueError):
            sbox(2, [0, 0, 0])

    # 3. Kiem tra Linear Transformation
    def test_LT_vi_du(self):
        dau_vao = [
            0x7121227F, 0x16205DEE,
            0xE4D25B85, 0xE5834051
        ]

        mong_doi = [
            0x5873D3D7, 0x29FADFCA,
            0x97DB22E5, 0xB776AF70
        ]

        self.assertEqual(LT(dau_vao), mong_doi)

    def test_LT_bien(self):
        self.assertEqual(
            LT([0, 0, 0, 0]),
            [0, 0, 0, 0]
        )

        self.assertEqual(
            LT([1, 0, 0, 0]),
            [0x100C0000, 0x00004000,
             0x00002800, 0x00800000]
        )

    def test_LT_tuyen_tinh(self):
        a = [0x12345678, 0x9ABCDEF0, 0x11223344, 0x55667788]
        b = [0x0F0F0F0F, 0xAAAAAAAA, 0x33333333, 0x87654321]

        tong = [x ^ y for x, y in zip(a, b)]

        ve_trai = LT(tong)
        ve_phai = [
            x ^ y for x, y in zip(LT(a), LT(b))
        ]

        self.assertEqual(ve_trai, ve_phai)

    # 4. Kiem tra nhan Alpha
    def test_mul_alpha(self):
        self.assertEqual(mul_alpha(0), 0)
        self.assertEqual(mul_alpha(1), 0x00000100)
        self.assertEqual(mul_alpha(0xD0A81B26), 0xDA07FB91)
        self.assertEqual(mul_alpha(0xFFFFFFFF), 0xC0AC4AEB)

    # 5. Kiem tra chia Alpha
    def test_div_alpha(self):
        self.assertEqual(div_alpha(0), 0)
        self.assertEqual(div_alpha(0x100), 1)
        self.assertEqual(div_alpha(0x6261C4B9), 0x422138B7)
        self.assertEqual(div_alpha(0xFFFFFFFF), 0xB60C5A1D)

    def test_alpha_nghich_dao(self):
        cac_so = [
            0, 1, 0x100, 0x12345678,
            0xD0A81B26, 0x6261C4B9,
            0x80000000, 0xFFFFFFFF
        ]

        for so in cac_so:
            with self.subTest(so=hex(so)):
                self.assertEqual(
                    div_alpha(mul_alpha(so)), so
                )
                self.assertEqual(
                    mul_alpha(div_alpha(so)), so
                )


if __name__ == "__main__":
    unittest.main()
