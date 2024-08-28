# Hướng dẫn sử dụng

Hướng dẫn này cho bạn thấy từng bước cách sử dụng **FastAPI** đa số các tính năng của nó.

Mỗi phần được xây dựng từ những phần trước đó, nhưng nó được cấu trúc thành các chủ đề riêng biệt, do đó bạn có thể xem trực tiếp từng phần cụ thể bất kì để giải quyết những API cụ thể mà bạn cần.

Nó cũng được xây dựng để làm việc như một tham chiếu trong tương lai.

Do đó bạn có thể quay lại và tìm chính xác những gì bạn cần.

## Chạy mã

Tất cả các code block có thể được sao chép và sử dụng trực tiếp (chúng thực chất là các tệp tin Python đã được kiểm thử).

Để chạy bất kì ví dụ nào, sao chép code tới tệp tin `main.py`, và bắt đầu `uvicorn` với:

<div class="termy">

```console
$ uvicorn main:app --reload

<span style="color: green;">INFO</span>:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
<span style="color: green;">INFO</span>:     Started reloader process [28720]
<span style="color: green;">INFO</span>:     Started server process [28722]
<span style="color: green;">INFO</span>:     Waiting for application startup.
<span style="color: green;">INFO</span>:     Application startup complete.
```

</div>

**Khuyến khích** bạn viết hoặc sao chép code, sửa và chạy nó ở local.

Sử dụng nó trong trình soạn thảo của bạn thực sự cho bạn thấy những lợi ích của FastAPI, thấy được cách bạn viết code ít hơn, tất cả đều được type check, autocompletion,...

---

## Cài đặt FastAPI

Bước đầu tiên là cài đặt FastAPI.

Với hướng dẫn này, bạn có thể muốn cài đặt nó với tất cả các phụ thuộc và tính năng tùy chọn:

<div class="termy">

```console
$ pip install "fastapi[all]"

---> 100%
```

</div>

...dó cũng bao gồm `uvicorn`, bạn có thể sử dụng như một server để chạy code của bạn.

/// note

Bạn cũng có thể cài đặt nó từng phần.

Đây là những gì bạn có thể sẽ làm một lần duy nhất bạn muốn triển khai ứng dụng của bạn lên production:

```
pip install fastapi
```

Cũng cài đặt `uvicorn` để làm việc như một server:

```
pip install "uvicorn[standard]"
```

Và tương tự với từng phụ thuộc tùy chọn mà bạn muốn sử dụng.

///

## Hướng dẫn nâng cao

Cũng có một **Hướng dẫn nâng cao** mà bạn có thể đọc nó sau **Hướng dẫn sử dụng**.

**Hướng dẫn sử dụng nâng cao**, xây dựng dựa trên cái này, sử dụng các khái niệm tương tự, và dạy bạn những tính năng mở rộng.

Nhưng bạn nên đọc **Hướng dẫn sử dụng** đầu tiên (những gì bạn đang đọc).

Nó được thiết kế do đó bạn có thể xây dựng một ứng dụng hoàn chỉnh chỉ với **Hướng dẫn sử dụng**, và sau đó mở rộng nó theo các cách khác nhau, phụ thuộc vào những gì bạn cần, sử dụng một vài ý tưởng bổ sung từ **Hướng dẫn sử dụng nâng cao**.
