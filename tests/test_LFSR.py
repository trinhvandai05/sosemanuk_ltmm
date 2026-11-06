from LFSR import lfsr_step
print("========== TEST LFSR ==========")

# 10 thanh ghi ban dau
cac_thanh_ghi = [
    0x12345678,
    0x23456789,
    0x3456789A,
    0x456789AB,
    0x56789ABC,
    0x6789ABCD,
    0x789ABCDE,
    0x89ABCDEF,
    0x9ABCDEF0,
    0xABCDEF01
]

# Gia tri moi mong doi
ket_qua_mong_doi = 0xA5035046
# Goi ham LFSR
ket_qua_thuc_te = lfsr_step(cac_thanh_ghi)

print("Ket qua mong doi:", hex(ket_qua_mong_doi))
print("Ket qua thuc te :", hex(ket_qua_thuc_te))
