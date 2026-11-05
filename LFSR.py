from smath import mul_alpha, div_alpha,rotl32
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
    s9
    ^ div_alpha(s3)
    ^ mul_alpha(s0)
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
  # Lay cac gia tri LFSR
    s1 = cac_thanh_ghi[1]
    s8 = cac_thanh_ghi[8]
    s9 = cac_thanh_ghi[9]

    # Tinh R1 moi
    R1_moi = (R2 + mux(R1, s1, s8)) & 0xFFFFFFFF

    # Tinh R2 moi
    R2_moi = trans(R1)
      # Tinh dau ra FSM
    f = ((s9 + R1_moi) & 0xFFFFFFFF) ^ R2_moi

    return R1_moi, R2_moi, f
