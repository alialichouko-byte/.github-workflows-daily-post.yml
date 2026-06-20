import requests, os, random
from email.mime.text import MIMEText
import smtplib, base64

GROQ_KEY = os.environ['GROQ_API_KEY']
BLOG_ID = os.environ['BLOGGER_BLOG_ID']
EMAIL = os.environ['GOOGLE_EMAIL']
APP_PASS = os.environ['GOOGLE_APP_PASSWORD']

topics = [
    "واحة فنت ورزازات دليل سياحي شامل 2026",
    "أفضل أماكن السياحة في ورزازات المغرب",
    "الصحراء المغربية رحلة من ورزازات",
    "قصبة أيت بنحدو التراث العالمي",
    "أفضل فنادق ورزازات 2026",
    "تكلفة رحلة ورزازات كاملة",
    "واحة فنت الجوهرة الخفية في المغرب",
    "مطاعم ورزازات الأفضل",
    "هوليود أفريقيا ورزازات السينما",
    "دليل المرشد السياحي في فنت"
]

topic = random.choice(topics)
print(f"📝 الموضوع: {topic}")

r = requests.post(
    "https://api.groq.com/openai/v1/chat/completions",
    headers={"Authorization": f"Bearer {GROQ_KEY}", "Content-Type": "application/json"},
    json={
        "model": "llama-3.3-70b-versatile",
        "temperature": 0.8,
        "messages": [
            {"role": "system", "content": "أنت كاتب محتوى سياحي محترف متخصص في السياحة المغربية وورزازات وواحة فنت."},
            {"role": "user", "content": f"""اكتب مقالاً سياحياً SEO احترافياً بالعربية عن: {topic}

المطلوب بهذا الترتيب:
TITLE: عنوان جذاب 60 حرف
CONTENT: مقال 800 كلمة احترافي مع فقرات منظمة ومعلومات عملية للسياح"""}
        ]
    }
)

text = r.json()['choices'][0]['message']['content']
lines = text.strip().split('\n')
title = lines[0].replace('TITLE:', '').replace('#', '').strip()
content = '\n'.join(lines[1:]).replace('CONTENT:', '').strip()

html = f"""
<div dir="rtl" style="font-family: Arial; line-height: 1.8; max-width: 800px; margin: auto;">
{content.replace(chr(10), '<br>')}
<hr>
<div style="background:#e8f4fd;padding:20px;border-radius:8px;margin-top:20px;">
<h3>📍 احجز جولتك في واحة فنت</h3>
<p>تواصل مع <strong>علي شوقر — مرشد سياحي محلي</strong> في ورزازات</p>
</div>
</div>
"""

url = f"https://www.googleapis.com/blogger/v3/blogs/{BLOG_ID}/posts/"
creds = base64.b64encode(f"{EMAIL}:{APP_PASS}".encode()).decode()

resp = requests.post(url,
    headers={"Authorization": f"Basic {creds}", "Content-Type": "application/json"},
    json={"title": title, "content": html}
)

if resp.status_code in [200, 201]:
    print(f"✅ نُشر بنجاح: {resp.json().get('url', '')}")
else:
    print(f"❌ خطأ: {resp.text}")
