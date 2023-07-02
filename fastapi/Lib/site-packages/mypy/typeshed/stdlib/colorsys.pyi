__all__ = [
    "rgb_to_yiq",
    "yiq_to_rgb",
    "rgb_to_hls",
    "hls_to_rgb",
    "rgb_to_hsv",
    "hsv_to_rgb",
]

def rgb_to_yiq(r: float, g: float, b: float) -> tuple[float, float, float]: ...
def yiq_to_rgb(y: float, i: float, q: float) -> tuple[float, float, float]: ...
def rgb_to_hls(r: float, g: float, b: float) -> tuple[float, float, float]: ...
def hls_to_rgb(h: float, l: float, s: float) -> tuple[float, float, float]: ...
def rgb_to_hsv(r: float, g: float, b: float) -> tuple[float, float, float]: ...
def hsv_to_rgb(h: float, s: float, v: float) -> tuple[float, float, float]: ...

# TODO undocumented
ONE_SIXTH: float
ONE_THIRD: float
TWO_THIRD: float
