[app]
title = Oussama Sat Pro AI
package.name = oussamasat
package.domain = org.oussama
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 1.0

# Bibliothèques requises pour l'exécution
requirements = python3,kivy==2.2.1,kivymd==1.1.1,pyserial,plyer,usb4a,usbserial4a

orientation = portrait
android.permissions = WRITE_EXTERNAL_STORAGE, READ_EXTERNAL_STORAGE, USB_PERMISSION
android.api = 31
android.minapi = 21
android.sdk = 31
android.ndk = 23b
android.archs = armeabi-v7a, arm64-v8a

# Activation de la fonctionnalité d'accès USB Host
android.meta_data = android.hardware.usb.host=true
p4a.branch = master
