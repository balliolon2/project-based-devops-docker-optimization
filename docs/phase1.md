- Build Time: ตอนมันรัน pip install numpy pandas นานมาก
- image size = 1.85GB เยอะมาก

- โค้ดจริงเรามีแค่ไม่กี่ KB แต่เราแบกบ้านทั้งหลังไปด้วย

ถ้าเราเอานี่ขึ้น Cloud จริง:
- เปลืองค่าเน็ต: อัปโหลด 1.85 GB ทุกครั้งที่แก้โค้ด
- เปลืองค่าที่: Docker Registry คิดตังค์ตามพื้นที่
- ช้า: เวลาจะ Scale เพิ่มเครื่องใหม่ ต้องรอโหลด 1.85 GB นานหลายนาที

แถม
```
01:27:32 (base) balliolon@fedora project-based-devops-docker-optimization ±|main ✗|→ docker run --rm sentinel:messy cat src/.env
DB_HOST=production-db.internal
DB_PASS=SuperSecretPassword1234
```