import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime

def send_report(report, report_format, cfg):
    msg = MIMEMultipart()
    msg["From"] = cfg["smtp_user"]
    msg["To"] = cfg["email_to"]
    msg["Subject"] = f"BSO N02 - Raport skanu sieci {cfg['subnet']} - {datetime.now().strftime('%Y-%m-%d %H:%M')}"

    if report_format == "html":
        msg.attach(MIMEText(report, "html"))
    else:
        msg.attach(MIMEText(report, "plain"))

    print(f"Wysylam email do {cfg['email_to']} przez {cfg['smtp_server']}:{cfg['smtp_port']}")
    with smtplib.SMTP(cfg["smtp_server"], cfg["smtp_port"]) as s:
        s.starttls()
        s.login(cfg["smtp_user"], cfg["smtp_pass"])
        s.send_message(msg)
    print("Email wyslany!")