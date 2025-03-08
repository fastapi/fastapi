# Về các phiên bản của FastAPI

**FastAPI** đã được sử dụng ở quy mô thực tế (production) trong nhiều ứng dụng và hệ thống. Và phạm vi kiểm thử được giữ ở mức 100%. Nhưng việc phát triển của nó vẫn đang diễn ra nhanh chóng.

Các tính năng mới được bổ sung thường xuyên, lỗi được sửa định kỳ, và mã nguồn vẫn đang được cải thiện liên tục

Đó là lí do các phiên bản hiện tại vẫn còn là 0.x.x, điều này phản ánh rằng mỗi phiên bản có thể có các thay đổi gây mất tương thích. Điều này tuân theo các quy ước về <a href="https://semver.org/" class="external-link" target="blank">Semantic Versioning</a>.

Bạn có thể tạo ra sản phẩm thực tế với **FastAPI** ngay bây giờ (và bạn có thể đã làm điều này trong một thời gian dài), bạn chỉ cần đảm bảo rằng bạn sử dụng một phiên bản hoạt động đúng với các đoạn mã còn lại của bạn.

## Cố định phiên bản của `fastapi`

Điều đầu tiên bạn nên làm là "cố định" phiên bản của **FastAPI** bạn đang sử dụng để phiên bản mới nhất mà bạn biết hoạt động đúng với ứng dụng của bạn.

Ví dụ, giả sử bạn đang sử dụng phiên bản `0.112.0` trong ứng dụng của bạn.

Nếu bạn sử dụng một tệp `requirements.txt` bạn có thể chỉ định phiên bản với:

```txt
fastapi[standard]==0.112.0
```

Như vậy, bạn sẽ sử dụng chính xác phiên bản `0.112.0`.

Hoặc bạn cũng có thể cố định nó với:

```txt
fastapi[standard]>=0.112.0,<0.113.0
```

Như vậy, bạn sẽ sử dụng các phiên bản `0.112.0` trở lên, nhưng nhỏ hơn `0.113.0`, ví dụ, một phiên bản `0.112.2` vẫn được chấp nhận.

Nếu bạn sử dụng bất kỳ công cụ nào để quản lý cài đặt của bạn, như `uv`, Poetry, Pipenv, hoặc bất kỳ công cụ nào khác, chúng đều có một cách để bạn có thể định nghĩa các phiên bản cụ thể cho các gói của bạn.

## Các phiên bản có sẵn

Bạn có thể xem các phiên bản có sẵn (ví dụ để kiểm tra phiên bản mới nhất) trong [Release Notes](../release-notes.md){.internal-link target=_blank}.

## Về các phiên bản

Theo quy ước về Semantic Versioning, bất kỳ phiên bản nào bên dưới `1.0.0` có thể thêm các thay đổi gây mất tương thích.

**FastAPI** cũng theo quy ước rằng bất kỳ thay đổi phiên bản "PATCH" nào là cho các lỗi và các thay đổi không gây mất tương thích.

/// tip

"PATCH" là số cuối cùng, ví dụ, trong `0.2.3`, phiên bản PATCH là `3`.

///

Vì vậy, bạn có thể cố định đến một phiên bản như:

```txt
fastapi>=0.45.0,<0.46.0
```

Các thay đổi gây mất tương thích và các tính năng mới được thêm vào trong các phiên bản "MINOR".

/// tip

"MINOR" là số ở giữa, ví dụ, trong `0.2.3`, phiên bản MINOR là `2`.

///

## Nâng cấp các phiên bản của FastAPI

Bạn nên thêm các bài kiểm tra (tests) cho ứng dụng của bạn.

Với **FastAPI** điều này rất dễ dàng (nhờ vào Starlette), kiểm tra tài liệu: [Testing](../tutorial/testing.md){.internal-link target=_blank}

Sau khi bạn có các bài kiểm tra, bạn có thể nâng cấp phiên bản **FastAPI** lên một phiên bản mới hơn, và đảm bảo rằng tất cả mã của bạn hoạt động đúng bằng cách chạy các bài kiểm tra của bạn.

Nếu mọi thứ đang hoạt động, hoặc sau khi bạn thực hiện các thay đổi cần thiết, và tất cả các bài kiểm tra của bạn đều đi qua, thì bạn có thể cố định phiên bản của `fastapi` đến phiên bản mới hơn.

## Về Starlette

Bạn không nên cố định phiên bản của `starlette`.

Các phiên bản khác nhau của **FastAPI** sẽ sử dụng một phiên bản Starlette mới hơn.

Vì vậy, bạn có thể để **FastAPI** sử dụng phiên bản Starlette phù hợp.

## Về Pydantic

Pydantic bao gồm các bài kiểm tra của riêng nó cho **FastAPI**, vì vậy các phiên bản mới hơn của Pydantic (trên `1.0.0`) luôn tương thích với **FastAPI**.

Bạn có thể cố định Pydantic đến bất kỳ phiên bản nào trên `1.0.0` mà bạn muốn.

Ví dụ:

```txt
pydantic>=2.7.0,<3.0.0
```
