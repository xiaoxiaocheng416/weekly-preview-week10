#!/usr/bin/env python3
"""
Weekly Preview Builder - Fetch Fastmoss data, download assets, generate HTML.
"""
import os, sys, json, time, random, string, html, re, urllib.request, urllib.error, ssl

# --- Config ---
PRODUCT_IDS = [
    # 早期仓位
    "1729481318832247979",  # COSRX PDRN 眼膜
    "1732243946083160091",  # Dr.Melaxin 姜黄酸爽肤棉
    "1732265867381740340",  # Lassi Lips 唇线笔
    "1732271500056563740",  # Khadlaj Angel Dust 香水
    # 稳健仓位
    "1732157257719255067",  # Dr.Melaxin Cactox 紧致套装
    "1731832307922407544",  # SKINTIFIC 唇部精华
    "1729414752134665015",  # ONE/SIZE 粉底
]

COOKIE = "utm_country=US; utm_south=google; utm_id=ggfm; fp_visid=d255ef2a57ae6663cd6cf41a082770bb; _fbp=fb.1.1769014070516.564171598931847573; HMACCOUNT=ACF71010138D9EF7; userTimeZone=America%2FNew_York; _rdt_uuid=1770384030361.1a217c6d-7378-4a7b-a960-f1d5315e75b6; _gcl_au=1.1.117127969.1770384030; _ga=GA1.1.259614830.1770384030; gg_client_id=259614830.1770384030; _tt_enable_cookie=1; _ttp=01KGSHRYS3TBGQFW40NERQV5V1_.tt.1; NEXT_LOCALE=zh; region=US; Hm_lvt_6ada669245fc6950ae4a2c0a86931766=1771953768; _clck=1s4ab9i%5E2%5Eg41%5E0%5E2050; fd_tk=e03d9a9f5701c482f541a1feecef9cb2; Hm_lpvt_6ada669245fc6950ae4a2c0a86931766=1772560149; _uetsid=537fe970167c11f18cda2bb4e87abd0f|eidr5t|2|g41|0|2252; _clsk=173q176%5E1772562600278%5E4%5E0%5Ewww.clarity.ms%2Feus2-c%2Fcollect; _uetvid=f4837ee077b311f09655af1eeb5ff6a0|1b6t2ar|1772562600582|4|1|bat.bing.com/p/insights/c/a"

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/144.0.0.0 Safari/537.36',
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,zh-TW;q=0.7',
    'lang': 'ZH_CN',
    'region': 'US',
    'source': 'pc',
    'fm-sign': '8f3009ade0161bcbcf0ce660b54804eb',
    'Cookie': COOKIE,
}

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
IMG_DIR = os.path.join(BASE_DIR, "assets", "img")
VCOVER_DIR = os.path.join(BASE_DIR, "assets", "vcover")
CHART_DIR = os.path.join(BASE_DIR, "assets", "charts")

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

def cnonce():
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))

def api_get(url, pid=None):
    """GET request with retries. Adds Referer header if pid provided."""
    headers = dict(HEADERS)
    if pid:
        headers['Referer'] = f'https://www.fastmoss.com/zh/e-commerce/detail/{pid}'
    for attempt in range(3):
        try:
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=15, context=ctx) as resp:
                return json.loads(resp.read().decode('utf-8'))
        except Exception as e:
            print(f"  [retry {attempt+1}] {e}")
            time.sleep(2)
    return None

def download_image(url, dest):
    """Download image to local file."""
    if os.path.exists(dest) and os.path.getsize(dest) > 500:
        return True
    for attempt in range(3):
        try:
            req = urllib.request.Request(url, headers={
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
            })
            with urllib.request.urlopen(req, timeout=20, context=ctx) as resp:
                data = resp.read()
                if len(data) > 500:
                    with open(dest, 'wb') as f:
                        f.write(data)
                    return True
        except Exception as e:
            print(f"  [dl retry {attempt+1}] {url[:60]}... {e}")
            time.sleep(1)
    return False

def fetch_product_base(pid):
    """Fetch product basic info."""
    ts = str(int(time.time()))
    url = f"https://www.fastmoss.com/api/goods/v3/base?product_id={pid}&_time={ts}&cnonce={cnonce()}"
    data = api_get(url, pid)
    if not data:
        return None
    product = data.get('data', {}).get('product', {})
    if not product:
        product = data.get('data', {})
    if not product.get('title'):
        return None
    comm_str = str(product.get('commission_rate', '0'))
    comm = float(comm_str.replace('%', '').strip()) if comm_str else 0
    return {
        'title': product.get('title', ''),
        'rating': product.get('product_rating', 0),
        'price': product.get('real_price', ''),
        'commission': comm,
        'sold_count': product.get('sold_count', 0),
        'cover': (product.get('cover_list') or [''])[0],
    }

def fetch_product_overview(pid, d_type=28):
    """Fetch product sales overview (28d)."""
    ts = str(int(time.time()))
    url = f"https://www.fastmoss.com/api/goods/v3/overview?product_id={pid}&d_type={d_type}&_time={ts}&cnonce={cnonce()}"
    data = api_get(url, pid)
    if not data:
        return {}
    return data.get('data', {}).get('overview', {})

def fetch_product_videos(pid):
    """Fetch top 3 videos for product."""
    ts = str(int(time.time()))
    url = f"https://www.fastmoss.com/api/goods/v3/video?product_id={pid}&page=1&pagesize=3&order=2,2&d_type=0&is_promoted=-1&date_type=28&_time={ts}&cnonce={cnonce()}"
    data = api_get(url, pid)
    if not data:
        return []
    items = data.get('data', {}).get('list', [])
    videos = []
    for item in items[:3]:
        v = item.get('video', {})
        a = item.get('author', {})
        videos.append({
            'cover': v.get('cover', ''),
            # video_id and unique_id are at TOP LEVEL of item, not nested
            'video_id': str(item.get('video_id', '') or v.get('video_id', '')),
            'nickname': a.get('author_nickname', '') or item.get('author_nickname', ''),
            'unique_id': item.get('unique_id', '') or a.get('unique_id', ''),
            'play_count': item.get('play_count', 0),
            'sold_count': item.get('sold_count', 0),
            'sale_amount': item.get('sale_amount', 0),
        })
    return videos

def fetch_product_trend(pid):
    """Fetch 90-day GMV trend."""
    ts = str(int(time.time()))
    url = f"https://www.fastmoss.com/api/goods/v3/overview/trend?product_id={pid}&d_type=90&_time={ts}&cnonce={cnonce()}"
    data = api_get(url, pid)
    if not data:
        return []
    chart_list = data.get('data', {}).get('chart_list', [])
    return [item.get('inc_sale_amount', 0) for item in chart_list]

def generate_svg(values, pid):
    """Generate SVG chart from daily GMV values."""
    dest = os.path.join(CHART_DIR, f"{pid}.svg")
    vals = [float(v) for v in values if v is not None]
    if not vals or all(v == 0 for v in vals):
        svg = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 720 200">
  <text x="360" y="110" text-anchor="middle" font-family="system-ui,sans-serif" font-size="16" fill="#94a3b8">No GMV data</text>
</svg>'''
        with open(dest, 'w') as f:
            f.write(svg)
        return
    max_val = max(vals) if max(vals) > 0 else 1
    n = len(vals)
    w, h = 720, 200
    pad_top, pad_bot = 15, 15
    usable_h = h - pad_top - pad_bot
    points = []
    for i, v in enumerate(vals):
        x = (i / max(n - 1, 1)) * w
        y = pad_top + usable_h - (v / max_val) * usable_h
        points.append(f"{x:.1f},{y:.1f}")
    polyline = " ".join(points)
    area_points = f"0,{h} " + polyline + f" {w},{h}"
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}">
  <defs>
    <linearGradient id="g" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#2f65c8" stop-opacity="0.18"/>
      <stop offset="100%" stop-color="#2f65c8" stop-opacity="0.02"/>
    </linearGradient>
  </defs>
  <polygon points="{area_points}" fill="url(#g)"/>
  <polyline points="{polyline}" fill="none" stroke="#2f65c8" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/>
</svg>'''
    with open(dest, 'w') as f:
        f.write(svg)

def fmt_number(n):
    if n is None: return "0"
    n = float(n)
    if n >= 1000000: return f"{n/1000000:.1f}M"
    elif n >= 1000: return f"{n/1000:.1f}K"
    return f"{n:,.0f}"

def fmt_money(n):
    if n is None: return "$0"
    n = float(n)
    if n >= 1000000: return f"${n/1000000:.1f}M"
    elif n >= 1000: return f"${n/1000:.1f}K"
    return f"${n:.2f}"

def fmt_sales(n):
    if n is None: return "0"
    n = int(n)
    return f"{n:,}" if n >= 1000 else str(n)

def esc(s):
    return html.escape(str(s)) if s else ''

# ========== MAIN ==========
def main():
    products = []
    vcover_idx = 0

    for idx, pid in enumerate(PRODUCT_IDS, 1):
        print(f"\n[{idx}/15] Fetching product {pid}...")

        base = fetch_product_base(pid)
        if not base:
            print(f"  SKIP: no base data")
            products.append(None)
            continue
        print(f"  Title: {base['title'][:60]}...")
        print(f"  Rating: {base['rating']}, Commission: {base['commission']}%, Sold: {base['sold_count']}")

        prod_img = f"prod_{idx:02d}.jpg"
        prod_img_path = os.path.join(IMG_DIR, prod_img)
        if base['cover']:
            ok = download_image(base['cover'], prod_img_path)
            print(f"  Product image: {'OK' if ok else 'FAILED'}")

        time.sleep(0.5)
        overview = fetch_product_overview(pid)
        author_count = overview.get('author_count', 0)
        print(f"  Creators (28d): {author_count}")

        time.sleep(0.5)
        videos = fetch_product_videos(pid)
        print(f"  Videos: {len(videos)} found")
        for vi, v in enumerate(videos):
            print(f"    [{vi}] {v['nickname']} | vid={v['video_id']} | sold={v['sold_count']}")

        for vi, v in enumerate(videos):
            vcover_idx += 1
            vcover_file = f"cover_{vcover_idx:02d}.jpg"
            vcover_path = os.path.join(VCOVER_DIR, vcover_file)
            if v['cover']:
                download_image(v['cover'], vcover_path)
            v['local_cover'] = f"assets/vcover/{vcover_file}"

        time.sleep(0.5)
        trend = fetch_product_trend(pid)
        print(f"  Trend data points: {len(trend)}")
        generate_svg(trend, pid)

        products.append({
            'pid': pid, 'base': base, 'videos': videos, 'author_count': author_count,
            'trend_len': len(trend), 'prod_img': f"assets/img/{prod_img}", 'idx': idx,
        })
        time.sleep(0.8)

    # ========== BUILD HTML ==========
    print("\n\nBuilding HTML...")
    ts = str(int(time.time()))

    cards_html = []
    for p in products:
        if p is None: continue
        b = p['base']
        pid = p['pid']
        rating = f"{float(b['rating']):.2f}" if b['rating'] else "N/A"
        commission = f"{float(b['commission']):.1f}" if b['commission'] else "0"
        sold = fmt_sales(b['sold_count'])
        creators_28d = fmt_number(p.get('author_count', 0))
        title_text = esc(b['title'])

        vcards = []
        for v in p['videos']:
            vid = v.get('video_id', '')
            uid = v.get('unique_id', '')
            nick = esc(v.get('nickname', 'Unknown'))
            plays = fmt_number(v.get('play_count', 0) or 0)
            v_sold = fmt_number(v.get('sold_count', 0) or 0)
            gmv = fmt_money(v.get('sale_amount', 0) or 0)
            vcard = f"""<a class='vcard' href='https://www.tiktok.com/@{esc(uid)}/video/{esc(str(vid))}' target='_blank' rel='noreferrer noopener'><div class='vthumb'><img src="{v['local_cover']}" alt="" loading="lazy"/></div><div class='vmeta'><div class='vnick'>{nick}</div><div class='vstat'>Views {plays}</div></div></a>"""
            vcards.append(vcard)

        videos_html = ""
        if vcards:
            videos_html = f"""<div class='videosBlock'><div class='backTitle' style='margin-top:10px'>Top 3 videos (28d sold)</div><div class='videosRow'>{"".join(vcards)}</div></div>"""

        card = f"""
        <div class='card flip' tabindex='0'>
          <div class='inner'>
            <div class='front'>
              <div class='imgWrap'>
                <img src='{p["prod_img"]}' alt='' loading='lazy'/>
              </div>
              <div class='title' title="{title_text}">{title_text}</div>
              <div class='sub'>{pid}</div>
              <div class='row'><span class='pill'>Rating {rating}</span><span class='pill'>Commission {commission}%</span></div>
              <div class='meta'>Lifetime sales: {sold} · Creators (28d): {creators_28d}</div>
              <div class='links'>
                <a class='btnlink' href='https://shop.tiktok.com/view/product/{pid}' target='_blank' rel='noreferrer noopener'>TikTok</a>
                <button class='btnlink copyBtn' type='button' data-copy='https://shop.tiktok.com/view/product/{pid}'>Copy link</button>
                <a class='btnlink ghost' href='https://www.fastmoss.com/en/e-commerce/detail/{pid}' target='_blank' rel='noreferrer noopener'>Fastmoss</a>
                <span class='linkHint'>If TikTok doesn't open, copy &amp; paste into Safari/Chrome.</span>
              </div>
            </div>
            <div class='back'>
              <div class='backTitle'>GMV per day (last 90d)</div>
              <div class='chartWrap'><img src='assets/charts/{pid}.svg?v={ts}' alt='' loading='lazy' style='width:100%;height:100%;object-fit:contain'/></div>
              <div class='xaxis'><span>90d ago</span><span>60d</span><span>30d</span><span>Now</span></div>
              {videos_html}
              <div class='hint'>Tap to flip back</div>
            </div>
          </div>
        </div>
"""
        cards_html.append(card)

    page = f"""<!doctype html>
<html lang='en'>
<head>
<meta charset='utf-8'>
<meta name='viewport' content='width=device-width, initial-scale=1'>
<title>Weekly Preview - Week 10 (Mar 3, 2026)</title>
<style>
:root{{--bg:#f6f7fb;--panel:#fff;--text:#0f172a;--muted:#64748b;--line:#e2e8f0;--accent:#2563eb;--shadow:0 1px 2px rgba(15,23,42,.06),0 10px 25px rgba(15,23,42,.06);}}
body{{margin:0;font-family:ui-sans-serif,system-ui,-apple-system,Segoe UI,Roboto,Helvetica,Arial;background:var(--bg);color:var(--text);-webkit-font-smoothing:antialiased;-moz-osx-font-smoothing:grayscale;}}
.wrap{{max-width:1200px;margin:0 auto;padding:18px 16px;}}
header{{background:#fff;border-bottom:1px solid var(--line);}}
h1{{margin:0;font-size:20px;letter-spacing:-0.01em;}}
.subttl{{margin-top:6px;color:var(--muted);font-size:13px;}}
small{{color:var(--muted);}}
.section{{margin-top:18px;}}
.h2{{display:flex;justify-content:space-between;align-items:baseline;gap:12px;}}
.h2 h2{{margin:0;font-size:16px;letter-spacing:-0.01em;}}
.grid{{display:grid;grid-template-columns:repeat(3,1fr);gap:14px;margin-top:12px;}}
@media (max-width: 980px){{.grid{{grid-template-columns:repeat(2,1fr);}}}}
@media (max-width: 720px){{.grid{{grid-template-columns:1fr;}}}}
.card{{background:var(--panel);border:1px solid rgba(226,232,240,.9);border-radius:16px;padding:12px;display:flex;flex-direction:column;gap:8px;min-height:560px;box-shadow:var(--shadow);transition:transform .12s ease, box-shadow .12s ease;}}
.card:hover{{transform:translateY(-1px);box-shadow:0 2px 6px rgba(15,23,42,.08),0 18px 40px rgba(15,23,42,.10);}}
.flip{{perspective:1000px;cursor:pointer;}}
.flip:focus{{outline:2px solid rgba(37,99,235,.25);outline-offset:2px;}}
.inner{{position:relative;width:100%;height:100%;transform-style:preserve-3d;transition:transform .6s cubic-bezier(.2,.8,.2,1);}}
.flip.isFlipped .inner{{transform:rotateY(180deg);}}
.front,.back{{backface-visibility:hidden;position:absolute;inset:0;display:flex;flex-direction:column;gap:8px;}}
.back{{transform:rotateY(180deg);padding-top:10px;padding-bottom:12px;}}
.chartWrap{{height:200px;border:1px solid rgba(226,232,240,.9);border-radius:14px;background:linear-gradient(180deg,#ffffff,#fbfdff);display:flex;flex-direction:column;align-items:stretch;justify-content:stretch;overflow:hidden;margin:6px 0 2px;}}
.chartWrap svg{{width:100%;height:100%;flex:1;}}
.chartWrap svg path{{stroke-width:3.6 !important;}}
.xaxis{{display:flex;justify-content:space-between;gap:8px;padding:6px 10px 0;color:var(--muted);font-size:11px;margin-top:-4px;}}
.backTitle{{font-weight:800;font-size:13px;letter-spacing:-0.01em;margin:6px 0;}}
.hint{{margin-top:auto;color:rgba(100,116,139,.85);font-size:11px;padding-top:8px;}}
.videosRow{{display:flex;gap:14px;overflow-x:auto;padding:6px 12px 10px;scroll-snap-type:x mandatory;-webkit-overflow-scrolling:touch;}}
.videosRow::-webkit-scrollbar{{display:none;}}
.vcard{{flex:0 0 auto;min-width:140px;max-width:140px;display:flex;flex-direction:column;gap:8px;padding:8px;border:1px solid rgba(226,232,240,.95);border-radius:14px;background:linear-gradient(180deg,#ffffff,#f8fafc);text-decoration:none;color:inherit;scroll-snap-align:start;}}
.vthumb{{width:100%;height:170px;border-radius:12px;overflow:hidden;background:#eef2ff;display:flex;align-items:center;justify-content:center;}}
.vthumb img{{width:100%;height:100%;object-fit:cover;}}
.vthumb .ph{{font-size:12px;color:#64748b;font-weight:800;}}
.vmeta{{min-width:0;display:flex;flex-direction:column;gap:4px;}}
.vnick{{font-weight:800;font-size:12px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;}}
.vstat{{color:var(--muted);font-size:11px;line-height:1.2;}}
.imgWrap{{height:300px;border:1px solid rgba(226,232,240,.9);border-radius:14px;background:linear-gradient(180deg,#ffffff,#fbfdff);display:flex;align-items:center;justify-content:center;overflow:hidden;}}
@media (max-width: 720px){{
  .wrap{{padding:14px 12px;}}
  .imgWrap{{height:340px;}}
  .chartWrap{{height:280px;}}
  .pill{{padding:6px 10px;font-size:12px;}}
  .links a{{font-size:13px;}}
}}
.imgWrap img{{max-width:100%;max-height:100%;object-fit:contain;}}
.title{{font-weight:650;font-size:13px;line-height:1.25;display:-webkit-box;-webkit-line-clamp:3;-webkit-box-orient:vertical;overflow:hidden;min-height:4.8em;}}
.sub{{display:none;}}
.row{{display:flex;flex-wrap:wrap;gap:6px;}}
.pill{{font-size:10.5px;border:1px solid rgba(226,232,240,.95);background:linear-gradient(180deg,#f8fafc,#ffffff);border-radius:999px;padding:2px 7px;color:#0f172a;font-weight:650;letter-spacing:-0.005em;}}
.meta{{font-size:11px;color:var(--muted);margin-top:auto;}}
.links{{display:flex;gap:8px;margin-top:4px;flex-wrap:wrap;align-items:center;}}
.btnlink{{display:inline-flex;align-items:center;justify-content:center;gap:6px;padding:7px 10px;border-radius:10px;border:1px solid rgba(226,232,240,.95);background:linear-gradient(180deg,#ffffff,#f8fafc);color:var(--accent);text-decoration:none;font-size:12px;font-weight:700;}}
.btnlink:hover{{text-decoration:none;filter:brightness(.98);}}
button.btnlink{{cursor:pointer;}}
.linkHint{{display:none;color:var(--muted);font-size:11px;line-height:1.2;}}
.card.showHint .linkHint{{display:block;}}
.toast{{position:fixed;left:50%;bottom:22px;transform:translateX(-50%);background:rgba(15,23,42,.92);color:#fff;padding:10px 12px;border-radius:12px;font-size:13px;box-shadow:0 12px 30px rgba(0,0,0,.18);opacity:0;pointer-events:none;transition:opacity .15s ease;}}
.toast.show{{opacity:1;}}
</style>
</head>
<body>
<header><div class='wrap'>
  <h1>Growth Picks Dashboard</h1>
  <div class='subttl'>Week 10 · Mar 3, 2026 · 7 picks</div>
</div></header>

<div class='wrap'>
  <div class='section'>
    <div class='h2'><h2>Recommended</h2></div>
    <div class='grid'>
{"".join(cards_html)}
    </div>
  </div>
</div>
<div class='toast'>Copied</div>

<script>
(function(){{
  console.log('flipjs ok');
  function toggle(card){{ if(card) card.classList.toggle('isFlipped'); }}
  async function copyText(text){{
    try{{ await navigator.clipboard.writeText(text); toast('Copied'); }}
    catch(e){{
      try{{ var ta=document.createElement('textarea'); ta.value=text; document.body.appendChild(ta); ta.select(); document.execCommand('copy'); ta.remove(); toast('Copied'); }}
      catch(_e){{ toast('Copy failed'); }}
    }}
  }}
  function toast(msg){{
    var el=document.querySelector('.toast');
    if(!el) return;
    el.textContent=msg; el.classList.add('show');
    clearTimeout(window.__toastT);
    window.__toastT=setTimeout(function(){{ el.classList.remove('show'); }}, 1200);
  }}
  document.querySelectorAll('.copyBtn').forEach(function(btn){{
    btn.addEventListener('click', function(e){{
      e.preventDefault(); e.stopPropagation();
      var url = btn.getAttribute('data-copy') || '';
      if(url) copyText(url);
      try{{
        var card = btn.closest && btn.closest('.card');
        if(card){{ card.classList.add('showHint'); clearTimeout(card.__hintT); card.__hintT=setTimeout(function(){{ card.classList.remove('showHint'); }}, 2200); }}
      }}catch(_e){{}}
    }});
  }});
  document.addEventListener('click', function(e){{
    if(e.target.closest && e.target.closest('a,button,.videosRow,.vcard,.links')) return;
    var card = e.target.closest && e.target.closest('.flip');
    if(!card) return;
    toggle(card);
  }});
}})();
</script>
</body>
</html>"""

    out_path = os.path.join(BASE_DIR, "index.html")
    with open(out_path, 'w', encoding='utf-8') as f:
        f.write(page)

    # ========== SELF-CHECK ==========
    print("\n" + "="*50)
    print("SELF-CHECK")
    print("="*50)
    ok_count = sum(1 for p in products if p is not None)
    print(f"Cards generated: {ok_count}/15")
    prod_imgs = [f for f in os.listdir(IMG_DIR) if f.startswith('prod_')]
    print(f"Product images: {len(prod_imgs)}")
    vcovers = [f for f in os.listdir(VCOVER_DIR) if f.startswith('cover_')]
    print(f"Video covers: {len(vcovers)}")
    charts = [f for f in os.listdir(CHART_DIR) if f.endswith('.svg')]
    print(f"SVG charts: {len(charts)}")

    with open(out_path, 'r') as f:
        content = f.read()
    img_refs = re.findall(r"src='(assets/[^']+)'", content) + re.findall(r'src="(assets/[^"]+)"', content)
    broken = 0
    for ref in img_refs:
        clean = ref.split('?')[0]
        full = os.path.join(BASE_DIR, clean)
        if not os.path.exists(full):
            print(f"  BROKEN: {ref}")
            broken += 1
    print(f"Broken image refs: {broken}")

    # Verify videos are unique across products
    all_vids = []
    for p in products:
        if p and p['videos']:
            for v in p['videos']:
                all_vids.append(v.get('video_id', ''))
    unique_vids = len(set(v for v in all_vids if v))
    print(f"Total video refs: {len(all_vids)}, Unique video_ids: {unique_vids}")
    if unique_vids < 10:
        print("WARNING: Too few unique videos - data may be fake!")
    else:
        print("Video uniqueness: OK")

    print(f"\nOutput: {out_path}")
    print("DONE!")

if __name__ == '__main__':
    main()
