เอกสารนี้แบ่งเป็น 2 เฟส: **Phase 1 (ทำให้รันได้)** และ **Phase 2 (ทำให้ดี)** เพื่อให้คุณเจอ Pain Point ด้วยตัวเองก่อนครับ

---

### เอกสารข้อสอบภาคปฏิบัติ DevOps Engineer (Intern)

**หัวข้อ:** Containerization & Optimization for "Sentinel Home"

**ผู้รับผิดชอบ:** คุณ (Infrastructure Team)

**โจทย์:** เปลี่ยน Application แบบ Monolith ให้เป็น Container-based ที่มีความปลอดภัยและขนาดเล็กที่สุด

#### 1) วัตถุประสงค์ (Objectives)

1. **Containerization Mastery:** เข้าใจการเขียน `Dockerfile` ตั้งแต่ระดับพื้นฐานจนถึงระดับ Advanced (Multi-stage build)
    
2. **Image Optimization:** เรียนรู้วิธีลดขนาด Image และการจัดการ Layer caching
    
3. **Security Hardening:** เข้าใจความเสี่ยงของการรัน Container ในฐานะ Root และการจัดการ Secrets
    
4. **Configuration Management:** แยก Config ออกจาก Code (12-factor App)
    

#### 2) สถานการณ์จำลอง (Scenario)

ทีม Developer ได้ส่งมอบ Source Code ของระบบ **"Log Ingestor Agent"** (ภาษา Python หรือ Go ก็ได้ ตามที่คุณถนัด) ที่ทำหน้าที่ดูด Log จากเครื่องแล้วส่งไป Server แต่ปัญหามีดังนี้:

- Dev รันบนเครื่องตัวเองผ่าน แต่พอย้ายไปเครื่องอื่น Library ตีกันมั่ว
    
- Dev ส่ง Code มาพร้อมกับไฟล์ `.env` ที่มี Password แปะมาด้วย
    
- Dev บอกว่า "พี่ช่วยเอาใส่ Docker ให้หน่อย ผมทำไม่เป็น"
    

#### 3) ขอบเขตงาน (Scope & Phases)

**Phase 1: The "It Works" (ทำให้รันได้ก่อน - ห้ามข้ามขั้นตอนนี้!)**

- **เป้าหมาย:** สร้าง Docker Image ที่รันโปรแกรมได้ โดยไม่สนเรื่องขนาดหรือความสวยงาม
    
- **ข้อบังคับ (Constraint):**
    
    - ให้ใช้ Base Image ตัวเต็มเท่านั้น (เช่น `python:3.9` หรือ `golang:1.21` ห้ามใช้ alpine/slim)
        
    - Copy source code **ทุกอย่าง** เข้าไปใน Image ดื้อๆ
        
    - สั่งรัน Application ด้วย User `root` (Default)
        
- **สิ่งที่ต้องเจอ (Pain Points):**
    
    - ลอง Build แล้วสังเกตเวลาที่ใช้ (ช้าไหม?)
        
    - ลองแก้ Code 1 บรรทัด แล้ว Build ใหม่ (ทำไมมันโหลด Library ใหม่หมดเลย?)
        
    - เช็คขนาด Image (`docker images`) ดูซิว่ามันใหญ่แค่ไหน (น่าจะ 800MB - 1GB+)
        

**Phase 2: The "Best Practice" (Refactor สู่ Production)**

- **เป้าหมาย:** แก้ไข Dockerfile จาก Phase 1 ให้เป็นไปตามมาตรฐาน DevOps
    
- **ข้อกำหนด (Requirements):**
    
    1. **Size Reduction:** ขนาด Image ต้องลดลง **อย่างน้อย 80%** จาก Phase 1 (เช่นจาก 1GB เหลือ < 100MB หรือ < 50MB ถ้าใช้ Go)
        
    2. **Multi-stage Build:** ต้องมีการแยก Stage `Builder` และ `Runner`
        
    3. **Security:**
        
        - **ห้าม** รันด้วย User `root` (ต้องสร้าง User ใหม่ใน Dockerfile)
            
        - **ห้าม** มีไฟล์ `.env` หรือ Secret ค้างอยู่ใน Image
            
    4. **Layer Caching:** จัดลำดับคำสั่งใน Dockerfile ให้ถูกต้อง (แก้ Code แล้วต้องไม่ต้องโหลด Library ใหม่)
        
    5. **Base Image:** เปลี่ยนไปใช้ `alpine` หรือ `distroless`
        

#### 4) Source Code สำหรับทดสอบ (Seed Data)

_(ให้คุณสร้างไฟล์ง่ายๆ ขึ้นมา 1 ไฟล์เพื่อใช้ทำโจทย์นี้)_

**Option A: Python (app.py)**

```Python
import os
import time
# สมมติว่ามีการใช้ library เยอะๆ ให้สร้าง requirements.txt ที่มี pandas, numpy, requests
# เพื่อจำลองความใหญ่ของ Library

def main():
    print("Sentinel Agent Starting...")
    db_pass = os.getenv("DB_PASS", "default_insecure")
    print(f"Connecting with password: {db_pass}") # ในความจริงห้ามปรินท์ pass
    while True:
        print("Ingesting logs...")
        time.sleep(5)

if __name__ == "__main__":
    main()
```

**Option B: Go (main.go)**

```Go
package main

import (
	"fmt"
	"os"
	"time"
)

func main() {
	fmt.Println("Sentinel Agent Starting...")
	dbPass := os.Getenv("DB_PASS")
	if dbPass == "" {
		dbPass = "default_insecure"
	}
	fmt.Printf("Connecting to DB... (Pass length: %d)\n", len(dbPass))
	for {
		fmt.Println("Ingesting logs...")
		time.Sleep(5 * time.Second)
	}
}
```

#### 5) เกณฑ์การให้คะแนน (Scoring Criteria)

|**หมวดหมู่**|**รายละเอียด (Pass Criteria)**|**คะแนนเต็ม**|
|---|---|---|
|**Functional**|Container รันขึ้น, ไม่ Crash, อ่าน Environment Variable ได้ถูกต้อง|20|
|**Optimization**|**(Highlight)** ขนาด Image เล็กกว่า 100MB (Python) หรือ 20MB (Go)|30|
|**Build Efficiency**|เมื่อแก้ Code แล้ว Re-build, Docker ใช้ Cache เดิมในส่วน Library (ไม่โหลดใหม่)|20|
|**Security**|Process ภายใน Container ไม่ใช่ PID 1 ที่เป็น Root (เช็คด้วย `docker top`)|15|
|**Cleanliness**|ไม่มีไฟล์ขยะ (Source code ที่ไม่จำเป็น, Cache ของ apt/pip) เหลือใน Image ปลายทาง|15|
|**Bonus**|ใช้ `.dockerignore` ได้อย่างถูกต้อง|+10|

---

#### 6) ขั้นตอนการส่งงาน (Deliverables)

1. **Folder `phase1_messy/`**: เก็บ Dockerfile แบบเผาๆ ที่ไฟล์ใหญ่ๆ
    
2. **Folder `phase2_clean/`**: เก็บ Dockerfile ที่จูนแล้ว
    
3. **Report (Markdown)**: เขียนสรุปสั้นๆ เปรียบเทียบ:
    
    - Image Size (Before vs After)
        
    - Build Time (Before vs After)
        
    - อธิบายว่าทำไมถึงเลือกใช้คำสั่งนี้ (เช่น ทำไม `COPY go.mod` ก่อน `COPY .`)
        

---

### วิธีเริ่มทำ (Instruction)

1. **Setup:** สร้าง Folder โปรเจกต์ ใส่ Code ภาษาที่คุณเลือก
    
2. **Do Phase 1:** เขียน Dockerfile แบบที่คิดออกตอนแรกเลย เอาให้รันได้พอ
    
    - _Self-Check:_ พิมพ์ `docker images` แล้วจดขนาดไฟล์ไว้
        
3. **Research & Fix:** พอเห็นขนาดไฟล์แล้วตกใจ ให้เริ่มค้นหาคำว่า:
    
    - "Docker multi-stage build python/go"
        
    - "How to reduce docker image size"
        
    - "Running docker as non-root user"
        
    - "Docker layer caching best practices"
        
4. **Do Phase 2:** เขียน Dockerfile ใหม่ (ตั้งชื่อ `Dockerfile.optimized`) แล้วเทียบผลลัพธ์
