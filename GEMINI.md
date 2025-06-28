# Gemini Project Workflow: Git Commit

**Objective:** To automate the process of creating a Git commit based on the current file changes.

**Trigger Command:** "Commit the changes", "Create a commit", or similar phrases.

**Workflow:**

1.  **Check Status:** Run `git status` to see the modified, new, and deleted files.
2.  **Stage Files:** Add all relevant changes to the staging area using `git add`.
3.  **Analyze Diff:** Run `git diff --staged` to understand the exact changes made.
4.  **Generate Message:** Create a descriptive commit message in English, summarizing the changes.
5.  **Execute Commit:** Run `git commit -m "..."` with the generated message.
6.  **Confirm:** Run `git status` again to confirm the commit was successful.

## Gemini Added Memories
- use uv to install python dependencies