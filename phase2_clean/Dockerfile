# 1. Base Image: เปลี่ยนจากตัวเต็ม (1GB) มาใช้แบบ Slim (Debian ย่อส่วน)
# ข้อดี: เล็กลงมาก แต่ยังรัน Python wheel (numpy/pandas) ได้ดีกว่า Alpine
FROM python:3.9-slim

# 2. Security: ตั้งค่า Environment ที่จำเป็น
# PYTHONDONTWRITEBYTECODE=1 -> ไม่ต้องสร้าง .pyc (รก)
# PYTHONUNBUFFERED=1 -> ให้ print log ออกมาทันที (เหมือนที่เรา flush ใน code)
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# 3. สร้าง User ปลอดภัย (Non-root) 
# สร้าง User ธรรมดา (Non-root) ขึ้นมาชื่อ 'appuser'
# สร้าง group และ user โดยระบุ UID เพื่อความชัวร์
RUN groupadd -r appuser && useradd -r -g appuser appuser

# 4. Setup Working Directory
WORKDIR /app

# 5. Optimization (Layer Caching):
# Copy *แค่* requirements.txt มาก่อน!
# ถ้าเราแก้โค้ดใน app.py แต่ไม่ได้แก้ requirements -> Docker จะข้ามบรรทัดนี้ไปใช้ Cache เดิม (ไม่ต้องโหลด numpy ใหม่!)
COPY src/requirements.txt .

# 6. Install Dependencies
# --no-cache-dir: โหลดเสร็จลบทิ้ง ลดขนาด Image ได้อีกเป็นร้อย MB
RUN pip install --no-cache-dir -r requirements.txt

# 7. Copy Code ที่เหลือ
COPY src/ src/

# 8. Security: เปลี่ยนเจ้าของไฟล์ทั้งหมดให้เป็นของ appuser
RUN chown -R appuser:appuser /app

# 9. Security: สลับร่างไปเป็น User ธรรมดา (จากนี้ไปเราไม่มีสิทธิ์ Root แล้ว)
USER appuser

# 10. Run App
CMD ["python", "src/app.py"]

