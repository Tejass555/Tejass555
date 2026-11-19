#!/usr/bin/env python3
"""Render six SVG cards. Python standard library only."""
import json, html
from collections import defaultdict
from datetime import date
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
P=json.loads((ROOT/"profile.json").read_text(encoding="utf-8"))
DP=ROOT/"data/contributions.json"
D=json.loads(DP.read_text(encoding="utf-8")) if DP.exists() else {"days":[],"total_contributions":0}
OUT=ROOT/"cards"; OUT.mkdir(exist_ok=True)
e=lambda x: html.escape(str(x),quote=True)

def base(w,h,label):
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="{e(label)}"><defs><style>.sans{{font-family:Arial,sans-serif}}.serif{{font-family:Georgia,serif}}.muted{{fill:#77766f}}.reveal{{opacity:0;animation:fadein .8s ease-out forwards}}.bar{{transform-box:fill-box;transform-origin:bottom;animation:grow .85s ease-out both}}@keyframes fadein{{to{{opacity:1}}}}@keyframes grow{{from{{transform:scaleY(.03)}}to{{transform:scaleY(1)}}}}@media(prefers-reduced-motion:reduce){{.motion,.reveal,.bar{{animation:none!important;opacity:1!important;transform:none!important}}}}</style></defs>"""
def save(n,s): (OUT/n).write_text(s,encoding="utf-8")

first,*rest=P["name"].split()
hero=base(1200,430,P["name"]+" "+P["role"])+f"""
<rect width="1200" height="430" rx="22" fill="#f5f4ef"/><circle cx="1080" cy="76" r="160" fill="#e9e7df"/>
<text x="64" y="62" class="sans" font-size="15" letter-spacing="3" fill="#77766f">● {e(P['role'])}</text>
<text x="64" y="190" class="serif reveal" font-size="100" fill="#171717">{e(first)}</text>
<text x="64" y="286" class="serif reveal" font-size="92" font-style="italic" fill="#171717">{e(' '.join(rest))}<tspan fill="#2457ed">.</tspan></text>
<rect x="64" y="322" width="58" height="4" rx="2" fill="#f2c500"/>
<text x="64" y="360" class="sans" font-size="22" fill="#383832">{e(P['tagline'])}</text>
<text x="64" y="400" class="sans muted" font-size="16">{e(P['location'])} · {e(P['website'])}</text>
<g transform="translate(930 190)"><circle r="112" fill="#e1dfd7"/><circle r="84" fill="none" stroke="#c8c5ba" stroke-width="2" stroke-dasharray="3 7"/>
<path d="M-58 25L-20 -20L10 10L55 -48" fill="none" stroke="#2457ed" stroke-width="7" stroke-linecap="round" stroke-linejoin="round"/>
<circle cx="-58" cy="25" r="8" fill="#f2c500"/><circle cx="-20" cy="-20" r="8" fill="#2457ed"/><circle cx="10" cy="10" r="8" fill="#e72b25"/><circle cx="55" cy="-48" r="8" fill="#2457ed"/>
<text y="76" text-anchor="middle" class="sans" font-size="13" letter-spacing="2" fill="#77766f">DATA → INSIGHT</text></g></svg>"""
save("hero.svg",hero)

def tile(color,label,metric,caption,desc):
    fg="#fff" if color in ("#2457ed","#e92727") else "#191919"
    return base(380,230,label)+f"""
<rect width="380" height="230" rx="20" fill="{color}"/>
<text x="28" y="38" class="sans" font-size="13" letter-spacing="2" fill="{fg}">{e(label.upper())}</text>
<text x="348" y="38" text-anchor="end" class="sans" font-size="20" fill="{fg}">↗</text>
<text x="28" y="116" class="serif" font-size="43" font-style="italic" fill="{fg}">{e(metric)}</text>
<text x="28" y="151" class="sans" font-size="15" font-weight="bold" fill="{fg}">{e(caption)}</text>
<text x="28" y="188" class="sans" font-size="13" fill="{fg}">{e(desc)}</text></svg>"""
save("build.svg",tile("#2457ed","Build",P["build_metric"],P["build_label"],P["build_description"]))
save("brand.svg",tile("#e92727","Brand",P["brand_metric"],P["brand_label"],P["brand_description"]))
save("learn.svg",tile("#f5c400","Learn",P["learn_metric"],P["learn_label"],P["learn_description"]))

months=defaultdict(int)
for item in D.get("days",[]): months[item["date"][:7]]+=int(item.get("count",0))
keys=sorted(months)[-12:]
labels=[date.fromisoformat(k+"-01").strftime("%b") for k in keys] if keys else ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
vals=[months[k] for k in keys] if keys else [0]*12
mx=max(vals) or 1; bars=[]
for i,(lab,val) in enumerate(zip(labels,vals)):
    x=52+i*92; h=max(5,int(118*val/mx)); y=205-h
    color="#2457ed" if val==mx and val else "#222"
    bars.append(f'<rect class="bar" style="animation-delay:{i*70}ms" x="{x}" y="{y}" width="56" height="{h}" rx="7" fill="{color}"/>')
    bars.append(f'<text x="{x+28}" y="230" text-anchor="middle" class="serif" font-size="13" fill="#77766f">{lab}</text>')
    if val: bars.append(f'<text x="{x+28}" y="{y-8}" text-anchor="middle" class="sans" font-size="12" fill="#2457ed">{val}</text>')
activity=base(1200,280,"Monthly GitHub contributions")+f"""
<rect width="1200" height="280" rx="22" fill="#f5f4ef"/>
<text x="54" y="52" class="serif" font-size="34" fill="#171717">The work, month by month</text>
<text x="1145" y="48" text-anchor="end" class="sans muted" font-size="12">LAST 12 MONTHS</text>
<text x="54" y="91" class="sans muted" font-size="14">{int(D.get('total_contributions',0)):,} contributions in the fetched calendar</text>
<line x1="42" y1="205" x2="1158" y2="205" stroke="#d9d7cf"/>{''.join(bars)}</svg>"""
save("activity.svg",activity)

days=D.get("days",[])[-371:]
palette=["#e8e7e1","#c9d5ff","#91aaff","#5279f4","#2457ed"]
cells=[]
for i,item in enumerate(days):
    n=int(item.get("count",0)); level=0 if n==0 else 1 if n<=2 else 2 if n<=5 else 3 if n<=9 else 4
    col,row=divmod(i,7); x,y=48+col*20,95+row*20
    cells.append(f'<rect x="{x}" y="{y}" width="14" height="14" rx="3" fill="{palette[level]}"><title>{e(item["date"])}: {n} contributions</title></rect>')
legend="".join(f'<rect x="{94+i*20}" y="242" width="14" height="14" rx="3" fill="{c}"/>' for i,c in enumerate(palette))
heat=base(1200,290,"GitHub contribution calendar")+f"""
<rect width="1200" height="290" rx="22" fill="#f5f4ef"/>
<text x="52" y="53" class="serif" font-size="34" fill="#171717">Every day, <tspan font-style="italic" fill="#2457ed">in blue</tspan></text>
<text x="1148" y="50" text-anchor="end" class="sans muted" font-size="12">REFRESHED DAILY</text>
<text x="52" y="78" class="sans muted" font-size="13">{int(D.get('total_contributions',0)):,} contributions over the fetched year</text>
{''.join(cells)}<text x="48" y="255" class="sans muted" font-size="12">Less</text>{legend}<text x="205" y="255" class="sans muted" font-size="12">More</text></svg>"""
save("contributions.svg",heat)
print("Rendered six SVG cards.")
