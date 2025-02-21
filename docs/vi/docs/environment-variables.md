# Biến môi trường (Environment Variables)

/// tip

Nếu bạn đã biết về "biến môi trường" và cách sử dụng chúng, bạn có thể bỏ qua phần này.

///

Một biến môi trường (còn được gọi là "**env var**") là một biến mà tồn tại **bên ngoài** đoạn mã Python, ở trong **hệ điều hành**, và có thể được đọc bởi đoạn mã Python của bạn (hoặc bởi các chương trình khác).

Các biến môi trường có thể được sử dụng để xử lí **các thiết lập** của ứng dụng, như một phần của **các quá trình cài đặt** Python, v.v.

## Tạo và Sử dụng các Biến Môi Trường

Bạn có thể **tạo** và sử dụng các biến môi trường trong **shell (terminal)**, mà không cần sử dụng Python:

//// tab | Linux, macOS, Windows Bash

<div class="termy">

```console
// Bạn có thể tạo một biến môi trường MY_NAME với
$ export MY_NAME="Wade Wilson"

// Sau đó bạn có thể sử dụng nó với các chương trình khác, như
$ echo "Hello $MY_NAME"

Hello Wade Wilson
```

</div>

////

//// tab | Windows PowerShell

<div class="termy">

```console
// Tạo một biến môi trường MY_NAME
$ $Env:MY_NAME = "Wade Wilson"

// Sử dụng nó với các chương trình khác, như là
$ echo "Hello $Env:MY_NAME"

Hello Wade Wilson
```

</div>

////

## Đọc các Biến Môi Trường trong Python

Bạn cũng có thể tạo các biến môi trường **bên ngoài** đoạn mã Python, trong terminal (hoặc bằng bất kỳ phương pháp nào khác), và sau đó **đọc chúng trong Python**.

Ví dụ, bạn có một file `main.py` với:

```Python hl_lines="3"
import os

name = os.getenv("MY_NAME", "World")
print(f"Hello {name} from Python")
```

/// tip

Tham số thứ hai cho <a href="https://docs.python.org/3.8/library/os.html#os.getenv" class="external-link" target="_blank">`os.getenv()`</a> là giá trị mặc định để trả về.

Nếu không được cung cấp, nó mặc định là `None`, ở đây chúng ta cung cấp `"World"` là giá trị mặc định để sử dụng.

///

Sau đó bạn có thể gọi chương trình Python:

//// tab | Linux, macOS, Windows Bash

<div class="termy">

```console
// Ở đây chúng ta chưa cài đặt biến môi trường
$ python main.py

// Vì chúng ta chưa cài đặt biến môi trường, chúng ta nhận được giá trị mặc định

Hello World from Python

// Nhưng nếu chúng ta tạo một biến môi trường trước đó
$ export MY_NAME="Wade Wilson"

// Và sau đó gọi chương trình lại
$ python main.py

// Bây giờ nó có thể đọc biến môi trường

Hello Wade Wilson from Python
```

</div>

////

//// tab | Windows PowerShell

<div class="termy">

```console
// Ở đây chúng ta chưa cài đặt biến môi trường
$ python main.py

// Vì chúng ta chưa cài đặt biến môi trường, chúng ta nhận được giá trị mặc định

Hello World from Python

// Nhưng nếu chúng ta tạo một biến môi trường trước đó
$ $Env:MY_NAME = "Wade Wilson"

// Và sau đó gọi chương trình lại
$ python main.py

// Bây giờ nó có thể đọc biến môi trường

Hello Wade Wilson from Python
```

</div>

////

Vì các biến môi trường có thể được tạo bên ngoài đoạn mã Python, nhưng có thể được đọc bởi đoạn mã Python, và không cần được lưu trữ (commit vào `git`) cùng với các file khác, nên chúng thường được sử dụng để lưu các thiết lập hoặc **cấu hình**.

Bạn cũng có thể tạo ra một biến môi trường dành riêng cho một **lần gọi chương trình**, chỉ có thể được sử dụng bởi chương trình đó, và chỉ trong thời gian chạy của chương trình.

Để làm điều này, tạo nó ngay trước chương trình đó, trên cùng một dòng:

<div class="termy">

```console
// Tạo một biến môi trường MY_NAME cho lần gọi chương trình này
$ MY_NAME="Wade Wilson" python main.py

// Bây giờ nó có thể đọc biến môi trường

Hello Wade Wilson from Python

// Biến môi trường không còn tồn tại sau đó
$ python main.py

Hello World from Python
```

</div>

/// tip

Bạn có thể đọc thêm về điều này tại <a href="https://12factor.net/config" class="external-link" target="_blank">The Twelve-Factor App: Config</a>.

///

## Các Kiểu (Types) và Kiểm tra (Validation)

Các biến môi trường có thể chỉ xử lí **chuỗi ký tự**, vì chúng nằm bên ngoài đoạn mã Python và phải tương thích với các chương trình khác và phần còn lại của hệ thống (và thậm chí với các hệ điều hành khác, như Linux, Windows, macOS).

Điều này có nghĩa là **bất kỳ giá trị nào** được đọc trong Python từ một biến môi trường **sẽ là một `str`**, và bất kỳ hành động chuyển đổi sang kiểu dữ liệu khác hoặc hành động kiểm tra nào cũng phải được thực hiện trong đoạn mã.

Bạn sẽ học thêm về việc sử dụng biến môi trường để xử lí **các thiết lập ứng dụng** trong [Hướng dẫn nâng cao - Các thiết lập và biến môi trường](./advanced/settings.md){.internal-link target=_blank}.

## Biến môi trường `PATH`

Có một biến môi trường **đặc biệt** được gọi là **`PATH`** được sử dụng bởi các hệ điều hành (Linux, macOS, Windows) nhằm tìm các chương trình để thực thi.

Giá trị của biến môi trường `PATH` là một chuỗi dài được tạo bởi các thư mục được phân tách bởi dấu hai chấm `:` trên Linux và macOS, và bởi dấu chấm phẩy `;` trên Windows.

Ví dụ, biến môi trường `PATH` có thể có dạng như sau:

//// tab | Linux, macOS

```plaintext
/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin
```

Điều này có nghĩa là hệ thống sẽ tìm kiếm các chương trình trong các thư mục:

* `/usr/local/bin`
* `/usr/bin`
* `/bin`
* `/usr/sbin`
* `/sbin`

////

//// tab | Windows

```plaintext
C:\Program Files\Python312\Scripts;C:\Program Files\Python312;C:\Windows\System32
```

Điều này có nghĩa là hệ thống sẽ tìm kiếm các chương trình trong các thư mục:

* `C:\Program Files\Python312\Scripts`
* `C:\Program Files\Python312`
* `C:\Windows\System32`

////

Khi bạn gõ một **lệnh** trong terminal, hệ điều hành **tìm kiếm** chương trình trong **mỗi thư mục** được liệt kê trong biến môi trường `PATH`.

Ví dụ, khi bạn gõ `python` trong terminal, hệ điều hành tìm kiếm một chương trình được gọi `python` trong **thư mục đầu tiên** trong danh sách đó.

Nếu tìm thấy, nó sẽ **sử dụng** nó. Nếu không tìm thấy, nó sẽ tiếp tục tìm kiếm trong **các thư mục khác**.

### Cài đặt Python và cập nhật biến môi trường `PATH`

Khi bạn cài đặt Python, bạn có thể được hỏi nếu bạn muốn cập nhật biến môi trường `PATH`.

//// tab | Linux, macOS

Giả sử bạn cài đặt Python vào thư mục `/opt/custompython/bin`.

Nếu bạn chọn cập nhật biến môi trường `PATH`, thì cài đặt sẽ thêm `/opt/custompython/bin` vào biến môi trường `PATH`.

Nó có thể có dạng như sau:

```plaintext
/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin:/opt/custompython/bin
```

Như vậy, khi bạn gõ `python` trong terminal, hệ thống sẽ tìm thấy chương trình Python trong `/opt/custompython/bin` (thư mục cuối) và sử dụng nó.

////

//// tab | Windows

Giả sử bạn cài đặt Python vào thư mục `C:\opt\custompython\bin`.

Nếu bạn chọn cập nhật biến môi trường `PATH`, thì cài đặt sẽ thêm `C:\opt\custompython\bin` vào biến môi trường `PATH`.

Nó có thể có dạng như sau:

```plaintext
C:\Program Files\Python312\Scripts;C:\Program Files\Python312;C:\Windows\System32;C:\opt\custompython\bin
```

Như vậy, khi bạn gõ `python` trong terminal, hệ thống sẽ tìm thấy chương trình Python trong `C:\opt\custompython\bin` (thư mục cuối) và sử dụng nó.

////

Vậy, nếu bạn gõ:

<div class="termy">

```console
$ python
```

</div>

//// tab | Linux, macOS

Hệ thống sẽ **tìm kiếm** chương trình `python` trong `/opt/custompython/bin` và thực thi nó.

Nó tương đương với việc bạn gõ:

<div class="termy">

```console
$ /opt/custompython/bin/python
```

</div>

////

//// tab | Windows

Hệ thống sẽ **tìm kiếm** chương trình `python` trong `C:\opt\custompython\bin\python` và thực thi nó.

Nó tương đương với việc bạn gõ:

<div class="termy">

```console
$ C:\opt\custompython\bin\python
```

</div>

////

Thông tin này sẽ hữu ích khi bạn học về [Môi trường ảo](virtual-environments.md){.internal-link target=_blank}.

## Kết luận

Với những thông tin này, bạn có thể hiểu được **các biến môi trường là gì** và **cách sử dụng chúng trong Python**.

Bạn có thể đọc thêm về chúng tại <a href="https://en.wikipedia.org/wiki/Environment_variable" class="external-link" target="_blank">Wikipedia cho Biến môi trường</a>.

Trong nhiều trường hợp, cách các biến môi trường trở nên hữu ích và có thể áp dụng không thực sự rõ ràng ngay từ đầu, nhưng chúng sẽ liên tục xuất hiện trong rất nhiều tình huống khi bạn phát triển ứng dụng, vì vậy việc hiểu biết về chúng là hữu ích.

Chẳng hạn, bạn sẽ cần những thông tin này khi bạn học về [Môi trường ảo](virtual-environments.md).
