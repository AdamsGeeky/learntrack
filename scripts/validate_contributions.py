import json, os, re, subprocess, sys
from pathlib import Path

ROOT = Path(".")
BASE = os.environ.get("BASE_SHA", "")
HEAD = os.environ.get("HEAD_SHA", "HEAD")
if not BASE:
    print("BASE_SHA missing; cannot safely determine changed files.")
    sys.exit(1)
changed = subprocess.check_output(["git","diff","--name-only",f"{BASE}...{HEAD}"], text=True).splitlines()
errors = []
username_re = re.compile(r"^[A-Za-z0-9-]{1,39}$")
assignment_ids = {x["id"] for x in json.loads(Path("data/assignments.json").read_text())}
lesson_ids = {x["id"] for x in json.loads(Path("config/lessons.json").read_text())}

for name in changed:
    p = Path(name)
    if not (name.startswith("submissions/") or name.startswith("progress/")) or p.suffix != ".json":
        continue
    try:
        obj = json.loads(p.read_text())
        if name.startswith("submissions/"):
            parts = p.parts
            if len(parts) != 3:
                raise ValueError("Expected submissions/<username>/<assignment-id>.json")
            folder_user, filename = parts[1], p.stem
            if not username_re.fullmatch(folder_user):
                raise ValueError("Invalid GitHub username in folder")
            if obj.get("github_username","").lower() != folder_user.lower():
                raise ValueError("github_username must match folder name")
            if obj.get("assignment_id") != filename or filename not in assignment_ids:
                raise ValueError("Assignment ID must match a configured assignment")
            url = obj.get("project_url","")
            if not isinstance(url,str) or not url.startswith("https://github.com/"):
                raise ValueError("project_url must be an https://github.com/ URL")
            if not obj.get("submitted_at"):
                raise ValueError("submitted_at is required")
        else:
            if len(p.parts) != 2 or not username_re.fullmatch(p.stem):
                raise ValueError("Expected progress/<github-username>.json")
            if obj.get("github_username","").lower() != p.stem.lower():
                raise ValueError("github_username must match filename")
            completed = obj.get("completed_lessons", [])
            if not isinstance(completed, list) or any(x not in lesson_ids for x in completed):
                raise ValueError("completed_lessons contains unknown lesson IDs")
    except Exception as e:
        errors.append(f"{name}: {e}")

if errors:
    print("\\n".join(errors))
    sys.exit(1)
print("All changed student contribution files are valid.")
