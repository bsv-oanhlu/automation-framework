# SauceDemo Automation

Dự án automation test cho website [SauceDemo](https://www.saucedemo.com).

## Framework

Toàn bộ source code nằm trong thư mục [`automation-framework/`](./automation-framework/), sử dụng **Python + Playwright + pytest** với mô hình **Page Object Model (POM)**.

Xem [README](./automation-framework/README.md) để biết cấu trúc POM, cách cài đặt, chạy test theo từng màn hình.

```bash
cd automation-framework
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
playwright install

# Chạy nhanh — 1 browser
pytest --browser chromium

# Chạy test login
pytest tests/login/ --browser chromium

# Chạy test cart
pytest tests/cart/ --browser chromium
```
