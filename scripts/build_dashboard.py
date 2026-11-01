import json
from pathlib import Path
from datetime import datetime, timezone

def read_json(path, default):
    try: return json.loads(Path(path).read_text())
    except FileNotFoundError: return default

students = read_json("data/students.json", [])
lessons = read_json("config/lessons.json", [])
assignments = read_json("data/assignments.json", [])
registered = {s["github_username"].lower(): s for s in students if s.get("active", True)}
progress = {}
for p in Path("progress").glob("*.json"):
    try:
        obj = json.loads(p.read_text())
        progress[obj["github_username"].lower()] = obj
    except Exception:
        continue

# Public repository receives only instructor-approved, sanitized score records.
# Keep full review notes and private records in a separate private instructor repository.
reviews = {}
for obj in read_json("data/published-assessments.json", []):
    try:
        if obj.get("status") == "graded" and obj.get("publish_score") is True:
            reviews[(obj["github_username"].lower(), obj["assignment_id"])] = obj
    except Exception:
        continue

subs = []
for p in Path("submissions").glob("*/*.json"):
    try:
        obj = json.loads(p.read_text())
        user = obj["github_username"].lower()
        if user in registered:
            subs.append(obj)
    except Exception:
        continue

rows = []
for username, student in registered.items():
    prog = progress.get(username, {})
    completed = len(set(prog.get("completed_lessons", [])) & {x["id"] for x in lessons})
    accepted = [s for s in subs if s["github_username"].lower() == username]
    published_scores = [r["score"] for (u,a),r in reviews.items()
                        if u == username and r.get("publish_score") is True
                        and isinstance(r.get("score"), (int,float))]
    rows.append({
        "github_username": student["github_username"],
        "display_name": student.get("display_name") if student.get("publish_profile") else None,
        "completed_lessons": completed,
        "total_lessons": len(lessons),
        "lesson_completion": round(100*completed/len(lessons)) if lessons else 0,
        "accepted_assignments": len(accepted),
        "published_score": round(sum(published_scores)/len(published_scores),1) if published_scores else None
    })

public_students = [r for r in rows if r["display_name"]]
all_scores = [r["published_score"] for r in rows if r["published_score"] is not None]
accepted_count = len(subs)
avg_completion = round(sum(r["lesson_completion"] for r in rows)/len(rows)) if rows else 0
recent = []
for s in sorted(subs, key=lambda x: x.get("submitted_at",""), reverse=True)[:10]:
    user = s["github_username"].lower()
    st = registered.get(user,{})
    # Project URL is deliberately published only for a registered student; submissions are public PR content.
    recent.append({
        "github_username": s["github_username"],
        "display_name": st.get("display_name") if st.get("publish_profile") else None,
        "assignment_title": next((a["title"] for a in assignments if a["id"] == s["assignment_id"]), s["assignment_id"]),
        "project_url": s.get("project_url",""),
        "submitted_at": s.get("submitted_at","")
    })

dashboard = {
    "generated_at": datetime.now(timezone.utc).isoformat(),
    "summary": {
        "registered_students": len(registered),
        "average_lesson_completion": avg_completion,
        "accepted_submissions": accepted_count,
        "average_published_score": round(sum(all_scores)/len(all_scores),1) if all_scores else None
    },
    "students": public_students,
    "recent_submissions": recent
}
Path("docs/data").mkdir(parents=True, exist_ok=True)
Path("docs/data/dashboard.json").write_text(json.dumps(dashboard, indent=2) + "\\n")
Path("docs/data/course.json").write_text(json.dumps(read_json("config/course.json", {}), indent=2) + "\\n")
Path("docs/data/lessons.json").write_text(json.dumps(lessons, indent=2) + "\\n")
print("Dashboard data generated.")
