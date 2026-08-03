"""Render infographic HTML to PDF/PNG with Playwright (relative paths)."""
import asyncio
from pathlib import Path

from playwright.async_api import async_playwright

ROOT = Path(__file__).resolve().parents[1]
IG = ROOT / "infographic"
IG_EN = IG / "en"

RENDER_TARGETS = [
    {
        "html": IG / "infografia.html",
        "pdf": IG / "Cuba_despoblacion_infografia.pdf",
        "png": IG / "Cuba_despoblacion_infografia.png",
        "viewport": None,
        "pdf_size": {"width": "420mm", "height": "594mm"},
    },
    {
        "html": IG / "social_1x1.html",
        "png": IG / "social_1x1.png",
        "viewport": {"width": 1080, "height": 1080},
    },
    {
        "html": IG / "social_4x5.html",
        "png": IG / "social_4x5.png",
        "viewport": {"width": 1080, "height": 1350},
    },
    {
        "html": IG_EN / "infographic.html",
        "pdf": IG_EN / "cuba-depopulation-infographic.pdf",
        "png": IG_EN / "cuba-depopulation-infographic.png",
        "viewport": None,
        "pdf_size": {"width": "420mm", "height": "594mm"},
    },
    {
        "html": IG_EN / "social_1x1.html",
        "png": IG_EN / "social_1x1.png",
        "viewport": {"width": 1080, "height": 1080},
    },
    {
        "html": IG_EN / "social_4x5.html",
        "png": IG_EN / "social_4x5.png",
        "viewport": {"width": 1080, "height": 1350},
    },
]


async def render_target(page, target: dict) -> None:
    html = target["html"]
    if not html.exists():
        raise FileNotFoundError(html)

    viewport = target.get("viewport")
    if viewport:
        await page.set_viewport_size(viewport)
    await page.goto(html.as_uri(), wait_until="networkidle")

    if "pdf" in target:
        pdf_size = target["pdf_size"]
        await page.pdf(
            path=str(target["pdf"]),
            width=pdf_size["width"],
            height=pdf_size["height"],
            print_background=True,
            margin={"top": "0", "bottom": "0", "left": "0", "right": "0"},
            prefer_css_page_size=True,
        )

    el = await page.query_selector("body")
    await el.screenshot(path=str(target["png"]))


async def main() -> None:
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page(device_scale_factor=2)
        for target in RENDER_TARGETS:
            await render_target(page, target)
            print(f"rendered -> {target['png'].relative_to(ROOT)}")
        await browser.close()


if __name__ == "__main__":
    asyncio.run(main())
