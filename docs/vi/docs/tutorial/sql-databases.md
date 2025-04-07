# Cơ sở dữ liệu SQL (Cơ sở dữ liệu quan hệ)

**FastAPI** không yêu cầu bạn sử dụng cơ sở dữ liệu SQL (cơ sở dữ liệu quan hệ). Bạn hoàn toàn có thể sử dụng **bất kỳ cơ sở dữ liệu** mà bạn muốn.

Ở đây chúng ta sẽ xem một ví dụ sử dụng <a href="https://sqlmodel.tiangolo.com/" class="external-link" target="_blank">SQLModel</a>.

**SQLModel** được xây dựng trên <a href="https://www.sqlalchemy.org/" class="external-link" target="_blank">SQLAlchemy</a> và Pydantic. Nó được tạo bởi tác giả của **FastAPI** nhằm phục vụ tốt nhất cho các ứng dụng **FastAPI** cần sử dụng **cơ sở dữ liệu SQL**.

/// tip

Bạn có thể sử dụng bất kỳ thư viện cơ sở dữ liệu SQL hoặc NoSQL khác mà bạn muốn (trong một số trường hợp được gọi là <abbr title="Object Relational Mapper, một thuật ngữ khác cho thư viện mà một số class đại diện cho bảng SQL và các instance đại diện cho các hàng trong các bảng đó">"ORMs"</abbr>), **FastAPI** không ép bạn phải sử dụng bất kỳ thứ gì. 😎

///

Bởi SQLModel dựa trên SQLAlchemy, bạn có thể dễ dàng sử dụng **bất kỳ cơ sở dữ liệu** được hỗ trợ bởi SQLAlchemy (điều này cũng làm cho chúng được hỗ trợ bởi SQLModel), ví dụ như:
* PostgreSQL
* MySQL
* SQLite
* Oracle
* Microsoft SQL Server, etc.

Trong ví dụ này, chúng ta sẽ sử dụng **SQLite**, vì nó sử dụng một tệp duy nhất và Python có hỗ trợ tích hợp. Do đó, bạn có thể sao chép ví dụ này và chạy nó như đã làm.

Sau đó, đối với ứng dụng chạy thực tế của mình, bạn có thể sẽ muốn sử dụng một máy chủ cơ sở dữ liệu như **PostgreSQL**.

/// tip

Có một dự án mẫu chính thức với **FastAPI** và **PostgreSQL** bao gồm một giao diện frontend và nhiều công cụ khác: <a href="https://github.com/fastapi/full-stack-fastapi-template" class="external-link" target="_blank">https://github.com/fastapi/full-stack-fastapi-template</a>

///

Đây chỉ là một hướng dẫn rất đơn giản và ngắn, nếu bạn muốn học về cơ sở dữ liệu một cách tổng quát, về SQL hoặc các tính năng nâng cao hơn, hãy đi đến <a href="https://sqlmodel.tiangolo.com/" class="external-link" target="_blank">tài liệu SQLModel</a>.

## Cài đặt `SQLModel`

Đầu tiên, hãy đảm bảo bạn đã tạo môi trường ảo của mình [virtual environment](../virtual-environments.md){.internal-link target=_blank}, kích hoạt nó, và sau đó cài đặt `sqlmodel`:

<div class="termy">

```console
$ pip install sqlmodel
---> 100%
```

</div>

## Tạo ứng dụng với một Model duy nhất

Chúng ta sẽ tạo phiên bản đơn giản nhất của ứng dụng với một model **SQLModel** duy nhất trước.

Sau đó chúng ta sẽ cải thiện nó bằng cách tăng cường bảo mật và tính linh hoạt với **nhiều model** dưới đây. 🤓

### Tạo Models

Nhập `SQLModel` và tạo một model cơ sở dữ liệu:

{* ../../docs_src/sql_databases/tutorial001_an_py310.py ln[1:11] hl[7:11] *}

Lớp `Hero` rất giống với một model Pydantic (về bản chất, nó thực ra là một model Pydantic).

Có một vài khác biệt:

* `table=True` chỉ dẫn SQLModel biết rằng đây là một table model, nó nên đại diện cho một **bảng** trong cơ sở dữ liệu SQL, nó không phải là một model dữ liệu (như sẽ là bất kỳ lớp Pydantic khác).

* `Field(primary_key=True)` chỉ dẫn SQLModel rằng `id` là **khóa chính** trong cơ sở dữ liệu SQL (bạn có thể học thêm về khóa chính SQL trong tài liệu SQLModel).

    Bằng cách có kiểu dữ liệu là `int | None`, SQLModel sẽ biết rằng cột này nên là `INTEGER` trong cơ sở dữ liệu SQL và nó nên là `NULLABLE`.

* `Field(index=True)` chỉ dẫn SQLModel rằng nó nên tạo một **SQL index** cho cột này, điều đó sẽ cho phép tìm kiếm nhanh hơn trong cơ sở dữ liệu khi đọc dữ liệu được lọc theo cột này.

    SQLModel sẽ biết rằng thứ gì đã được khai báo là `str` sẽ là một cột SQL có kiểu dữ liệu `TEXT` (hoặc `VARCHAR`, tùy thuộc vào cơ sở dữ liệu).

### Tạo một Engine

Một `engine` SQLModel (về bản chất là một `engine` SQLAlchemy) là nơi **lưu trữ các kết nối** đến cơ sở dữ liệu.

Bạn sẽ có **một đối tượng `engine` duy nhất** cho tất cả code của bạn để kết nối với cùng một cơ sở dữ liệu.

{* ../../docs_src/sql_databases/tutorial001_an_py310.py ln[14:18] hl[14:15,17:18] *}

Sử dụng `check_same_thread=False` cho phép FastAPI sử dụng cùng một cơ sở dữ liệu SQLite trong các luồng khác nhau. Điều này là cần thiết vì **một yêu cầu duy nhất** có thể sử dụng **hơn một luồng** (ví dụ trong dependencies).

Đừng lo lắng, với cách mà code được xây dựng, chúng ta sẽ đảm bảo rằng ta chỉ sử dụng **một *session* SQLModel duy nhất cho mỗi yêu cầu** sau đó, điều này thực sự là điều mà `check_same_thread` đang cố gắng đạt được.

### Tạo các bảng

Chúng ta thêm một hàm sử dụng `SQLModel.metadata.create_all(engine)` để **tạo các bảng** cho tất cả các table model.

{* ../../docs_src/sql_databases/tutorial001_an_py310.py ln[21:22] hl[21:22] *}

### Tạo một Session Dependency


Một **`Session`** là nơi lưu trữ **đối tượng trong bộ nhớ** và theo dõi bất kỳ thay đổi nào cần thiết trong dữ liệu, sau đó nó **sử dụng `engine`** để liên lạc với cơ sở dữ liệu.

Chúng ta sẽ tạo một **dependency** FastAPI với `yield`, từ đó sẽ cung cấp một `Session` mới cho mỗi yêu cầu. Điều này đảm bảo rằng chúng ta sử dụng một phiên duy nhất cho mỗi yêu cầu. 🤓

Tiếp đó chúng ta tạo một `Annotated` dependency `SessionDep` để đơn giản hóa phần còn lại của code sẽ sử dụng dependency này.

{* ../../docs_src/sql_databases/tutorial001_an_py310.py ln[25:30]  hl[25:27,30] *}

### Tạo các bảng cơ sở dữ liệu khi khởi chạy

Chúng ta sẽ tạo các bảng cơ sở dữ liệu khi ứng dụng khởi chạy.

{* ../../docs_src/sql_databases/tutorial001_an_py310.py ln[32:37] hl[35:37] *}

Ở đây chúng ta tạo các bảng trên sự kiện khởi chạy ứng dụng.

Khi triển khai thực tế, bạn có thể sẽ sử dụng một script migration chạy trước khi khởi động ứng dụng. 🤓

/// tip

SQLModel sẽ có các tiện ích migration được xây dựng dựa trên Alembic, nhưng hiện tại, bạn có thể sử dụng trực tiếp <a href="https://alembic.sqlalchemy.org/en/latest/" class="external-link" target="blank">Alembic</a>.

///

### Tạo một Hero

Vì mỗi model SQLModel cũng là một model Pydantic, bạn có thể sử dụng nó trong cùng **type annotations** mà bạn có thể sử dụng với model Pydantic.

Ví dụ, nếu bạn khai báo một tham số có kiểu `Hero`, nó sẽ được đọc từ **JSON body**.

Tương tự, bạn có thể khai báo nó như là **kiểu dữ liệu trả về** của hàm, và khi đó cấu trúc dữ liệu sẽ được hiển thị trong giao diện tài liệu API tự động.

{* ../../docs_src/sql_databases/tutorial001_an_py310.py ln[40:45] hl[40:45] *}

Ở đây chúng ta sử dụng dependency `SessionDep` (một `Session`) để thêm `Hero` mới vào instance `Session`, commit các thay đổi đến cơ sở dữ liệu, làm mới dữ liệu trong `hero`, và sau đó trả về nó.

### Đọc các Hero

Chúng ta có thể **đọc** `Hero`s từ cơ sở dữ liệu bằng cách sử dụng `select()`. Chúng ta có thể bao gồm `limit` và `offset` để phân trang kết quả.

{* ../../docs_src/sql_databases/tutorial001_an_py310.py ln[48:55] hl[51:52,54] *}

### Đọc một Hero

Chúng ta có thể **đọc** một `Hero`.

{* ../../docs_src/sql_databases/tutorial001_an_py310.py ln[58:63] hl[60] *}

### Xóa một Hero

Chúng ta cũng có thể **xóa** một `Hero`.

{* ../../docs_src/sql_databases/tutorial001_an_py310.py ln[66:73] hl[71] *}

### Chạy ứng dụng

Bạn có thể chạy ứng dụng:

<div class="termy">

```console
$ fastapi dev main.py

<span style="color: green;">INFO</span>:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

</div>

Sau đó đi đến `/docs` UI, bạn sẽ thấy rằng **FastAPI** đang sử dụng các **model** để **tài liệu hóa** API, và nó sẽ sử dụng chúng để **chuẩn hóa** và **xác thực** dữ liệu.

<div class="screenshot">
<img src="/img/tutorial/sql-databases/image01.png">
</div>

## Cập nhật ứng dụng với nhiều model


Bây giờ chúng ta sẽ **refactor** ứng dụng một chút để tăng cường **bảo mật** và **tính linh hoạt**.

Nếu bạn kiểm tra ứng dụng trước đó, trong giao diện bạn có thể thấy rằng, cho đến nay, nó cho phép client quyết định `id` của `Hero` để tạo. 😱

Chúng ta không nên để điều đó xảy ra, họ có thể ghi đè `id` đã được gán trong DB. Quyết định `id` nên được thực hiện bởi **backend** hoặc **database**, **không phải bởi client**.

Ngoài ra, chúng ta tạo một `secret_name` cho hero, nhưng cho đến nay, chúng ta đang trả về nó ở khắp mọi nơi, điều đó không thực sự **bí mật**... 😅

Chúng ta sẽ khắc phục điều này bằng cách thêm một số **model phụ trợ**. Đây chính là lúc SQLModel thể hiện sức mạnh của nó. ✨

### Tạo nhiều models

Trong **SQLModel**, bất kỳ lớp model nào có `table=True` đều là **table model**.

Và bất kỳ lớp model nào không có `table=True` đều là **model dữ liệu**, các lớp này thực sự chỉ là các model Pydantic (với một vài tính năng nhỏ phụ trợ). 🤓

Với SQLModel, chúng ta có thể sử dụng **kế thừa** để **tránh lặp lại** tất cả các trường trong mọi hoàn cảnh.

#### `HeroBase` - lớp cơ sở

Hãy bắt đầu với `HeroBase` model có tất cả **các trường được chia sẻ** bởi tất cả các models:

* `name`
* `age`

{* ../../docs_src/sql_databases/tutorial002_an_py310.py ln[7:9] hl[7:9] *}

#### `Hero` - **table model**

Sau đó hãy tạo `Hero`, *table model* thực sự, với các **trường thêm** không phải lúc nào cũng có trong các models khác:

* `id`
* `secret_name`

Bởi vì `Hero` kế thừa từ `HeroBase`, nó **cũng** có các **trường** được đã khai báo trong `HeroBase`, do đó tất cả các trường cho `Hero` là:

* `id`
* `name`
* `age`
* `secret_name`

{* ../../docs_src/sql_databases/tutorial002_an_py310.py ln[7:14] hl[12:14] *}

#### `HeroPublic` - **model dữ liệu** công khai

Tiếp theo, chúng ta tạo `HeroPublic` model, đây là model mà sẽ được **trả về** cho client của API.

Nó có các trường giống như `HeroBase`, do đó nó sẽ không bao gồm `secret_name`.

Cuối cùng, danh tính các hero đã được bảo vệ! 🥷

Nó cũng khai báo lại `id: int`. Bằng cách này, chúng ta đang tạo một **hợp đồng** với các client API, để họ luôn có thể mong đợi `id` sẽ tồn tại và là một `int` (không bao giờ là `None`).

/// tip

Việc model trả về đảm bảo rằng một giá trị luôn có sẵn và luôn là `int` (không phải `None`) rất hữu ích cho các client API, họ có thể viết code đơn giản hơn với sự chắc chắn này.

Ngoài ra, các client được tạo tự động sẽ có giao diện đơn giản hơn, nhờ đó các developer giao tiếp với API của bạn có thể làm việc dễ dàng hơn với API của bạn. 😎

///

Tất cả các trường trong `HeroPublic` đều giống như trong `HeroBase`, với `id` được khai báo là `int` (không phải `None`):

* `id`
* `name`
* `age`

{* ../../docs_src/sql_databases/tutorial002_an_py310.py ln[7:18] hl[17:18] *}

#### `HeroCreate` - **model dữ liệu** để tạo một hero

Bây giờ chúng ta tạo một model `HeroCreate`, đây là model sẽ xác thực dữ liệu từ các client.

Nó có các trường giống như `HeroBase`, và còn có thêm `secret_name`.

Bây giờ, khi các client **tạo một hero mới**, họ sẽ gửi `secret_name`, nó sẽ được lưu trong cơ sở dữ liệu, nhưng những tên bí mật này sẽ không được trả về cho client thông qua API.

/// tip

Đây là cách bạn xử lý **mật khẩu**. Nhận chúng, nhưng không trả về chúng trong API.

Bạn cũng nên **hash** giá trị của mật khẩu trước khi lưu trữ, **không bao giờ lưu trữ chúng dưới dạng văn bản thuần túy**.

///

Các trường của `HeroCreate` là:

* `name`
* `age`
* `secret_name`

{* ../../docs_src/sql_databases/tutorial002_an_py310.py ln[7:22] hl[21:22] *}

#### `HeroUpdate` - **model dữ liệu** để cập nhật một hero

Chúng ta chưa có cách để **cập nhật một hero** trong phiên bản trước của ứng dụng, nhưng giờ với nhiều model, chúng ta có thể làm được. 🎉

`HeroUpdate` là một *model dữ liệu* hơi đặc biệt, nó có **tất cả các trường tương tự** cần thiết để tạo một hero mới, nhưng tất cả các trường đều là tùy chọn (tất cả đều có giá trị mặc định). Bằng cách này, khi bạn cập nhật một hero, bạn có thể chỉ gửi những trường mà bạn muốn cập nhật.

Bởi vì tất cả **các trường thực sự thay đổi** (kiểu dữ liệu giờ bao gồm `None` và chúng có giá trị mặc định là `None`), chúng ta cần **khai báo lại** chúng.

Chúng ta không thực sự cần kế thừa từ `HeroBase` vì chúng ta đang khai báo lại tất cả các trường. Tôi sẽ để nó kế thừa chỉ để giữ tính nhất quán, nhưng điều này không cần thiết. Nó chỉ là vấn đề sở thích cá nhân. 🤷

Các trường của `HeroUpdate` là:

* `name`
* `age`
* `secret_name`

{* ../../docs_src/sql_databases/tutorial002_an_py310.py ln[7:28] hl[25:28] *}

### Tạo với `HeroCreate` và trả về `HeroPublic`

Bây giờ chúng ta đã có **nhiều model**, chúng ta có thể cập nhật các phần của ứng dụng sử dụng chúng.

Chúng ta nhận trong request một data model `HeroCreate`, và từ đó, chúng ta tạo một *table model* `Hero`.

*Table model* `Hero` mới này sẽ có các trường được gửi bởi client, và cũng sẽ có một `id` được tạo bởi cơ sở dữ liệu.

Sau đó chúng ta trả về cùng *table model* `Hero` nguyên trạng từ hàm. Nhưng vì chúng ta khai báo `response_model` với `HeroPublic` *data model*, **FastAPI** sẽ sử dụng `HeroPublic` để xác thực và chuẩn hóa dữ liệu.

{* ../../docs_src/sql_databases/tutorial002_an_py310.py ln[56:62] hl[56:58] *}

/// tip

Bây giờ chúng ta sử dụng `response_model=HeroPublic` thay vì **trả về chú thích dữ liệu** `-> HeroPublic` bởi vì giá trị mà chúng ta đang trả về thực sự *không phải* là một `HeroPublic`.

Nếu chúng ta đã khai báo `-> HeroPublic`, trình soạn thảo và linter của bạn sẽ phàn nàn (một cách hợp lý) rằng bạn đang trả về một `Hero` thay vì một `HeroPublic`.

Bằng cách khai báo trong `response_model`, chúng ta đang chỉ dẫn **FastAPI** để làm việc của nó, mà không can thiệp vào các chú thích kiểu dữ liệu và sự trợ giúp từ trình soạn thảo cũng như các công cụ khác của bạn.

///

### Đọc các Hero với `HeroPublic`

Chúng ta có thể làm giống như trước để **đọc** các `Hero`, một lần nữa, chúng ta sử dụng `response_model=list[HeroPublic]` để đảm bảo rằng dữ liệu được xác thực và chuẩn hóa một cách chính xác.

{* ../../docs_src/sql_databases/tutorial002_an_py310.py ln[65:72] hl[65:72] *}

### Đọc một Hero với `HeroPublic`

Chúng ta có thể **đọc** một hero đơn lẻ:

{* ../../docs_src/sql_databases/tutorial002_an_py310.py ln[75:80] hl[77] *}

### Cập nhật một Hero với `HeroUpdate`

Chúng ta có thể **cập nhật một hero**. Để làm điều này, chúng ta sử dụng thao tác HTTP `PATCH`.

Và trong code, chúng ta nhận một `dict` với tất cả dữ liệu được gửi bởi client, **chỉ dữ liệu được gửi bởi client**, loại trừ bất kỳ giá trị nào chỉ có mặt chỉ vì là giá trị mặc định. Để làm điều này, chúng ta sử dụng `exclude_unset=True`. Đây là thủ thuật chính. 🪄

Sau đó chúng ta sử dụng `hero_db.sqlmodel_update(hero_data)` để cập nhật `hero_db` với dữ liệu từ `hero_data`.

{* ../../docs_src/sql_databases/tutorial002_an_py310.py ln[83:93] hl[83:84,88:89] *}

### Xóa một Hero

**Xóa** một hero vẫn giống như trước.

Chúng ta sẽ chưa thực hiện việc cải tổ toàn bộ code trong phần này nhé. 😅

{* ../../docs_src/sql_databases/tutorial002_an_py310.py ln[96:103] hl[101] *}

### Chạy lại ứng dụng

Bạn có thể chạy lại ứng dụng:

<div class="termy">

```console
$ fastapi dev main.py

<span style="color: green;">INFO</span>:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

</div>

Nếu bạn đi đến `/docs` UI của API, bạn sẽ thấy rằng nó đã được cập nhật, và nó sẽ không mong đợi nhận vào `id` từ người dùng khi tạo một hero, v.v.

<div class="screenshot">
<img src="/img/tutorial/sql-databases/image02.png">
</div>

## Tổng kết

Bạn có thể sử dụng <a href="https://sqlmodel.tiangolo.com/" class="external-link" target="blank">**SQLModel**</a> để tương tác với cơ sở dữ liệu SQL và đơn giản hóa code với *data models* và *table models*.

Bạn có thể tìm hiểu thêm nhiều điều trong tài liệu của **SQLModel**, có một <a href="https://sqlmodel.tiangolo.com/tutorial/fastapi/" class="external-link" target="blank">hướng dẫn chi tiết hơn về việc sử dụng SQLModel với **FastAPI**</a>. 🚀
