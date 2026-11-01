# Private instructor records

**Do not use this folder for real student records in the public course repository.**

Keep complete assessment records, private feedback, and any student information that should not be public in a separate private instructor repository with access limited to trusted GeekInk instructors.

The public learning tracker reads only `data/published-assessments.json`. Add a sanitized score record there only when the student and instructor have approved public display. Example:
```json
[
  {
    "github_username": "studenthandle",
    "assignment_id": "markdown-profile",
    "status": "graded",
    "score": 86,
    "max_score": 100,
    "publish_score": true
  }
]
```
