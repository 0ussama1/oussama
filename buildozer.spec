[app]

# (str) Title of your application
title = OUSSAMA SAT PRO AI

# (str) Package name
package.name = oussamasat

# (str) Package domain (needed for android packaging)
package.domain = org.oussama

# (str) Source code where the main.py lives
source.dir = .

# (list) Source files to include (let empty to include all the files)
source.include_exts = py,png,jpg,kv,atlas

# (str) Application versioning
version = 1.0

# (list) Application requirements
# Les bibliothèques nécessaires pour le fonctionnement de l'USB et de l'interface
requirements = python3,kivy==2.2.1,kivymd==1.1.1,pyserial,plyer,usb4a,usbserial4a

# (str) Supported orientation
orientation = portrait

# (list) Permissions
# Autorisations nécessaires pour le stockage et l'accès USB OTG
android.permissions = WRITE_EXTERNAL_STORAGE, READ_EXTERNAL_STORAGE, USB_PERMISSION, INTERNET

# (int) Target Android API
# API 33 est requis pour la compatibilité avec GitHub Actions et Android moderne
android.api = 33

# (int) Minimum API your APK will support
android.minapi = 21

# (int) Android SDK version to use
android.sdk = 33

# (str) Android NDK version to use
# La version 25b corrige l'erreur rencontrée précédemment
android.ndk = 25b

# (list) The Android architectures to build for
android.archs = armeabi-v7a, arm64-v8a

# (list) Android meta-data to set (key=value)
# Activation de la fonction USB Host pour détecter les récepteurs
android.meta_data = android.hardware.usb.host=true

# (str) Android entry point
android.entrypoint = org.kivy.android.PythonActivity

# (str) python-for-android branch to use
p4a.branch = master

[buildozer]
# (int) Log level (0 = error only, 1 = info, 2 = debug)
log_level = 2

# (int) Display warning if buildozer is run as root
warn_on_root = 1
