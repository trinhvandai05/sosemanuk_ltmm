# aes_tables.py - Sinh bảng S-box, Inverse S-box và Rcon cho AES-128


def nhandathuc(A,B,n=8,m=0x1B):
    C = 0 # kết quả cuối
    bit_cao = 1 << (n-1) 
    quychieu = (1 <<n) - 1 # check xem cần bao nhiêu bit trong GF
    while(n!= 0):
        if (A&1)!= 0:
            C = C ^B 
        A  = A >> 1
        carry = B & bit_cao
        B = (B << 1) & quychieu
        if ( carry != 0): 
            B = B ^ m  # nếu bit cao của B = 1 nghĩa là sẽ tràn so với GF nên phải XOR với m để giảm bậc
        n = n - 1
    return C


def nghich_dao_gf(a):
    if a == 0: 
        return 0
    # a^254
    ket_qua = 1
    co_so= a
    so_mu = 254
    while so_mu > 0:
        if so_mu & 1: 
            ket_qua= nhandathuc(ket_qua, co_so, 8, 0x1B)
        co_so = nhandathuc(co_so, co_so, 8, 0x1B)
        so_mu = so_mu>> 1
    return ket_qua


def bien_doi_affine(b):
    c = 0x63
    ket_qua= 0
    for i in range(8):
        bit_i = ((b >> i) & 1) ^ ((b >> ((i+4)%8)) & 1) ^ ((b >> ((i+5)%8))& 1) ^ ((b>> ((i+6)%8)) & 1) ^ ((b >> ((i+7)%8)) & 1) ^ ((c >>i) & 1)
        ket_qua |= (bit_i <<i)
    return ket_qua


# sinh S_BOX 256 phần tử
S_BOX = []
for i in range( 256 ):
    S_BOX.append(bien_doi_affine(nghich_dao_gf(i)))


# bảng nghịch đảo
INV_S_BOX= [ 0 ]*256
for x in range(256):
    INV_S_BOX[S_BOX[x]] = x


# sinh hằng số vòng RCON cho 10 vòng
RCON = [None] * 11
rc =1
for i in range(1, 11):
    RCON[i] = [rc, 0, 0, 0]
    rc= nhandathuc(rc, 2, 8, 0x1B)
