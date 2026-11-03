from smath.py import mul_alpha, div_alpha
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
        ^ ((s3 << 8) & 0xFFFFFFFF)
        ^ div_alpha(s3)
        ^ mul_alpha(s0)
    )
