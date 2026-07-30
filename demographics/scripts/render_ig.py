"""Render infographic HTML to PDF/PNG with Playwright (relative paths)."""
import asyncio
from pathlib import Path

from playwright.async_api import async_playwright

ROOT = Path(__file__).resolve().parents[1]
IG = ROOT / "infographic"
HTML = IG / "infografia.html"
PDF = IG / "Cuba_despoblacion_infografia.pdf"
PNG = IG / "Cuba_despoblacion_infografia.png"


async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page(device_scale_factor=2)
        await page.goto(HTML.as_uri(), wait_until="networkidle")
        await page.pdf(
            path=str(PDF),
            width="420mm",
            height="594mm",
            print_background=True,
            margin={"top": "0", "bottom": "0", "left": "0", "right": "0"},
            prefer_css_page_size=True,
        )
        el = await page.query_selector("body")
        await el.screenshot(path=str(PNG))
        await browser.close()


asyncio.run(main())
print(f"infographic rendered -> {PDF.name}, {PNG.name}")
