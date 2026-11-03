
def rotl32(so, buoc):
    # Xoay trai trong 32 bit
    buoc = buoc % 32
    so = so & 0xFFFFFFFF

    return ((so << buoc) | (so >> (32 - buoc))) & 0xFFFFFFFF


def sbox(chi_so, cac_tu):
    if chi_so < 0 or chi_so > 7:
        raise ValueError('Chi so S-box phai tu 0 den 7')
    if len(cac_tu) != 4:
        raise ValueError('Dau vao phai co dung 4 tu 32 bit')

    # 8 bang S-box cua Serpent
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

    bang = cac_bang[chi_so]
    ket_qua = [0, 0, 0, 0]

    for vi_tri in range(32):
        dau_vao = 0

        # Lay 1 bit tu moi tu 32 bit
        for i in range(4):
            bit = (cac_tu[i] >> vi_tri) & 1
            dau_vao = dau_vao | (bit << i)

        # Thay the qua S-box
        dau_ra = bang[dau_vao]

        # Dua 4 bit ket qua ve 4 tu
        for i in range(4):
            bit = (dau_ra >> i) & 1
            ket_qua[i] = ket_qua[i] | (bit << vi_tri)

    return ket_qua


def LT(cac_tu):
    # Bien doi tuyen tinh Serpent
    a, b, c, d = cac_tu

    a = rotl32(a, 13)
    c = rotl32(c, 3)

    b = b ^ a ^ c
    d = d ^ c ^ (a << 3)

    b = rotl32(b, 1)
    d = rotl32(d, 7)

    a = a ^ b ^ d
    c = c ^ d ^ (b << 7)

    a = rotl32(a, 5)
    c = rotl32(c, 22)

    return [
        a & 0xFFFFFFFF,
        b & 0xFFFFFFFF,
        c & 0xFFFFFFFF,
        d & 0xFFFFFFFF
    ]


def _nhan_gf8(a, b):
    # Nhan hai byte trong GF(2^8)
    # Da thuc bat kha quy: 0x1A9
    ket_qua = 0

    for i in range(8):
        if b & 1:
            ket_qua = ket_qua ^ a

        bit_cao = a & 0x80
        a = (a << 1) & 0xFF

        if bit_cao:
            a = a ^ 0xA9

        b = b >> 1

    return ket_qua


def mul_alpha(so):
    # Nhan voi alpha trong GF(2^32)
    byte_cao = (so >> 24) & 0xFF

    phan_bu = (
        (_nhan_gf8(byte_cao, 0xE1) << 24)
        | (_nhan_gf8(byte_cao, 0x9F) << 16)
        | (_nhan_gf8(byte_cao, 0xCF) << 8)
        | _nhan_gf8(byte_cao, 0x13)
    )

    ket_qua = ((so << 8) & 0xFFFFFFFF) ^ phan_bu
    return ket_qua


def div_alpha(so):
    # Nhan voi alpha nghich dao trong GF(2^32)
    byte_thap = so & 0xFF

    phan_bu = (
        (_nhan_gf8(byte_thap, 0x18) << 24)
        | (_nhan_gf8(byte_thap, 0x0F) << 16)
        | (_nhan_gf8(byte_thap, 0x40) << 8)
        | _nhan_gf8(byte_thap, 0xCD)
    )

    ket_qua = (so >> 8) ^ phan_bu
    return ket_qua
