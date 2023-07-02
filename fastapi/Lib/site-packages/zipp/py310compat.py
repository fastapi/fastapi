import io
import sys

te_impl = "lambda encoding, stacklevel=2, /: encoding"
te_impl_37 = te_impl.replace(", /", "")
_text_encoding = eval(te_impl) if sys.version_info > (3, 8) else eval(te_impl_37)


text_encoding = (
    io.text_encoding if sys.version_info > (3, 10) else _text_encoding  # type: ignore
)
