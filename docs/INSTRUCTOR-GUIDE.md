# Instructor operating guide

## Register students
Edit `data/students.json` and add:
```json
{"github_username":"studenthandle","display_name":"Student display name","cohort":"GeekInk Cohort","active":true,"publish_profile":true}
```
Set `publish_profile` to false unless the learner has agreed to public display. Registered learners without public profiles still contribute to aggregate counts.

## Review a submission
1. Review the student's pull request and linked project.
2. Merge the PR only after the submission meets the requirements.
3. Store the full rubric, private notes and review history in a separate **private instructor repository**.
4. If a score is approved for public display, add a sanitized record to `data/published-assessments.json` in this public course repository.
5. Commit to `main`. The dashboard workflow regenerates the public dashboard.

## Record lesson progress
A student can submit `progress/studenthandle.json` via PR. These lesson completions are self-reported. The instructor should review evidence before merging if verified progress is required.

## Instructor dashboard
The public homepage includes cohort metrics, approved public profiles, accepted submissions and published scores. It is a public reporting view, not a private admin console. Use GitHub repository permissions and the private instructor repository for confidential records.

## Security
The PR validation workflow is read-only and does not execute student code. Never run untrusted student code in workflows with write permissions or secrets. Do not publish private feedback, personal contact information, or unapproved student scores.
