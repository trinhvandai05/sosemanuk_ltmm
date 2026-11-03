from smath.py import mul_alpha, div_alpha,rot132
#code cho ham LFSR
def lfsr_step(cac_thanh_ghi):
    # Kiem tra phai co dung 10 thanh ghi
    if len(cac_thanh_ghi) != 10:
        raise ValueError("LFSR phai co dung 10 thanh ghi")
   # Lay cac thanh ghi can thiet
    s0 = cac_thanh_ghi[0]
    s3 = cac_thanh_ghi[3]
    s9 = cac_thanh_ghi[9]

    # Tinh gia tri thanh ghi moi
    s_moi = (
        s_t9
        ^ ((s_t3 << 8) & 0xFFFFFFFF)
        ^ div_alpha(s_t3)
        ^ mul_alpha(s_t)
    )

    s_moi = s_moi & 0xFFFFFFFF
      # Dich chuyen cac thanh ghi
    for i in range(9):
        cac_thanh_ghi[i] = cac_thanh_ghi[i + 1]

    cac_thanh_ghi[9] = s_moi

    return s_moi
#code cho ham FSM
def mux(dieu_khien, x, y):
    if dieu_khien & 1:
        return x ^ y
    else:
        return x
# Ham TRANS
def trans(x):
    x = (x * 0x54655307) & 0xFFFFFFFF
    return rotl32(x, 7)


# Ham FSM
def fsm_step(R1, R2, cac_thanh_ghi):

    # Kiem tra LFSR co dung 10 thanh ghi
    if len(cac_thanh_ghi) != 10:
        raise ValueError("Can dung 10 thanh ghi LFSR")

