import re
import json
from pathlib import Path

# =====================================
# READ INPUT FILE
# =====================================

input_path = Path("../input/raw-text.txt")

with open(input_path, "r", encoding="utf-8") as file:
    raw_text = file.read()

# =====================================
# REGEX PATTERNS
# =====================================

# Emails
email_pattern = r'\b[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}\b'

# URLs
url_pattern = r'https?://[^\s]+'

# Credit cards
credit_card_pattern = r'\b(?:\d{4}[- ]?){3}\d{4}\b'

# Hashtags
hashtag_pattern = r'#\w+'

# =====================================
# EXTRACTION
# =====================================

emails = re.findall(email_pattern, raw_text)

urls = re.findall(url_pattern, raw_text)

credit_cards = re.findall(credit_card_pattern, raw_text)

hashtags = re.findall(hashtag_pattern, raw_text)

# =====================================
# ALU EMAIL VALIDATION
# =====================================

alu_official = [
    email for email in emails
    if email.endswith("@alueducation.com")
]

alu_alumni = [
    email for email in emails
    if email.endswith("@alumni.alueducation.com")
]

alu_si = [
    email for email in emails
    if email.endswith("@si.alueducation.com")
]

# =====================================
# SECURITY CHECKS
# =====================================

unsafe_patterns = [
    r'<script.*?>.*?</script>',
    r'DROP TABLE'
]

unsafe_content = []

for pattern in unsafe_patterns:
    matches = re.findall(pattern, raw_text, re.IGNORECASE)
    unsafe_content.extend(matches)

# =====================================
# MASK CREDIT CARD NUMBERS
# =====================================

def mask_card(card):
    digits = re.sub(r'\D', '', card)
    return "****-****-****-" + digits[-4:]

masked_cards = [mask_card(card) for card in credit_cards]

# =====================================
# FINAL OUTPUT
# =====================================

results = {
    "emails": emails,
    "alu_official_emails": alu_official,
    "alu_alumni_emails": alu_alumni,
    "alu_si_emails": alu_si,
    "credit_cards_masked": masked_cards,
    "urls": urls,
    "hashtags": hashtags,
    "unsafe_content_detected": unsafe_content
}

# =====================================
# SAVE OUTPUT
# =====================================

output_path = Path("../output/sample-output.json")

with open(output_path, "w", encoding="utf-8") as outfile:
    json.dump(results, outfile, indent=4)

# Print results
print(json.dumps(results, indent=4))
