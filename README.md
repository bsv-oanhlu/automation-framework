# SauceDemo Automation Framework (Python)

Framework automation test cho [SauceDemo](https://www.saucedemo.com), sử dụng **Playwright + pytest**, áp dụng **Page Object Model (POM)**.

## Cấu trúc POM

```
automation-framework/
├── playwright.config.py        # Cấu hình Playwright (baseURL, timeout, browsers)
├── config/
│   ├── settings.py             # Giá trị cấu hình
│   └── playwright.py           # Cấu hình runtime Playwright
├── locators/                   # Định nghĩa locator (tách khỏi logic)
│   ├── common_locators.py
│   ├── login_locators.py
│   ├── inventory_locators.py
│   ├── cart_locators.py
│   ├── product_detail_locators.py
│   └── checkout_locators.py
├── components/                 # UI component tái sử dụng
│   ├── header.py               # Giỏ hàng, badge
│   └── sidebar.py              # Menu, logout, reset
├── pages/                      # Page Objects — hành động UI
│   ├── base_page.py
│   ├── login_page.py
│   ├── inventory_page.py
│   ├── product_detail_page.py
│   ├── cart_page.py
│   ├── checkout_info_page.py
│   ├── checkout_overview_page.py
│   └── checkout_complete_page.py
├── data/                       # Dữ liệu test
│   ├── loader.py
│   ├── users.json
│   ├── users.csv
│   ├── products.json
│   └── checkout.json
├── workflows/                  # Luồng nghiệp vụ (chuẩn bị dữ liệu test)
│   ├── auth_workflow.py
│   └── checkout_workflow.py
├── tests/                      # Test cases (không chứa locator)
│   ├── login/
│   │   └── test_login.py       # 9 TC
│   ├── product/
│   │   ├── test_inventory.py   # 11 TC
│   │   └── test_product_detail.py  # 6 TC
│   ├── cart/
│   │   └── test_cart.py        # 6 TC
│   └── checkout/
│       ├── test_checkout_info.py      # 6 TC
│       ├── test_checkout_overview.py  # 5 TC
│       └── test_checkout_complete.py  # 3 TC
├── conftest.py
├── pytest.ini
└── requirements.txt
```

**Tổng cộng: 46 test cases**

## Nguyên tắc POM

| Layer | Trách nhiệm |
|-------|-------------|
| **locators/** | Chứa selector CSS/data-test — một nơi duy nhất |
| **components/** | Hành vi UI dùng chung (header, sidebar) |
| **pages/** | Mỗi màn hình = 1 class, kế thừa `BasePage` |
| **workflows/** | Chuỗi bước nghiệp vụ (login → add cart → checkout) |
| **tests/** | Mô tả hành vi, gọi page/workflow, assert kết quả — **không viết locator** |

## Cài đặt

```bash
cd automation-framework
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
playwright install
```

## Cách chạy test

> **Lưu ý:** `pages/` chứa **Page Object** (code UI), **không phải** file test.  
> File test nằm trong `tests/` — luôn chạy pytest trỏ vào thư mục/file trong `tests/`.

```bash
# Toàn bộ (46 TC × 3 browsers = 138 tests, chạy song song — có thể mất vài phút)
pytest

# Chạy nhanh hơn — chỉ 1 browser (46 tests)
pytest --browser chromium

# Có giao diện trình duyệt
pytest --headed --browser chromium
```

### Chạy theo màn hình / module

| Màn hình | Lệnh | File test | Số TC |
|----------|------|-----------|-------|
| Đăng nhập | `pytest tests/login/` | `tests/login/test_login.py` | 9 |
| Danh sách SP | `pytest tests/product/test_inventory.py` | `tests/product/test_inventory.py` | 11 |
| Chi tiết SP | `pytest tests/product/test_product_detail.py` | `tests/product/test_product_detail.py` | 6 |
| Giỏ hàng | `pytest tests/cart/` | `tests/cart/test_cart.py` | 6 |
| Checkout | `pytest tests/checkout/` | `tests/checkout/test_checkout_*.py` | 14 |

```bash
# Theo module
pytest tests/login/ -v
pytest tests/product/ -v
pytest tests/cart/ -v
pytest tests/checkout/ -v

# Chỉ Chromium (nhanh hơn)
pytest tests/cart/ --browser chromium
```

### Chạy 1 test case cụ thể

```bash
# Cú pháp: pytest <file_test>::<Class>::<tên_hàm_test>
pytest tests/login/test_login.py::TestLogin::test_tc02_login_success_standard_user
pytest tests/cart/test_cart.py::TestCart::test_tc01_display_cart_with_one_product
```

### Lọc theo tên test với `-k`

`-k` lọc theo **tên test**, không phải đường dẫn file.

```bash
# Đúng — lọc test có chữ "login" trong tên
pytest -k login --browser chromium

# Đúng — lọc test cart
pytest -k cart --browser chromium

# Sai — login_page.py là Page Object, không phải file test
# pytest -k tests/login_page.py
```

### Phân biệt `pages/` và `tests/`

```
pages/cart_page.py       → Page Object (locator + hành động UI)  ❌ không chạy pytest
tests/cart/test_cart.py  → Test case (assert kết quả)           ✅ chạy pytest ở đây
```

## Cấu hình Playwright

File `playwright.config.py` (chi tiết trong `config/playwright.py`):

| Thiết lập | Giá trị |
|-----------|---------|
| `baseURL` | `https://www.saucedemo.com` |
| `DEFAULT_TIMEOUT` | 30 giây |
| `EXPECT_TIMEOUT` | 10 giây |
| `NAVIGATION_TIMEOUT` | 15 giây |
| Chạy song song | `-n auto` (pytest-xdist) |
| Browsers | Chromium, Firefox, WebKit |

## Cách thêm Test Data

### Thêm dữ liệu JSON

1. Tạo hoặc chỉnh sửa file trong `data/`, ví dụ `users.json`:

```json
{
  "validUser": {
    "username": "standard_user",
    "password": "secret_sauce"
  }
}
```

2. Đọc trong test hoặc workflow:

```python
from data.loader import load_json

users = load_json("users.json")
products = load_json("products.json")
```

### Thêm dữ liệu CSV

1. Thêm dòng vào `data/users.csv`:

```csv
username,password,description
new_user,secret_sauce,New test user
```

2. Đọc bằng `load_csv` hoặc `get_user_from_csv`:

```python
from data.loader import get_user_from_csv

user = get_user_from_csv("New test user")
```

### Dùng trong workflow

```python
# workflows/auth_workflow.py
users = load_json("users.json")

def login_as_standard_user(page):
    login_page.login(users["validUser"]["username"], users["validUser"]["password"])
```

## Ví dụ POM

**Locator** (`locators/login_locators.py`):

```python
class LoginLocators:
    USERNAME = "#user-name"
    PASSWORD = "#password"
    LOGIN_BUTTON = "#login-button"
```

**Page Object** (`pages/login_page.py`):

```python
class LoginPage(BasePage):
    def login(self, username: str, password: str) -> None:
        self.username_input.fill(username)
        self.password_input.fill(password)
        self.login_button.click()
```

**Test** (`tests/login/test_login.py`):

```python
def test_login_success(self, page: Page):
    login_page = LoginPage(page)
    login_page.goto()
    login_page.login(users["validUser"]["username"], users["validUser"]["password"])
    inventory_page = login_page.wait_for_inventory_page()
    expect(inventory_page.page_title).to_have_text("Products")
```

Test **không** chứa selector như `#user-name` — tất cả nằm trong `locators/` và `pages/`.

## Best Practices

- **Test độc lập**: Mỗi test tự chuẩn bị dữ liệu qua `workflows/`, không phụ thuộc TC khác.
- **Smart Wait**: Dùng `expect(locator).to_be_visible()` và `page.wait_for_url()`, không dùng `wait_for_timeout()`.

## Thêm Page Object mới

1. Tạo `locators/<page>_locators.py` — định nghĩa selector
2. Tạo `pages/<page>_page.py` — kế thừa `BasePage`, dùng locator + hành động
3. Export trong `pages/__init__.py`
4. Viết test trong `tests/<module>/`
