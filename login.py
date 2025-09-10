# login.py - ورود به اینستاگرام
from instagrapi import Client

cl = Client()
try:
    cl.login("Par3a._.rahnama", "Peyman4311319452")
    cl.dump_settings("session.json")
    print("✅ ورود موفق! فایل session.json ساخته شد.")
except Exception as e:
    print(f"❌ خطا در ورود: {e}")