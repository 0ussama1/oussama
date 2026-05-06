[app]
title = OUSSAMA SAT PRO AI
package.name = oussamasat
package.domain = org.oussama
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 1.0

# تم حذف أرقام النسخ هنا لحل مشكلة فشل الـ toolchain الأخيرة
requirements = python3, kivy, kivymd, pyserial, plyer, usb4a, usbserial4a

orientation = portrait
android.permissions = INTERNET, WRITE_EXTERNAL_STORAGE, USB_PERMISSION

# استخدام API 31 (أندرويد 12) لضمان استقرار تعريفات الـ USB والـ OTG
android.api = 31
android.minapi = 21
android.ndk = 25b

android.archs = armeabi-v7a, arm64-v8a
android.meta_data = android.hardware.usb.host=true
p4a.branch = master

[buildozer]
log_level = 2
warn_on_root = 1
