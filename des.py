from des_tables import IP, FP, E, P, PC1, PC2, SO_BUOC_DICH, S_BOXES


def hex_sang_danh_sach_bit(chuoi_hex, so_bit=64):
    gia_tri_so = int(chuoi_hex, 16)
    danh_sach_bit = []
    for i in range(so_bit - 1, -1, -1):  # bit cao xuong thap
        bit = (gia_tri_so >> i)& 1
        danh_sach_bit.append(bit)
    return danh_sach_bit


def danh_sach_bit_sang_hex(danh_sach_bit):
    gia_tri_so= 0
    for bit in danh_sach_bit:
        gia_tri_so = (gia_tri_so << 1) | bit
    do_dai_hex= len(danh_sach_bit) // 4
    return f"{gia_tri_so:0{do_dai_hex}X}"


def hoan_vi(danh_sach_bit, bang_hoan_vi):
    ket_qua = []
    for vi_tri in bang_hoan_vi:
        bit = danh_sach_bit[vi_tri - 1]
        ket_qua.append( bit )
    return ket_qua


def dich_vong_trai(danh_sach_bit, so_buoc):
    return danh_sach_bit[so_buoc:] + danh_sach_bit[:so_buoc]


def sinh_16_khoa_con(khoa_64_bit):
    khoa_56= hoan_vi(khoa_64_bit, PC1)
    C = khoa_56[:28]
    D= khoa_56[28:]

    danh_sach_16_khoa = []
    for r in range(16):
        buoc_dich = SO_BUOC_DICH[r]
        C= dich_vong_trai(C, buoc_dich)
        D = dich_vong_trai(D, buoc_dich)
        CD= C + D
        khoa_con_48 = hoan_vi(CD, PC2)
        danh_sach_16_khoa.append(khoa_con_48)

    return danh_sach_16_khoa


def ham_feistel_F(nua_phai_32, khoa_con_48):
    R_48 = hoan_vi(nua_phai_32, E)

    R_xor_K= []
    for i in range(48):
        R_xor_K.append(R_48[i] ^ khoa_con_48[i])

    dau_ra_sbox = []
    for i in range(8):
        khoi_6_bit = R_xor_K[i * 6 : (i + 1) * 6]
        hang = (khoi_6_bit[0] << 1)| khoi_6_bit[5]
        cot= (khoi_6_bit[1] << 3) | (khoi_6_bit[2] << 2) | (khoi_6_bit[3] << 1)| khoi_6_bit[4]
        gia_tri_ra= S_BOXES[i][hang][cot]
        for k in range(3, -1, -1):
            dau_ra_sbox.append((gia_tri_ra >> k) & 1)

    return hoan_vi(dau_ra_sbox, P)


def ma_hoa_khoi_des(khoi_ro_hex, khoa_hex, in_trang_thai=False):
    khoi_ro_bits= hex_sang_danh_sach_bit(khoi_ro_hex, 64)
    khoa_bits = hex_sang_danh_sach_bit(khoa_hex, 64)

    if in_trang_thai:
        print(f"\n=== MA HOA DES ===")
        print(f"Ban ro: {khoi_ro_hex} | Khoa: {khoa_hex}")

    danh_sach_khoa = sinh_16_khoa_con(khoa_bits)
    khoi_ip= hoan_vi(khoi_ro_bits, IP)
    L = khoi_ip[:32]
    R = khoi_ip[32:]

    if in_trang_thai:
        print(f"Sau IP:  L0 = {danh_sach_bit_sang_hex(L)}, R0 = {danh_sach_bit_sang_hex(R)}")

    for r in range(16):
        L_moi = R
        f_ra= ham_feistel_F(R, danh_sach_khoa[r])
        R_moi = []
        for j in range(32):
            R_moi.append(L[j] ^ f_ra[j])
        L= L_moi
        R = R_moi

        if in_trang_thai:
            k_hex = danh_sach_bit_sang_hex(danh_sach_khoa[r])
            print(f"Vong {r+1:2d}: K = {k_hex} | L{r+1:02d} = {danh_sach_bit_sang_hex(L)}, R{r+1:02d} = {danh_sach_bit_sang_hex(R)}")

    ghep_nguoc= R + L
    khoi_ma_bits = hoan_vi(ghep_nguoc, FP)
    ban_ma = danh_sach_bit_sang_hex(khoi_ma_bits)
    if in_trang_thai:
        print(f"Sau FP (Ban ma): {ban_ma}")
    return ban_ma


def giai_ma_khoi_des(khoi_ma_hex, khoa_hex):
    khoi_ma_bits = hex_sang_danh_sach_bit(khoi_ma_hex, 64)
    khoa_bits= hex_sang_danh_sach_bit(khoa_hex, 64)

    danh_sach_khoa_nguoc = sinh_16_khoa_con(khoa_bits)[::-1]
    khoi_ip = hoan_vi(khoi_ma_bits, IP)
    L= khoi_ip[:32]
    R = khoi_ip[32:]

    for r in range(16):
        L_moi = R
        f_ra= ham_feistel_F(R, danh_sach_khoa_nguoc[r])
        R_moi = []
        for j in range(32):
            R_moi.append(L[j] ^ f_ra[j])
        L = L_moi
        R= R_moi

    ghep_nguoc = R + L
    khoi_ro_bits= hoan_vi(ghep_nguoc, FP)
    return danh_sach_bit_sang_hex(khoi_ro_bits)
