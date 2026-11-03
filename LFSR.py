from smath.py import mul_alpha, div_alpha
def lfsr_step(cac_thanh_ghi):
    # Kiem tra phai co dung 10 thanh ghi
    if len(cac_thanh_ghi) != 10:
        raise ValueError("LFSR phai co dung 10 thanh ghi")
