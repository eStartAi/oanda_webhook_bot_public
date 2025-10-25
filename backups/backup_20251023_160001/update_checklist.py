import sys
from datetime import datetime

mode = sys.argv[1]  # 'live' or 'practice'
backup_path = sys.argv[2]

template_file = f"CHECKLIST.{mode}.md"
output_file = "CHECKLIST.md"

with open(template_file, "r") as f:
    content = f.read()

content = content.replace("{{backup_path}}", backup_path)
from datetime import datetime, timezone
content = content.replace("{{timestamp}}", datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S"))


with open(output_file, "w") as f:
    f.write(content)

print(f"✅ CHECKLIST.md updated from {template_file}")
