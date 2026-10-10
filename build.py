# index.src.html + style.retro.css + 폰트 → index.html (아티팩트로 올리는 파일)
import base64, pathlib
here = pathlib.Path(__file__).parent
font = here/'fonts'/'Galmuri11.woff2'
css = (here/'style.retro.css').read_text().replace('__GALMURI__', base64.b64encode(font.read_bytes()).decode())
src = (here/'index.src.html').read_text()
# 위키미디어 자유 이용 사진 → data URI
import json
meta = json.loads((here/'photos'/'meta.json').read_text())
wm = {k:{'src':'data:image/jpeg;base64,'+base64.b64encode((here/'photos'/(k+'.jpg')).read_bytes()).decode(),'by':v['by'],'lic':v['lic'],'page':v['page']} for k,v in meta.items()}
assert src.count('__PHOTOS__')==1
src = src.replace('__PHOTOS__', json.dumps(wm, ensure_ascii=False))
assert src.count('__STYLE__')==1
(here/'index.html').write_text(src.replace('__STYLE__', css))
print('built', (here/'index.html').stat().st_size, 'bytes')
# 배포용(GitHub Pages: docs/) + 미리보기 — 아티팩트는 머리를 자동으로 붙여 주지만 여기선 직접 붙임
HEAD = """<!doctype html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-title" content="광저우">
<meta name="theme-color" content="#EFE8D4">
</head>
<body>
"""
page = HEAD + (here/'index.html').read_text() + "\n</body>\n</html>\n"
docs = here/'docs'; docs.mkdir(exist_ok=True)
(docs/'index.html').write_text(page); (docs/'.nojekyll').write_text('')
pv = pathlib.Path('/tmp/triplog-preview'); pv.mkdir(parents=True, exist_ok=True)
(pv/'index.html').write_text(page)
print('docs/index.html', (docs/'index.html').stat().st_size, 'bytes')
