# Random Weekly SEO Article Publisher

This website includes a GitHub Actions workflow that publishes one **random, prewritten, unpublished article** every Wednesday.

## What it does

Each run:

1. Reads `automation/article_queue.json`.
2. Excludes article slugs listed in `automation/published_queue.json`.
3. Randomly selects one remaining article.
4. Creates `resources/<article-slug>/index.html`.
5. Updates `resources/index.html`.
6. Updates `sitemap.xml`.
7. Records the slug so it cannot be published twice.
8. Commits the changes to the `main` branch.

No paid API or AI service is required. The system publishes from the reviewed article queue already included in the repository.

## Required GitHub settings

In the repository, open:

**Settings → Actions → General**

Under **Actions permissions**, select:

**Allow all actions and reusable workflows**

Under **Workflow permissions**, select:

**Read and write permissions**

Click **Save**.

## Test the workflow

1. Open the repository's **Actions** tab.
2. Select **Publish random weekly SEO article**.
3. Click **Run workflow**.
4. Choose the `main` branch.
5. Click the green **Run workflow** button.

A successful test creates one article, updates the Resource Center and sitemap, and triggers a GitHub Pages deployment.

## Schedule

The workflow runs every Wednesday at `14:15 UTC`.

- Approximately 9:15 AM Central during daylight-saving time.
- Approximately 8:15 AM Central during standard time.

GitHub Actions cron schedules always use UTC.

## Add more future articles

Add new objects to:

`automation/article_queue.json`

Each article needs:

- `slug`
- `title`
- `category`
- `description`
- `sections`

Do not reuse a slug. The publisher validates the queue and stops if duplicate slugs are detected.

## Important limitation

This system randomly publishes existing reviewed content. It does not invent a brand-new article topic or article text on every run. Generating new content automatically would require an external content-generation API, API credentials stored as GitHub Secrets, quality controls, and fact-checking before publication.
