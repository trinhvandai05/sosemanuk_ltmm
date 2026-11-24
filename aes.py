# aes.py - Mã hóa và giải mã AES-128

from aes_tables import S_BOX, INV_S_BOX, RCON, nhandathuc


# đổi 16 byte thành ma trận state 4x4 theo cột
def bytes_sang_state(danh_sach_byte):
    state= [[0]*4 for _ in range(4)]
    for cot in range(4):
        for hang in range( 4 ):
            state[hang][cot] = danh_sach_byte[cot*4 + hang]
    return state


def state_sang_bytes(state):
    danh_sach_byte = [0]*16
    for cot in range(4):
        for hang in range(4):
            danh_sach_byte[cot*4+ hang]= state[hang][cot]
    return danh_sach_byte


def sub_bytes(state):
    for hang in range(4):
        for cot in range(4):
            state[hang][cot]= S_BOX[state[hang][cot]]

def inv_sub_bytes(state):
    for hang in range( 4 ):
        for cot in range(4):
            state[hang][cot] = INV_S_BOX[state[hang][cot]]


def shift_rows(state):
    state[1] = state[1][1:] +state[1][:1]
    state[2] = state[2][2:]+ state[2][:2]
    state[3] = state[3][3:]+state[3][:3]

def inv_shift_rows(state):
    state[1] = state[1][3:] + state[1][:3]
    state[2]= state[2][2:]+state[2][:2]
    state[3] = state[3][1:] +state[3][:1]


def mix_columns(state):
    for cot in range(4):
        a0 = state[0][cot]
        a1= state[1][cot]
        a2 = state[2][cot]
        a3= state[3][cot]

        state[0][cot] = nhandathuc(a0, 2, 8, 0x1B) ^ nhandathuc(a1, 3, 8, 0x1B) ^ a2 ^ a3
        state[1][cot]= a0 ^ nhandathuc(a1, 2, 8, 0x1B) ^ nhandathuc(a2, 3, 8, 0x1B) ^ a3
        state[2][cot] = a0 ^ a1 ^ nhandathuc(a2, 2, 8, 0x1B) ^ nhandathuc(a3, 3, 8, 0x1B)
        state[3][cot]= nhandathuc(a0, 3, 8, 0x1B) ^ a1 ^ a2 ^ nhandathuc(a3, 2, 8, 0x1B)


def inv_mix_columns(state):
    for cot in range( 4 ):
        a0= state[0][cot]
        a1 = state[1][cot]
        a2= state[2][cot]
        a3 = state[3][cot]

        state[0][cot] = (
            nhandathuc(a0, 14, 8, 0x1B) ^
            nhandathuc(a1, 11, 8, 0x1B) ^
            nhandathuc(a2, 13, 8, 0x1B) ^
            nhandathuc(a3, 9, 8, 0x1B)
        )
        state[1][cot]= (
            nhandathuc(a0, 9, 8, 0x1B) ^
            nhandathuc(a1, 14, 8, 0x1B) ^
            nhandathuc(a2, 11, 8, 0x1B) ^
            nhandathuc(a3, 13, 8, 0x1B)
        )
        state[2][cot] = (
            nhandathuc(a0, 13, 8, 0x1B) ^
            nhandathuc(a1, 9, 8, 0x1B) ^
            nhandathuc(a2, 14, 8, 0x1B) ^
            nhandathuc(a3, 11, 8, 0x1B)
        )
        state[3][cot]= (
            nhandathuc(a0, 11, 8, 0x1B) ^
            nhandathuc(a1, 13, 8, 0x1B) ^
            nhandathuc(a2, 9, 8, 0x1B) ^
            nhandathuc(a3, 14, 8, 0x1B)
        )


def add_round_key(state, khoa_vong):
    for hang in range(4):
        for cot in range(4):
            state[hang][cot] ^= khoa_vong[hang][cot]


def rot_word(w): return w[1:] + w[:1]

def sub_word(w): return [ S_BOX[b] for b in w ]


def mo_rong_khoa(khoa_16_byte):
    w = []
    for i in range(4):
        w.append([khoa_16_byte[4*i], khoa_16_byte[4*i + 1], khoa_16_byte[4*i+2], khoa_16_byte[4*i + 3]])

    for i in range(4, 44):
        temp= list(w[i - 1])
        if i % 4 ==0:
            temp = sub_word(rot_word(temp))
            temp[0] ^= RCON[i // 4][0]
        tu_moi = [w[i - 4][k] ^ temp[k] for k in range(4)]
        w.append(tu_moi)

    danh_sach_khoa_vong = []
    for vong in range(11):
        khoa_vong = [[0] * 4 for _ in range(4)]
        for cot in range(4):
            tu_cot = w[vong * 4 + cot]
            for hang in range(4):
                khoa_vong[hang][cot]= tu_cot[hang]
        danh_sach_khoa_vong.append(khoa_vong)

    return danh_sach_khoa_vong


def ma_hoa_aes_128(ban_ro_hex, khoa_hex, in_trang_thai=False):
    ban_ro_bytes = list(bytes.fromhex(ban_ro_hex))
    khoa_bytes= list(bytes.fromhex(khoa_hex))

    if in_trang_thai:
        print(f"\n=== MA HOA AES-128 ===")
        print(f"Ban ro: {ban_ro_hex}")
        print(f"Khoa:   {khoa_hex}")

    khoa_vong = mo_rong_khoa(khoa_bytes)
    state = bytes_sang_state(ban_ro_bytes)

    # Vòng 0
    add_round_key(state, khoa_vong[0])
    if in_trang_thai:
        s0 = bytes(state_sang_bytes(state)).hex()
        k0 = bytes(state_sang_bytes(khoa_vong[0])).hex()
        print(f"Vong  0: AddRoundKey (K0 = {k0}) -> State = {s0}")

    # Vòng 1 đến 9
    for vong in range(1, 10):
        sub_bytes(state)
        s_sub = bytes(state_sang_bytes(state)).hex() if in_trang_thai else ""

        shift_rows(state)
        s_shift = bytes(state_sang_bytes(state)).hex() if in_trang_thai else ""

        mix_columns(state)
        s_mix = bytes(state_sang_bytes(state)).hex() if in_trang_thai else ""

        add_round_key(state, khoa_vong[vong])
        s_add = bytes(state_sang_bytes(state)).hex() if in_trang_thai else ""

        if in_trang_thai:
            kv_hex = bytes(state_sang_bytes(khoa_vong[vong])).hex()
            print(f"Vong {vong:2d}: SubBytes   = {s_sub}")
            print(f"         ShiftRows  = {s_shift}")
            print(f"         MixColumns = {s_mix}")
            print(f"         AddKey(K{vong:02d}) = {s_add}  (K{vong:02d} = {kv_hex})")

    # Vòng 10 không có mix_columns
    sub_bytes(state)
    s_sub = bytes(state_sang_bytes(state)).hex() if in_trang_thai else ""

    shift_rows(state)
    s_shift = bytes(state_sang_bytes(state)).hex() if in_trang_thai else ""

    add_round_key(state, khoa_vong[10])
    s_add = bytes(state_sang_bytes(state)).hex() if in_trang_thai else ""

    if in_trang_thai:
        kv_hex = bytes(state_sang_bytes(khoa_vong[10])).hex()
        print(f"Vong 10: SubBytes   = {s_sub}")
        print(f"         ShiftRows  = {s_shift}")
        print(f"         AddKey(K10)= {s_add}  (K10 = {kv_hex})")

    ban_ma_bytes= state_sang_bytes(state)
    ban_ma = bytes(ban_ma_bytes).hex()
    if in_trang_thai:
        print(f"Ban ma cuoi cung: {ban_ma}")
    return ban_ma


def giai_ma_aes_128(ban_ma_hex, khoa_hex):
    ban_ma_bytes= list(bytes.fromhex(ban_ma_hex))
    khoa_bytes = list(bytes.fromhex(khoa_hex))

    khoa_vong = mo_rong_khoa(khoa_bytes)
    state = bytes_sang_state(ban_ma_bytes)

    add_round_key(state, khoa_vong[10])

    for vong in range(9, 0, -1):
        inv_shift_rows(state)
        inv_sub_bytes(state)
        add_round_key(state, khoa_vong[vong])
        inv_mix_columns(state)

    inv_shift_rows(state)
    inv_sub_bytes(state)
    add_round_key(state, khoa_vong[0])

    ban_ro_bytes = state_sang_bytes(state)
    return bytes(ban_ro_bytes).hex()
