# HỆ THỐNG QUẢN LÝ SINH VIÊN - STUDENT MANAGEMENT API

## 📋 GIỚI THIỆU

Đây là bài tập xây dựng REST API để quản lý thông tin sinh viên sử dụng FastAPI và PostgreSQL/MySQL. Hệ thống cho phép thêm, xem, sửa, xóa thông tin sinh viên với đầy đủ validation và phân trang.

**Thời gian hoàn thành**: 6 ngày

---

## 🎯 MỤC TIÊU HỌC TẬP

Sau khi hoàn thành bài tập này, bạn sẽ nắm vững:
- ✅ Xây dựng REST API với FastAPI
- ✅ Kết nối và thao tác với Database
- ✅ Sử dụng SQLAlchemy ORM
- ✅ Validation dữ liệu với Pydantic
- ✅ Xử lý lỗi và HTTP Status Codes
- ✅ Phân trang dữ liệu
- ✅ CRUD operations (Create, Read, Update, Delete)

---

## 🛠️ CÔNG NGHỆ SỬ DỤNG

- **Python**: 3.8+
- **FastAPI**: Web framework
- **SQLAlchemy**: ORM (Object-Relational Mapping)
- **PostgreSQL** hoặc **MySQL**: Database
- **Pydantic**: Data validation
- **Uvicorn**: ASGI server

---

## 📁 CẤU TRÚC PROJECT
```
student-management/
│
├── app/
│   ├── __init__.py
│   ├── main.py              # File chính - FastAPI application
│   ├── database.py          # Cấu hình kết nối database
│   ├── models.py            # SQLAlchemy models (bảng database)
│   ├── schemas.py           # Pydantic schemas (validation)
│   └── crud.py              # Các hàm CRUD (thao tác database)
│
├── .env                     # Biến môi trường (không commit lên git)
├── .gitignore              # File ignore cho git
├── requirements.txt         # Danh sách thư viện Python
└── README.md               # File hướng dẫn này
```

---

## 🗄️ CẤU TRÚC DATABASE

### Bảng: `students`

| Tên cột | Kiểu dữ liệu | Ràng buộc | Mô tả |
|---------|-------------|-----------|-------|
| `id` | Integer | PRIMARY KEY, AUTO_INCREMENT | ID sinh viên |
| `name` | String(100) | NOT NULL | Họ và tên đầy đủ |
| `email` | String(100) | NOT NULL, UNIQUE | Email sinh viên |
| `phone` | String(20) | NULLABLE | Số điện thoại |
| `major` | String(100) | NOT NULL | Ngành học |
| `gpa` | Float | NOT NULL, CHECK (0 <= gpa <= 4) | Điểm trung bình |
| `created_at` | DateTime | DEFAULT CURRENT_TIMESTAMP | Thời gian tạo |

---

## 🚀 CÀI ĐẶT VÀ CHẠY PROJECT

### Bước 1: Clone hoặc tải project
```bash
git clone <repository-url>
cd student-management
```

### Bước 2: Tạo môi trường ảo (Virtual Environment)

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### Bước 3: Cài đặt thư viện
```bash
pip install -r requirements.txt
```

### Bước 4: Cấu hình Database

#### Nếu dùng PostgreSQL:

1. Cài đặt PostgreSQL
2. Tạo database mới:
```sql
CREATE DATABASE student_db;
```

3. Tạo file `.env` trong thư mục gốc:
```env
DATABASE_URL=postgresql://username:password@localhost:5432/student_db
```

#### Nếu dùng MySQL:

1. Cài đặt MySQL
2. Tạo database mới:
```sql
CREATE DATABASE student_db;
```

3. Tạo file `.env`:
```env
DATABASE_URL=mysql+pymysql://username:password@localhost:3306/student_db
```

**⚠️ Lưu ý**: Thay `username` và `password` bằng thông tin database của bạn

### Bước 5: Chạy server
```bash
cd app
uvicorn main:app --reload
```

hoặc từ thư mục gốc:
```bash
uvicorn app.main:app --reload
```

Server sẽ chạy tại: **http://127.0.0.1:8000**

### Bước 6: Truy cập Swagger UI

Mở trình duyệt và truy cập:
- **Swagger UI**: http://127.0.0.1:8000/docs
- **ReDoc**: http://127.0.0.1:8000/redoc

---

## 📡 API ENDPOINTS

### 1. Thêm sinh viên mới

**Endpoint**: `POST /students`

**Request Body**:
```json
{
  "name": "Nguyễn Văn A",
  "email": "nguyenvana@example.com",
  "phone": "0901234567",
  "major": "Công nghệ thông tin",
  "gpa": 3.5
}
```

**Response Success (201)**:
```json
{
  "id": 1,
  "name": "Nguyễn Văn A",
  "email": "nguyenvana@example.com",
  "phone": "0901234567",
  "major": "Công nghệ thông tin",
  "gpa": 3.5,
  "created_at": "2025-11-04T10:30:00"
}
```

**Response Error (400)**:
```json
{
  "detail": "Email already exists"
}
```

---

### 2. Lấy danh sách sinh viên (có phân trang)

**Endpoint**: `GET /students?page=1&limit=10`

**Query Parameters**:
- `page` (integer, optional): Số trang, mặc định = 1
- `limit` (integer, optional): Số lượng sinh viên mỗi trang, mặc định = 10

**Response Success (200)**:
```json
{
  "total": 50,
  "page": 1,
  "limit": 10,
  "total_pages": 5,
  "data": [
    {
      "id": 1,
      "name": "Nguyễn Văn A",
      "email": "nguyenvana@example.com",
      "phone": "0901234567",
      "major": "Công nghệ thông tin",
      "gpa": 3.5,
      "created_at": "2025-11-04T10:30:00"
    },
    {
      "id": 2,
      "name": "Trần Thị B",
      "email": "tranthib@example.com",
      "phone": "0907654321",
      "major": "Kỹ thuật phần mềm",
      "gpa": 3.8,
      "created_at": "2025-11-04T11:00:00"
    }
  ]
}
```

---

### 3. Xem chi tiết 1 sinh viên

**Endpoint**: `GET /students/{id}`

**Path Parameters**:
- `id` (integer): ID của sinh viên

**Response Success (200)**:
```json
{
  "id": 1,
  "name": "Nguyễn Văn A",
  "email": "nguyenvana@example.com",
  "phone": "0901234567",
  "major": "Công nghệ thông tin",
  "gpa": 3.5,
  "created_at": "2025-11-04T10:30:00"
}
```

**Response Error (404)**:
```json
{
  "detail": "Student not found"
}
```

---

### 4. Cập nhật thông tin sinh viên

**Endpoint**: `PUT /students/{id}`

**Path Parameters**:
- `id` (integer): ID của sinh viên

**Request Body** (có thể update một phần hoặc toàn bộ):
```json
{
  "name": "Nguyễn Văn A Updated",
  "email": "nguyenvana.new@example.com",
  "phone": "0909999999",
  "major": "An toàn thông tin",
  "gpa": 3.7
}
```

**Response Success (200)**:
```json
{
  "id": 1,
  "name": "Nguyễn Văn A Updated",
  "email": "nguyenvana.new@example.com",
  "phone": "0909999999",
  "major": "An toàn thông tin",
  "gpa": 3.7,
  "created_at": "2025-11-04T10:30:00"
}
```

**Response Error (404)**:
```json
{
  "detail": "Student not found"
}
```

---

### 5. Xóa sinh viên

**Endpoint**: `DELETE /students/{id}`

**Path Parameters**:
- `id` (integer): ID của sinh viên

**Response Success (200)**:
```json
{
  "message": "Student deleted successfully"
}
```

**Response Error (404)**:
```json
{
  "detail": "Student not found"
}
```

---

## ✅ VALIDATION RULES

Hệ thống sẽ tự động kiểm tra và trả về lỗi nếu:

| Trường hợp | HTTP Code | Error Message |
|------------|-----------|---------------|
| Email không đúng định dạng | 422 | "Invalid email format" |
| Email đã tồn tại | 400 | "Email already exists" |
| GPA < 0 hoặc > 4 | 422 | "GPA must be between 0 and 4" |
| Name trống | 422 | "Name is required" |
| Email trống | 422 | "Email is required" |
| Major trống | 422 | "Major is required" |
| GPA không phải số | 422 | "GPA must be a number" |

---

## 🧪 TEST API

### Sử dụng Swagger UI (Khuyến nghị cho người mới)

1. Truy cập: http://127.0.0.1:8000/docs
2. Click vào endpoint muốn test
3. Click "Try it out"
4. Điền dữ liệu vào form
5. Click "Execute"
6. Xem kết quả ở phần Response

### Sử dụng Postman

1. Import collection hoặc tạo request mới
2. Đặt URL: `http://127.0.0.1:8000/students`
3. Chọn Method (GET, POST, PUT, DELETE)
4. Điền Body (nếu là POST/PUT)
5. Click Send

### Sử dụng cURL (Command line)

**Thêm sinh viên mới**:
```bash
curl -X POST "http://127.0.0.1:8000/students" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Nguyễn Văn A",
    "email": "nguyenvana@example.com",
    "phone": "0901234567",
    "major": "Công nghệ thông tin",
    "gpa": 3.5
  }'
```

**Lấy danh sách sinh viên**:
```bash
curl -X GET "http://127.0.0.1:8000/students?page=1&limit=10"
```

**Xem chi tiết sinh viên**:
```bash
curl -X GET "http://127.0.0.1:8000/students/1"
```

**Cập nhật sinh viên**:
```bash
curl -X PUT "http://127.0.0.1:8000/students/1" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Nguyễn Văn A Updated",
    "gpa": 3.7
  }'
```

**Xóa sinh viên**:
```bash
curl -X DELETE "http://127.0.0.1:8000/students/1"
```

---

## 📦 FILE REQUIREMENTS.TXT
```txt
fastapi==0.104.1
uvicorn[standard]==0.24.0
sqlalchemy==2.0.23
pydantic==2.5.0
pydantic-settings==2.1.0
python-dotenv==1.0.0

# Chọn 1 trong 2 database driver:
psycopg2-binary==2.9.9     # Cho PostgreSQL
# pymysql==1.1.0           # Cho MySQL (bỏ comment nếu dùng MySQL)
```

---

## 🌟 BONUS FEATURES (TÙY CHỌN)

### Bonus 1: Tìm kiếm sinh viên ⭐⭐

**Endpoint**: `GET /students/search?keyword=nguyen`

**Query Parameters**:
- `keyword` (string): Từ khóa tìm kiếm (tìm trong tên)

**Response**:
```json
{
  "total": 5,
  "data": [
    {
      "id": 1,
      "name": "Nguyễn Văn A",
      "email": "nguyenvana@example.com",
      ...
    }
  ]
}
```

**Gợi ý cài đặt**:
- Sử dụng SQL LIKE hoặc ILIKE
- Không phân biệt hoa thường

---

### Bonus 2: Export danh sách ra CSV ⭐⭐⭐

**Endpoint**: `GET /students/export`

**Response**: File CSV download

**Gợi ý cài đặt**:
- Sử dụng thư viện `csv` của Python
- Set header `Content-Disposition: attachment; filename=students.csv`
- Return `StreamingResponse`

**Thêm vào requirements.txt**:
```txt
aiofiles==23.2.1
```

---

### Bonus 3: Quản lý môn học ⭐⭐⭐⭐

#### Thêm 2 bảng mới:

**Bảng `courses`**:
| Cột | Kiểu | Ràng buộc |
|-----|------|-----------|
| id | Integer | PRIMARY KEY |
| course_name | String(100) | NOT NULL |
| course_code | String(20) | UNIQUE, NOT NULL |
| credits | Integer | NOT NULL |
| created_at | DateTime | DEFAULT NOW() |

**Bảng `enrollments`**:
| Cột | Kiểu | Ràng buộc |
|-----|------|-----------|
| id | Integer | PRIMARY KEY |
| student_id | Integer | FOREIGN KEY → students.id |
| course_id | Integer | FOREIGN KEY → courses.id |
| enrolled_at | DateTime | DEFAULT NOW() |

#### API endpoints mới:

1. `POST /courses` - Thêm môn học
2. `GET /courses` - Danh sách môn học
3. `GET /courses/{id}` - Chi tiết môn học
4. `POST /students/{student_id}/enroll/{course_id}` - Đăng ký môn
5. `GET /students/{student_id}/courses` - Xem môn đã đăng ký
6. `DELETE /students/{student_id}/enroll/{course_id}` - Hủy đăng ký

---

## 📊 TIÊU CHÍ ĐÁNH GIÁ

| Hạng mục | Điểm | Mô tả |
|----------|------|-------|
| **Code chạy được không lỗi** | 30đ | Server khởi động thành công, không crash |
| **5 API hoạt động đúng** | 30đ | CRUD đầy đủ, đúng HTTP methods |
| **Validation đầy đủ** | 15đ | Kiểm tra email, GPA, trùng lặp |
| **Cấu trúc project** | 10đ | Tách file rõ ràng, tuân thủ quy chuẩn |
| **README & Comments** | 10đ | Hướng dẫn đầy đủ, code có giải thích |
| **Error handling** | 5đ | Xử lý lỗi đúng, HTTP status codes phù hợp |
| **Bonus 1: Search** | +5đ | Tìm kiếm hoạt động tốt |
| **Bonus 2: Export CSV** | +10đ | Export đúng format, download OK |
| **Bonus 3: Courses** | +15đ | Đầy đủ CRUD courses & enrollments |

**Tổng điểm tối đa**: 100 + 30 (bonus) = 130 điểm

**Phân loại**:
- 🥉 Đạt: ≥ 70 điểm
- 🥈 Khá: ≥ 80 điểm
- 🥇 Giỏi: ≥ 90 điểm
- 🏆 Xuất sắc: ≥ 100 điểm (có bonus)

---

## 📅 LỘ TRÌNH HỌC TẬP (6 NGÀY)

### 📘 Ngày 1: Setup môi trường
- [ ] Cài Python, PostgreSQL/MySQL
- [ ] Tạo virtual environment
- [ ] Cài đặt thư viện
- [ ] Tạo database
- [ ] Test kết nối database thành công

**Mục tiêu**: Chạy được FastAPI hello world

---

### 📗 Ngày 2: Database Models
- [ ] Tạo file `models.py` - định nghĩa bảng students
- [ ] Tạo file `database.py` - kết nối database
- [ ] Chạy script tạo bảng trong database
- [ ] Insert thử 2-3 sinh viên bằng SQL

**Mục tiêu**: Database có bảng students và dữ liệu mẫu

---

### 📙 Ngày 3: Schemas & CRUD
- [ ] Tạo file `schemas.py` - Pydantic models
- [ ] Tạo file `crud.py` - Viết hàm create_student, get_students
- [ ] Test CRUD functions riêng lẻ

**Mục tiêu**: Có thể thêm và lấy sinh viên từ database

---

### 📕 Ngày 4: API Endpoints (Part 1)
- [ ] Tạo file `main.py`
- [ ] Viết API: POST /students (thêm sinh viên)
- [ ] Viết API: GET /students (lấy danh sách + phân trang)
- [ ] Test 2 API này bằng Swagger UI

**Mục tiêu**: 2 API đầu tiên hoạt động

---

### 📓 Ngày 5: API Endpoints (Part 2) & Validation
- [ ] Viết API: GET /students/{id}
- [ ] Viết API: PUT /students/{id}
- [ ] Viết API: DELETE /students/{id}
- [ ] Thêm validation: email format, GPA range, unique email
- [ ] Xử lý lỗi 404, 400

**Mục tiêu**: Đủ 5 API + validation hoàn chỉnh

---

### 📔 Ngày 6: Hoàn thiện & Bonus
- [ ] Test lại toàn bộ API
- [ ] Fix bugs (nếu có)
- [ ] Viết README đầy đủ
- [ ] Thêm comments vào code
- [ ] Làm bonus (nếu còn thời gian)
- [ ] Quay video demo
- [ ] Push code lên GitHub

**Mục tiêu**: Hoàn thành project, sẵn sàng nộp bài

---

## 🐛 TROUBLESHOOTING (XỬ LÝ LỖI THƯỜNG GẶP)

### Lỗi: `ModuleNotFoundError: No module named 'fastapi'`
**Giải pháp**:
```bash
pip install -r requirements.txt
```

### Lỗi: `Could not connect to database`
**Giải pháp**:
1. Kiểm tra PostgreSQL/MySQL đã chạy chưa
2. Kiểm tra thông tin trong file `.env`
3. Kiểm tra database đã được tạo chưa

### Lỗi: `Table doesn't exist`
**Giải pháp**:
- Chạy lại script tạo bảng
- Hoặc thêm vào `main.py`:
```python
from app.database import engine
from app.models import Base

@app.on_event("startup")
def startup():
    Base.metadata.create_all(bind=engine)
```

### Lỗi: `422 Unprocessable Entity`
**Giải pháp**:
- Kiểm tra dữ liệu gửi lên có đúng format không
- Xem chi tiết lỗi trong response body

---

## 📚 TÀI LIỆU THAM KHẢO

### Documentation chính thức:
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [Pydantic Documentation](https://docs.pydantic.dev/)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)

### Video tutorials (tiếng Việt):
- FastAPI cơ bản: Search "FastAPI tutorial tiếng Việt" trên YouTube
- SQLAlchemy ORM: Search "Python SQLAlchemy" trên YouTube

### Bài viết hay:
- [Real Python - FastAPI Tutorial](https://realpython.com/fastapi-python-web-apis/)
- [FastAPI Best Practices](https://github.com/zhanymkanov/fastapi-best-practices)

---

## ⚠️ LƯU Ý QUAN TRỌNG

### ❌ KHÔNG ĐƯỢC:
- Copy nguyên xi code từ GitHub hoặc tutorial
- Sử dụng ChatGPT/AI để generate toàn bộ code
- Nộp bài trễ deadline
- Fake commit history
- Để lộ password database trong code

### ✅ NÊN LÀM:
- Tự viết code, có thể tham khảo document
- Commit code thường xuyên (mỗi tính năng mới)
- Test kỹ từng API trước khi làm tiếp
- Viết code sạch, dễ đọc
- Đặt tên biến có ý nghĩa
- Thêm comments giải thích logic phức tạp
- Hỏi khi thực sự bị kẹt (sau khi đã research)

### 📝 FILE .gitignore:
```
# File này để git không track những file không cần thiết
__pycache__/
*.pyc
.env
venv/
.vscode/
.idea/
*.db
*.sqlite3
```

---

## 📬 CÁCH NỘP BÀI

### Bước 1: Push code lên GitHub
```bash
git init
git add .
git commit -m "Complete student management API"
git branch -M main
git remote add origin <your-repo-url>
git push -u origin main
```

### Bước 2: Tạo video demo (3-5 phút)
Quay màn hình demo:
1. Chạy server
2. Mở Swagger UI
3. Test từng API (POST, GET, PUT, DELETE)
4. Show validation errors
5. Show database có dữ liệu

**Tools quay màn hình**: OBS Studio, Loom, hoặc quay bằng điện thoại

### Bước 3: Nộp bài
Gửi email hoặc message gồm:
- Link GitHub repository (public)
- Link video demo (YouTube/Google Drive)
- File README.md

**Deadline**: 23:59 ngày thứ 6

---

## 🎓 LỜI KHUYÊN

> **"Code không chạy được 1 lần = bình thường. Code không chạy được 10 lần = debug skills đang phát triển. Code chạy được ngay lần đầu = bạn đang làm bài tập quá dễ!"**

Khi gặp lỗi:
1. **Đọc kỹ error message** - 80% lỗi đã nói rõ vấn đề
2. **Google error message** - thêm "python" hoặc "fastapi" vào search
3. **Kiểm tra lại code** - typo, thiếu dấu, indent sai
4. **Debug bằng print()** - in ra giá trị biến để xem
5. **Hỏi người khác** - sau khi đã thử 4 bước trên

**Chìa khóa thành công**: Kiên trì + Tự research + Practice

---

## 🏆 CHECKLIST TRƯỚC KHI NỘP BÀI

- [ ] Code chạy được không lỗi
- [ ] 5 API hoạt động đúng
- [ ] Validation đầy đủ
- [ ] Database có dữ liệu test
- [ ] README đầy đủ hướng dẫn
- [ ] Code có comments
- [ ] File .env không bị commit
- [ ] requirements.txt đầy đủ
- [ ] Video demo rõ ràng
- [ ] GitHub repository là public
- [ ] Đã test lại toàn bộ trên máy khác (nếu có thể)

---

## 💬 HỖ TRỢ

Nếu gặp khó khăn:
1. Đọc lại phần Troubleshooting
2. Google error message
3. Hỏi trong group chat
4. Liên hệ mentor/teacher

**Nhớ**: Học lập trình là quá trình, không phải đích đến. Mỗi lỗi bạn gặp là một bài học quý giá!

---

## 📄 LICENSE

Bài tập này được tạo ra cho mục đích học tập. Bạn có thể tự do sử dụng, sửa đổi và chia sẻ.

---

**CHÚC BẠN HỌC TỐT VÀ CODING VUI VẺ!** 🚀💻

**"The only way to learn programming is by writing code!"**

---

*README version: 1.0*  
*Last updated: 04/11/2025*
