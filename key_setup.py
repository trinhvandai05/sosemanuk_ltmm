# key_setup.py - Vũ Trung Hiếu
# Nhiệm vụ: Từ key đầu vào sinh 25 key con đầu ra (K0 đến K24)

from smath import rotl32, sbox

# Hằng số Phi trong đặc tả Sosemanuk
PHI = 0x9E3779B9


def dem_khoa(khoa_goc):
    # Nếu truyền vào là chuỗi hex thì chuyển sang bytes
    if isinstance(khoa_goc, str):
        khoa_bytes = bytes.fromhex(khoa_goc)
    else:
        khoa_bytes = bytes(khoa_goc)  # chuyển thành bytes để xử lý thống nhất

    # Độ dài khóa phải từ 1 đến 32 byte (8 đến 256 bit)
    do_dai = len(khoa_bytes)
    if do_dai < 1 or do_dai > 32:
        raise ValueError("Độ dài khóa phải từ 1 đến 32 byte")

    # Nếu nhỏ hơn 32 byte (256 bit) thì đệm thêm byte 0x01 rồi các byte 0x00
    if do_dai < 32:
        khoa_dem = khoa_bytes + bytes([1]) + bytes([0] * (31 - do_dai))
    else:
        khoa_dem = khoa_bytes

    return khoa_dem


def chia_thanh_8_tu(khoa_dem):
    # Chia 32 byte đã đệm thành 8 từ 32 bit theo kiểu Little-Endian (là từ bit dưới lên trên ví dụ 00 01 02 03 -> 03020100)
    cac_tu = []
    for i in range(8):
        doan_4_byte = khoa_dem[i * 4 : (i + 1) * 4]
        tu = int.from_bytes(doan_4_byte, "little")
        cac_tu.append(tu)  # các từ này là w -8,w-7,...,w-1
    return cac_tu


def mo_rong_khoa(cac_tu_ban_dau):
    # w ban đầu có 8 từ (w-8 đến w-1)
    w = list(cac_tu_ban_dau)

    # Mở rộng thêm 100 từ (để đủ 25 khóa con * 4 từ = 100 từ)
    for i in range(100):
        # Công thức: w_i = rotl32(w_{i-8} ^ w_{i-5} ^ w_{i-3} ^ w_{i-1} ^ PHI ^ i, 11)
        # Trong mảng w hiện tại: w[i] là w_{i-8}, w[i+3] là w_{i-5}, w[i+5] là w_{i-3}, w[i+7] là w_{i-1}
        gia_tri_xor = w[i] ^ w[i + 3] ^ w[i + 5] ^ w[i + 7] ^ PHI ^ i
        tu_moi = rotl32(gia_tri_xor, 11)
        w.append(tu_moi)

    return w


def tao_25_khoa_con(w):
    danh_sach_khoa_con = []
    # Sinh 25 khóa con K0 đến K24
    for r in range(25):
        chi_so_sbox = (3 - r) % 8
        # Lấy 4 từ tiếp theo từ w8 trở đi là lấy từ mở rộng trở đi
        bon_tu = [w[8 + 4 * r], w[8 + 4 * r + 1], w[8 + 4 * r + 2], w[8 + 4 * r + 3]]
        # K_r = S_(3-r mod 8)(w_(4r), w_(4r+1), w_(4r+2), w_(4r+3))
        khoa_con = sbox(chi_so_sbox, bon_tu)
        danh_sach_khoa_con.append(khoa_con)
    return danh_sach_khoa_con


def key_setup(khoa_dau_vao):
    # Hàm tổng hợp toàn bộ quy trình key setup
    khoa_dem = dem_khoa(khoa_dau_vao)
    cac_tu_8 = chia_thanh_8_tu(khoa_dem)
    w_mo_rong = mo_rong_khoa(cac_tu_8)
    cac_khoa_con = tao_25_khoa_con(w_mo_rong)
    return cac_khoa_con
