import threading
import time
import serial
from kivy.lang import Builder
from kivy.clock import Clock
from kivy.animation import Animation
from kivymd.app import MDApp
from kivymd.uix.snackbar import Snackbar
from plyer import filechooser

# Tentative d'importation des bibliothèques Android pour l'USB
try:
    from usb4a import usb
    from usbserial4a import serial4a
    plateforme = "android"
except ImportError:
    plateforme = "desktop"

# Interface Utilisateur Professionnelle OUSSAMA SAT PRO AI
KV = '''
MDScreen:
    md_bg_color: 0.05, 0.05, 0.05, 1

    MDBoxLayout:
        orientation: 'vertical'
        padding: "20dp"
        spacing: "15dp"

        MDLabel:
            text: "OUSSAMA SAT PRO AI"
            halign: "center"
            font_style: "H6"
            theme_text_color: "Custom"
            text_color: 0, 0.8, 0.4, 1
            bold: True

        MDCard:
            orientation: "vertical"
            padding: "15dp"
            size_hint: 1, None
            height: "100dp"
            md_bg_color: 0.1, 0.1, 0.1, 1
            radius: [15,]

            MDLabel:
                text: "FIRMWARE CIBLE (Fichier .bin):"
                theme_text_color: "Hint"
                font_style: "Caption"
            
            MDLabel:
                id: label_chemin_fichier
                text: "Sélectionnez un fichier .bin"
                theme_text_color: "Primary"
                font_style: "Body2"
                shorten: True
                shorten_from: "center"

        MDRaisedButton:
            text: "1. SÉLECTIONNER LE FICHIER"
            size_hint_x: 1
            md_bg_color: 0.5, 0, 0.5, 1
            on_release: app.ouvrir_gestionnaire_fichiers()

        MDCard:
            size_hint: 1, None
            height: "120dp"
            md_bg_color: 0.08, 0.08, 0.08, 1
            radius: [15,]
            padding: "15dp"
            
            MDBoxLayout:
                orientation: 'vertical'
                spacing: "10dp"

                MDBoxLayout:
                    orientation: 'horizontal'
                    spacing: "10dp"
                    adaptive_height: True
                    pos_hint: {"center_x": .5}

                    MDIcon:
                        id: led_statut
                        icon: "circle"
                        theme_text_color: "Custom"
                        text_color: 0.3, 0.3, 0.3, 1
                        font_size: "18sp"
                        pos_hint: {"center_y": .5}

                    MDLabel:
                        id: label_statut
                        text: "IA: Recherche de récepteur..."
                        theme_text_color: "Secondary"
                        font_style: "Button"
                        adaptive_width: True
                        pos_hint: {"center_y": .5}

                MDProgressBar:
                    id: barre_progression
                    value: 0
                    max: 100
                    color: 0, 0.8, 0.4, 1

        MDRaisedButton:
            id: bouton_flash
            text: "LANCER LA MISE À JOUR"
            size_hint_x: 1
            md_bg_color: 0.2, 0.2, 0.2, 1
            disabled: True
            on_release: app.demarrer_thread_flash()

        MDLabel:
            text: "Statut: Mode " + ("Android OTG" if app.est_android else "Bureau")
            halign: "center"
            font_style: "Caption"
            theme_text_color: "Hint"
'''

class OussamaSatApp(MDApp):
    fichier_selectionne = None
    port_actif = None
    anim_pulsation = None
    est_android = plateforme == "android"

    def build(self):
        self.theme_cls.theme_style = "Dark"
        return Builder.load_string(KV)

    def on_start(self):
        threading.Thread(target=self.moteur_capteur_intelligent, daemon=True).start()

    def moteur_capteur_intelligent(self):
        deja_trouve = False
        while True:
            trouve = False
            nom_port = None
            if self.est_android:
                liste_peripheriques_usb = usb.get_usb_device_list()
                if liste_peripheriques_usb:
                    nom_port = liste_peripheriques_usb[0].getDeviceName()
                    trouve = True
            else:
                import serial.tools.list_ports
                ports = list(serial.tools.list_ports.comports())
                if ports:
                    nom_port = ports[0].device
                    trouve = True

            if trouve != deja_trouve:
                if trouve:
                    self.port_actif = nom_port
                    Clock.schedule_once(lambda dt: self.ui_connecte())
                else:
                    self.port_actif = None
                    Clock.schedule_once(lambda dt: self.ui_deconnecte())
                deja_trouve = trouve
            time.sleep(1)

    def ui_connecte(self):
        led = self.root.ids.led_statut
        lbl = self.root.ids.label_statut
        btn = self.root.ids.bouton_flash
        led.text_color = (0, 1, 0.5, 1)
        self.anim_pulsation = Animation(opacity=0.3, duration=0.6) + Animation(opacity=1, duration=0.6)
        self.anim_pulsation.repeat = True
        self.anim_pulsation.start(led)
        lbl.text = "IA: Connecté (OTG Détecté)"
        lbl.text_color = (0, 0.8, 0.4, 1)
        btn.disabled = False
        btn.md_bg_color = (0, 0.5, 0.3, 1)

    def ui_deconnecte(self):
        led = self.root.ids.led_statut
        lbl = self.root.ids.label_statut
        btn = self.root.ids.bouton_flash
        if self.anim_pulsation: self.anim_pulsation.stop(led)
        led.text_color = (0.3, 0.3, 0.3, 1)
        led.opacity = 1
        lbl.text = "IA: Recherche de récepteur..."
        lbl.text_color = (0.6, 0.6, 0.6, 1)
        btn.disabled = True
        btn.md_bg_color = (0.2, 0.2, 0.2, 1)

    def ouvrir_gestionnaire_fichiers(self):
        filechooser.open_file(on_selection=self.lors_du_choix_fichier)

    def lors_du_choix_fichier(self, selection):
        if selection:
            self.fichier_selectionne = selection[0]
            self.root.ids.label_chemin_fichier.text = self.fichier_selectionne

    def demarrer_thread_flash(self):
        if not self.fichier_selectionne:
            self.afficher_msg("Choisissez un fichier .bin", (0.8, 0, 0, 1))
            return
        threading.Thread(target=self.processus_flashage, daemon=True).start()

    def processus_flashage(self):
        try:
            with open(self.fichier_selectionne, "rb") as f:
                donnees = f.read()
            
            if self.est_android:
                peripherique = usb.get_usb_device_list()[0]
                ser = serial4a.get_serial_port(peripherique.getDeviceName(), 115200, 8, 'N', 1, timeout=1)
            else:
                ser = serial.Serial(self.port_actif, 115200, timeout=1)
            
            if not ser.is_open: ser.open()
            
            total = len(donnees)
            bloc = 1024
            for i in range(0, total, bloc):
                ser.write(donnees[i:i+bloc])
                progression = int((i/total)*100)
                Clock.schedule_once(lambda dt, p=progression: self.maj_ui_progression(p))
            
            ser.close()
            self.afficher_msg("Mise à jour terminée ✅")
        except Exception as e:
            self.afficher_msg(f"Erreur: {str(e)}", (0.8, 0, 0, 1))

    def maj_ui_progression(self, val):
        self.root.ids.barre_progression.value = val
        self.root.ids.label_statut.text = f"Transfert: {val}%"

    def afficher_msg(self, texte, couleur=(0, 0.5, 0.3, 1)):
        Snackbar(text=texte, bg_color=couleur).open()

if __name__ == "__main__":
    OussamaSatApp().run()
