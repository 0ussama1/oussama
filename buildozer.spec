[app]
# --- Informations de base ---
title = OUSSAMA SAT PRO AI
package.name = oussamasat
package.domain = org.oussama
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 1.0

# --- Dépendances (Simplifiées pour éviter les erreurs de build) ---
# On laisse buildozer choisir les meilleures versions compatibles avec GitHub
requirements = python3, kivy, kivymd, pyserial, plyer, usb4a, usbserial4a

orientation = portrait

# --- Permissions Android (Nécessaires pour ton matériel satellite) ---
android.permissions = WRITE_EXTERNAL_STORAGE, READ_EXTERNAL_STORAGE, USB_PERMISSION, INTERNET

# --- Configuration Android Stable ---
# Utilisation de l'API 31 (Android 12) pour éviter les erreurs de SDK rencontrées
android.api = 31
android.minapi = 21
android.ndk = 25b

# Support de toutes les architectures mobiles
android.archs = armeabi-v7a, arm64-v8a

# --- Configuration OTG / USB ---
# Indispensable pour la détection de tes récepteurs satellite
android.meta_data = android.hardware.usb.host=true

# --- Paramètres de compilation ---
p4a.branch = master

[buildozer]
# Niveau 2 pour voir précisément où le build avance
log_level = 2
warn_on_root = 1
