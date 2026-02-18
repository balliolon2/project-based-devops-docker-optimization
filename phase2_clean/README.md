## Step 1: สร้าง "ยันต์กันผี" (.dockerignore)

ไฟล์นี้สำคัญมาก! มันบอก Docker ว่า "อย่าเอาไฟล์ขยะพวกนี้ส่งไป Build นะ"
ให้สร้างไฟล์ชื่อ .dockerignore ไว้ที่ Root Folder (sentinel-exam/.dockerignore)

## Step 2: เขียน Dockerfile ฉบับ "Pro"

ให้สร้างไฟล์ phase2_clean/Dockerfile แล้วใส่โค้ดชุดนี้ครับ (ผมใส่ Comment อธิบายจุดที่แก้ไว้ให้แล้ว)

สิ่งที่เปลี่ยนไป:
- เปลี่ยน Base เป็น python:3.9-slim (ตัวบาง ตัดเครื่องมือสิ้นเปลืองออก)
- เพิ่ม USER appuser (ไม่รันเป็น Root แล้ว ปลอดภัยขึ้น 1000%)
- ใช้ --no-cache-dir (บอก pip ว่าโหลดเสร็จไม่ต้องเก็บไฟล์ติดตั้งไว้ ให้ลบทิ้งเลย)


## ผมจะเจาะลึกทีละส่วนแบบ "ทำไมต้องทำ?" (Why) ให้เห็นภาพชัดๆ ครับ

---

### 1. ทำไมต้อง `python:3.9-slim`? (Diet Plan)

```dockerfile
FROM python:3.9-slim

```

* **แบบเดิม (`python:3.9`):** เหมือนเราจะไปเที่ยวแค่พัทยา แต่แบกกระเป๋าเดินทางไปยุโรป (มี compiler, debugger, manual ครบ) ขนาดเลยปาไป 1GB+
* **แบบ Slim (`python:3.9-slim`):** เหมือนพกแค่เป้ใบเดียว (มีแค่ OS ขั้นต่ำกับ Python Runtime)
* **ทำไมไม่ใช้ Alpine (`python:3.9-alpine`)?:** อันนี้โปรบางคนจะเถียงกัน แต่สำหรับ Data Science (numpy/pandas) **Alpine คือนรกครับ** เพราะ Alpine ใช้ `musl` แทน `glibc` ทำให้ compile library พวกนี้ยากมากและช้ามาก การใช้ **Slim (Debian-based)** คือจุดสมดุลที่ดีที่สุดระหว่าง "ขนาดเล็ก" กับ "ความเข้ากันได้" ครับ

---

### 2. Environment Variables: สั่งให้ Python ทำตัวดีๆ

```dockerfile
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

```

* **`PYTHONDONTWRITEBYTECODE=1`**: ปกติ Python จะสร้างไฟล์ `.pyc` (Compiled bytecode) เพื่อให้รันครั้งต่อไปเร็วขึ้น แต่ใน Docker เรา **สร้างทิ้งแล้วทำลาย** (Container อายุสั้น) ไฟล์พวกนี้เลยกลายเป็นขยะรกพื้นที่ครับ
* **`PYTHONUNBUFFERED=1`**: **สำคัญมาก!** ถ้าไม่ใส่ Log ของ Python จะถูก "อม" ไว้ใน Buffer จนกว่าจะเต็มแล้วค่อยคายออกมาทีเดียว ทำให้เวลาเราสั่ง `docker logs -f` เราจะไม่เห็น Log ทันที (Real-time) การใส่ค่านี้คือบังคับให้ "มีอะไรพูดออกมาเลย!"

---

### 3. Security Hardening: เกราะกันกระสุน (Non-root)

```dockerfile
RUN groupadd -r appuser && useradd -r -g appuser appuser
...
USER appuser

```

* **ความเสี่ยง:** โดยปกติ Docker รันเป็น `root` (God Mode) ถ้า Hacker เจาะผ่าน Python เข้ามาได้ เขาจะได้สิทธิ์ `root` ใน Container นั้นทันที และอาจทะลุออกมายังเครื่อง Host ได้
* **ทางแก้:** เราสร้าง User ธรรมดาชื่อ `appuser` ที่ไม่มีสิทธิ์แก้อะไรในระบบเลย (No sudo) ให้มารันโปรแกรมแทน
* **ผลลัพธ์:** ต่อให้โดนแฮก Hacker ก็ติดอยู่ในห้องขัง ทำอะไรต่อไม่ได้ครับ (นี่คือข้อสอบข้อ Security คะแนนเต็มครับ)

---

### 4. The Magic of Layer Caching: เวทมนตร์แห่งความเร็ว ⚡

นี่คือส่วนที่ "ฉลาด" ที่สุดของไฟล์นี้ครับ ดูลำดับดีๆ นะครับ:

```dockerfile
# Step A: ก๊อปแค่ใบสั่งยา (requirements.txt)
COPY src/requirements.txt . 

# Step B: ซื้อยาตามใบสั่ง (pip install)
RUN pip install --no-cache-dir -r requirements.txt

# Step C: ก๊อปตัวคนไข้ (Source Code)
COPY src/ src/

```

**ทำไมต้องแยก `COPY` เป็น 2 รอบ?**
Docker สร้าง Image เป็นชั้นๆ (Layers) เหมือนเค้กชั้นครับ

* **สถานการณ์:** บอนด์แก้โค้ด `app.py` บ่อยมาก แต่ `requirements.txt` นานๆ แก้ที
* **ผลลัพธ์:**
1. Docker เช็ค Step A: "เอ๊ะ ไฟล์ requirements.txt หน้าตาเหมือนเดิมไหม?" -> **เหมือนเดิม!**
2. Docker เช็ค Step B: "งั้นไม่ต้องรัน `pip install` ใหม่นะ ไปเอา **Cache** (เค้กชั้นเดิม) มาใช้เลย" **(ประหยัดเวลาไป 5-10 นาที)**
3. Docker เช็ค Step C: "อ้าว ไฟล์ `src/` เปลี่ยนนี่นา" -> **โอเค สร้างใหม่แค่ชั้นนี้**



ถ้าบอนด์เขียน `COPY . .` ไว้บรรทัดบนสุด Docker จะมองว่า "ไฟล์เปลี่ยนแล้ว" และจะสั่ง `pip install` ใหม่ **ทุกครั้ง** ที่บอนด์แก้โค้ดแม้แต่ตัวอักษรเดียวครับ (นรกของการรอคอย)

---

### 5. `pip install --no-cache-dir`: ทิ้งขยะทันที

```dockerfile
RUN pip install --no-cache-dir -r requirements.txt

```

* ปกติ `pip` จะใจดี โหลดไฟล์ติดตั้งมาเก็บไว้ใน Cache (`~/.cache/pip`) เผื่อเราจะลงซ้ำ
* แต่ใน Docker เราลงครั้งเดียวแล้วจบ Cache พวกนี้คือน้ำหนักส่วนเกิน (หลายร้อย MB) ที่เราแบกขึ้น Production ไปด้วย
* คำสั่งนี้บอก pip ว่า "ลงเสร็จแล้วลบไฟล์ทิ้งให้หมดนะ" ทำให้ Image เล็กลงฮวบฮาบครับ

---

### สรุปความเจ๋งของไฟล์นี้ (เอาไว้ตอบกรรมการ)

1. **Slim:** เล็กแต่ทรงพลัง (Compatible กับ Data Libs)
2. **Fast Build:** แก้โค้ดไม่ต้องรอลง Library ใหม่ (ด้วย Layer Caching)
3. **Secure:** แฮกยากเพราะไม่ใช่ Root
4. **Clean:** ไม่มีไฟล์ขยะ (.pyc, pip cache)

พร้อมจะลอง **Build** ตัว Optimized นี้แล้วเอาผลลัพธ์มาขิงใส่ตัวเก่ารึยัง