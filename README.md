# sosemanuk_ltmm
mô phỏng lại mã dòng sosemanuk

# Thông tin nhóm
Nhóm 9 - Trịnh Văn Đại | Vũ Trung Hiếu | Ngô Thùy Linh | Nguyễn Công Hùng | Lê Hoàng Long | Đỗ Thành Long

# Cơ sở lý thuyết
## Mô tả
Sosemanuk là mã dòng được thiết kế để bảo vệ dữ liệu bằng mật mã học. Nhận khóa bí mật key và giá trị khởi tạo iv để sinh key stream

## Quá trình tìm hiểu
  <sau chèn ảnh vào>

# Phân công và báo cáo nhiệm vụ
1. math.py
   Trịnh Văn Đại thực hiện cung cấp các hàm cần sử dụng trong từng giai đoạn ứng với quá trình tìm hiểu
2. key_setup.py
   Vũ Trung Hiếu
   Từ key đầu vào sinh 25 key con đầu ra
3. iv_setup.py
   Từ đầu ra của key_setup tiến hành gán thanh ghi
4. LFSR.py
   Từ 320 + 64 bit đầu ra của iv_setup trả ra s1->s4 và s5-s14
5. FSM.py
   Ngô Thùy Linh
   Từ 320 + 64 bit đầu ra của iv_setup trả ra f1->f4
7. gen_key_stream.py
   Từ đầu ra FSM.py và LFSR.py trả về key stream
8. Folder test
   Yêu cầu thành viên nào code gì thì test trực tiếp ở đây, minh chứng cập nhật bằng file .tex
   Khi hoàn thành code yêu cầu test toàn bộ chương trình
   Tạo 2 bộ benchmark, 1 bộ do sinh viên tự tính tay 1 bộ sử dụng benchmark trên mạng
   ví dụ: test_math.py test chức năng của từng hàm con, key_setup.pt test cả hàm con và full chương trình
   
   
   
