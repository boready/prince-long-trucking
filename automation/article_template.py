from pathlib import Path
import json, html, re


def sid(s):
    return re.sub(r'[^a-z0-9]+', '-', s.lower()).strip('-')


def render_article(post, pub):
    slug = post['slug']
    title = post['title']
    cat = post['category']
    desc = post['description']
    sections = post['sections']
    url = f'https://princeandlong.com/resources/{slug}/'

    schema = {
        '@context': 'https://schema.org',
        '@graph': [
            {
                '@type': 'Article',
                'headline': title,
                'description': desc,
                'datePublished': pub,
                'dateModified': pub,
                'mainEntityOfPage': url,
                'image': 'https://princeandlong.com/assets/peterbilt-golden-closeup.webp',
                'author': {'@type': 'Organization', 'name': 'Prince & Long Trucking, LLC'},
                'publisher': {'@type': 'Organization', 'name': 'Prince & Long Trucking, LLC'},
            },
            {
                '@type': 'BreadcrumbList',
                'itemListElement': [
                    {'@type': 'ListItem', 'position': 1, 'name': 'Home', 'item': 'https://princeandlong.com/'},
                    {'@type': 'ListItem', 'position': 2, 'name': 'Resources', 'item': 'https://princeandlong.com/resources/'},
                    {'@type': 'ListItem', 'position': 3, 'name': title, 'item': url},
                ],
            },
        ],
    }

    toc = ''.join(
        f'<li><a href="#{sid(heading)}">{html.escape(heading)}</a></li>'
        for heading, _ in sections
    )
    article_body = ''.join(
        f'<h2 id="{sid(heading)}">{html.escape(heading)}</h2><p>{html.escape(paragraph)}</p>'
        for heading, paragraph in sections
    )
    words = sum(len(paragraph.split()) for _, paragraph in sections) + 180
    minutes = max(3, round(words / 210))

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <title>{html.escape(title)} | Prince &amp; Long</title>
  <meta name="description" content="{html.escape(desc)}">
  <link rel="canonical" href="{url}">
  <meta name="robots" content="index,follow,max-image-preview:large">
  <meta property="og:type" content="article">
  <meta property="og:title" content="{html.escape(title)}">
  <meta property="og:description" content="{html.escape(desc)}">
  <meta property="og:url" content="{url}">
  <meta property="og:image" content="https://princeandlong.com/assets/peterbilt-golden-closeup.webp">
  <link href="../../styles.css" rel="stylesheet">
  <link href="../../assets/favicon-32.png" rel="icon">
  <script type="application/ld+json">{json.dumps(schema, separators=(',', ':'))}</script>
</head>
<body class="resource-article-page">
<a class="skip-link" href="#main-content">Skip to main content</a>
<header class="site-header pl-pro-header">
  <a class="brand" href="../../"><img alt="Prince &amp; Long Trucking LLC" src="../../assets/logo-transparent.png"></a>
  <nav aria-label="Main navigation" class="nav pl-pro-nav">
    <a href="../../">Home</a><a href="../../#services">Services</a><a href="../../#area">Service Area</a>
    <a aria-current="page" href="../../resources/">Resources</a><a href="../../about/">About &amp; Safety</a><a href="../../contact/">Request Pricing</a>
  </nav>
  <a class="header-call pl-pro-call" href="tel:17858445001">Call (785) 844-5001</a>
</header>
<main class="seo-page" id="main-content">
  <nav class="article-breadcrumbs" aria-label="Breadcrumb"><a href="../../">Home</a><span aria-hidden="true">/</span><a href="../">Resources</a><span aria-hidden="true">/</span><span aria-current="page">Article</span></nav>
  <section class="seo-page-hero">
    <p class="kicker">{html.escape(cat)}</p><h1>{html.escape(title)}</h1><p>{html.escape(desc)}</p>
    <div class="actions"><a class="btn gold" href="../../contact/">Request Pricing</a></div>
  </section>
  <article class="seo-copy">
    <p class="article-meta"><span>Prince &amp; Long Resource Center</span><span>Updated {pub}</span><span>{minutes} min read</span></p>
    <p class="article-deck">{html.escape(desc)}</p>
    <div class="article-note"><strong>Planning note:</strong> Confirm project-specific material and construction requirements with the appropriate supplier or contractor.</div>
    <nav class="article-toc" aria-label="Article contents"><strong>In this guide</strong><ol>{toc}</ol></nav>
    {article_body}
    <h2>Plan the delivery before ordering</h2>
    <p>Provide the project address, measurements, expected material, quantity, timing and site-access details. Identify overhead lines, soft ground, narrow gates, steep grades and limited turnaround areas. A loaded dump truck requires safe access and the driver must make the final placement decision.</p>
    <h2>Get a local project quote</h2>
    <p>Prince &amp; Long Trucking provides hauling and material delivery support across Wamego, Manhattan, Junction City and surrounding Northeast Kansas communities. Availability, source location, load size and access all affect scheduling and pricing.</p>
    <div class="content-link-grid"><a href="../../services/dump-truck-hauling/">Explore hauling services</a><a href="../../resources/">View all resources</a><a href="../../contact/">Request delivery pricing</a></div>
    <section class="article-cta"><h2>Need hauling or material delivery?</h2><p>Send your location, project details and access notes for a project-specific response.</p><a class="btn gold" href="../../contact/">Request Pricing</a></section>
  </article>
</main>
<footer class="site-footer"><div class="footer-bottom"><span>© 2026 Prince &amp; Long Trucking, LLC.</span><span><a href="../../resources/">Resource Center</a></span></div></footer>
<a class="sticky-call" href="tel:17858445001">Call Now</a>
</body>
</html>"""


def rebuild_resources_index(root):
    idx = root / 'resources' / 'index.html'
    text = idx.read_text(encoding='utf-8')
    published = json.loads((root / 'automation' / 'published_queue.json').read_text(encoding='utf-8'))
    queue = {
        item['slug']: item
        for item in json.loads((root / 'automation' / 'article_queue.json').read_text(encoding='utf-8'))
    }

    for slug in published:
        post = queue.get(slug)
        if not post or f'href="{slug}/"' in text:
            continue
        card = (
            f'<a class="resource-card" data-category="{html.escape(post["category"])}" href="{slug}/">'
            f'<span class="resource-cat">{html.escape(post["category"])}</span>'
            f'<h2>{html.escape(post["title"])}</h2>'
            f'<p>{html.escape(post["description"])}</p>'
            '<span class="read-more">Read guide →</span></a>'
        )
        text = text.replace('</section></main>', card + '</section></main>', 1)

    idx.write_text(text, encoding='utf-8')


def rebuild_sitemap(root):
    urls = []
    for file_path in sorted(root.rglob('index.html')):
        relative = file_path.relative_to(root)
        if any(part.startswith('.') or part == 'automation' for part in relative.parts):
            continue
        path = '/' if relative.as_posix() == 'index.html' else '/' + relative.parent.as_posix().strip('/') + '/'
        urls.append('https://princeandlong.com' + path)

    xml = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
    ]
    xml.extend(f'  <url><loc>{html.escape(url)}</loc></url>' for url in urls)
    xml.append('</urlset>')
    (root / 'sitemap.xml').write_text('\n'.join(xml) + '\n', encoding='utf-8')
