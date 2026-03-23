"""
이메일 알림 발송
"""
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from src.config import GMAIL_EMAIL, GMAIL_APP_PASSWORD, EMAIL_RECIPIENTS, KAKAO_CHANNEL_ID


def send_duplicate_notification_email() -> None:
    """중복 게시물 발견으로 중단됐을 때 이메일 알림"""
    if not GMAIL_EMAIL or not GMAIL_APP_PASSWORD:
        print("⚠️ Gmail 설정 없음, 이메일 스킵")
        return

    body = """안녕하세요!

에보닉 케어솔루션 인스타-카카오 자동화 포스팅 서비스입니다.

Instagram 수집 중 기존에 처리된 중복 게시물이 발견되어 수집이 중단되었습니다.
새로운 게시물이 없거나, 모든 신규 게시물이 이미 처리된 상태입니다.

별도 조치가 필요하지 않으면 이 메일을 무시하셔도 됩니다.

감사합니다.
에보닉 자동화 시스템
"""

    msg = MIMEMultipart()
    msg["From"] = GMAIL_EMAIL
    msg["To"] = ", ".join(EMAIL_RECIPIENTS)
    msg["Subject"] = "[에보닉] 카카오 자동화 - 중복 게시물 발견으로 수집 중단"
    msg.attach(MIMEText(body, "plain", "utf-8"))

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(GMAIL_EMAIL, GMAIL_APP_PASSWORD)
            server.sendmail(GMAIL_EMAIL, EMAIL_RECIPIENTS, msg.as_string())
        print("✅ 중복 알림 이메일 전송 완료")
    except smtplib.SMTPAuthenticationError:
        print("⚠️ Gmail 인증 실패 - GMAIL_APP_PASSWORD를 확인하세요")
    except Exception as e:
        print(f"⚠️ 이메일 전송 실패: {e}")


def send_notification_email(count: int, posts_data: list[dict]) -> None:
    if not GMAIL_EMAIL or not GMAIL_APP_PASSWORD:
        print("⚠️ Gmail 설정 없음, 이메일 스킵")
        return

    body = f"""안녕하세요!

에보닉 케어솔루션 인스타-카카오 자동화 포스팅 서비스입니다.
총 {count}개의 신규 게시글이 카카오 채널에 임시저장되었습니다.

{"="*70}
"""

    for i, data in enumerate(posts_data):
        body += f"""
📌 게시물 {i+1}
{"─"*50}

📝 영어 원문:
{data.get("english", "(없음)")}

{"─"*50}

✨ 소식 제목 (ChatGPT 작성):
{data.get("title", "(없음)")}

📄 소식 내용 (인스타그램 번역):
{data.get("korean", "(없음)")}

💬 메시지 내용 (ChatGPT 작성):
{data.get("message", "(없음)")}

{"="*70}
"""

    body += f"""

📋 카카오 채널 관리자 링크:

   • 소식 관리: https://center-pf.kakao.com/{KAKAO_CHANNEL_ID}/posts
   • 메시지 관리: https://business.kakao.com/{KAKAO_CHANNEL_ID}/messages
   • 카카오비즈니스: https://business.kakao.com/

확인 후 발행해주세요!

감사합니다.
에보닉 자동화 시스템
"""

    msg = MIMEMultipart()
    msg["From"] = GMAIL_EMAIL
    msg["To"] = ", ".join(EMAIL_RECIPIENTS)
    msg["Subject"] = f"[에보닉] 카카오 채널 신규 게시글 {count}개 임시저장 완료"
    msg.attach(MIMEText(body, "plain", "utf-8"))

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(GMAIL_EMAIL, GMAIL_APP_PASSWORD)
            server.sendmail(GMAIL_EMAIL, EMAIL_RECIPIENTS, msg.as_string())
        print("✅ 이메일 전송 완료")
    except smtplib.SMTPAuthenticationError:
        print("⚠️ Gmail 인증 실패 - GMAIL_APP_PASSWORD를 확인하세요")
    except Exception as e:
        print(f"⚠️ 이메일 전송 실패: {e}")
