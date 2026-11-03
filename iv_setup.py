# iv_setup.py - Vũ Trung Hiếu
# Nhiệm vụ: Lấy đầu ra từ key_setup (25 khóa con K0..K24) và IV để gán giá trị khởi tạo cho thanh ghi LFSR và FSM

from smath import sbox, LT


def chuyen_iv_thanh_4_tu(iv_dau_vao):
    # Nếu đầu vào là chuỗi hex thì đổi ra bytes cho dễ dùng
    if isinstance(iv_dau_vao, str):
        iv_bytes = bytes.fromhex(iv_dau_vao)
    else:
        iv_bytes = bytes(iv_dau_vao)

    # Đề bài quy định IV 128 bit tức là đúng 16 byte, khác 16 byte thì ném ra lỗi luôn
    if len(iv_bytes) != 16:
        raise ValueError("IV bắt buộc phải có đúng 16 byte (128 bit)")

    # Cắt 16 byte ra làm 4 từ (mỗi từ 4 byte) theo kiểu little endian (đảo từ dưới lên)
    # sẽ ra 4 từ x0, x1, x2, x3 chính là trạng thái Y0 ban đầu
    cac_tu = []
    for i in range(4):
        doan_4_byte = iv_bytes[i * 4 : (i + 1) * 4]
        tu = int.from_bytes(doan_4_byte, "little")
        cac_tu.append(tu)

    return cac_tu


def chay_serpent_24_vong(iv_4_tu, danh_sach_khoa_con):
    # Phải đủ 25 khóa con từ K0 đến K24 mới chạy được 24 vòng Serpent
    if len(danh_sach_khoa_con) != 25:
        raise ValueError("Cần đúng 25 khóa con để chạy Serpent-24")

    trang_thai = list(iv_4_tu)
    vong_12 = None
    vong_18 = None
    vong_24 = None

    # Chạy lặp 24 vòng từ vòng r = 0 đến 23
    for r in range(24):
        # 1. Key mixing: Lấy 4 từ trạng thái XOR với khóa con K_r tương ứng của vòng đấy
        khoa_r = danh_sach_khoa_con[r]
        for i in range(4):
            trang_thai[i] = trang_thai[i] ^ khoa_r[i]

        # 2. Thay thế qua hộp S-box (chọn S_box theo công thức r % 8)
        chi_so_sbox = r % 8
        trang_thai = sbox(chi_so_sbox, trang_thai)

        # 3. Biến đổi tuyến tính LT (trộn các bit và xoay bit)
        trang_thai = LT(trang_thai)

        # Đề bài bảo cần kết quả ở vòng 12 và vòng 18 nên thấy đến vòng đấy là lưu lại luôn
        if r + 1 == 12:
            vong_12 = list(trang_thai)
        elif r + 1 == 18:
            vong_18 = list(trang_thai)

    # Riêng vòng 24: Sau khi qua LT xong thì phải XOR thêm 1 lần nữa với khóa con cuối K24
    # (cái này là quy ước chuẩn của Serpent / Sosemanuk)
    khoa_24 = danh_sach_khoa_con[24]
    for i in range(4):
        trang_thai[i] = trang_thai[i] ^ khoa_24[i]
    vong_24 = list(trang_thai)

    return vong_12, vong_18, vong_24


def iv_setup(iv_dau_vao, danh_sach_khoa_con):
    # Bước 1: Đổi IV ban đầu thành 4 từ 32 bit (x0, x1, x2, x3)
    iv_4_tu = chuyen_iv_thanh_4_tu(iv_dau_vao)

    # Bước 2: Cho chạy 24 vòng Serpent để lấy 3 mốc Y12, Y18, Y24
    y12, y18, y24 = chay_serpent_24_vong(iv_4_tu, danh_sach_khoa_con)

    # Bước 3 & 4: Nhét các giá trị vào 10 thanh ghi LFSR (từ s1 đến s10)
    # - Vòng 24 nhét ngược: y3, y2, y1, y0 vào s1, s2, s3, s4
    # - Vòng 18 nhét: y1, y3 vào s5, s6
    # - Vòng 12 nhét ngược: y3, y2, y1, y0 vào s7, s8, s9, s10
    thanh_ghi_lfsr = [
        y24[3], y24[2], y24[1], y24[0],
        y18[1], y18[3],
        y12[3], y12[2], y12[1], y12[0]
    ]

    # Bước 5: Hai giá trị còn sót lại của vòng 18 thì đem gán cho 2 thanh ghi FSM
    # R1 lấy y0 của vòng 18
    # R2 lấy y2 của vòng 18
    r1 = y18[0]
    r2 = y18[2]
    thanh_ghi_fsm = [r1, r2]

    # Xong thì trả về cả 2 bộ để tí các bạn làm LFSR và FSM chỉ việc lấy dùng
    return thanh_ghi_lfsr, thanh_ghi_fsm
