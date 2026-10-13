#!/usr/bin/env python3
"""Bounded live availability checks of source landing pages; never infer rights from HTTP."""
import argparse,concurrent.futures,datetime,json,urllib.request,urllib.error
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def probe(url):
 result={'url':url,'checked_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'method':'GET, read at most 1024 bytes','rights_inferred':False}
 try:
  with urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'KaiTakArchiveSourceAudit/1.0'}),timeout=20) as response:
   result.update(http_status=response.status,final_url=response.geturl(),content_type=response.headers.get('Content-Type'),status='reachable');response.read(1024)
 except urllib.error.HTTPError as e:result.update(http_status=e.code,status='not-reachable-at-check',error_type='HTTPError')
 except Exception as e:result.update(status='unverified',error_type=type(e).__name__)
 return result
def main():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--online',action='store_true',required=True);p.add_argument('--report',type=Path,required=True);a=p.parse_args();sources=json.loads((ROOT/'archive/catalogue/sources.json').read_text())['sources'];urls=sorted({u for s in sources for u in s['urls'] if u.startswith('https://')})
 with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:rows=list(pool.map(probe,urls))
 result={'schema_version':'1.0.0','scope':'Source registry landing/product/API routes, not every time-limited historical download URL; response reachability is not content validation or permission.','checked':len(rows),'reachable':sum(r['status']=='reachable' for r in rows),'unverified_or_unreachable':sum(r['status']!='reachable' for r in rows),'results':rows};a.report.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:v for k,v in result.items() if k!='results'},indent=2))
if __name__=='__main__':main()
