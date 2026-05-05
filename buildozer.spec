[app]

# (section) Informations de base
title = OUSSAMA SAT PRO AI
package.name = oussamasat
package.domain = org.oussama
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 1.0

# (CORRECTION) Liste des bibliothèques avec versions stables pour éviter les crashs
# Ajout de hostpython3 et cython spécifique pour la compatibilité GitHub
requirements = python3, kivy==2.2.1, kivymd==1.1.1, pyserial, plyer, usb4a, usbserial4a, hostpython3==3.10.12, cython==0.29.33

orientation = portrait

# (section) Permissions Android pour l'USB et le stockage
android.permissions = WRITE_EXTERNAL_STORAGE, READ_EXTERNAL_STORAGE, USB_PERMISSION, INTERNET

# (CORRECTION) Paramètres Android Stables (API 31 est recommandé pour Kivy/USB)
# Suppression de android.sdk pour éviter les conflits
android.api = 31
android.minapi = 21
android.ndk = 25b

# Support des architectures pour tous les téléphones modernes
android.archs = armeabi-v7a, arm64-v8a

# (section) Configuration USB Host pour le câble OTG (Indispensable pour ton matériel)
android.meta_data = android.hardware.usb.host=true

# (section) Python for Android configuration
p4a.branch = master

[buildozer]
# Niveau de log pour voir les détails en cas de besoin
log_level = 2
warn_on_root = 1
