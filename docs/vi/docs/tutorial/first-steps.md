# Những bước đầu tiên

Tệp tin FastAPI đơn giản nhất có thể trông như này:

{* ../../docs_src/first_steps/tutorial001.py *}

Sao chép sang một tệp tin `main.py`.

Chạy live server:

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

/// note

Câu lệnh `uvicorn main:app` được giải thích như sau:

* `main`: tệp tin `main.py` (một Python "mô đun").
* `app`: một object được tạo ra bên trong `main.py` với dòng `app = FastAPI()`.
* `--reload`: làm server khởi động lại sau mỗi lần thay đổi. Chỉ sử dụng trong môi trường phát triển.

///

Trong output, có một dòng giống như:

```hl_lines="4"
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

Dòng đó cho thấy URL, nơi mà app của bạn đang được chạy, trong máy local của bạn.

### Kiểm tra

Mở trình duyệt của bạn tại <a href="http://127.0.0.1:8000" class="external-link" target="_blank">http://127.0.0.1:8000</a>.

Bạn sẽ thấy một JSON response như:

```JSON
{"message": "Hello World"}
```

### Tài liệu tương tác API

Bây giờ tới <a href="http://127.0.0.1:8000/docs" class="external-link" target="_blank">http://127.0.0.1:8000/docs</a>.

Bạn sẽ thấy một tài liệu tương tác API (cung cấp bởi <a href="https://github.com/swagger-api/swagger-ui" class="external-link" target="_blank">Swagger UI</a>):

![Swagger UI](https://fastapi.tiangolo.com/img/index/index-01-swagger-ui-simple.png)

### Phiên bản thay thế của tài liệu API

Và bây giờ tới <a href="http://127.0.0.1:8000/redoc" class="external-link" target="_blank">http://127.0.0.1:8000/redoc</a>.

Bạn sẽ thấy một bản thay thế của tài liệu (cung cấp bởi <a href="https://github.com/Rebilly/ReDoc" class="external-link" target="_blank">ReDoc</a>):

![ReDoc](https://fastapi.tiangolo.com/img/index/index-02-redoc-simple.png)

### OpenAPI

**FastAPI** sinh một "schema" với tất cả API của bạn sử dụng tiêu chuẩn **OpenAPI** cho định nghĩa các API.

#### "Schema"

Một "schema" là một định nghĩa hoặc mô tả thứ gì đó. Không phải code triển khai của nó, nhưng chỉ là một bản mô tả trừu tượng.

#### API "schema"

Trong trường hợp này, <a href="https://github.com/OAI/OpenAPI-Specification" class="external-link" target="_blank">OpenAPI</a> là một bản mô tả bắt buộc cơ chế định nghĩa API của bạn.

Định nghĩa cấu trúc này bao gồm những đường dẫn API của bạn, các tham số có thể có,...

#### "Cấu trúc" dữ liệu

Thuật ngữ "cấu trúc" (schema) cũng có thể được coi như là hình dạng của dữ liệu, tương tự như một JSON content.

Trong trường hợp đó, nó có nghĩa là các thuộc tính JSON và các kiểu dữ liệu họ có,...

#### OpenAPI và JSON Schema

OpenAPI định nghĩa một cấu trúc API cho API của bạn. Và cấu trúc đó bao gồm các dịnh nghĩa (or "schema") về dữ liệu được gửi đi và nhận về bởi API của bạn, sử dụng **JSON Schema**, một tiêu chuẩn cho cấu trúc dữ liệu JSON.

#### Kiểm tra `openapi.json`

Nếu bạn tò mò về việc cấu trúc OpenAPI nhìn như thế nào thì FastAPI tự động sinh một JSON (schema) với các mô tả cho tất cả API của bạn.

Bạn có thể thấy nó trực tiếp tại: <a href="http://127.0.0.1:8000/openapi.json" class="external-link" target="_blank">http://127.0.0.1:8000/openapi.json</a>.

Nó sẽ cho thấy một JSON bắt đầu giống như:

```JSON
{
    "openapi": "3.1.0",
    "info": {
        "title": "FastAPI",
        "version": "0.1.0"
    },
    "paths": {
        "/items/": {
            "get": {
                "responses": {
                    "200": {
                        "description": "Successful Response",
                        "content": {
                            "application/json": {



...
```

#### OpenAPI dùng để làm gì?

Cấu trúc OpenAPI là sức mạnh của tài liệu tương tác.

Và có hàng tá các bản thay thế, tất cả đều dựa trên OpenAPI. Bạn có thể dễ dàng thêm bất kì bản thay thế bào cho ứng dụng của bạn được xây dựng với **FastAPI**.

Bạn cũng có thể sử dụng nó để sinh code tự động, với các client giao viết qua API của bạn. Ví dụ, frontend, mobile hoặc các ứng dụng IoT.

## Tóm lại, từng bước một

### Bước 1: import `FastAPI`

{* ../../docs_src/first_steps/tutorial001.py hl[1] *}

`FastAPI` là một Python class cung cấp tất cả chức năng cho API của bạn.

/// note | Chi tiết kĩ thuật

`FastAPI` là một class kế thừa trực tiếp `Starlette`.

Bạn cũng có thể sử dụng tất cả <a href="https://www.starlette.dev/" class="external-link" target="_blank">Starlette</a> chức năng với `FastAPI`.

///

### Bước 2: Tạo một `FastAPI` "instance"

{* ../../docs_src/first_steps/tutorial001.py hl[3] *}

Biến `app` này là một "instance" của class `FastAPI`.

Đây sẽ là điểm cốt lõi để tạo ra tất cả API của bạn.

`app` này chính là điều được nhắc tới bởi `uvicorn` trong câu lệnh:

<div class="termy">

```console
$ uvicorn main:app --reload

<span style="color: green;">INFO</span>:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

</div>

Nếu bạn tạo ứng dụng của bạn giống như:

{* ../../docs_src/first_steps/tutorial002.py hl[3] *}

Và đặt nó trong một tệp tin `main.py`, sau đó bạn sẽ gọi `uvicorn` giống như:

<div class="termy">

```console
$ uvicorn main:my_awesome_api --reload

<span style="color: green;">INFO</span>:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

</div>

### Bước 3: tạo một *đường dẫn toán tử*

#### Đường dẫn

"Đường dẫn" ở đây được nhắc tới là phần cuối cùng của URL bắt đầu từ `/`.

Do đó, trong một URL nhìn giống như:

```
https://example.com/items/foo
```

...đường dẫn sẽ là:

```
/items/foo
```

/// info

Một đường dẫn cũng là một cách gọi chung cho một "endpoint" hoặc một "route".

///

Trong khi xây dựng một API, "đường dẫn" là các chính để phân tách "mối quan hệ" và "tài nguyên".

#### Toán tử (Operation)

"Toán tử" ở đây được nhắc tới là một trong các "phương thức" HTTP.

Một trong những:

* `POST`
* `GET`
* `PUT`
* `DELETE`

...và một trong những cái còn lại:

* `OPTIONS`
* `HEAD`
* `PATCH`
* `TRACE`

Trong giao thức HTTP, bạn có thể giao tiếp trong mỗi đường dẫn sử dụng một (hoặc nhiều) trong các "phương thức này".

---

Khi xây dựng các API, bạn thường sử dụng cụ thể các phương thức HTTP này để thực hiện một hành động cụ thể.

Thông thường, bạn sử dụng

* `POST`: để tạo dữ liệu.
* `GET`: để đọc dữ liệu.
* `PUT`: để cập nhật dữ liệu.
* `DELETE`: để xóa dữ liệu.

Do đó, trong OpenAPI, mỗi phương thức HTTP được gọi là một "toán tử (operation)".

Chúng ta cũng sẽ gọi chúng là "**các toán tử**".

#### Định nghĩa moojt *decorator cho đường dẫn toán tử*

{* ../../docs_src/first_steps/tutorial001.py hl[6] *}

`@app.get("/")` nói **FastAPI** rằng hàm bên dưới có trách nhiệm xử lí request tới:

* đường dẫn `/`
* sử dụng một <abbr title="an HTTP GET method">toán tử<code>get</code></abbr>

/// info | Thông tin về "`@decorator`"

Cú pháp `@something` trong Python được gọi là một "decorator".

Bạn đặt nó trên một hàm. Giống như một chiếc mũ xinh xắn (Tôi ddonas đó là lí do mà thuật ngữ này ra đời).

Một "decorator" lấy một hàm bên dưới và thực hiện một vài thứ với nó.

Trong trường hợp của chúng ta, decorator này nói **FastAPI** rằng hàm bên dưới ứng với **đường dẫn** `/` và một **toán tử** `get`.

Nó là một "**decorator đường dẫn toán tử**".

///

Bạn cũng có thể sử dụng với các toán tử khác:

* `@app.post()`
* `@app.put()`
* `@app.delete()`

Và nhiều hơn với các toán tử còn lại:

* `@app.options()`
* `@app.head()`
* `@app.patch()`
* `@app.trace()`

/// tip

Bạn thoải mái sử dụng mỗi toán tử (phương thức HTTP) như bạn mơ ước.

**FastAPI** không bắt buộc bất kì ý nghĩa cụ thể nào.

Thông tin ở đây được biểu thị như là một chỉ dẫn, không phải là một yêu cầu bắt buộc.

Ví dụ, khi sử dụng GraphQL bạn thông thường thực hiện tất cả các hành động chỉ bằng việc sử dụng các toán tử `POST`.

///

### Step 4: Định nghĩa **hàm cho đường dẫn toán tử**

Đây là "**hàm cho đường dẫn toán tử**":

* **đường dẫn**: là `/`.
* **toán tử**: là `get`.
* **hàm**: là hàm bên dưới "decorator" (bên dưới `@app.get("/")`).

{* ../../docs_src/first_steps/tutorial001.py hl[7] *}

Đây là một hàm Python.

Nó sẽ được gọi bởi **FastAPI** bất cứ khi nào nó nhận một request tới URL "`/`" sử dụng một toán tử `GET`.

Trong trường hợp này, nó là một hàm `async`.

---

Bạn cũng có thể định nghĩa nó như là một hàm thông thường thay cho `async def`:

{* ../../docs_src/first_steps/tutorial003.py hl[7] *}

/// note

Nếu bạn không biết sự khác nhau, kiểm tra [Async: *"Trong khi vội vàng?"*](../async.md#in-a-hurry){.internal-link target=_blank}.

///

### Bước 5: Nội dung trả về

{* ../../docs_src/first_steps/tutorial001.py hl[8] *}

Bạn có thể trả về một `dict`, `list`, một trong những giá trị đơn như `str`, `int`,...

Bạn cũng có thể trả về Pydantic model (bạn sẽ thấy nhiều hơn về nó sau).

Có nhiều object và model khác nhau sẽ được tự động chuyển đổi sang JSON (bao gồm cả ORM,...). Thử sử dụng loại ưa thích của bạn, nó có khả năng cao đã được hỗ trợ.

## Tóm lại

* Import `FastAPI`.
* Tạo một `app` instance.
* Viết một **decorator cho đường dẫn toán tử** (giống như `@app.get("/")`).
* Viết một **hàm cho đường dẫn toán tử** (giống như  `def root(): ...` ở trên).
* Chạy server trong môi trường phát triển (giống như `uvicorn main:app --reload`).
