[app]
title = OUSSAMA SAT PRO AI
package.name = oussamasat
package.domain = org.oussama
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 1.0

# Bibliothèques nécessaires pour l'USB et l'interface
requirements = python3,kivy==2.2.1,kivymd==1.1.1,pyserial,plyer,usb4a,usbserial4a

orientation = portrait
android.permissions = WRITE_EXTERNAL_STORAGE, READ_EXTERNAL_STORAGE, USB_PERMISSION, INTERNET

# Configuration pour éviter l'erreur NDK sur GitHub Actions
android.api = 33
android.minapi = 21
android.sdk = 33
android.ndk = 25b
android.archs = armeabi-v7a, arm64-v8a

# Activation du mode USB Host pour le câble OTG
android.meta_data = android.hardware.usb.host=true
p4a.branch = master

[buildozer]
log_level = 2
warn_on_root = 1
