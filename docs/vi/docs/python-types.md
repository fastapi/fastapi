# Giới thiệu kiểu dữ liệu Python

Python hỗ trợ tùy chọn "type hints" (còn được gọi là "type annotations").

Những **"type hints"** hay chú thích là một cú pháp đặc biệt cho phép khai báo <abbr title="ví dụ: str, int, float, bool"> kiểu dữ liệu</abbr> của một biến.

Bằng việc khai báo kiểu dữ liệu cho các biến của bạn, các trình soạn thảo và các công cụ có thể hỗ trợ bạn tốt hơn.

Đây chỉ là một **hướng dẫn nhanh** về gợi ý kiểu dữ liệu trong Python. Nó chỉ bao gồm những điều cần thiết tối thiểu để sử dụng chúng với **FastAPI**... đó thực sự là rất ít.

**FastAPI** hoàn toàn được dựa trên những gợi ý kiểu dữ liệu, chúng mang đến nhiều ưu điểm và lợi ích.

Nhưng thậm chí nếu bạn không bao giờ sử dụng **FastAPI**, bạn sẽ được lợi từ việc học một ít về chúng.

/// note

Nếu bạn là một chuyên gia về Python, và bạn đã biết mọi thứ về gợi ý kiểu dữ liệu, bỏ qua và đi tới chương tiếp theo.

///

## Động lực

Hãy bắt đầu với một ví dụ đơn giản:

{* ../../docs_src/python_types/tutorial001.py *}


Kết quả khi gọi chương trình này:

```
John Doe
```

Hàm thực hiện như sau:

* Lấy một `first_name` và `last_name`.
* Chuyển đổi kí tự đầu tiên của mỗi biến sang kiểu chữ hoa với `title()`.
* <abbr title="Đặt chúng lại với nhau thành một. Với các nội dung lần lượt.">Nối</abbr> chúng lại với nhau bằng một kí tự trắng ở giữa.

{* ../../docs_src/python_types/tutorial001.py hl[2] *}


### Sửa đổi

Nó là một chương trình rất đơn giản.

Nhưng bây giờ hình dung rằng bạn đang viết nó từ đầu.

Tại một vài thời điểm, bạn sẽ bắt đầu định nghĩa hàm, bạn có các tham số...

Nhưng sau đó bạn phải gọi "phương thức chuyển đổi kí tự đầu tiên sang kiểu chữ hoa".

Có phải là `upper`? Có phải là `uppercase`? `first_uppercase`? `capitalize`?

Sau đó, bạn thử hỏi người bạn cũ của mình, autocompletion của trình soạn thảo.

Bạn gõ tham số đầu tiên của hàm, `first_name`, sau đó một dấu chấm (`.`) và sau đó ấn `Ctrl+Space` để kích hoạt bộ hoàn thành.

Nhưng đáng buồn, bạn không nhận được điều gì hữu ích cả:

<img src="/img/python-types/image01.png">

### Thêm kiểu dữ liệu

Hãy sửa một dòng từ phiên bản trước.

Chúng ta sẽ thay đổi chính xác đoạn này, tham số của hàm, từ:

```Python
    first_name, last_name
```

sang:

```Python
    first_name: str, last_name: str
```

Chính là nó.

Những thứ đó là "type hints":

{* ../../docs_src/python_types/tutorial002.py hl[1] *}


Đó không giống như khai báo những giá trị mặc định giống như:

```Python
    first_name="john", last_name="doe"
```

Nó là một thứ khác.

Chúng ta sử dụng dấu hai chấm (`:`), không phải dấu bằng (`=`).

Và việc thêm gợi ý kiểu dữ liệu không làm thay đổi những gì xảy ra so với khi chưa thêm chúng.

But now, imagine you are again in the middle of creating that function, but with type hints.

Tại cùng một điểm, bạn thử kích hoạt autocomplete với `Ctrl+Space` và bạn thấy:

<img src="/img/python-types/image02.png">

Với cái đó, bạn có thể cuộn, nhìn thấy các lựa chọn, cho đến khi bạn tìm thấy một "tiếng chuông":

<img src="/img/python-types/image03.png">

## Động lực nhiều hơn

Kiểm tra hàm này, nó đã có gợi ý kiểu dữ liệu:

{* ../../docs_src/python_types/tutorial003.py hl[1] *}


Bởi vì trình soạn thảo biết kiểu dữ liệu của các biến, bạn không chỉ có được completion, bạn cũng được kiểm tra lỗi:

<img src="/img/python-types/image04.png">

Bây giờ bạn biết rằng bạn phải sửa nó, chuyển `age` sang một xâu với `str(age)`:

{* ../../docs_src/python_types/tutorial004.py hl[2] *}


## Khai báo các kiểu dữ liệu

Bạn mới chỉ nhìn thấy những nơi chủ yếu để đặt khai báo kiểu dữ liệu. Như là các tham số của hàm.

Đây cũng là nơi chủ yếu để bạn sử dụng chúng với **FastAPI**.

### Kiểu dữ liệu đơn giản

Bạn có thể khai báo tất cả các kiểu dữ liệu chuẩn của Python, không chỉ là `str`.

Bạn có thể sử dụng, ví dụ:

* `int`
* `float`
* `bool`
* `bytes`

{* ../../docs_src/python_types/tutorial005.py hl[1] *}


### Các kiểu dữ liệu tổng quát với tham số kiểu dữ liệu

Có một vài cấu trúc dữ liệu có thể chứa các giá trị khác nhau như `dict`, `list`, `set` và `tuple`. Và những giá trị nội tại cũng có thể có kiểu dữ liệu của chúng.

Những kiểu dữ liệu nội bộ này được gọi là những kiểu dữ liệu "**tổng quát**". Và có khả năng khai báo chúng, thậm chí với các kiểu dữ liệu nội bộ của chúng.

Để khai báo những kiểu dữ liệu và những kiểu dữ liệu nội bộ đó, bạn có thể sử dụng mô đun chuẩn của Python là `typing`. Nó có hỗ trợ những gợi ý kiểu dữ liệu này.

#### Những phiên bản mới hơn của Python

Cú pháp sử dụng `typing` **tương thích** với tất cả các phiên bản, từ Python 3.6 tới những phiên bản cuối cùng, bao gồm Python 3.9, Python 3.10,...

As Python advances, **những phiên bản mới** mang tới sự hỗ trợ được cải tiến cho những chú thích kiểu dữ liệu và trong nhiều trường hợp bạn thậm chí sẽ không cần import và sử dụng mô đun `typing` để khai báo chú thích kiểu dữ liệu.

Nếu bạn có thể chọn một phiên bản Python gần đây hơn cho dự án của bạn, ban sẽ có được những ưu điểm của những cải tiến đơn giản đó.

Trong tất cả các tài liệu tồn tại những ví dụ tương thích với mỗi phiên bản Python (khi có một sự khác nhau).

Cho ví dụ "**Python 3.6+**" có nghĩa là nó tương thích với Python 3.7 hoặc lớn hơn (bao gồm 3.7, 3.8, 3.9, 3.10,...). và "**Python 3.9+**" nghĩa là nó tương thích với Python 3.9 trở lên (bao gồm 3.10,...).

Nếu bạn có thể sử dụng **phiên bản cuối cùng của Python**, sử dụng những ví dụ cho phiên bản cuối, những cái đó sẽ có **cú pháp đơn giản và tốt nhât**, ví dụ, "**Python 3.10+**".

#### List

Ví dụ, hãy định nghĩa một biến là `list` các `str`.

//// tab | Python 3.9+

Khai báo biến với cùng dấu hai chấm (`:`).

Tương tự kiểu dữ liệu `list`.

Như danh sách là một kiểu dữ liệu chứa một vài kiểu dữ liệu có sẵn, bạn đặt chúng trong các dấu ngoặc vuông:

```Python hl_lines="1"
{!> ../../docs_src/python_types/tutorial006_py39.py!}
```

////

//// tab | Python 3.8+

Từ `typing`, import `List` (với chữ cái `L` viết hoa):

```Python hl_lines="1"
{!> ../../docs_src/python_types/tutorial006.py!}
```

Khai báo biến với cùng dấu hai chấm (`:`).

Tương tự như kiểu dữ liệu, `List` bạn import từ `typing`.

Như danh sách là một kiểu dữ liệu chứa các kiểu dữ liệu có sẵn, bạn đặt chúng bên trong dấu ngoặc vuông:

```Python hl_lines="4"
{!> ../../docs_src/python_types/tutorial006.py!}
```

////

/// info

Các kiểu dữ liệu có sẵn bên trong dấu ngoặc vuông được gọi là "tham số kiểu dữ liệu".

Trong trường hợp này, `str` là tham số kiểu dữ liệu được truyền tới `List` (hoặc `list` trong Python 3.9 trở lên).

///

Có nghĩa là: "biến `items` là một `list`, và mỗi phần tử trong danh sách này là một `str`".

/// tip

Nếu bạn sử dụng Python 3.9 hoặc lớn hơn, bạn không phải import `List` từ `typing`, bạn có thể sử dụng `list` để thay thế.

///

Bằng cách này, trình soạn thảo của bạn có thể hỗ trợ trong khi xử lí các phần tử trong danh sách:

<img src="/img/python-types/image05.png">

Đa phần đều không thể đạt được nếu không có các kiểu dữ liệu.

Chú ý rằng, biến `item` là một trong các phần tử trong danh sách `items`.

Và do vậy, trình soạn thảo biết nó là một `str`, và cung cấp sự hỗ trợ cho nó.

#### Tuple and Set

Bạn sẽ làm điều tương tự để khai báo các `tuple` và  các `set`:

//// tab | Python 3.9+

```Python hl_lines="1"
{!> ../../docs_src/python_types/tutorial007_py39.py!}
```

////

//// tab | Python 3.8+

```Python hl_lines="1  4"
{!> ../../docs_src/python_types/tutorial007.py!}
```

////

Điều này có nghĩa là:

* Biến `items_t` là một `tuple` với 3 phần tử, một `int`, một `int` nữa, và một `str`.
* Biến `items_s` là một `set`, và mỗi phần tử của nó có kiểu `bytes`.

#### Dict

Để định nghĩa một `dict`, bạn truyền 2 tham số kiểu dữ liệu, phân cách bởi dấu phẩy.

Tham số kiểu dữ liệu đầu tiên dành cho khóa của `dict`.

Tham số kiểu dữ liệu thứ hai dành cho giá trị của `dict`.

//// tab | Python 3.9+

```Python hl_lines="1"
{!> ../../docs_src/python_types/tutorial008_py39.py!}
```

////

//// tab | Python 3.8+

```Python hl_lines="1  4"
{!> ../../docs_src/python_types/tutorial008.py!}
```

////

Điều này có nghĩa là:

* Biến `prices` là một `dict`:
    * Khóa của `dict` này là kiểu `str` (đó là tên của mỗi vật phẩm).
    * Giá trị của `dict` này là kiểu `float` (đó là giá của mỗi vật phẩm).

#### Union

Bạn có thể khai báo rằng một biến có thể là **một vài kiểu dữ liệu" bất kì, ví dụ, một `int` hoặc một `str`.

Trong Python 3.6 hoặc lớn hơn (bao gồm Python 3.10) bạn có thể sử dụng kiểu `Union` từ `typing` và đặt trong dấu ngoặc vuông những giá trị được chấp nhận.

In Python 3.10 there's also a **new syntax** where you can put the possible types separated by a <abbr title='also called "bitwise or operator", but that meaning is not relevant here'>vertical bar (`|`)</abbr>.

Trong Python 3.10 cũng có một **cú pháp mới** mà bạn có thể đặt những kiểu giá trị khả thi phân cách bởi một dấu <abbr title='cũng được gọi là "toán tử nhị phân"'>sổ dọc (`|`)</abbr>.


//// tab | Python 3.10+

```Python hl_lines="1"
{!> ../../docs_src/python_types/tutorial008b_py310.py!}
```

////

//// tab | Python 3.8+

```Python hl_lines="1  4"
{!> ../../docs_src/python_types/tutorial008b.py!}
```

////

Trong cả hai trường hợp có nghĩa là `item` có thể là một `int` hoặc `str`.

#### Khả năng `None`

Bạn có thể khai báo một giá trị có thể có một kiểu dữ liệu, giống như `str`, nhưng nó cũng có thể là `None`.

Trong Python 3.6 hoặc lớn hơn (bao gồm Python 3.10) bạn có thể khai báo nó bằng các import và sử dụng `Optional` từ mô đun `typing`.

```Python hl_lines="1  4"
{!../../docs_src/python_types/tutorial009.py!}
```

Sử dụng `Optional[str]` thay cho `str` sẽ cho phép trình soạn thảo giúp bạn phát hiện các lỗi mà bạn có thể gặp như một giá trị luôn là một `str`, trong khi thực tế nó rất có thể là `None`.

`Optional[Something]` là một cách viết ngắn gọn của `Union[Something, None]`, chúng là tương đương nhau.

Điều này cũng có nghĩa là trong Python 3.10, bạn có thể sử dụng `Something | None`:

//// tab | Python 3.10+

```Python hl_lines="1"
{!> ../../docs_src/python_types/tutorial009_py310.py!}
```

////

//// tab | Python 3.8+

```Python hl_lines="1  4"
{!> ../../docs_src/python_types/tutorial009.py!}
```

////

//// tab | Python 3.8+ alternative

```Python hl_lines="1  4"
{!> ../../docs_src/python_types/tutorial009b.py!}
```

////

#### Sử dụng `Union` hay `Optional`

If you are using a Python version below 3.10, here's a tip from my very **subjective** point of view:

Nếu bạn đang sử dụng phiên bản Python dưới 3.10, đây là một mẹo từ ý kiến rất "chủ quan" của tôi:

* 🚨 Tránh sử dụng `Optional[SomeType]`
* Thay vào đó ✨ **sử dụng `Union[SomeType, None]`** ✨.

Cả hai là tương đương và bên dưới chúng giống nhau, nhưng tôi sẽ đễ xuất `Union` thay cho `Optional` vì từ "**tùy chọn**" có vẻ ngầm định giá trị là tùy chọn, và nó thực sự có nghĩa rằng "nó có thể là `None`", do đó nó không phải là tùy chọn và nó vẫn được yêu cầu.

Tôi nghĩ `Union[SomeType, None]` là rõ ràng hơn về ý nghĩa của nó.

Nó chỉ là về các từ và tên. Nhưng những từ đó có thể ảnh hưởng cách bạn và những đồng đội của bạn suy nghĩ về code.

Cho một ví dụ, hãy để ý hàm này:

{* ../../docs_src/python_types/tutorial009c.py hl[1,4] *}


Tham số `name` được định nghĩa là `Optional[str]`, nhưng nó **không phải là tùy chọn**, bạn không thể gọi hàm mà không có tham số:

```Python
say_hi()  # Oh, no, this throws an error! 😱
```

Tham số `name` **vẫn được yêu cầu** (không phải là *tùy chọn*) vì nó không có giá trị mặc định. Trong khi đó, `name` chấp nhận `None` như là giá trị:

```Python
say_hi(name=None)  # This works, None is valid 🎉
```

Tin tốt là, khi bạn sử dụng Python 3.10, bạn sẽ không phải lo lắng về điều đó, bạn sẽ có thể sử dụng `|` để định nghĩa hợp của các kiểu dữ liệu một cách đơn giản:

{* ../../docs_src/python_types/tutorial009c_py310.py hl[1,4] *}


Và sau đó, bạn sẽ không phải lo rằng những cái tên như `Optional` và `Union`. 😎


#### Những kiểu dữ liệu tổng quát

Những kiểu dữ liệu này lấy tham số kiểu dữ liệu trong dấu ngoặc vuông được gọi là **Kiểu dữ liệu tổng quát**, cho ví dụ:

//// tab | Python 3.10+

Bạn có thể sử dụng các kiểu dữ liệu có sẵn như là kiểu dữ liệu tổng quát (với ngoặc vuông và kiểu dữ liệu bên trong):

* `list`
* `tuple`
* `set`
* `dict`

Và tương tự với Python 3.6, từ mô đun `typing`:

* `Union`
* `Optional` (tương tự như Python 3.6)
* ...và các kiểu dữ liệu khác.

Trong Python 3.10, thay vì sử dụng `Union` và `Optional`, bạn có thể sử dụng <abbr title='cũng gọi là "toán tử nhị phân", nhưng ý nghĩa không liên quan ở đây'>sổ dọc ('|')</abbr> để khai báo hợp của các kiểu dữ liệu, điều đó tốt hơn và đơn giản hơn nhiều.

////

//// tab | Python 3.9+

Bạn có thể sử dụng các kiểu dữ liệu có sẵn tương tự như (với ngoặc vuông và kiểu dữ liệu bên trong):

* `list`
* `tuple`
* `set`
* `dict`

Và tương tự với Python 3.6, từ mô đun `typing`:

* `Union`
* `Optional`
* ...and others.

////

//// tab | Python 3.8+

* `List`
* `Tuple`
* `Set`
* `Dict`
* `Union`
* `Optional`
* ...và các kiểu khác.

////

### Lớp như kiểu dữ liệu

Bạn cũng có thể khai báo một lớp như là kiểu dữ liệu của một biến.

Hãy nói rằng bạn muốn có một lớp `Person` với một tên:

{* ../../docs_src/python_types/tutorial010.py hl[1:3] *}


Sau đó bạn có thể khai báo một biến có kiểu là `Person`:

{* ../../docs_src/python_types/tutorial010.py hl[6] *}


Và lại một lần nữa, bạn có được tất cả sự hỗ trợ từ trình soạn thảo:

<img src="/img/python-types/image06.png">

Lưu ý rằng, điều này có nghĩa rằng "`one_person`" là một **thực thể** của lớp `Person`.

Nó không có nghĩa "`one_person`" là một **lớp** gọi là `Person`.

## Pydantic models

<a href="https://docs.pydantic.dev/" class="external-link" target="_blank">Pydantic</a> là một thư viện Python để validate dữ liệu hiệu năng cao.

Bạn có thể khai báo "hình dạng" của dữa liệu như là các lớp với các thuộc tính.

Và mỗi thuộc tính có một kiểu dữ liệu.

Sau đó bạn tạo một thực thể của lớp đó với một vài giá trị và nó sẽ validate các giá trị, chuyển đổi chúng sang kiểu dữ liệu phù hợp (nếu đó là trường hợp) và cho bạn một object với toàn bộ dữ liệu.

Và bạn nhận được tất cả sự hỗ trợ của trình soạn thảo với object kết quả đó.

Một ví dụ từ tài liệu chính thức của Pydantic:

//// tab | Python 3.10+

```Python
{!> ../../docs_src/python_types/tutorial011_py310.py!}
```

////

//// tab | Python 3.9+

```Python
{!> ../../docs_src/python_types/tutorial011_py39.py!}
```

////

//// tab | Python 3.8+

```Python
{!> ../../docs_src/python_types/tutorial011.py!}
```

////

/// info

Để học nhiều hơn về <a href="https://docs.pydantic.dev/" class="external-link" target="_blank">Pydantic, tham khảo tài liệu của nó</a>.

///

**FastAPI** được dựa hoàn toàn trên Pydantic.

Bạn sẽ thấy nhiều ví dụ thực tế hơn trong [Hướng dẫn sử dụng](tutorial/index.md){.internal-link target=_blank}.

/// tip

Pydantic có một hành vi đặc biệt khi bạn sử dụng `Optional` hoặc `Union[Something, None]` mà không có giá trị mặc dịnh, bạn có thể đọc nhiều hơn về nó trong tài liệu của Pydantic về <a href="https://docs.pydantic.dev/latest/concepts/models/#required-optional-fields" class="external-link" target="_blank">Required Optional fields</a>.

///

## Type Hints với Metadata Annotations

Python cũng có một tính năng cho phép đặt **metadata bổ sung** trong những gợi ý kiểu dữ liệu này bằng cách sử dụng `Annotated`.

//// tab | Python 3.9+

Trong Python 3.9, `Annotated` là một phần của thư viện chuẩn, do đó bạn có thể import nó từ `typing`.

```Python hl_lines="1  4"
{!> ../../docs_src/python_types/tutorial013_py39.py!}
```

////

//// tab | Python 3.8+

Ở phiên bản dưới Python 3.9, bạn import `Annotated` từ `typing_extensions`.

Nó đã được cài đặt sẵng cùng với **FastAPI**.

```Python hl_lines="1  4"
{!> ../../docs_src/python_types/tutorial013.py!}
```

////

Python bản thân nó không làm bất kì điều gì với `Annotated`. Với các trình soạn thảo và các công cụ khác, kiểu dữ liệu vẫn là `str`.

Nhưng bạn có thể sử dụng `Annotated` để cung cấp cho **FastAPI** metadata bổ sung về cách mà bạn muốn ứng dụng của bạn xử lí.

Điều quan trọng cần nhớ là ***tham số kiểu dữ liệu* đầu tiên** bạn truyền tới `Annotated` là **kiểu giá trị thực sự**. Phần còn lại chỉ là metadata cho các công cụ khác.

Bây giờ, bạn chỉ cần biết rằng `Annotated` tồn tại, và nó là tiêu chuẩn của Python. 😎


Sau đó, bạn sẽ thấy sự **mạnh mẽ** mà nó có thể làm.

/// tip

Thực tế, cái này là **tiêu chuẩn của Python**, nghĩa là bạn vẫn sẽ có được **trải nghiệm phát triển tốt nhất có thể** với trình soạn thảo của bạn, với các công cụ bạn sử dụng để phân tích và tái cấu trúc code của bạn, etc. ✨

Và code của bạn sẽ tương thích với nhiều công cụ và thư viện khác của Python. 🚀

///

## Các gợi ý kiểu dữ liệu trong **FastAPI**

**FastAPI** lấy các ưu điểm của các gợi ý kiểu dữ liệu để thực hiện một số thứ.

Với **FastAPI**, bạn khai báo các tham số với gợi ý kiểu và bạn có được:

* **Sự hỗ trợ từ các trình soạn thảo**.
* **Kiểm tra kiểu dữ liệu (type checking)**.

...và **FastAPI** sử dụng các khia báo để:

* **Định nghĩa các yêu cầu**: từ tham số đường dẫn của request, tham số query, headers, bodies, các phụ thuộc (dependencies),...
* **Chuyển dổi dữ liệu*: từ request sang kiểu dữ liệu được yêu cầu.
* **Kiểm tra tính đúng đắn của dữ liệu**: tới từ mỗi request:
    * Sinh **lỗi tự động** để trả về máy khác khi dữ liệu không hợp lệ.
* **Tài liệu hóa** API sử dụng OpenAPI:
    * cái mà sau được được sử dụng bởi tài liệu tương tác người dùng.

Điều này có thể nghe trừu tượng. Đừng lo lắng. Bạn sẽ thấy tất cả chúng trong [Hướng dẫn sử dụng](tutorial/index.md){.internal-link target=_blank}.

Điều quan trọng là bằng việc sử dụng các kiểu dữ liệu chuẩn của Python (thay vì thêm các lớp, decorators,...), **FastAPI** sẽ thực hiện nhiều công việc cho bạn.

/// info

Nếu bạn đã đi qua toàn bộ các hướng dẫn và quay trở lại để tìm hiểu nhiều hơn về các kiểu dữ liệu, một tài nguyên tốt như <a href="https://mypy.readthedocs.io/en/latest/cheat_sheet_py3.html" class="external-link" target="_blank">"cheat sheet" từ `mypy`</a>.

///
