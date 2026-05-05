[app]

# --- Informations Générales ---
title = OUSSAMA SAT PRO AI
package.name = oussamasat
package.domain = org.oussama
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 1.0

# --- Dépendances (Versions Fixées pour la Stabilité) ---
# Ajout de hostpython3 et cython spécifique pour éviter les erreurs de compilation sur GitHub
requirements = python3, kivy==2.2.1, kivymd==1.1.1, pyserial, plyer, usb4a, usbserial4a, hostpython3==3.10.12, cython==0.29.33

orientation = portrait

# --- Permissions Android ---
android.permissions = WRITE_EXTERNAL_STORAGE, READ_EXTERNAL_STORAGE, USB_PERMISSION, INTERNET

# --- Configuration Android (API 31 pour Stabilité Maximale) ---
# Correction : Suppression de android.sdk pour éviter les conflits de version
android.api = 31
android.minapi = 21
android.ndk = 25b

# Architectures supportées
android.archs = armeabi-v7a, arm64-v8a

# --- Configuration Matérielle ---
# Activation obligatoire du mode USB Host pour tes outils satellite (OTG)
android.meta_data = android.hardware.usb.host=true

# --- Python for Android ---
p4a.branch = master

[buildozer]
# Niveau de log élevé pour le débogage
log_level = 2
warn_on_root = 1
