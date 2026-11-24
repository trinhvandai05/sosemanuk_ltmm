# test_aes.py - test thuat toan aes-128

import unittest
from aes_tables import S_BOX, INV_S_BOX, RCON, nhandathuc
from aes import (
    add_round_key,
    ma_hoa_aes_128,
    giai_ma_aes_128,
    mix_columns,
    inv_mix_columns,
    bytes_sang_state,
    mo_rong_khoa,
    shift_rows,
    state_sang_bytes,
    sub_bytes
)


class TestAES128(unittest.TestCase):

    def test_0_nhandathuc_gf(self):
        self.assertEqual(nhandathuc(0x57, 0x83, 8, 0x1B), 0xC1)
        self.assertEqual(nhandathuc(0xA6, 0x3D, 8, 0x1B), 0xC6)

    def test_1_sinh_bang_s_box(self):
        self.assertEqual(S_BOX[0x00], 0x63)
        self.assertEqual(S_BOX[0x01], 0x7c)
        self.assertEqual(S_BOX[0x02], 0x77)
        self.assertEqual(S_BOX[0x53], 0xed)
        self.assertEqual(S_BOX[0xff], 0x16)
        for x in range(256):
            self.assertEqual(INV_S_BOX[S_BOX[x]], x)

    def test_2_hang_so_vong_rcon(self):
        self.assertEqual(RCON[1][0], 0x01)
        self.assertEqual(RCON[2][0], 0x02)
        self.assertEqual(RCON[8][0], 0x80)
        self.assertEqual(RCON[9][0], 0x1b)
        self.assertEqual(RCON[10][0], 0x36)

    def test_3_mix_columns(self):
        state = [
            [0xd4, 0, 0, 0],
            [0xbf, 0, 0, 0],
            [0x5d, 0, 0, 0],
            [0x30, 0, 0, 0]
        ]
        mix_columns(state)
        self.assertEqual(state[0][0], 0x04)
        self.assertEqual(state[1][0], 0x66)
        self.assertEqual(state[2][0], 0x81)
        self.assertEqual(state[3][0], 0xe5)

        inv_mix_columns(state)
        self.assertEqual(state[0][0], 0xd4)
        self.assertEqual(state[1][0], 0xbf)
        self.assertEqual(state[2][0], 0x5d)
        self.assertEqual(state[3][0], 0x30)

    def test_vi_du_1(self):
        khoa= "0f1571c947d9e8590cb7add6af7f6798"
        ban_ro = "0123456789abcdeffedcba9876543210"
        ban_ma_chuan= "ff0b844a0853bf7c6934ab4364148fb9"

        ban_ma= ma_hoa_aes_128(ban_ro, khoa)
        self.assertEqual(ban_ma.lower(), ban_ma_chuan.lower())

        ban_ro_giai_ma = giai_ma_aes_128(ban_ma, khoa)
        self.assertEqual(ban_ro_giai_ma.lower(), ban_ro.lower())

    def test_in_cac_buoc(self):
        # in thu cac buoc
        khoa = "0f1571c947d9e8590cb7add6af7f6798"
        ban_ro= "0123456789abcdeffedcba9876543210"
        ban_ma = ma_hoa_aes_128(ban_ro, khoa, in_trang_thai=True)
        self.assertEqual(ban_ma.lower(), "ff0b844a0853bf7c6934ab4364148fb9")

    def test_vi_du_2(self):
        khoa = "2b7e151628aed2a6abf7158809cf4f3c"
        ban_ro= "3243f6a8885a308d313198a2e0370734"
        ban_ma_chuan = "3925841d02dc09fbdc118597196a0b32"

        ban_ma= ma_hoa_aes_128(ban_ro, khoa)
        self.assertEqual(ban_ma.lower(), ban_ma_chuan.lower())

        ban_ro_giai_ma= giai_ma_aes_128(ban_ma, khoa)
        self.assertEqual(ban_ro_giai_ma.lower(), ban_ro.lower())

    def test_toan_0(self):
        khoa = "00"* 16
        ban_ro = "00"* 16
        ban_ma_chuan= "66e94bd4ef8a2c3b884cfa59ca342b2e"

        ban_ma = ma_hoa_aes_128(ban_ro, khoa)
        self.assertEqual(ban_ma.lower(), ban_ma_chuan.lower())

    def test_vong_1(self):
        from aes import (
        mo_rong_khoa, sub_bytes,
        shift_rows, add_round_key
    )

        p = "00000000000000000000000000000011"
        k = "00000000000000000000000000000000"

        keys = mo_rong_khoa(list(bytes.fromhex(k)))
        state = bytes_sang_state(list(bytes.fromhex(p)))

        def to_hex(s):
            return bytes(state_sang_bytes(s)).hex()

        self.assertEqual(
            to_hex(keys[1]),
            "62636363626363636263636362636363"
        )

        add_round_key(state, keys[0])
        sub_bytes(state)
        shift_rows(state)
        mix_columns(state)
        add_round_key(state, keys[1])

        self.assertEqual(
            to_hex(state),
            "e0e138d9010000000100000001000000"
        )


if __name__ == "__main__":
    unittest.main()
