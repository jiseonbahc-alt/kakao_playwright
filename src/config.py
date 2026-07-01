"""
환경변수 및 경로 상수
"""
import os
from dotenv import load_dotenv

load_dotenv()

# ── 인증 ──────────────────────────────────────────────
INSTA_USERNAME = os.getenv("INSTA_USERNAME")
INSTA_PASSWORD = os.getenv("INSTA_PASSWORD")
KAKAO_USERNAME = os.getenv("KAKAO_USERNAME")
KAKAO_PASSWORD = os.getenv("KAKAO_PASSWORD")
GMAIL_EMAIL = os.getenv("GMAIL_EMAIL")
GMAIL_APP_PASSWORD = os.getenv("GMAIL_APP_PASSWORD")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# ── 경로 ──────────────────────────────────────────────
PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SESSIONS_DIR = os.path.join(PROJECT_DIR, "sessions")
IMAGES_DIR = os.path.join(PROJECT_DIR, "images")
DEBUG_DIR = os.path.join(PROJECT_DIR, "debug_screenshots")
TEXTS_JSON = os.path.join(PROJECT_DIR, "texts.json")

INSTA_STATE = os.path.join(SESSIONS_DIR, "instagram_state.json")
KAKAO_STATE = os.path.join(SESSIONS_DIR, "kakao_state.json")

# ── 카카오 채널 ────────────────────────────────────────
KAKAO_CHANNEL_ID = "_QNVxoxj"
KAKAO_POST_URL = f"https://center-pf.kakao.com/{KAKAO_CHANNEL_ID}/posts"
KAKAO_MSG_URL = f"https://business.kakao.com/{KAKAO_CHANNEL_ID}/messages/new/feed"

# ── 이메일 수신자 ──────────────────────────────────────
EMAIL_RECIPIENTS = ["sean.bahc@evonik.com"]

# ── 기타 ──────────────────────────────────────────────
DRY_RUN = os.getenv("DRY_RUN", "false").lower() == "true"

os.makedirs(SESSIONS_DIR, exist_ok=True)
os.makedirs(IMAGES_DIR, exist_ok=True)
os.makedirs(DEBUG_DIR, exist_ok=True)
