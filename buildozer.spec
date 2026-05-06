[app]
# (str) Title of your application
title = OussamaSat

# (str) Package name
package.name = oussamasat

# (str) Package domain (needed for android packaging)
package.domain = org.oussama

# (str) Source code where the main.py live
source.dir = .

# (list) Source files to include (let empty to include all the files)
source.include_exts = py,png,jpg,kv,atlas

# (list) Application requirements
# تمت إضافة المتطلبات التي طلبتها بدقة لضمان التوافق
requirements = python3, kivy==2.2.1, kivymd==1.1.1, pyserial, plyer, usb4a, usbserial4a

# (str) Supported orientation (one of landscape, sensorLandscape, portrait or all)
orientation = portrait

# ----------------------------------
# Android specific
# ----------------------------------

# (int) Target Android API, should be as high as possible.
# الـ API 31 هو الأكثر استقراراً لتعريفات الـ USB
android.api = 31

# (int) Minimum API your APK will support.
android.minapi = 21

# (str) Android NDK version to use
# النسخة 25b هي المطلوبة لتوافق المكتبات الحديثة
android.ndk = 25b

# (bool) Use --private data storage (True) or --dir public storage (False)
android.private_storage = True

# (bool) Accept SDK license agreement
# تخطي الموافقة اليدوية لتسريع البناء في GitHub و Termux
android.accept_sdk_license = True

# (str) Android architectures to build for
android.archs = arm64-v8a, armeabi-v7a

# (list) Permissions
android.permissions = INTERNET, USB_PERMISSION, READ_EXTERNAL_STORAGE, WRITE_EXTERNAL_STORAGE

# (list) Meta-data to include in AndroidManifest.xml
# هذا السطر ضروري جداً لكي يتعرف التطبيق على الـ USB Host لمشروعك
android.meta_data = android.hardware.usb.host=true

# (str) The Android arch to build for
android.arch = arm64-v8a

[buildozer]
# (int) Log level (0 = error only, 1 = info, 2 = debug (with command output))
log_level = 2

# (int) Display warning if buildozer is run as root (0 = off, 1 = on)
warn_on_root = 1
