- Build Time: ไม่นานมาก
- Image Size: 383.55MB น้อยกว่ามาก
- ขนาดของ Layer ที่สร้างเพิ่มขึ้นมาเอง จาก 483 MB เป็น 86.8 MB (Unique/Layer Size)
    - messy: เราแบก Cache ของ pip และไฟล์ขยะต่างๆ ไปด้วย (483 MB)
    - clean: เราใช้ --no-cache-dir และ .dockerignore ทำให้เหลือแค่ Library ที่จำเป็นจริงๆ (86.8 MB)

```
01:27:36 (base) balliolon@fedora project-based-devops-docker-optimization ±|main ✗|→ docker run --rm sentinel:clean cat src/.env
cat: src/.env: No such file or directory
```
- ถือว่าปลอดภัยกว่าปกติมาก