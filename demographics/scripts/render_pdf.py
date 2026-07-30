"""Render Spanish manuscript HTML to PDF with Playwright (relative paths)."""
import asyncio
from pathlib import Path

from playwright.async_api import async_playwright

ROOT = Path(__file__).resolve().parents[1]
MS = ROOT / "manuscript" / "es"
HTML = MS / "manuscript.html"
PDF = MS / "Cuba_despoblacion_2019-2025_manuscrito.pdf"


async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        await page.goto(HTML.as_uri(), wait_until="networkidle")
        await page.pdf(
            path=str(PDF),
            format="A4",
            print_background=True,
            margin={"top": "0", "bottom": "0", "left": "0", "right": "0"},
            prefer_css_page_size=True,
        )
        await browser.close()
        print(f"PDF rendered -> {PDF}")


asyncio.run(main())
