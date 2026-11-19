#!/usr/bin/env python3
"""Fetch GitHub contribution calendar using GraphQL."""
import json, os, urllib.request
from datetime import datetime, timezone, timedelta
from pathlib import Path

username = os.environ.get("GITHUB_USERNAME", "").strip()
token = os.environ.get("GH_TOKEN", "").strip()
if not username or not token:
    raise SystemExit("Set GITHUB_USERNAME and GH_TOKEN.")
now = datetime.now(timezone.utc)
query = """query($login:String!,$from:DateTime!,$to:DateTime!){
 user(login:$login){contributionsCollection(from:$from,to:$to){
 contributionCalendar{totalContributions weeks{contributionDays{date contributionCount color}}}
 }} }"""
payload = {"query":query,"variables":{
    "login":username,
    "from":(now-timedelta(days=365)).isoformat().replace("+00:00","Z"),
    "to":now.isoformat().replace("+00:00","Z")}}
req = urllib.request.Request("https://api.github.com/graphql",
    data=json.dumps(payload).encode(),
    headers={"Authorization":"Bearer "+token,"Content-Type":"application/json",
             "User-Agent":"profile-readme-generator"}, method="POST")
with urllib.request.urlopen(req, timeout=30) as response:
    result = json.loads(response.read().decode())
if result.get("errors"):
    raise SystemExit("GitHub GraphQL errors: "+json.dumps(result["errors"]))
user = result.get("data",{}).get("user")
if not user:
    raise SystemExit("GitHub user not found or inaccessible: "+username)
cal = user["contributionsCollection"]["contributionCalendar"]
days = [{"date":d["date"],"count":d["contributionCount"],"color":d.get("color","#ebedf0")}
        for w in cal["weeks"] for d in w["contributionDays"]]
out = {"username":username,"generated_at":now.isoformat(),
       "total_contributions":cal["totalContributions"],"days":days}
Path("data").mkdir(exist_ok=True)
Path("data/contributions.json").write_text(json.dumps(out,indent=2),encoding="utf-8")
print(f"Fetched {len(days)} days; total contributions: {out['total_contributions']}")
