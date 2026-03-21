"""
로컬 1회성 세션 저장 스크립트
────────────────────────────────────────
실행 방법:
  python scripts/save_sessions.py

동작:
  1. Chromium 창을 열어 Instagram 수동 로그인 대기
  2. 로그인 완료 후 Enter → sessions/instagram_state.json 저장
  3. Kakao 수동 로그인 대기
  4. 로그인 완료 후 Enter → sessions/kakao_state.json 저장
  5. GitHub Secrets 등록용 내용 출력

GitHub Secrets에 등록할 키:
  INSTAGRAM_STATE_JSON  ← instagram_state.json 전체 내용
  KAKAO_STATE_JSON      ← kakao_state.json 전체 내용
"""

import json
import os
import sys

# 프로젝트 루트를 path에 추가
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from playwright.sync_api import sync_playwright
from src.config import SESSIONS_DIR, INSTA_STATE, KAKAO_STATE


def save_instagram_session() -> None:
    print("\n" + "="*60)
    print("📸 Instagram 세션 저장")
    print("="*60)
    print("브라우저가 열립니다. Instagram에 로그인하세요.")
    print("로그인 완료 후 이 터미널에서 Enter를 누르세요.\n")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=50)
        context = browser.new_context(
            viewport={"width": 1280, "height": 800},
            user_agent=(
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/124.0.0.0 Safari/537.36"
            ),
            locale="ko-KR",
            timezone_id="Asia/Seoul",
        )
        page = context.new_page()
        page.goto("https://www.instagram.com/")

        input("✋ Instagram 로그인 완료 후 Enter...")

        context.storage_state(path=INSTA_STATE)
        print(f"✅ 저장 완료: {INSTA_STATE}")
        browser.close()


def save_kakao_session() -> None:
    print("\n" + "="*60)
    print("💬 Kakao 세션 저장")
    print("="*60)
    print("브라우저가 열립니다. Kakao Business에 로그인하세요.")
    print("로그인 완료 후 이 터미널에서 Enter를 누르세요.\n")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=50)
        context = browser.new_context(
            viewport={"width": 1280, "height": 800},
            locale="ko-KR",
            timezone_id="Asia/Seoul",
        )
        page = context.new_page()
        page.goto("https://center-pf.kakao.com/")

        input("✋ Kakao 로그인 완료 후 Enter...")

        context.storage_state(path=KAKAO_STATE)
        print(f"✅ 저장 완료: {KAKAO_STATE}")
        browser.close()


def print_secrets_guide() -> None:
    print("\n" + "="*60)
    print("🔑 GitHub Secrets 등록 가이드")
    print("="*60)
    print("아래 링크에서 각 Secret을 등록하세요:")
    print("https://github.com/minsung1013/kakao_playwright/settings/secrets/actions")
    print()

    for path, key in [(INSTA_STATE, "INSTAGRAM_STATE_JSON"), (KAKAO_STATE, "KAKAO_STATE_JSON")]:
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                content = f.read()
            size_kb = len(content.encode()) / 1024
            print(f"  Secret 이름: {key}")
            print(f"  파일 크기:   {size_kb:.1f} KB (GitHub 한도 64KB)")
            print(f"  파일 경로:   {path}")
            print(f"  (파일 내용을 복사해서 Secret 값으로 붙여넣으세요)")
            print()
        else:
            print(f"  ⚠️ {path} 없음 - 세션 저장이 실패했을 수 있습니다")
            print()


if __name__ == "__main__":
    os.makedirs(SESSIONS_DIR, exist_ok=True)

    save_instagram_session()
    save_kakao_session()
    print_secrets_guide()

    print("완료! 세션 만료 시 이 스크립트를 다시 실행하세요.")
    print("(Instagram 세션: 약 90일 / Kakao 세션: 약 30일)")
