# 🛒 Odoo-based Retail Fashion Management Solution

<div align="center">

**Bộ addon Odoo 18 cho bán lẻ thời trang – Giao diện gọn, Kiểm tra tồn kho, Quick checkout**

[![Odoo](https://img.shields.io/badge/Odoo-18.0-875A7B?style=flat&logo=odoo)](https://www.odoo.com/)
[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat&logo=python)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-LGPL--3-green?style=flat)](https://www.gnu.org/licenses/lgpl-3.0)

[Giới thiệu](#-giới-thiệu) •
[Tính năng](#-tính-năng) •
[Tech Stack](#️-tech-stack) •
[Cài đặt & Sử dụng](#-cài-đặt--sử-dụng) •
[Cấu trúc dự án](#-cấu-trúc-dự-án) •
[License](#-license)

</div>

---

## 📖 Giới thiệu

**Odoo-based Retail Fashion Management Solution** là bộ addon Odoo 18 phục vụ quản lý bán lẻ thời trang tại quầy (counter retail):

- 🛍️ **Quick checkout** – Đặt hàng nhanh, giao hàng & hóa đơn xử lý sau
- 📦 **Kiểm tra tồn kho** – Chặn xác nhận đơn khi vượt tồn, cảnh báo ngay trên dòng đơn
- 🖥️ **Giao diện gọn** – Sales Order và Contact đơn giản, phù hợp nhân viên bán hàng
- 🏪 **Một kho, không thuế** – Tối ưu cho mô hình cửa hàng thời trang đơn giản

---

## 🎯 Mục tiêu dự án

### Mục tiêu chính

- **Tăng tốc bán tại quầy:** Form đơn hàng và khách hàng chỉ giữ trường cần thiết, ẩn bớt tính năng nâng cao (pricelist, thuế, analytic…).
- **Tránh bán vượt tồn:** Kiểm tra tồn kho theo warehouse trước khi confirm; hiển thị cột "In Stock" và onchange giới hạn số lượng.
- **Trải nghiệm rõ ràng:** Thông báo lỗi và cảnh báo bằng tiếng Việt.

### Đối tượng sử dụng

- **Nhân viên bán hàng** – Tạo và xác nhận đơn nhanh, thấy tồn kho ngay trên đơn
- **Quản lý bán hàng** – Vẫn truy cập pricelist và tab "Other Info" khi cần

---

## ✨ Tính năng

### 📦 Module 1: Sale Quick Checkout (`sale_quick_checkout`)

- **Kiểm tra tồn khi xác nhận đơn**
  - Mọi dòng hàng hóa (Product/Consumable) phải có số lượng ≤ tồn kho tại kho bán
  - Bỏ qua dòng dịch vụ (Service)
  - Nếu thiếu tồn hoặc số lượng ≤ 0 → chặn confirm và báo lỗi tiếng Việt
- **Cột "In Stock" (Tồn kho)** trên dòng đơn bán (readonly, optional show)
- **Onchange UX**
  - Chọn sản phẩm → cập nhật tồn; nếu hết hàng thì đặt qty = 0 (không popup ngay)
  - Sửa số lượng vượt tồn → tự giới hạn theo tồn + cảnh báo "Không đủ tồn kho"
- **View:** Khóa ngày đơn (readonly), ẩn ngày hết hạn báo giá (Validity Date)

### 🖥️ Module 2: GR2 Lean Sales UI (`gr2_lean_ui`)

**Sales Order**

- **Quyền:** Pricelist và tab "Other Info" chỉ hiển thị cho **Sales Manager**
- **Dòng đơn ẩn:** Mô tả dòng, Analytic, Delivered/Invoiced, UoM, Customer lead, Packaging, Discount, Thuế

**Contact (Partner)**

- **Chỉ hiển thị:** Tên, Địa chỉ (Street, City), Điện thoại
- **Ẩn:** Email, Mobile, Website, Mã số thuế, Tags, Ghi chú, Công ty cha, Chức vụ, Xưng hô, Ngôn ngữ, Street2, ZIP, Tỉnh/thành, Quốc gia, Avatar, Loại công ty, Is Company
- **Chuẩn bị mở rộng:** Trường Ngày sinh (Birthdate) – đã có trong view, đang comment; cần bật field trong `res_partner.py` và nâng cấp module để tạo cột DB

---

## 🛠️ Tech Stack

| Thành phần   | Công nghệ        | Ghi chú                    |
|-------------|------------------|----------------------------|
| **Platform** | Odoo 18.0        | Community / Enterprise     |
| **Language** | Python 3.10+     | Backend logic              |
| **View**    | XML              | Inherit view, xpath        |
| **Depends** | sale, stock, account, contacts | Theo từng module |

---

## 🚀 Cài đặt & Sử dụng

### Yêu cầu

| Công cụ    | Phiên bản  | Ghi chú              |
|-----------|------------|----------------------|
| **Odoo**  | 18.0       | Đã cài sẵn           |
| **Python**| 3.10+      | Theo Odoo 18         |

### Cài đặt

**Bước 1: Đặt addons vào thư mục addons**

- Copy cả thư mục `codenew` vào thư mục addons của Odoo 18 (ví dụ: `odoo-18.0/addons/codenew`).
- Đảm bảo đường dẫn addons có chứa `codenew` (cấu hình `addons_path` trong Odoo nếu cần).

**Bước 2: Cập nhật danh sách ứng dụng**

- Vào **Apps** → **Update Apps List**.

**Bước 3: Cài từng module**

- **GR2 Lean Sales UI** (`gr2_lean_ui`) – nên cài trước nếu dùng chung giao diện gọn.
- **Sale Quick Checkout** (`sale_quick_checkout`) – phụ thuộc: `sale_management`, `stock`, `account`, `contacts`.

### Hướng dẫn sử dụng nhanh

1. **Tạo đơn bán (Sales Order)**  
   Vào Sales → Tạo báo giá/đơn hàng mới. Form gọn (Lean UI): ít cột, ít tab hơn cho nhân viên.

2. **Xem tồn kho trên đơn (khi đã cài Sale Quick Checkout)**  
   Trên dòng đơn, bật cột **In Stock** (optional) để xem tồn tại kho. Chọn sản phẩm → tồn tự cập nhật; nhập số lượng > tồn sẽ bị giới hạn và cảnh báo.

3. **Xác nhận đơn**  
   Click **Confirm**. Nếu có dòng vượt tồn hoặc qty ≤ 0 → hệ thống chặn và báo lỗi tiếng Việt.

4. **Quản lý khách hàng (Contact)**  
   Form Contact gọn: chỉ Tên, Địa chỉ (Street, City), Điện thoại (và sau này có thể bật thêm Ngày sinh).

### Lưu ý

- **Sale Quick Checkout** tính tồn theo warehouse của đơn hàng (hoặc warehouse mặc định của công ty). Đảm bảo sản phẩm và kho đã cấu hình đúng.
- Dòng **dịch vụ** không kiểm tra tồn kho.

---

## 📁 Cấu trúc dự án

```
codenew/
├── sale_quick_checkout/          # Quick checkout & kiểm tra tồn kho
│   ├── __manifest__.py
│   ├── __init__.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── sale_order.py         # Kiểm tra tồn khi confirm
│   │   └── sale_order_line.py    # available_qty, onchange
│   └── views/
│       └── sale_order_views.xml  # Cột In Stock, khóa ngày, ẩn validity
│
├── gr2_lean_ui/                  # Giao diện gọn Sales Order & Partner
│   ├── __manifest__.py
│   ├── __init__.py
│   ├── models/
│   │   ├── __init__.py
│   │   └── res_partner.py        # (Chuẩn bị birthdate)
│   └── views/
│       ├── sale_lean_order_views.xml   # Ẩn pricelist/tab/columns
│       └── partner_lean_views.xml     # Form Contact gọn
│
└── README.md
```

---

## 📄 License

Dự án sử dụng **LGPL-3**. Xem file [LICENSE](LICENSE) nếu có.

---

## 👤 Tác giả

**Bùi Hà My**

---

<div align="center">

**Made with ❤️ – Odoo-based Retail Fashion Management Solution**

</div>
# Odoo-based-Retail-Fashion-Management-Solution
