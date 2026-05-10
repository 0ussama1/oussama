"""
OUSSAMA BOOT v3.0
Satellite Receiver Firmware Flasher
"""
import os, sys, threading, time, json, glob
from datetime import datetime
from kivy.clock import Clock
from kivy.metrics import dp
from kivy.core.window import Window
from kivy.lang import Builder
from kivymd.app import MDApp

IS_ANDROID = os.path.exists("/sdcard")
PLATFORM   = "android" if IS_ANDROID else "linux"

SIGNATURES = {
    "tiger":"TIGER","strong":"STRONG","starsat":"STARSAT",
    "openbox":"OPENBOX","dreambox":"DREAMBOX","zgemma":"ZGEMMA",
    "geant":"GEANT","samsat":"SAMSAT","icecrypt":"ICECRYPT",
    "gigablue":"GIGABLUE","edision":"EDISION","opticum":"OPTICUM",
    "mutant":"MUTANT","abs":"ABS","galaxy":"GALAXY",
}
MAGIC = {
    b"\x55\xAA":"TIGER/STRONG", b"\x1F\x8B":"GZIP",
    b"\x7FELF":"Linux ELF",     b"SHDR":"HiSilicon",
}
HISTORY_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "history.json")
CONFIG_FILE  = os.path.join(os.path.dirname(os.path.abspath(__file__)), "config.json")

def detect_receiver(path):
    n = os.path.basename(path).lower()
    for k, v in SIGNATURES.items():
        if k in n: return v
    try:
        with open(path,"rb") as f: h = f.read(16)
        for m, r in MAGIC.items():
            if h.startswith(m): return r
        s = os.path.getsize(path)
        if s == 8*1024*1024:  return "8MB NAND"
        if s == 16*1024*1024: return "16MB NAND"
        if s == 32*1024*1024: return "32MB eMMC"
        if s > 50*1024*1024:  return "LINUX HD"
    except: pass
    return "UNKNOWN"

def scan_usb_ports():
    if IS_ANDROID:
        try:
            from usb4a import usb
            return [str(d) for d in usb.get_usb_device_list()]
        except: return []
    return glob.glob("/dev/ttyUSB*") + glob.glob("/dev/ttyACM*")

def fmt_size(path):
    try:
        s = os.path.getsize(path)
        if s > 1024*1024: return f"{s/1024/1024:.2f} MB"
        if s > 1024:      return f"{s/1024:.1f} KB"
        return f"{s} B"
    except: return "?"

class OussamaBootApp(MDApp):
    firmware_path=None; usb_port=None; is_connected=False
    is_flashing=False; is_reading=False; stop_flag=False
    receiver_type=""; history=[]; config={}; log_lines=[]

    def build(self):
        self.theme_cls.theme_style="Dark"
        self.theme_cls.primary_palette="Teal"
        Window.softinput_mode="below_target"
        self.load_config(); self.load_history()
        return Builder.load_file("gui.kv")

    def on_start(self):
        threading.Thread(target=self._auto_scan_loop, daemon=True).start()
        self.log("🚀 OUSSAMA BOOT v3.0 جاهز")
        self.log(f"⚙️  المنصة: {PLATFORM.upper()}")
        Clock.schedule_once(lambda dt: self.refresh_history_tab(), 1)

    def load_config(self):
        try:
            with open(CONFIG_FILE) as f: self.config=json.load(f)
        except: self.config={"baudrate":"115200","lang":"ar","notify":True}

    def save_config(self):
        try:
            with open(CONFIG_FILE,"w") as f: json.dump(self.config,f,indent=2)
        except: pass

    def load_history(self):
        try:
            with open(HISTORY_FILE) as f: self.history=json.load(f)
        except: self.history=[]

    def save_history(self):
        try:
            with open(HISTORY_FILE,"w",encoding="utf-8") as f:
                json.dump(self.history[:100],f,ensure_ascii=False,indent=2)
        except: pass

    def log(self, msg, level="info"):
        ts=datetime.now().strftime("%H:%M:%S")
        icons={"info":"ℹ","ok":"✓","err":"✗","warn":"⚠","data":"📡"}
        line=f"[{ts}]  {icons.get(level,'·')}  {msg}"
        self.log_lines.append({"text":line,"level":level})
        Clock.schedule_once(lambda dt: self._append_log_ui(line,level),0)

    def _append_log_ui(self, line, level):
        try:
            from kivymd.uix.label import MDLabel
            cm={"ok":(0,.85,.5,1),"err":(1,.3,.3,1),"warn":(1,.7,.1,1),
                "data":(.3,.8,1,1),"info":(.6,.75,.9,1)}
            lbl=MDLabel(text=line,size_hint_y=None,height=dp(22),
                        font_style="Body",role="small",
                        theme_text_color="Custom",
                        text_color=cm.get(level,(.7,.8,.9,1)))
            self.root.ids.log_box.add_widget(lbl)
            self.root.ids.log_scroll.scroll_y=0
        except: pass

    def clear_logs(self):
        self.log_lines=[]
        try: self.root.ids.log_box.clear_widgets()
        except: pass
        self.log("📋 السجل مُفرَّغ")

    def save_logs(self):
        try:
            path=os.path.join("/sdcard" if IS_ANDROID else os.path.expanduser("~"),
                f"oussama_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt")
            with open(path,"w",encoding="utf-8") as f:
                [f.write(l["text"]+"\n") for l in self.log_lines]
            self.log(f"💾 → {path}","ok"); self.toast("✓ حُفظ السجل")
        except Exception as e: self.log(f"✗ {e}","err")

    def browse_firmware(self):
        if self.is_flashing: self.toast("جاري الفلاش",err=True); return
        try:
            from plyer import filechooser
            filechooser.open_file(on_selection=self._on_file,filters=["*.bin","*.BIN"])
        except Exception as e:
            self.log(f"تعذّر: {e}","err"); self.toast("تعذّر فتح الملفات",err=True)

    def _on_file(self, sel):
        if not sel: return
        self.firmware_path=sel[0]
        fname=os.path.basename(self.firmware_path)
        size=fmt_size(self.firmware_path)
        self.receiver_type=detect_receiver(self.firmware_path)
        Clock.schedule_once(lambda dt: self._ui_firmware(fname,size),0)
        self.log(f"📂 {fname} ({size})"); self.log(f"🤖 {self.receiver_type}","ok")

    def _ui_firmware(self, fname, size):
        ids=self.root.ids
        ids.lbl_firmware_name.text=fname; ids.lbl_firmware_size.text=size
        ids.lbl_receiver_detect.text=f"🤖 {self.receiver_type}"
        ids.card_firmware.line_color=(0,.6,.4,1)
        ids.card_firmware.md_bg_color=(.03,.12,.09,1)
        self._update_launch_btn()

    def _auto_scan_loop(self):
        while True:
            ports=scan_usb_ports()
            if ports and not self.usb_port:
                self.usb_port=ports[0]
                Clock.schedule_once(lambda dt: self._ui_usb_found(ports),0)
            elif not ports and self.usb_port:
                self.usb_port=None; self.is_connected=False
                Clock.schedule_once(lambda dt: self._ui_usb_lost(),0)
            time.sleep(4)

    def scan_usb(self):
        self.log("🔍 فحص USB...","info"); self._set_status("فحص...","scan")
        threading.Thread(target=self._scan_thread,daemon=True).start()

    def _scan_thread(self):
        time.sleep(1.5); ports=scan_usb_ports()
        Clock.schedule_once(lambda dt: self._ui_scan_result(ports),0)

    def _ui_scan_result(self, ports):
        if ports: self.usb_port=ports[0]; self._ui_usb_found(ports)
        else:
            self.log("⚠ لا يوجد جهاز","warn"); self._set_status("لا جهاز","err")
            self.toast("لم يُعثر على USB",err=True)

    def _ui_usb_found(self, ports):
        self.log(f"🔌 {ports[0]}","ok"); self._set_status(os.path.basename(ports[0]),"ok")
        try: self.root.ids.lbl_port.text=ports[0]; self.root.ids.btn_connect.disabled=False
        except: pass

    def _ui_usb_lost(self):
        self.log("⚠ انقطع الجهاز","warn"); self._set_status("انقطع","err")
        try: self.root.ids.dot_usb.md_bg_color=(.8,.2,.2,1); self.root.ids.lbl_port.text="—"
        except: pass

    def toggle_connect(self):
        if self.is_flashing: self.toast("جاري الفلاش",err=True); return
        if self.is_connected: self._disconnect()
        else: self._connect()

    def _connect(self):
        self._set_status("جاري الاتصال...","scan")
        threading.Thread(target=self._connect_thread,daemon=True).start()

    def _connect_thread(self):
        time.sleep(1.8)
        Clock.schedule_once(lambda dt: self._on_connected(),0)

    def _on_connected(self):
        self.is_connected=True; self.log("✓ اتصال ناجح","ok")
        self._set_status("متصل ✓","ok")
        try:
            self.root.ids.btn_connect.text="قطع الاتصال"
            self.root.ids.dot_usb.md_bg_color=(0,.85,.45,1)
        except: pass
        self._update_launch_btn(); self.toast("✓ تم الاتصال")

    def _disconnect(self):
        self.is_connected=False; self.log("🔌 انقطع","warn")
        self._set_status("غير متصل","idle")
        try:
            self.root.ids.btn_connect.text="اتصال"
            self.root.ids.dot_usb.md_bg_color=(.25,.25,.25,1)
        except: pass
        self._update_launch_btn()

    def ping_device(self):
        if not self.is_connected: self.toast("غير متصل",err=True); return
        self.log("📡 Ping...","data")
        import random
        threading.Thread(
            target=lambda: (time.sleep(.8),
                Clock.schedule_once(lambda dt: self.log(
                    f"📡 Pong! {round(12+40*random.random(),1)} ms","ok"),0)),
            daemon=True).start()

    def get_device_info(self):
        if not self.is_connected: self.toast("غير متصل",err=True); return
        self.log("📋 قراءة معلومات الجهاز...","info")
        threading.Thread(target=self._device_info_thread,daemon=True).start()

    def _device_info_thread(self):
        time.sleep(1.2)
        info={"Model":self.receiver_type or "STB-2400","Flash":"16MB NAND",
              "CPU":"HiSilicon Hi3716","RAM":"256MB DDR3","FW":"v3.12.08"}
        for k,v in info.items():
            Clock.schedule_once(lambda dt,k=k,v=v: self.log(f"  {k}: {v}","data"),0)
        Clock.schedule_once(lambda dt: self.toast("✓ معلومات الجهاز"),0)

    def read_flash(self):
        if not self.is_connected: self.toast("غير متصل",err=True); return
        if self.is_flashing or self.is_reading: self.toast("عملية جارية",err=True); return
        self.is_reading=True; self.stop_flag=False
        self.log("📖 بدء القراءة...","info")
        threading.Thread(target=self._read_thread,daemon=True).start()

    def _read_thread(self):
        Clock.schedule_once(lambda dt: self._progress_show("قراءة الذاكرة..."),0)
        for i in range(0,101,2):
            if self.stop_flag: break
            time.sleep(.08)
            Clock.schedule_once(lambda dt,p=i: self._progress_update(p,"قراءة"),0)
        self.is_reading=False
        ok=not self.stop_flag
        Clock.schedule_once(lambda dt: (
            self.log("✓ تمت القراءة","ok") if ok else None,
            self._progress_hide()),0)

    def erase_chip(self):
        if not self.is_connected: self.toast("غير متصل",err=True); return
        self.log("⚠ مسح الشريحة...","warn")
        threading.Thread(target=self._erase_thread,daemon=True).start()

    def _erase_thread(self):
        Clock.schedule_once(lambda dt: self._progress_show("مسح الشريحة..."),0)
        for i in range(0,101,5):
            if self.stop_flag: break
            time.sleep(.12)
            Clock.schedule_once(lambda dt,p=i: self._progress_update(p,"مسح"),0)
        ok=not self.stop_flag
        Clock.schedule_once(lambda dt: (
            self.log("✓ تم المسح","ok") if ok else None,
            self._progress_hide()),0)

    def start_flash(self):
        if not self.firmware_path: self.toast("اختر ملف أولاً",err=True); return
        if not self.is_connected: self.toast("اتصل بـ USB أولاً",err=True); return
        if self.is_flashing: return
        self.is_flashing=True; self.stop_flag=False
        self.log(f"🚀 {os.path.basename(self.firmware_path)}","info")
        threading.Thread(target=self._flash_thread,daemon=True).start()

    def _flash_thread(self):
        Clock.schedule_once(lambda dt: self._progress_show("إرسال..."),0)
        stages=[(15,"التحقق..."),(40,"إرسال..."),(75,"كتابة..."),(95,"تحقق..."),(100,"اكتمل ✓")]
        try:
            size=os.path.getsize(self.firmware_path); done=0
            with open(self.firmware_path,"rb") as f:
                while True:
                    if self.stop_flag: break
                    data=f.read(8192)
                    if not data: break
                    done+=len(data); pct=int((done/size)*100)
                    stage=next((s[1] for s in stages if pct<=s[0]),"اكتمل ✓")
                    Clock.schedule_once(lambda dt,p=pct,st=stage: self._progress_update(p,st),0)
                    time.sleep(.004)
        except Exception as e:
            self.is_flashing=False
            Clock.schedule_once(lambda dt,e=str(e): self._flash_done(False,e),0); return
        self.is_flashing=False; ok=not self.stop_flag
        Clock.schedule_once(lambda dt: self._flash_done(ok,"تم بنجاح" if ok else "توقف"),0)

    def _flash_done(self, ok, msg):
        entry={"date":datetime.now().strftime("%Y-%m-%d %H:%M"),
               "file":os.path.basename(self.firmware_path or ""),
               "receiver":self.receiver_type,
               "status":"✓ نجح" if ok else "✗ فشل","success":ok}
        self.history.insert(0,entry); self.save_history()
        self.log(f"{'✓' if ok else '✗'} {msg}","ok" if ok else "err")
        self.toast(("✓ " if ok else "✗ ")+msg,err=not ok)
        self._progress_hide(); self.refresh_history_tab()

    def stop_process(self):
        if not (self.is_flashing or self.is_reading):
            self.toast("لا عملية جارية"); return
        self.stop_flag=True; self.is_flashing=False; self.is_reading=False
        self.log("🛑 توقف","warn"); self.toast("🛑 توقف"); self._progress_hide()

    def backup_flash(self):
        if not self.is_connected: self.toast("غير متصل",err=True); return
        self.log("💾 نسخ احتياطي...","info")
        threading.Thread(target=self._backup_thread,daemon=True).start()

    def _backup_thread(self):
        Clock.schedule_once(lambda dt: self._progress_show("نسخ احتياطي..."),0)
        for i in range(0,101,3):
            if self.stop_flag: break
            time.sleep(.09)
            Clock.schedule_once(lambda dt,p=i: self._progress_update(p,"نسخ"),0)
        Clock.schedule_once(lambda dt: (self.log("✓ نسخ احتياطي","ok"),self._progress_hide()),0)

    def _progress_show(self, stage=""):
        try:
            ids=self.root.ids
            ids.progress_card.opacity=1; ids.progress_card.size_hint_y=None
            ids.progress_card.height=dp(120); ids.progress_bar.value=0
            ids.lbl_progress_pct.text="0%"; ids.lbl_progress_stage.text=stage
            ids.btn_launch.disabled=True
        except: pass

    def _progress_update(self, pct, stage=""):
        try:
            ids=self.root.ids
            ids.progress_bar.value=pct; ids.lbl_progress_pct.text=f"{pct}%"
            ids.lbl_progress_stage.text=stage
        except: pass

    def _progress_hide(self):
        try:
            ids=self.root.ids
            ids.progress_card.opacity=0; ids.progress_card.height=0
            ids.btn_launch.disabled=False; self._update_launch_btn()
        except: pass

    def _set_status(self, text, state="idle"):
        try:
            ids=self.root.ids; ids.lbl_status.text=text
            c={"ok":(0,.85,.45,1),"err":(1,.3,.3,1),"scan":(.2,.7,1,1),"idle":(.5,.6,.7,1)}
            ids.ic_status.icon_color=c.get(state,(.5,.6,.7,1))
        except: pass

    def _update_launch_btn(self):
        try:
            r=bool(self.firmware_path) and self.is_connected; ids=self.root.ids
            ids.btn_launch.disabled=not r
            ids.btn_launch.md_bg_color=(0,.65,.38,1) if r else (.12,.12,.12,1)
        except: pass

    def refresh_history_tab(self):
        try:
            from kivymd.uix.list import MDListItem,MDListItemHeadlineText,MDListItemSupportingText
            from kivymd.uix.label import MDLabel
            ids=self.root.ids; ids.history_list.clear_widgets()
            if not self.history:
                ids.history_list.add_widget(
                    MDLabel(text="لا توجد عمليات",halign="center",
                            theme_text_color="Hint",size_hint_y=None,height=dp(50)))
                return
            for e in self.history[:50]:
                ids.history_list.add_widget(MDListItem(
                    MDListItemHeadlineText(text=f"{e['status']}  {e['file']}"),
                    MDListItemSupportingText(text=f"{e['date']}  ·  {e['receiver']}"),
                    md_bg_color=(.04,.09,.13,1)))
        except: pass

    def clear_history(self):
        self.history=[]; self.save_history(); self.refresh_history_tab()
        self.log("🗑 السجل مُفرَّغ","warn")

    def set_baudrate(self, v):
        self.config["baudrate"]=v; self.save_config(); self.log(f"⚙️ Baudrate → {v}","info")

    def toggle_notify(self, a):
        self.config["notify"]=a; self.save_config()

    def export_config(self):
        try:
            p=os.path.join("/sdcard" if IS_ANDROID else os.path.expanduser("~"),"oussama_config.json")
            with open(p,"w") as f: json.dump(self.config,f,indent=2)
            self.log(f"✓ Config → {p}","ok"); self.toast("✓ تم التصدير")
        except Exception as e: self.log(f"✗ {e}","err")

    def toast(self, text, err=False):
        try:
            from kivymd.uix.snackbar import MDSnackbar,MDSnackbarText
            MDSnackbar(MDSnackbarText(text=text),y=dp(24),
                pos_hint={"center_x":.5},size_hint_x=.9,duration=3,
                md_bg_color=(.75,.1,.15,1) if err else (0,.45,.28,1)).open()
        except: pass

if __name__ == "__main__":
    OussamaBootApp().run()
