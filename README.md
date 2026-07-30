# Prince & Long Trucking Website

Production static website for **princeandlong.com**.

## Upload to GitHub

Upload the **contents of this folder** to the root of the `boready/prince-long-trucking` repository. `index.html`, `CNAME`, `sitemap.xml`, `resources/`, `assets/`, and `.github/` must appear at the repository root.

## GitHub Pages

1. Open **Settings → Pages**.
2. Choose **Deploy from a branch**.
3. Select `main` and `/ (root)`.
4. Set the custom domain to `princeandlong.com`.
5. Enable **Enforce HTTPS** after DNS verification succeeds.

## Weekly resource publishing

`.github/workflows/publish-weekly-article.yml` publishes one queued guide each Wednesday. In **Settings → Actions → General → Workflow permissions**, select **Read and write permissions**. Then run the workflow manually once from the Actions tab to test it.

Queued content is stored in `automation/article_queue.json`. Published slugs are tracked in `automation/published_queue.json`. The workflow updates the Resources index and sitemap automatically.

## Random weekly article publishing

The repository includes `.github/workflows/publish-weekly-article.yml`. It randomly publishes one unpublished article from `automation/article_queue.json` every Wednesday and prevents repeats using `automation/published_queue.json`.

See `WEEKLY-SEO-AUTOMATION.md` for GitHub permission settings and testing instructions.
