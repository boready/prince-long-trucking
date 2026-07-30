from pathlib import Path
import json, html, re

def sid(s): return re.sub(r'[^a-z0-9]+','-',s.lower()).strip('-')
def render_article(post,pub):
    slug,title,cat,desc=post['slug'],post['title'],post['category'],post['description']
    sections=post['sections'];url=f'https://princeandlong.com/resources/{slug}/'
    schema={"@context":"https://schema.org","@graph":[{"@type":"Article","headline":title,"description":desc,"datePublished":pub,"dateModified":pub,"mainEntityOfPage":url,"author":{"@type":"Organization","name":"Prince & Long Trucking, LLC"},"publisher":{"@type":"Organization","name":"Prince & Long Trucking, LLC"}},{"@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":1,"name":"Home","item":"https://princeandlong.com/"},{"@type":"ListItem","position":2,"name":"Resources","item":"https://princeandlong.com/resources/"},{"@type":"ListItem","position":3,"name":title,"item":url}]}]}
    toc=''.join(f'<li><a href="#{sid(h)}">{html.escape(h)}</a></li>' for h,_ in sections)
    body=''.join(f'<h2 id="{sid(h)}">{html.escape(h)}</h2><p>{html.escape(p)}</p>' for h,p in sections)
    return f'''<!DOCTYPE html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{html.escape(title)} | Prince & Long</title><meta name="description" content="{html.escape(desc)}"><link rel="canonical" href="{url}"><meta name="robots" content="index,follow"><link href="../../styles.css" rel="stylesheet"><link href="../../assets/favicon-32.png" rel="icon"><script type="application/ld+json">{json.dumps(schema,separators=(',',':'))}</script></head><body><header class="site-header pl-pro-header"><a class="brand" href="../../"><img alt="Prince & Long Trucking LLC" src="../../assets/logo-transparent.png"></a><nav class="nav pl-pro-nav"><a href="../../">Home</a><a href="../../#services">Services</a><a href="../../#area">Service Area</a><a href="../../resources/">Resources</a><a href="../../about/">About & Safety</a><a href="../../contact/">Request Pricing</a></nav><a class="header-call pl-pro-call" href="tel:17858445001">Call (785) 844-5001</a></header><main class="seo-page"><section class="seo-page-hero"><p class="kicker">{html.escape(cat)}</p><h1>{html.escape(title)}</h1><p>{html.escape(desc)}</p><div class="actions"><a class="btn gold" href="../../contact/">Request Pricing</a></div></section><article class="seo-copy"><p class="article-meta">Published {pub} · Prince & Long Trucking Resource Center</p><div class="article-note"><strong>Planning note:</strong> Confirm project-specific material and construction requirements with the appropriate supplier or contractor.</div><nav class="article-toc"><strong>In this guide</strong><ol>{toc}</ol></nav>{body}<h2>Plan the delivery before ordering</h2><p>Provide the project address, measurements, expected material, quantity, timing and site-access details. Identify overhead lines, soft ground, narrow gates, steep grades and limited turnaround areas. A loaded dump truck requires safe access and the driver must make the final placement decision.</p><h2>Get a local project quote</h2><p>Prince & Long Trucking provides hauling and material delivery support across Wamego, Manhattan, Junction City and surrounding Northeast Kansas communities. Availability, source location, load size and access all affect scheduling and pricing.</p><div class="article-cta"><h2>Need hauling or material delivery?</h2><p>Send your location, project details and access notes for a project-specific response.</p><a class="btn gold" href="../../contact/">Request Pricing</a></div></article></main><footer class="site-footer"><div class="footer-bottom"><span>© 2026 Prince & Long Trucking, LLC.</span><span><a href="../../resources/">Resource Center</a></span></div></footer><a class="sticky-call" href="tel:17858445001">Call Now</a></body></html>'''

def rebuild_resources_index(root):
    # Add newly published cards before closing grid; avoid duplicates
    idx=root/'resources'/'index.html';text=idx.read_text()
    published=json.loads((root/'automation'/'published_queue.json').read_text())
    queue={x['slug']:x for x in json.loads((root/'automation'/'article_queue.json').read_text())}
    for slug in published:
        p=queue[slug]
        if f'href="{slug}/"' in text: continue
        card=f'<a class="resource-card" data-category="{html.escape(p["category"])}" href="{slug}/"><span class="resource-cat">{html.escape(p["category"])}</span><h2>{html.escape(p["title"])}</h2><p>{html.escape(p["description"])}</p><span class="read-more">Read guide →</span></a>'
        text=text.replace('</section></main>',card+'</section></main>',1)
    idx.write_text(text)

def rebuild_sitemap(root):
    urls=[]
    for f in sorted(root.rglob('index.html')):
        rel=f.relative_to(root)
        if any(part.startswith('.') or part=='automation' for part in rel.parts): continue
        path='/' if rel.as_posix()=='index.html' else '/'+rel.parent.as_posix().strip('/')+'/'
        urls.append('https://princeandlong.com'+path)
    xml=['<?xml version="1.0" encoding="UTF-8"?>','<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for u in urls: xml.append(f'  <url><loc>{html.escape(u)}</loc></url>')
    xml.append('</urlset>')
    (root/'sitemap.xml').write_text('\n'.join(xml)+'\n')
