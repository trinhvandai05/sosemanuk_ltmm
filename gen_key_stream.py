#gen_key_stream.py
from smath import sbox
def gen_key_stream(f_tu, s_tu):
   #biến FSM(f1, f2, f3, f4) thanh Serpent1(sbox s2)
   f_sau_box = sbox(2, f_tu)
   #Tạo keystream bằng cách XOR giữa f_sau_box và s_tu
   keystream = [f^s for f, s in zip(f_sau_box, s_tu[:4])]
   return keystream