[app]
title = Oussama Boot
package.name = oussama_boot
package.domain = org.oussama
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,json,txt
version = 3.0
requirements = python3,kivy==2.3.0,kivymd==2.0.1.dev0,pillow,plyer,requests,certifi
orientation = portrait
fullscreen = 0
presplash_color = #030712
android.permissions = INTERNET,READ_EXTERNAL_STORAGE,WRITE_EXTERNAL_STORAGE,USB_PERMISSION,MANAGE_USB
android.features = android.hardware.usb.host
android.api = 33
android.minapi = 26
android.sdk = 33
android.ndk = 25b
android.archs = arm64-v8a,armeabi-v7a
android.allow_backup = True
android.release_artifact = apk
[buildozer]
log_level = 2
warn_on_root = 1
