[app]
# (section) Informations générales
title = OUSSAMA SAT PRO AI
package.name = oussamasat
package.domain = org.oussama
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 1.0

# (Correction) Fixation de Cython à 0.29.33 pour éviter les erreurs de compilation
requirements = python3, kivy==2.2.1, kivymd==1.1.1, pyserial, plyer, usb4a, usbserial4a, cython==0.29.33

orientation = portrait

# (section) Permissions Android
android.permissions = WRITE_EXTERNAL_STORAGE, READ_EXTERNAL_STORAGE, USB_PERMISSION, INTERNET

# (Correction) Suppression de android.sdk pour éviter le conflit "deprecated"
# On utilise uniquement android.api pour piloter le build
android.api = 33
android.minapi = 21
android.ndk = 25b

# Support des architectures modernes (32 et 64 bits)
android.archs = armeabi-v7a, arm64-v8a

# (section) Configuration USB Host pour le câble OTG
android.meta_data = android.hardware.usb.host=true

# Utilisation de la branche master pour python-for-android
p4a.branch = master

[buildozer]
log_level = 2
warn_on_root = 1
