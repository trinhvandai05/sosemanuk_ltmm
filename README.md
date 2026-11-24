# Trịnh Văn Đại - 20233298

Lookup table để tra bảng

des và aes là thuật toán

test case 

test_0_nhandathuc_gf (test_aes.TestAES128.test_0_nhandathuc_gf) ... ok
test_1_sinh_bang_s_box (test_aes.TestAES128.test_1_sinh_bang_s_box) ... ok
test_2_hang_so_vong_rcon (test_aes.TestAES128.test_2_hang_so_vong_rcon) ... ok
test_3_mix_columns (test_aes.TestAES128.test_3_mix_columns) ... ok
test_in_cac_buoc (test_aes.TestAES128.test_in_cac_buoc) ... 
=== MA HOA AES-128 ===
Ban ro: 0123456789abcdeffedcba9876543210
Khoa:   0f1571c947d9e8590cb7add6af7f6798
Vong  0: AddRoundKey (K0 = 0f1571c947d9e8590cb7add6af7f6798) -> State = 0e3634aece7225b6f26b174ed92b5588
Vong  1: SubBytes   = ab0518e48b403f4e897ff02f35f1fcc4
         ShiftRows  = ab40f0c48b7ffce489f1184e35053f2f
         MixColumns = b9e447c5948e20d657169af575513f3b
         AddKey(K01) = 657470750fc7ff3fc0e8e8ca4dd02a9c  (K01 = dc9037b09b49dfe997fe723f388115a7)
Vong  2: SubBytes   = 4d92519d76c61675ba9b9b74e370e5de
         ShiftRows  = 4dc69bde769be59dba705175e3921674
         MixColumns = 8eb2df2d22f280c5dbdcf71e1292c152
         AddKey(K02) = 5c7bb49a6b72349b05a2317ff46d1294  (K02 = d2c96bb74980b45ede7ec661e6ffd3c6)
Vong  3: SubBytes   = 4a218db87f4018146b3ac7d2bf3cc922
         ShiftRows  = 4a40c7227f3ac9b86b3c8d14bf2118d2
         MixColumns = b1baf91dc1f31f190b8b6a24cc07c35c
         AddKey(K03) = 7115262448dc747e5cdac7227da9bd9c  (K03 = c0afdf39892f6b675751ad06b1ae7ec0)
Vong  4: SubBytes   = a359f736528692f34a57c693ffd37ade
         ShiftRows  = a386c6de52577a364ad3f7f3ff599293
         MixColumns = d43bcb191144abb7fe0662070f7337ec
         AddKey(K04) = f867aee8b437a5210c24c1974cffeabc  (K04 = 2c5c65f1a5730e96f222a390438cdd50)
Vong  5: SubBytes   = 4185e49b8d9a06fdfe36788829168765
         ShiftRows  = 419a78658d36879bfe16e4fd29850688
         MixColumns = 2a8384eb47e81810c418270a48ba23f3
         AddKey(K05) = 721eb200ba06206dcbd4bce704fa654e  (K05 = 589d36ebfdee387d0fcc9bed4c4046bd)
Vong  6: SubBytes   = 40723763f46fb73c1f486594f22d4d2f
         ShiftRows  = 406f652ff4484d631f2d373cf272b794
         MixColumns = 7b1e949405d083c4422018434a4052fb
         AddKey(K06) = 0ad9d85689f9f77bc1c5f71185e5fb14  (K06 = 71c74cc28c2974bf83e5ef52cfa5a9ef)
Vong  7: SubBytes   = 673561b1a799682178a6688297d90ffa
         ShiftRows  = 679968faa7a60fb178d9612197356882
         MixColumns = ec0c3bb71a50d722c053007280c7efe0
         AddKey(K07) = db18a8ffa16d30d5f88b08d777ba4eaa  (K07 = 37149348bb3de7f738d808a5f77da14a)
Vong  8: SubBytes   = b9adc216323c0403413d300ef5f42fac
         ShiftRows  = b93c30ac323d2f1641f4c203f5ad040e
         MixColumns = b13d0a9f1a2f6b6844ec2ff317b642b1
         AddKey(K08) = f91b4fbfe934c9bf8f2f85812b084989  (K08 = 48264520f31ba2d7cbc3aa723cbe0b38)
Vong  9: SubBytes   = 99af84081e18dd087315970cf1303ba7
         ShiftRows  = 991897a71e153b0873308408f1afdd0c
         MixColumns = 31ac466a3071651c3a8c4831c2c4eb62
         AddKey(K09) = cca104a13e678500ff59025f3bafaa34  (K09 = fd0d42cb0e16e01cc5d54a6ef96b4156)
Vong 10: SubBytes   = 4b32f232b285976316cb77cfe279ac18
         ShiftRows  = 4b857718b2cbac321679f263e23297cf
         AddKey(K10)= ff0b844a0853bf7c6934ab4364148fb9  (K10 = b48ef352ba98134e7f4d592086261876)
Ban ma cuoi cung: ff0b844a0853bf7c6934ab4364148fb9
ok
test_toan_0 (test_aes.TestAES128.test_toan_0) ... ok
test_vi_du_1 (test_aes.TestAES128.test_vi_du_1) ... ok
test_vi_du_2 (test_aes.TestAES128.test_vi_du_2) ... ok
test_vong_1 (test_aes.TestAES128.test_vong_1) ... ok
