
# ---------------------------------------------------------------- DỮ LIỆU
# List lồng nhau: thư viện là list, mỗi phần tử là 1 list đại diện cho 1 sách
thu_vien = [
    [1, "Dế Mèn Phiêu Lưu Ký", "Tô Hoài", 45000, 5],
    [2, "Lập Trình Python Cơ Bản", "Teky", 120000, 3],
    [3, "Số Đỏ", "Vũ Trọng Phụng", 68000, 2],
    [4, "Nhà Giả Kim", "Paulo Coelho", 79000, 0],
]

# Chỉ số các cột (để code dễ đọc hơn)
MA, TEN, TAC_GIA, GIA, SO_LUONG = 0, 1, 2, 3, 4


# ---------------------------------------------------------------- HÀM TIỆN ÍCH
def dinh_dang_tien(so_tien):
    """Đổi 120000 -> '120,000 đ'."""
    return "{:,} đ".format(so_tien)


def nhap_so_nguyen(thong_bao, nho_nhat=0):
    """Nhập số nguyên >= nho_nhat. Nhập sai thì bắt nhập lại (vòng lặp while)."""
    while True:
        chuoi = input(thong_bao).strip()
        if not chuoi.isdigit():                      # xử lý chuỗi
            print("  [!] Vui lòng nhập một số nguyên không âm.")
            continue                                 # continue: quay lại đầu vòng lặp
        so = int(chuoi)                              # ép kiểu str -> int
        if so < nho_nhat:
            print("  [!] Giá trị phải từ", nho_nhat, "trở lên.")
        else:
            return so


def tim_sach_theo_ma(ma):
    """Trả về cuốn sách (list) có mã = ma, không có thì trả về None."""
    for sach in thu_vien:
        if sach[MA] == ma:
            return sach
    return None


def tao_ma_moi():
    """Mã mới = mã lớn nhất hiện có + 1."""
    ma_lon_nhat = 0
    for sach in thu_vien:
        if sach[MA] > ma_lon_nhat:
            ma_lon_nhat = sach[MA]
    return ma_lon_nhat + 1


# ---------------------------------------------------------------- CHỨC NĂNG 1
def hien_thi_danh_sach():
    print("\n" + "=" * 78)
    print("{:^78}".format("DANH SÁCH SÁCH TRONG THƯ VIỆN"))
    print("=" * 78)

    if len(thu_vien) == 0:
        print("Thư viện đang trống.")
        return

    print("{:<4} {:<28} {:<18} {:>12} {:>9}".format(
        "Mã", "Tên sách", "Tác giả", "Giá", "Còn lại"))
    print("-" * 78)

    tong_dau_sach = 0
    tong_so_cuon = 0
    for sach in thu_vien:
        trang_thai = str(sach[SO_LUONG])
        if sach[SO_LUONG] == 0:
            trang_thai = "Hết"
        print("{:<4} {:<28} {:<18} {:>12} {:>9}".format(
            sach[MA], sach[TEN], sach[TAC_GIA],
            dinh_dang_tien(sach[GIA]), trang_thai))
        tong_dau_sach += 1
        tong_so_cuon += sach[SO_LUONG]

    print("-" * 78)
    print("Tổng:", tong_dau_sach, "đầu sách |", tong_so_cuon, "cuốn trong kho")


# ---------------------------------------------------------------- CHỨC NĂNG 2
def them_sach():
    print("\n--- THÊM SÁCH MỚI ---")

    ten = input("Tên sách: ").strip().title()
    if ten == "":
        print("  [!] Tên sách không được để trống. Huỷ thao tác.")
        return

    tac_gia = input("Tác giả: ").strip().title()
    if tac_gia == "":
        tac_gia = "Không rõ"

    # Nếu sách đã tồn tại (cùng tên, không phân biệt hoa thường) -> cộng thêm số lượng
    for sach in thu_vien:
        if sach[TEN].lower() == ten.lower():
            so_them = nhap_so_nguyen("Sách đã có trong kho. Nhập số lượng thêm: ", 1)
            sach[SO_LUONG] += so_them
            print("  => Đã cộng thêm", so_them, "cuốn. Hiện có:", sach[SO_LUONG])
            return

    gia = nhap_so_nguyen("Giá (đồng): ", 0)
    so_luong = nhap_so_nguyen("Số lượng: ", 1)

    sach_moi = [tao_ma_moi(), ten, tac_gia, gia, so_luong]
    thu_vien.append(sach_moi)                        # thêm list con vào list lớn
    print("  => Đã thêm sách '{}' (mã {}).".format(ten, sach_moi[MA]))


# ---------------------------------------------------------------- CHỨC NĂNG 3
def thanh_toan():
    print("\n--- THANH TOÁN ---")
    hien_thi_danh_sach()

    gio_hang = []        # list lồng nhau: [[mã, tên, số lượng, đơn giá, thành tiền], ...]

    # Vòng lặp chọn sách cho đến khi người dùng nhập 0
    while True:
        ma = nhap_so_nguyen("\nNhập mã sách muốn mua (0 = xong): ", 0)
        if ma == 0:
            break

        sach = tim_sach_theo_ma(ma)
        if sach is None:
            print("  [!] Không có sách mã", ma)
            continue

        # Số lượng còn lại phải trừ đi phần đã đặt trong giỏ
        da_dat = 0
        for dong in gio_hang:
            if dong[0] == ma:
                da_dat += dong[2]
        con_lai = sach[SO_LUONG] - da_dat

        if con_lai <= 0:
            print("  [!] Sách '{}' đã hết hàng.".format(sach[TEN]))
            continue

        so_luong = nhap_so_nguyen("Số lượng (còn {}): ".format(con_lai), 1)
        if so_luong > con_lai:
            print("  [!] Không đủ hàng, chỉ còn", con_lai, "cuốn.")
            continue

        # Nếu đã có trong giỏ thì cộng dồn, chưa có thì thêm dòng mới
        da_co = False
        for dong in gio_hang:
            if dong[0] == ma:
                dong[2] += so_luong
                dong[4] = dong[2] * dong[3]
                da_co = True
                break
        if not da_co:
            gio_hang.append([ma, sach[TEN], so_luong, sach[GIA], so_luong * sach[GIA]])
        print("  => Đã thêm vào giỏ:", sach[TEN], "x", so_luong)

    if len(gio_hang) == 0:
        print("Giỏ hàng trống, huỷ thanh toán.")
        return

    # ---- Tính tiền
    tong = 0
    tong_so_cuon = 0
    for dong in gio_hang:
        tong += dong[4]
        tong_so_cuon += dong[2]

    giam_gia = 0
    # if - elif - else: chiết khấu theo số lượng sách
    if tong_so_cuon >= 10:
        giam_gia = tong * 15 // 100
    elif tong_so_cuon >= 5:
        giam_gia = tong * 10 // 100
    elif tong_so_cuon >= 3:
        giam_gia = tong * 5 // 100
    phai_tra = tong - giam_gia

    print("\n" + "=" * 62)
    print("{:^62}".format("HOÁ ĐƠN"))
    print("=" * 62)
    print("{:<28} {:>4} {:>13} {:>14}".format("Tên sách", "SL", "Đơn giá", "Thành tiền"))
    print("-" * 62)
    for dong in gio_hang:
        print("{:<28} {:>4} {:>13} {:>14}".format(
            dong[1], dong[2], dinh_dang_tien(dong[3]), dinh_dang_tien(dong[4])))
    print("-" * 62)
    print("{:<47} {:>14}".format("Tạm tính:", dinh_dang_tien(tong)))
    print("{:<47} {:>14}".format("Giảm giá:", "-" + dinh_dang_tien(giam_gia)))
    print("{:<47} {:>14}".format("PHẢI TRẢ:", dinh_dang_tien(phai_tra)))
    print("=" * 62)

    xac_nhan = input("Xác nhận thanh toán? (c/k): ").strip().lower()
    if xac_nhan != "c":
        print("Đã huỷ thanh toán. Kho sách không thay đổi.")
        return

    # Nhập tiền khách đưa; nếu thiếu thì bắt nhập lại hoặc thoát (break)
    while True:
        khach_dua = nhap_so_nguyen("Tiền khách đưa (0 = huỷ): ", 0)
        if khach_dua == 0:
            print("Đã huỷ thanh toán. Kho sách không thay đổi.")
            return
        if khach_dua < phai_tra:
            print("  [!] Còn thiếu", dinh_dang_tien(phai_tra - khach_dua))
        else:
            break

    # Trừ kho
    for dong in gio_hang:
        sach = tim_sach_theo_ma(dong[0])
        sach[SO_LUONG] -= dong[2]

    print("\nThanh toán thành công!")
    print("Tiền thừa trả khách:", dinh_dang_tien(khach_dua - phai_tra))
    print("Cảm ơn quý khách!")


# ---------------------------------------------------------------- MENU CHÍNH
def hien_thi_menu():
    print("\n" + "*" * 40)
    print("{:^40}".format("QUẢN LÝ THƯ VIỆN"))
    print("*" * 40)
    print("  1. Hiển thị danh sách sách")
    print("  2. Thêm sách")
    print("  3. Thanh toán")
    print("  0. Thoát")
    print("*" * 40)


def main():
    while True:                                      # vòng lặp menu
        hien_thi_menu()
        lua_chon = input("Chọn chức năng: ").strip()

        if lua_chon == "1":
            hien_thi_danh_sach()
        elif lua_chon == "2":
            them_sach()
        elif lua_chon == "3":
            thanh_toan()
        elif lua_chon == "0":
            print("Tạm biệt!")
            break                                    # thoát vòng lặp
        else:
            print("  [!] Lựa chọn không hợp lệ, vui lòng chọn 0-3.")


main()