# 1. ใช้ Base Image ตัวเต็ม (Full Fat)
# (ปกติมันมีเครื่องมือเยอะดี แต่ขนาดใหญ่มาก)
FROM python:3.9
# 2. กำหนด Working Directory
WORKDIR /app
# 3. Copy "ทุกอย่าง" จาก Folder โปรเจกต์เข้าไปใน Image
# (จุดนี้คือหายนะแรก: เรา Copy ทั้ง src, docs, และไฟล์ขยะอื่นๆ เข้าไปหมดเลย)
COPY . .
# 4. ติดตั้ง Dependencies (รวมถึงไฟล์ .env ที่มี Password!)
# (จุดนี้จะช้ามาก เพราะต้องโหลด Library ใหญ่ๆ และมันจะ Cache ไว้ตลอด)
RUN pip install -r src/requirements.txt
# 5. สั่งรันโปรแกรมด้วย User Root (Default)
# (จุดนี้คือหายนะที่สอง: รันด้วยสิทธิ์ผู้ดูแลระบบ ซึ่งอันตรายมาก)
CMD ["python", "src/app.py"]
