# Tính năng

## Tính năng của FastAPI

**FastAPI** cho bạn những tính năng sau:

### Dựa trên những tiêu chuẩn mở

* <a href="https://github.com/OAI/OpenAPI-Specification" class="external-link" target="_blank"><strong>OpenAPI</strong></a> cho việc tạo API, bao gồm những khai báo về <abbr title="cũng được biết đến như: endpoints, routes">đường dẫn</abbr> <abbr title="cũng được biết đến như các phương thức HTTP, như POST, GET, PUT, DELETE"> các toán tử</abbr>, tham số, body requests, cơ chế bảo mật, etc.
* Tự động tài liệu hóa data model theo <a href="https://json-schema.org/" class="external-link" target="_blank"><strong>JSON Schema</strong></a> (OpenAPI bản thân nó được dựa trên JSON Schema).
* Được thiết kế xung quanh các tiêu chuẩn này sau khi nghiên cứu tỉ mỉ thay vì chỉ suy nghĩ đơn giản và sơ xài.
* Điều này cho phép tự động hóa **trình sinh code client** cho nhiều ngôn ngữ lập trình khác nhau.

### Tự động hóa tài liệu


Tài liệu tương tác API và web giao diện người dùng. Là một framework được dựa trên OpenAPI do đó có nhiều tùy chọn giao diện cho tài liệu API, 2 giao diện bên dưới là mặc định.

* <a href="https://github.com/swagger-api/swagger-ui" class="external-link" target="_blank"><strong>Swagger UI</strong></a>, với giao diện khám phá, gọi và kiểm thử API trực tiếp từ trình duyệt.

![Swagger UI interaction](https://fastapi.tiangolo.com/img/index/index-03-swagger-02.png)

* Thay thế với tài liệu API với <a href="https://github.com/Rebilly/ReDoc" class="external-link" target="_blank"><strong>ReDoc</strong></a>.

![ReDoc](https://fastapi.tiangolo.com/img/index/index-06-redoc-02.png)

### Chỉ cần phiên bản Python hiện đại

Tất cả được dựa trên khai báo kiểu dữ liệu chuẩn của **Python 3.6** (cảm ơn Pydantic). Bạn không cần học cú pháp mới, chỉ cần biết chuẩn Python hiện đại.

Nếu bạn cần 2 phút để làm mới lại cách sử dụng các kiểu dữ liệu mới của Python (thậm chí nếu bạn không sử dụng FastAPI), xem hướng dẫn ngắn: [Kiểu dữ liệu Python](python-types.md){.internal-link target=_blank}.

Bạn viết chuẩn Python với kiểu dữ liệu như sau:

```Python
from datetime import date

from pydantic import BaseModel

# Declare a variable as a str
# and get editor support inside the function
def main(user_id: str):
    return user_id


# A Pydantic model
class User(BaseModel):
    id: int
    name: str
    joined: date
```

Sau đó có thể được sử dụng:

```Python
my_user: User = User(id=3, name="John Doe", joined="2018-07-19")

second_user_data = {
    "id": 4,
    "name": "Mary",
    "joined": "2018-11-30",
}

my_second_user: User = User(**second_user_data)
```

!!! info
    `**second_user_data` nghĩa là:

    Truyền các khóa và giá trị của dict `second_user_data` trực tiếp như các tham số kiểu key-value, tương đương với: `User(id=4, name="Mary", joined="2018-11-30")`

### Được hỗ trợ từ các trình soạn thảo


Toàn bộ framework được thiết kế để sử dụng dễ dàng và trực quan, toàn bộ quyết định đã được kiểm thử trên nhiều trình soạn thảo thậm chí trước khi bắt đầu quá trình phát triển, để chắc chắn trải nghiệm phát triển là tốt nhất.

Trong lần khảo sát cuối cùng dành cho các lập trình viên Python, đã rõ ràng <a href="https://www.jetbrains.com/research/python-developers-survey-2017/#tools-and-features" class="external-link" target="_blank">rằng đa số các lập trình viên sử dụng tính năng "autocompletion"</a>.

Toàn bộ framework "FastAPI" phải đảm bảo rằng: autocompletion hoạt động ở mọi nơi. Bạn sẽ hiếm khi cần quay lại để đọc tài liệu.

Đây là các trình soạn thảo có thể giúp bạn:

* trong <a href="https://code.visualstudio.com/" class="external-link" target="_blank">Visual Studio Code</a>:

![editor support](https://fastapi.tiangolo.com/img/vscode-completion.png)

* trong <a href="https://www.jetbrains.com/pycharm/" class="external-link" target="_blank">PyCharm</a>:

![editor support](https://fastapi.tiangolo.com/img/pycharm-completion.png)

Bạn sẽ có được auto-completion trong code, thậm chí trước đó là không thể. Như trong ví dụ, khóa `price` bên trong một JSON (đó có thể được lồng nhau) đến từ một request.

Không còn nhập sai tên khóa, quay đi quay lại giữa các tài liệu hoặc cuộn lên cuộn xuống để tìm xem cuối cùng bạn đã sử dụng `username` hay `user_name`.

### Ngắn gọn

FastAPI có các giá trị mặc định hợp lý cho mọi thứ, với các cấu hình tùy chọn ở mọi nơi. Tất cả các tham số có thể được tinh chỉnh để thực hiện những gì bạn cần và để định nghĩa API bạn cần.

Nhưng mặc định, tất cả **đều hoạt động**.

### Validation

* Validation cho đa số (hoặc tất cả?) **các kiểu dữ liệu** Python, bao gồm:
    * JSON objects (`dict`).
    * Mảng JSON (`list`) định nghĩa kiểu dữ liệu từng phần tử.
    * Xâu (`str`), định nghĩa độ dài lớn nhất, nhỏ nhất.
    * Số (`int`, `float`) với các giá trị lớn nhất, nhỏ nhất, etc.

* Validation cho nhiều kiểu dữ liệu bên ngoài như:
    * URL.
    * Email.
    * UUID.
    * ...và nhiều cái khác.

Tất cả validation được xử lí bằng những thiết lập tốt và mạnh mẽ của **Pydantic**.

### Bảo mật và xác thực

Bảo mật và xác thực đã tích hợp mà không làm tổn hại tới cơ sở dữ liệu hoặc data models.

Tất cả cơ chế bảo mật định nghĩa trong OpenAPI, bao gồm:

* HTTP Basic.
* **OAuth2** (với **JWT tokens**). Xem hướng dẫn [OAuth2 with JWT](tutorial/security/oauth2-jwt.md){.internal-link target=_blank}.
* API keys in:
    * Headers.
    * Các tham số trong query string.
    * Cookies, etc.

Cộng với tất cả các tính năng bảo mật từ Starlette (bao gồm **session cookies**).

Tất cả được xây dựng dưới dạng các công cụ và thành phần có thể tái sử dụng, dễ dàng tích hợp với hệ thống, kho lưu trữ dữ liệu, cơ sở dữ liệu quan hệ và NoSQL của bạn,...

### Dependency Injection

FastAPI bao gồm một hệ thống <abbr title='cũng biết đến như là "components", "resources", "services", "providers"'><strong>Dependency Injection</strong></abbr> vô cùng dễ sử dụng nhưng vô cùng mạnh mẽ.

* Thậm chí, các dependency có thể có các dependency khác, tạo thành một phân cấp hoặc **"một đồ thị" của các dependency**.
* Tất cả **được xử lí tự động** bởi framework.
* Tất cả các dependency có thể yêu cầu dữ liệu từ request và **tăng cường các ràng buộc từ đường dẫn** và tự động tài liệu hóa.
* **Tự động hóa validation**, thậm chí với các tham số *đường dẫn* định nghĩa trong các dependency.
* Hỗ trợ hệ thống xác thực người dùng phức tạp, **các kết nối cơ sở dữ liệu**,...
* **Không làm tổn hại** cơ sở dữ liệu, frontends,... Nhưng dễ dàng tích hợp với tất cả chúng.

### Không giới hạn "plug-ins"

Hoặc theo một cách nào khác, không cần chúng, import và sử dụng code bạn cần.

Bất kì tích hợp nào được thiết kế để sử dụng đơn giản (với các dependency), đến nỗi bạn có thể tạo một "plug-in" cho ứng dụng của mình trong 2 dòng code bằng cách sử dụng cùng một cấu trúc và cú pháp được sử dụng cho *path operations* của bạn.

### Đã được kiểm thử

* 100% <abbr title=" Lượng code đã được kiểm thử tự động">test coverage</abbr>.
* 100% <abbr title="Python type annotations, với điều này trình soạn thảo của bạn và các công cụ bên ngoài có thể hỗ trợ bạn tốt hơn">type annotated</abbr> code base.
* Được sử dụng cho các ứng dụng sản phẩm.

## Tính năng của Starlette

`FastAPI` is thực sự là một sub-class của `Starlette`. Do đó, nếu bạn đã biết hoặc đã sử dụng Starlette, đa số các chức năng sẽ làm việc giống như vậy.

Với **FastAPI**, bạn có được tất cả những tính năng của **Starlette**:

* Hiệu năng thực sự ấn tượng. Nó là <a href="https://github.com/encode/starlette#performance" class="external-link" target="_blank">một trong nhưng framework Python nhanh nhất, khi so sánh với **NodeJS** và **Go**</a>.
* Hỗ trợ **WebSocket**.
* In-process background tasks.
* Startup and shutdown events.
* Client cho kiểm thử xây dựng trên HTTPX.
* **CORS**, GZip, Static Files, Streaming responses.
* Hỗ trợ **Session and Cookie**.
* 100% test coverage.
* 100% type annotated codebase.

## Tính năng của Pydantic

**FastAPI** tương thích đầy đủ với (và dựa trên) <a href="https://pydantic-docs.helpmanual.io" class="external-link" target="_blank"><strong>Pydantic</strong></a>. Do đó, bất kì code Pydantic nào bạn thêm vào cũng sẽ hoạt động.

Bao gồm các thư viện bên ngoài cũng dựa trên Pydantic, như <abbr title="Object-Relational Mapper">ORM</abbr>s, <abbr title="Object-Document Mapper">ODM</abbr>s cho cơ sở dữ liệu.

Nó cũng có nghĩa là trong nhiều trường hợp, bạn có thể truyền cùng object bạn có từ một request **trực tiếp cho cơ sở dữ liệu**, vì mọi thứ được validate tự động.

Điều tương tự áp dụng cho các cách khác nhau, trong nhiều trường hợp, bạn có thể chỉ truyền object từ cơ sở dữ liêu **trực tiếp tới client**.

Với **FastAPI**, bạn có tất cả những tính năng của **Pydantic** (FastAPI dựa trên Pydantic cho tất cả những xử lí về dữ liệu):

* **Không gây rối não**:
    * Không cần học ngôn ngữ mô tả cấu trúc mới.
    * Nếu bạn biết kiểu dữ liệu Python, bạn biết cách sử dụng Pydantic.
* Sử dụng tốt với **<abbr title="Môi trường phát triển tích hợp, tương tự như một trình soạn thảo code">IDE</abbr>/<abbr title="Một chương trình kiểm tra code lỗi">linter</abbr>/não của bạn**:

    * Bởi vì các cấu trúc dữ liệu của Pydantic chỉ là các instances của class bạn định nghĩa; auto-completion, linting, mypy và trực giác của bạn nên làm việc riêng biệt với những dữ liệu mà bạn đã validate.
* Validate **các cấu trúc phức tạp**:
    * Sử dụng các models Pydantic phân tầng, `List` và `Dict` của Python `typing`,...
    * Và các validators cho phép các cấu trúc dữ liệu phức tạp trở nên rõ ràng và dễ dàng để định nghĩa, kiểm tra và tài liệu hóa thành JSON Schema.
    * Bạn có thể có các object **JSON lồng nhau** và tất cả chúng đã validate và annotated.
* **Có khả năng mở rộng**:
    * Pydantic cho phép bạn tùy chỉnh kiểu dữ liệu bằng việc định nghĩa hoặc bạn có thể mở rộng validation với các decorator trong model.
* 100% test coverage.
