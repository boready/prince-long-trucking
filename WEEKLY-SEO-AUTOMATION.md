# Weekly SEO Article Publisher

This package includes 25 published resource articles and 27 additional queued articles.

## How it works
- GitHub Actions runs every Wednesday.
- `automation/publish_next.py` publishes the next article in `article_queue.json`.
- It adds the article to the Resource Center and regenerates `sitemap.xml`.
- The workflow commits the update to the repository, allowing GitHub Pages to deploy it.

## One-time GitHub setup
1. Upload every file and folder in this package, including `.github` and `automation`.
2. Open the GitHub repository: Settings → Actions → General.
3. Under Workflow permissions, select **Read and write permissions**.
4. Save the setting.
5. Open Actions → Publish weekly SEO article → Run workflow to test it manually.

## Important
The workflow publishes from a reviewed local queue and does not require an AI API key. Review or edit `automation/article_queue.json` at any time.
