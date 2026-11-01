# GeekInk Automated Learning Tracker

A GitHub-native learning tracker using GitHub Pages, GitHub Actions, pull-request submissions, instructor review records, and a public aggregate dashboard.

## Features
- Course and lesson portal built with GitHub Pages.
- Student registry and individual progress records.
- Pull-request-based assignment submissions.
- Automated submission validation and progress aggregation.
- Instructor-controlled grading through review JSON files.
- Public dashboard showing aggregate progress and published scores.
- GitHub Actions deployment.

## Architecture and privacy
This is a static GitHub Pages application. It does **not** provide private student accounts or private data storage.
- Student submissions are pull requests. Repository visibility and PR visibility follow GitHub repository settings.
- Instructor review records live in `instructor/reviews/`. Keep this repository private if those files contain personal information.
- The generated `docs/data/dashboard.json` is public when published. It contains only fields intentionally approved for publication.
- Do not store phone numbers, home addresses, sensitive personal data, passwords, API keys, or private feedback in public files.
- For a public course repository, publish only anonymized aggregate results or explicitly approved student display names and scores.

## Quick start
1. Create a GitHub repository named `geekink-automated-learning-tracker`.
2. Upload this project, preserving the folder structure.
3. In **Settings → Pages**, choose **GitHub Actions** as the source.
4. In **Settings → Actions → General**, allow the workflow to create pull requests only if you later add that capability. The included workflows need read access and Pages deployment permissions.
5. Commit to `main`. The Pages workflow deploys the site from `docs/`.
6. Edit `config/course.json` and `config/lessons.json`.
7. Add students to `data/students.json` or accept a student registration PR.
8. Instruct students to fork the repository and submit assignments using the PR template.

## Student submission workflow
1. Student forks the repository.
2. Student adds `submissions/<github-username>/<assignment-id>.json`.
3. Student opens a pull request against `main`.
4. The validation workflow checks the JSON schema, username, assignment ID, and required fields.
5. Instructor reviews the work and merges accepted submissions.
6. On merge, the aggregation workflow updates the dashboard data and deploys the site.

See `docs/submit.md` for the exact submission format.

## Instructor grading
After merging a submission, create or update:
`instructor/reviews/<github-username>/<assignment-id>.json`

Example:
```json
{
  "github_username": "studenthandle",
  "assignment_id": "markdown-profile",
  "status": "graded",
  "score": 86,
  "max_score": 100,
  "rubric": {
    "markdown_structure": 18,
    "formatting": 9,
    "lists_and_links": 9,
    "tables": 9,
    "code_and_images": 14,
    "collapsible_sections": 14,
    "readme_quality": 13
  },
  "publish_score": true,
  "public_feedback": "Good structure and clear documentation.",
  "reviewed_by": "instructor-github-username",
  "reviewed_at": "2026-11-01"
}
```
Only `publish_score: true` reviews are included in public dashboard output. Keep detailed/private feedback in a private system, not this public repository.

## Progress records
Students can track lessons by adding `progress/<github-username>.json` through a PR. The dashboard aggregates completed lessons and accepted assignments. A self-reported lesson completion is not equivalent to instructor verification; the dashboard labels it accordingly.

## Local preview
The site is plain HTML/CSS/JavaScript. Open `docs/index.html` in a browser, or run a local static server:
```bash
python -m http.server 8000 --directory docs
```
Then visit `http://localhost:8000`.

## Repository structure
```text
.
├── .github/
│   ├── ISSUE_TEMPLATE/student-registration.yml
│   ├── PULL_REQUEST_TEMPLATE.md
│   └── workflows/
├── config/
├── data/
├── docs/
├── instructor/reviews/
├── progress/
├── submissions/
└── scripts/
```

## Recommended governance
- Protect `main` with pull-request reviews.
- Require instructor approval before merging submissions.
- Keep instructor review files restricted to trusted maintainers.
- Publish only the minimum student information needed.
- Back up the repository and periodically export assessment records.
