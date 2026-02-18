import os
import time
import sys

# จำลอง App ที่ทำหน้าที่ดูด Log
def main():
    print("Sentinel Log Ingestor: STARTING...")
    
    # ดึงค่าจาก Environment Variable
    db_host = os.getenv("DB_HOST", "localhost")
    db_pass = os.getenv("DB_PASS", "NoPasswordSet")
    
    print(f"[INFO] Target Database: {db_host}")
    
    # จุดที่ Dev มักพลาด: ปรินท์ Password ออกมาดู (Security Risk!)
    print(f"[DEBUG] Using Password: {db_pass}") 
    
    counter = 0
    while True:
        counter += 1
        print(f"[Ingestor] Processing log batch #{counter} ...")
        sys.stdout.flush() # บังคับให้ print ออกมาทันที (สำคัญสำหรับ Docker logs)
        time.sleep(5)

if __name__ == "__main__":
    main()