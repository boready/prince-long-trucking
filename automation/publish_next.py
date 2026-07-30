from pathlib import Path
from datetime import date
import json, sys
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'automation'))
from article_template import render_article, rebuild_resources_index, rebuild_sitemap
queue_path=ROOT/'automation'/'article_queue.json'
pub_path=ROOT/'automation'/'published_queue.json'
queue=json.loads(queue_path.read_text())
published=json.loads(pub_path.read_text())
remaining=[x for x in queue if x['slug'] not in published]
if not remaining:
    print('No queued articles remain.')
    raise SystemExit(0)
post=remaining[0]
out=ROOT/'resources'/post['slug']
out.mkdir(parents=True,exist_ok=True)
(out/'index.html').write_text(render_article(post,date.today().isoformat()),encoding='utf-8')
published.append(post['slug'])
pub_path.write_text(json.dumps(published,indent=2)+'\n')
rebuild_resources_index(ROOT)
rebuild_sitemap(ROOT)
print('Published:',post['title'])
