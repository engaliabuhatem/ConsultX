"""
Brand hex -> Unfold COLORS ramps.

Unfold wants an eleven-step ramp (50..950) for `primary` and `base`. Writing
those by hand means converting a brand color to OKLCH and picking a lightness
ladder that keeps hue and reads evenly — fiddly, and easy to get subtly wrong
on the next project. This does it from one hex value.

Why OKLCH rather than HSL: OKLCH lightness is perceptual, so a fixed lightness
ladder produces steps that *look* evenly spaced, and holding hue constant while
lightness moves does not shift the color the way HSL does (HSL blues go purple
as they darken). The ladders below are the ones tuned by hand for the ConsultX
admin, kept because they satisfy two constraints Unfold imposes:

  * step 600 carries white text (Unfold paints white on primary-600), so it is
    pinned near L 53% — light brand colors are darkened to reach it rather than
    used raw.
  * step 950 stays above L 15%, because Unfold uses it as a dark-mode surface
    and anything lower crushes against pure black.

No third-party dependency: the sRGB -> OKLab math is ~20 lines of stdlib.
"""

from math import atan2, cos, degrees, pi, radians, sin

__all__ = ["hex_to_oklch", "oklch_to_hex", "primary_ramp", "base_ramp", "ramps"]

STEPS = ("50", "100", "200", "300", "400", "500", "600", "700", "800", "900", "950")

# Lightness ladder for an accent ramp. 600 is the white-text anchor.
_PRIMARY_L = (97.2, 94.0, 88.5, 80.0, 66.5, 58.0, 52.8, 45.0, 37.5, 31.5, 22.0)
# Chroma as a multiple of the brand color's own chroma. Saturation peaks around
# 500 and falls off at both ends: near-white and near-black cannot hold chroma
# without looking muddy.
_PRIMARY_C = (0.136, 0.291, 0.534, 0.825, 1.019, 1.117, 1.0, 0.874, 0.718, 0.583, 0.408)

# Neutral ramp. Chroma is almost zero — just enough to tint the greys toward the
# brand hue so they read warm/cool with the site instead of default blue-grey.
_BASE_L = (98.4, 96.2, 92.4, 86.5, 72.0, 58.5, 47.5, 39.5, 30.0, 22.0, 15.5)
_BASE_C = (0.006, 0.008, 0.010, 0.011, 0.012, 0.012, 0.011, 0.010, 0.009, 0.010, 0.010)
# Deep neutrals drift a few degrees warmer; a flat hue makes dark surfaces look
# slightly green next to the lighter steps.
_BASE_H_DRIFT = (0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.8, 5.8, 9.8, 13.2)


def _srgb_to_linear(c: float) -> float:
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4


def _linear_to_srgb(c: float) -> float:
    return c * 12.92 if c <= 0.0031308 else 1.055 * (c ** (1 / 2.4)) - 0.055


def hex_to_oklch(value: str) -> tuple[float, float, float]:
    """'#9c5539' -> (lightness 0-100, chroma, hue degrees 0-360)."""
    h = value.strip().lstrip("#")
    if len(h) == 3:
        h = "".join(ch * 2 for ch in h)
    if len(h) != 6:
        raise ValueError(f"expected a 3- or 6-digit hex color, got {value!r}")
    r, g, b = (_srgb_to_linear(int(h[i : i + 2], 16) / 255) for i in (0, 2, 4))

    l = 0.4122214708 * r + 0.5363325363 * g + 0.0514459929 * b
    m = 0.2119034982 * r + 0.6806995451 * g + 0.1073969566 * b
    s = 0.0883024619 * r + 0.2817188376 * g + 0.6299787005 * b
    l_, m_, s_ = (v ** (1 / 3) if v > 0 else -((-v) ** (1 / 3)) for v in (l, m, s))

    L = 0.2104542553 * l_ + 0.7936177850 * m_ - 0.0040720468 * s_
    a = 1.9779984951 * l_ - 2.4285922050 * m_ + 0.4505937099 * s_
    bb = 0.0259040371 * l_ + 0.7827717662 * m_ - 0.8086757660 * s_

    chroma = (a * a + bb * bb) ** 0.5
    hue = degrees(atan2(bb, a)) % 360
    return L * 100, chroma, hue


def oklch_to_hex(lightness: float, chroma: float, hue: float) -> str:
    """Inverse of hex_to_oklch, clipped to sRGB. Only used for previews."""
    L, a, bb = lightness / 100, chroma * cos(radians(hue)), chroma * sin(radians(hue))
    l_ = L + 0.3963377774 * a + 0.2158037573 * bb
    m_ = L - 0.1055613458 * a - 0.0638541728 * bb
    s_ = L - 0.0894841775 * a - 1.2914855480 * bb
    l, m, s = l_**3, m_**3, s_**3

    r = 4.0767416621 * l - 3.3077115913 * m + 0.2309699292 * s
    g = -1.2684380046 * l + 2.6097574011 * m - 0.3413193965 * s
    b = -0.0041960863 * l - 0.7034186147 * m + 1.7076147010 * s
    return "#" + "".join(
        f"{round(max(0.0, min(1.0, _linear_to_srgb(c))) * 255):02x}" for c in (r, g, b)
    )


def _fmt(lightness: float, chroma: float, hue: float) -> str:
    return f"oklch({lightness:.1f}% {chroma:.3f} {hue % 360:.1f})"


def primary_ramp(brand_hex: str, *, saturation: float = 1.0) -> dict[str, str]:
    """Accent ramp from one brand hex. `saturation` scales the whole ramp: drop
    below 1.0 for a more muted admin, raise it for a punchier one."""
    _, chroma, hue = hex_to_oklch(brand_hex)
    # Very light or very dark brand colors carry little chroma at their own
    # lightness but should still produce a saturated mid-ramp, so the anchor
    # chroma has a floor.
    anchor = max(chroma, 0.045) * saturation
    return {
        step: _fmt(L, anchor * mult, hue)
        for step, L, mult in zip(STEPS, _PRIMARY_L, _PRIMARY_C)
    }


def base_ramp(neutral_hex: str, *, tint: float = 1.0) -> dict[str, str]:
    """Neutral ramp tinted toward `neutral_hex`'s hue. `tint` of 0 gives pure
    greys; 1.0 gives the subtle warm/cool cast used on the ConsultX admin."""
    _, _, hue = hex_to_oklch(neutral_hex)
    return {
        step: _fmt(L, C * tint, hue + drift)
        for step, L, C, drift in zip(STEPS, _BASE_L, _BASE_C, _BASE_H_DRIFT)
    }


def ramps(brand_hex: str, neutral_hex: str, *, saturation: float = 1.0,
          tint: float = 1.0) -> dict[str, dict[str, str]]:
    """Both ramps, shaped for UNFOLD["COLORS"]."""
    return {
        "base": base_ramp(neutral_hex, tint=tint),
        "primary": primary_ramp(brand_hex, saturation=saturation),
    }
