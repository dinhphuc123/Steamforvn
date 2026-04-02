# genai-agents-for-teachers
In this repos, we have implemented examples of AI Agents interfaced with various GenAI services

## Dữ Liệu
Để phục vụ cho việc tạo RAG Agent, chúng ta sẽ sử dụng 1 file pdf có ví dụ nội dung SGK. Chúng ta sẽ xử lý các file này, biến các nội dung hình ảnh hoặc chữ viết thành dạng dữ liệu máy tính có thể xử lý được. Trong buổi office hour, các thầy cô sẽ được cung cấp một Vector Database (Cơ sở dữ liệu cho Véc-tơ). Trong Cơ sở dữ liệu nêu trên, chúng ta đã có sẵn nội dung SGK được biến tấu thành Véc-tơ, sẵn sàng cho chúng ta sử dụng.

Ví dụ: [place holder]

**Ở mục `data`, chúng ta có sẵn một file pdf đã được tạo ra vởi Gen AI từ lesson 4 để phục vụ cho mục đích chạy thử. Các bạn có thể tuỳ biến thay đổi**

## Các thành phần Agents




## App tạo mảnh ghép toán học

Để tạo phiếu mảnh ghép tương tự hình mẫu, chạy app Streamlit:

```bash
streamlit run apps/puzzle_generator_app.py
```

Tính năng chính:
- Chỉnh sửa 8 ô nội dung (7 ô xung quanh + 1 ô trung tâm).
- Chỉnh nhãn cho các đường nối.
- Tuỳ chỉnh màu từng ô.
- Xuất ảnh PNG để in hoặc chèn vào tài liệu.


### Web app (Flask)

Nếu bạn muốn chạy bản web app thuần (không dùng Streamlit):

```bash
python apps/puzzle_web_app.py
```

Mở trình duyệt tại `http://127.0.0.1:5000`.
