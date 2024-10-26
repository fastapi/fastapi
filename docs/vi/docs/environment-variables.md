# Biến Môi Trường

/// tip

Nếu bạn đã biết "biến môi trường" là gì và cách sử dụng chúng, bạn có thể bỏ qua phần này.

///

Biến môi trường (còn được gọi là "**env var**") là một biến tồn tại **bên ngoài** mã Python, trong **hệ điều hành**, và có thể được đọc bởi mã Python của bạn (hoặc bởi các chương trình khác).

Biến môi trường có thể hữu ích cho việc xử lý **cài đặt** ứng dụng, như một phần của quá trình **cài đặt** Python, v.v.

## Tạo và Sử Dụng Biến Môi Trường

Bạn có thể **tạo** và sử dụng biến môi trường trong **shell (terminal)**, mà không cần Python:

//// tab | Linux, macOS, Windows Bash

<div class="termy">

```console
// Bạn có thể tạo một biến môi trường MY_NAME với
$ export MY_NAME="Wade Wilson"

// Sau đó bạn có thể sử dụng nó với các chương trình khác, như
$ echo "Xin chào $MY_NAME"

Xin chào Wade Wilson
```

</div>

////

//// tab | Windows PowerShell

<div class="termy">

```console
// Tạo một biến môi trường MY_NAME
$ $Env:MY_NAME = "Wade Wilson"

// Sử dụng nó với các chương trình khác, như
$ echo "Xin chào $Env:MY_NAME"

Xin chào Wade Wilson
```

</div>

////

## Đọc biến môi trường trong Python

Bạn cũng có thể tạo biến môi trường **bên ngoài** Python, trong terminal (hoặc bằng bất kỳ phương pháp nào khác), và sau đó **đọc chúng trong Python**.

Ví dụ, bạn có thể có một tệp `main.py` với nội dung:

```Python hl_lines="3"
import os

name = os.getenv("MY_NAME", "World")
print(f"Xin chào {name} từ Python")
```

/// tip

Đối số thứ hai của <a href="https://docs.python.org/3.8/library/os.html#os.getenv" class="external-link" target="_blank">`os.getenv()`</a> là giá trị mặc định để trả về.

Nếu không được cung cấp, mặc định là `None`, ở đây chúng ta cung cấp `"World"` làm giá trị mặc định để sử dụng.

///

Sau đó, bạn có thể gọi chương trình Python đó:

//// tab | Linux, macOS, Windows Bash

<div class="termy">

```console
// Ở đây chúng ta chưa đặt biến môi trường
$ python main.py

// Vì chúng ta chưa đặt biến môi trường, chúng ta nhận được giá trị mặc định

Xin chào World từ Python

// Nhưng nếu chúng ta tạo một biến môi trường trước
$ export MY_NAME="Wade Wilson"

// Và sau đó gọi chương trình lại
$ python main.py

// Bây giờ nó có thể đọc biến môi trường

Xin chào Wade Wilson từ Python
```

</div>

////

//// tab | Windows PowerShell

<div class="termy">

```console
// Ở đây chúng ta chưa đặt biến môi trường
$ python main.py

// Vì chúng ta chưa đặt biến môi trường, chúng ta nhận được giá trị mặc định

Xin chào World từ Python

// Nhưng nếu chúng ta tạo một biến môi trường trước
$ $Env:MY_NAME = "Wade Wilson"

// Và sau đó gọi chương trình lại
$ python main.py

// Bây giờ nó có thể đọc biến môi trường

Xin chào Wade Wilson từ Python
```

</div>

////

Vì biến môi trường có thể được đặt bên ngoài mã, nhưng có thể được đọc bởi mã, và không cần phải được lưu trữ (commit vào `git`) cùng với các tệp khác, nên thường được sử dụng cho cấu hình hoặc **cài đặt**.

Bạn cũng có thể tạo một biến môi trường chỉ cho một **lần gọi chương trình cụ thể**, chỉ có sẵn cho chương trình đó và chỉ trong thời gian chạy của nó.

Để làm điều đó, hãy tạo nó ngay trước chương trình, trên cùng một dòng:

<div class="termy">

```console
// Tạo một biến môi trường MY_NAME trong dòng cho lần gọi chương trình này
$ MY_NAME="Wade Wilson" python main.py

// Bây giờ nó có thể đọc biến môi trường

Xin chào Wade Wilson từ Python

// Biến môi trường không còn tồn tại sau đó
$ python main.py

Xin chào World từ Python
```

</div>

/// tip

Bạn có thể đọc thêm về nó tại <a href="https://12factor.net/config" class="external-link" target="_blank">The Twelve-Factor App: Config</a>.

///

## Kiểu dữ liệu và Xác thực

Các biến môi trường này chỉ có thể xử lý **chuỗi văn bản**, vì chúng nằm bên ngoài Python và phải tương thích với các chương trình khác và phần còn lại của hệ thống (và thậm chí với các hệ điều hành khác nhau, như Linux, Windows, macOS).

Điều đó có nghĩa là **bất kỳ giá trị nào** được đọc trong Python từ một biến môi trường **sẽ là một `str`**, và bất kỳ chuyển đổi sang kiểu dữ liệu khác hoặc bất kỳ xác thực nào đều phải được thực hiện trong mã.

Bạn sẽ tìm hiểu thêm về việc sử dụng biến môi trường để xử lý **cài đặt ứng dụng** trong [Hướng dẫn Nâng cao cho Người dùng - Cài đặt và Biến Môi trường](./advanced/settings.md){.internal-link target=\_blank}.

## Biến Môi Trường `PATH`

Có một biến môi trường **đặc biệt** gọi là **`PATH`** được sử dụng bởi các hệ điều hành (Linux, macOS, Windows) để tìm các chương trình để chạy.

Giá trị của biến `PATH` là một chuỗi dài được tạo thành từ các thư mục được phân tách bằng dấu hai chấm `:` trên Linux và macOS, và bằng dấu chấm phẩy `;` trên Windows.

Ví dụ, biến môi trường `PATH` có thể trông như thế này:

//// tab | Linux, macOS

```plaintext
/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin
```

Điều này có nghĩa là hệ thống sẽ tìm kiếm các chương trình trong các thư mục:

- `/usr/local/bin`
- `/usr/bin`
- `/bin`
- `/usr/sbin`
- `/sbin`

////

//// tab | Windows

```plaintext
C:\Program Files\Python312\Scripts;C:\Program Files\Python312;C:\Windows\System32
```

Điều này có nghĩa là hệ thống sẽ tìm kiếm các chương trình trong các thư mục:

- `C:\Program Files\Python312\Scripts`
- `C:\Program Files\Python312`
- `C:\Windows\System32`

////

Khi bạn nhập một **lệnh** trong terminal, hệ điều hành **tìm kiếm** chương trình trong **từng thư mục** được liệt kê trong biến môi trường `PATH`.

Ví dụ, khi bạn nhập `python` trong terminal, hệ điều hành tìm kiếm một chương trình có tên `python` trong **thư mục đầu tiên** trong danh sách đó.

Nếu nó tìm thấy, nó sẽ **sử dụng nó**. Nếu không, nó tiếp tục tìm kiếm trong các **thư mục khác**.

### Cài đặt Python và Cập nhật `PATH`

Khi bạn cài đặt Python, bạn có thể được hỏi liệu bạn có muốn cập nhật biến môi trường `PATH` hay không.

//// tab | Linux, macOS

Giả sử bạn cài đặt Python và nó kết thúc trong thư mục `/opt/custompython/bin`.

Nếu bạn đồng ý cập nhật biến môi trường `PATH`, thì trình cài đặt sẽ thêm `/opt/custompython/bin` vào biến môi trường `PATH`.

Nó có thể trông như thế này:

```plaintext
/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin:/opt/custompython/bin
```

Bằng cách này, khi bạn nhập `python` trong terminal, hệ thống sẽ tìm thấy chương trình Python trong `/opt/custompython/bin` (thư mục cuối cùng) và sử dụng nó.

////

//// tab | Windows

Giả sử bạn cài đặt Python và nó kết thúc trong thư mục `C:\opt\custompython\bin`.

Nếu bạn đồng ý cập nhật biến môi trường `PATH`, thì trình cài đặt sẽ thêm `C:\opt\custompython\bin` vào biến môi trường `PATH`.

```plaintext
C:\Program Files\Python312\Scripts;C:\Program Files\Python312;C:\Windows\System32;C:\opt\custompython\bin
```

Bằng cách này, khi bạn nhập `python` trong terminal, hệ thống sẽ tìm thấy chương trình Python trong `C:\opt\custompython\bin` (thư mục cuối cùng) và sử dụng nó.

////

Vì vậy, nếu bạn nhập:

<div class="termy">

```console
$ python
```

</div>

//// tab | Linux, macOS

Hệ thống sẽ **tìm thấy** chương trình `python` trong `/opt/custompython/bin` và chạy nó.

Nó sẽ tương đương với việc nhập:

<div class="termy">

```console
$ /opt/custompython/bin/python
```

</div>

////

//// tab | Windows

Hệ thống sẽ **tìm thấy** chương trình `python` trong `C:\opt\custompython\bin\python` và chạy nó.

Nó sẽ tương đương với việc nhập:

<div class="termy">

```console
$ C:\opt\custompython\bin\python
```

</div>

////

Thông tin này sẽ hữu ích khi học về [Môi trường Ảo](virtual-environments.md){.internal-link target=\_blank}.

## Kết luận

Với điều này, bạn nên có hiểu biết cơ bản về **biến môi trường** là gì và cách sử dụng chúng trong Python.

Bạn cũng có thể đọc thêm về chúng trong <a href="https://en.wikipedia.org/wiki/Environment_variable" class="external-link" target="_blank">Wikipedia về Biến Môi Trường</a>.

Trong nhiều trường hợp, không rõ ràng ngay lập tức biến môi trường sẽ hữu ích và áp dụng như thế nào. Nhưng chúng tiếp tục xuất hiện trong nhiều tình huống khác nhau khi bạn đang phát triển, vì vậy tốt nhất là biết về chúng.

Ví dụ, bạn sẽ cần thông tin này trong phần tiếp theo, về [Môi trường Ảo](virtual-environments.md).
