"""
Instagram @evonikpc 스크래퍼 (Playwright)
"""
import os
import time
import requests
from playwright.sync_api import sync_playwright, Page, BrowserContext

from src.config import INSTA_STATE, IMAGES_DIR, DEBUG_DIR


# ── 헬퍼 ──────────────────────────────────────────────────────────

def _save_debug(page: Page, name: str) -> None:
    path = os.path.join(DEBUG_DIR, f"{name}.png")
    try:
        page.screenshot(path=path)
        print(f"   📷 스크린샷: {path}")
    except Exception:
        pass


def _make_context(playwright, headless: bool = True) -> tuple:
    browser = playwright.chromium.launch(
        headless=headless,
        args=["--no-sandbox", "--disable-dev-shm-usage"],
    )
    context = browser.new_context(
        viewport={"width": 1280, "height": 900},
        user_agent=(
            "Mozilla/5.0 (X11; Linux x86_64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/124.0.0.0 Safari/537.36"
        ),
        locale="ko-KR",
        timezone_id="Asia/Seoul",
        storage_state=INSTA_STATE if os.path.exists(INSTA_STATE) else None,
    )
    return browser, context


def _get_caption(page: Page) -> str:
    """게시물 캡션 텍스트 추출"""
    try:
        return page.locator("._a9zr").first.inner_text(timeout=5000)
    except Exception:
        return ""


def _click_translate(page: Page) -> bool:
    """'번역 보기' 버튼 클릭"""
    try:
        btn = page.locator("span:has-text('번역 보기')").first
        btn.wait_for(state="visible", timeout=5000)
        btn.click()
        return True
    except Exception:
        return False


def _wait_for_translation(page: Page, original: str, timeout: int = 20) -> str:
    """번역 텍스트 안정화 대기"""
    deadline = time.time() + timeout
    last = ""
    stable_since = None

    while time.time() < deadline:
        current = _get_caption(page).strip()
        if current and current != original:
            if current != last:
                last = current
                stable_since = time.time()
            elif stable_since and time.time() - stable_since >= 2:
                return current
        time.sleep(0.5)

    return last or original


def _download_image(url: str, path: str) -> bool:
    try:
        resp = requests.get(url, timeout=15)
        resp.raise_for_status()
        with open(path, "wb") as f:
            f.write(resp.content)
        return True
    except Exception as e:
        print(f"   ⚠️ 이미지 다운로드 실패: {e}")
        return False


# ── 메인 함수 ─────────────────────────────────────────────────────

def scrape_posts(loaded_texts: list[str]) -> tuple[list[str], list[str], list[str]]:
    """
    Instagram @evonikpc 게시물 수집

    Returns:
        english_texts: 영문 원문 리스트
        korean_texts:  한국어 번역 리스트
        img_paths:     다운로드된 이미지 경로 리스트
    """
    whole = ",".join(loaded_texts)
    english_texts: list[str] = []
    korean_texts: list[str] = []
    img_paths: list[str] = []

    with sync_playwright() as p:
        browser, context = _make_context(p, headless=True)
        page = context.new_page()

        print("   Instagram 접속 중...")
        page.goto("https://www.instagram.com/evonikpc/", wait_until="domcontentloaded")
        page.wait_for_timeout(8000)

        # 로그인 확인
        if "login" in page.url:
            _save_debug(page, "insta_login_required")
            browser.close()
            raise RuntimeError(
                "Instagram 세션 만료. scripts/save_sessions.py를 로컬에서 실행하여 세션을 갱신하세요."
            )

        # 팝업 닫기 (알림 허용 등)
        try:
            page.locator("button:has-text('나중에')").first.click(timeout=3000)
        except Exception:
            pass
        try:
            page.locator("button:has-text('닫기')").first.click(timeout=2000)
        except Exception:
            pass

        page.wait_for_timeout(3000)

        # 게시물 목록 수집
        posts = page.locator("div._aagw").all()
        print(f"   게시물 {len(posts)}개 발견")

        for i, post in enumerate(posts):
            try:
                post.scroll_into_view_if_needed()
                page.wait_for_timeout(1500)
                post.click()
                page.wait_for_timeout(3000)

                english_text = _get_caption(page)
                if not english_text:
                    page.keyboard.press("Escape")
                    page.wait_for_timeout(1000)
                    continue

                # 중복 체크 → 이전에 수집한 게시물이면 중단
                if english_text[30:100] in whole:
                    print(f"   ✅ 게시물 {i+1}: 중복 발견 → 수집 중단")
                    page.keyboard.press("Escape")
                    break

                # 번역 클릭
                if _click_translate(page):
                    korean_text = _wait_for_translation(page, english_text)
                else:
                    korean_text = english_text

                english_texts.append(english_text)
                korean_texts.append(korean_text)

                print(f"\n{'='*55}")
                print(f"   게시물 {i+1} 수집 완료")
                print(f"   🇺🇸 영문 (앞 150자): {english_text[:150]}")
                print(f"   🇰🇷 한글 (앞 150자): {korean_text[:150]}")
                print(f"{'='*55}")

                page.keyboard.press("Escape")
                page.wait_for_timeout(1500)

            except Exception as e:
                print(f"   ⚠️ 게시물 {i+1} 수집 오류: {e}")
                _save_debug(page, f"insta_error_post{i}")
                try:
                    page.keyboard.press("Escape")
                except Exception:
                    pass
                continue

        # 이미지 다운로드 (신규 게시물 수만큼)
        if english_texts:
            print(f"\n   이미지 다운로드 중...")
            img_elements = page.locator("div._aagv img").all()
            for idx in range(min(len(english_texts), len(img_elements))):
                img_url = img_elements[idx].get_attribute("src")
                img_path = os.path.join(IMAGES_DIR, f"post{idx}.jpg")
                if _download_image(img_url, img_path):
                    img_paths.append(img_path)
                    print(f"   ✅ 이미지 {idx+1}: {img_path}")
                else:
                    img_paths.append(None)

        browser.close()

    return english_texts, korean_texts, img_paths
