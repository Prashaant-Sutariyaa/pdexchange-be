import httpx
import time
from typing import List, Optional
from pathlib import Path
from app.core.config import settings

from jinja2 import (
    Environment,
    FileSystemLoader,
    select_autoescape,
)


class GraphMailer:
    def __init__(self):
        self.tenant_id = settings.graph_tenant_id

        self.client_id = settings.graph_client_id

        self.client_secret = settings.graph_client_secret

        self.sender_email = settings.graph_sender_email

        self._token = None
        self._expires_at = 0

    async def get_access_token(self) -> Optional[str]:
        # Check cache
        if self._token and self._expires_at > time.time():
            return self._token

        url = f"https://login.microsoftonline.com/{self.tenant_id}/oauth2/v2.0/token"
        data = {
            "client_id": self.client_id,
            "scope": "https://graph.microsoft.com/.default",
            "client_secret": self.client_secret,
            "grant_type": "client_credentials",
        }

        async with httpx.AsyncClient() as client:
            response = await client.post(url, data=data)

        if response.status_code != 200:
            print(f"Token Error: {response.text}")
            return None

        token_data = response.json()
        self._token = token_data["access_token"]
        # Cache for the duration minus a 60-second buffer
        self._expires_at = time.time() + token_data["expires_in"] - 60
        return self._token

    async def send_mail(
        self,
        to_emails: List[str],
        subject: str,
        html_content: str,
        cc_emails: List[str] = None,
    ):
        token = await self.get_access_token()
        if not token:
            return {"success": False, "message": "Failed to acquire token"}

        url = f"https://graph.microsoft.com/v1.0/users/{self.sender_email}/sendMail"

        email_data = {
            "message": {
                "subject": subject,
                "body": {"contentType": "HTML", "content": html_content},
                "toRecipients": [
                    {"emailAddress": {"address": email}} for email in to_emails
                ],
                "ccRecipients": [
                    {"emailAddress": {"address": email}} for email in (cc_emails or [])
                ],
            },
            "saveToSentItems": "true",
        }

        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        }

        async with httpx.AsyncClient() as client:
            response = await client.post(url, json=email_data, headers=headers)

        if response.status_code == 202:
            return {"success": True}

        return {"success": False, "message": response.text}


# Instantiate as a singleton
mailer = GraphMailer()


# ============================================================
# 🔹 TEMPLATE ENVIRONMENT
# ============================================================

template_dir = Path(__file__).resolve().parent.parent.parent / "templates" / "emails"

jinja_env = Environment(
    loader=FileSystemLoader(template_dir),
    autoescape=select_autoescape(["html", "xml"]),
)

# ============================================================
# 🔹 LOAD TEMPLATE
# ============================================================


def load_html_template(
    template_name: str,
):

    return jinja_env.get_template(template_name)


# ============================================================
# 🔹 RENDER TEMPLATE
# ============================================================


def render_template(
    template,
    context: dict,
):

    return template.render(**context)


# ============================================================
# 🔹 SEND SENTINEL JOB EMAIL
# ============================================================


# async def send_sentinel_job_completed_email(
#     context: dict,
# ):

#     try:

#         html_template = load_html_template("sentinel_job_completed.html")

#         html_content = render_template(
#             html_template,
#             context,
#         )

#         result = await mailer.send_mail(
#             to_emails=[
#                 "arbaj.b@prospectvine.com",
#             ],
#             subject=(f"Sentinel Job Completed - " f"{context['department']}"),
#             html_content=html_content,
#         )

#         print(
#             "EMAIL RESULT:",
#             result,
#         )

#     except Exception as e:

#         print(
#             "EMAIL ERROR:",
#             str(e),
#         )
