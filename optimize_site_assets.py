"""Optimize portfolio images for faster loading. Skips BeanAndTofu.gif."""

from io import BytesIO
from pathlib import Path
from urllib.request import urlopen

from PIL import Image

ROOT = Path(__file__).parent
IMG = ROOT / "images"
THUMBS = IMG / "thumbs"
SKIP_GIF = {"BeanAndTofu.gif"}

THUMB_SOURCES = {
    "drivers-of-tomorrow.webp": "https://static.wixstatic.com/media/ac96b4_44eb12e561f0405d85aa810a9d0d7925~mv2.png/v1/fill/w_800,h_450,al_c,q_85,usm_0.66_1.00_0.01,enc_auto/ac96b4_44eb12e561f0405d85aa810a9d0d7925~mv2.png",
    "marsvr.webp": "https://shared.fastly.steamstatic.com/store_item_assets/steam/apps/1618720/header.jpg",
    "adventure-climb.webp": "https://shared.fastly.steamstatic.com/store_item_assets/steam/apps/1040430/header.jpg",
    "swedish-rehab.webp": "https://img.youtube.com/vi/GInl5jsAfrc/hqdefault.jpg",
    "wheelchair.webp": "https://static.wixstatic.com/media/e3b92c_754080f1aba242a5a2701bb915fa2ffa~mv2.png/v1/fill/w_800,h_450,al_c,q_85,usm_0.66_1.00_0.01,enc_auto/e3b92c_754080f1aba242a5a2701bb915fa2ffa~mv2.png",
    "europa.webp": "https://static.wixstatic.com/media/e3b92c_e69f9b253e67424e9c0829ee372b28a8f000.jpg/v1/fill/w_800,h_450,al_c,q_85,usm_0.66_1.00_0.01,enc_auto/e3b92c_e69f9b253e67424e9c0829ee372b28a8f000.jpg",
    "anatomy.webp": "images/anatomyViewerBan.JPG",
    "music-cubes.webp": "images/cubeBanner.JPG",
    "vr-class.webp": "images/class.jpg",
}


def save_webp(src_path: Path, dest_path: Path, max_width: int = 900, quality: int = 82):
    im = Image.open(src_path)
    if im.mode in ("RGBA", "P"):
        im = im.convert("RGBA")
    else:
        im = im.convert("RGB")
    if im.width > max_width:
        ratio = max_width / im.width
        im = im.resize((max_width, int(im.height * ratio)), Image.Resampling.LANCZOS)
    im.save(dest_path, "WEBP", quality=quality, method=6)


def gif_to_webp(gif_path: Path, quality: int = 75):
    out = gif_path.with_suffix(".webp")
    im = Image.open(gif_path)
    frames = []
    durations = []
    try:
        while True:
            frame = im.copy().convert("RGBA")
            if frame.width > 900:
                ratio = 900 / frame.width
                frame = frame.resize((900, int(frame.height * ratio)), Image.Resampling.LANCZOS)
            frames.append(frame)
            durations.append(im.info.get("duration", 100))
            im.seek(im.tell() + 1)
    except EOFError:
        pass
    if not frames:
        return
    frames[0].save(
        out,
        save_all=True,
        append_images=frames[1:],
        duration=durations,
        loop=0,
        quality=quality,
        method=6,
    )
    print(f"GIF->WebP {gif_path.name} ({gif_path.stat().st_size/1024/1024:.1f}MB) -> {out.name} ({out.stat().st_size/1024:.0f}KB)")


def download_thumb(name: str, source: str):
    dest = THUMBS / name
    if source.startswith("http"):
        data = urlopen(source, timeout=30).read()
        tmp = THUMBS / f"_tmp_{name}"
        tmp.write_bytes(data)
        save_webp(tmp, dest, max_width=480, quality=80)
        tmp.unlink()
    else:
        save_webp(ROOT / source, dest, max_width=480, quality=80)
    print(f"Thumb {dest.name} ({dest.stat().st_size/1024:.0f}KB)")


def compress_static_images():
    targets = [
        "lantern.jpg",
        "pic01.PNG",
        "classShowing.jpg",
        "profilePic.PNG",
        "polePosition.PNG",
        "Tron.PNG",
        "temple.jpg",
        "mil.jpg",
        "class.jpg",
        "cubeBanner.JPG",
        "anatomyViewerBan.JPG",
        "altPres.png",
        "cubeGrab.png",
    ]
    for name in targets:
        src = IMG / name
        if not src.exists():
            continue
        out = IMG / (src.stem + ".webp")
        save_webp(src, out, max_width=1200, quality=82)
        print(f"Static {name} -> {out.name} ({out.stat().st_size/1024:.0f}KB)")


def main():
    THUMBS.mkdir(exist_ok=True)
    for name, src in THUMB_SOURCES.items():
        download_thumb(name, src)
    compress_static_images()
    for gif in IMG.glob("*.gif"):
        if gif.name in SKIP_GIF:
            print(f"Skip {gif.name}")
            continue
        gif_to_webp(gif)


if __name__ == "__main__":
    main()