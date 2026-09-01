#!/usr/bin/env python3
import argparse, hashlib, json, os
from datetime import datetime, timezone
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
CONTRACT=json.loads((ROOT/".stegverse/transition-ledger/contract.json").read_text())

def canon(v): return json.dumps(v,sort_keys=True,separators=(",",":"),ensure_ascii=False).encode()
def sha(v): return "sha256:"+hashlib.sha256(v if isinstance(v,(bytes,bytearray)) else canon(v)).hexdigest()

def ledger_root():
    override=os.getenv("STEGVERSE_REPO_LEDGER_ROOT")
    if override: return Path(override).expanduser().resolve()
    base=Path(os.getenv("XDG_STATE_HOME",str(Path.home()/".local/state")))
    return (base/"stegverse/repo-ledgers"/CONTRACT["repository"]).resolve()

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--transition-id",required=True)
    ap.add_argument("--transition-class",required=True)
    ap.add_argument("--predecessor-state-sha256",required=True)
    ap.add_argument("--successor-state-sha256",required=True)
    ap.add_argument("--evidence-json",default="{}")
    ap.add_argument("--authority-effect",default="NONE")
    ap.add_argument("--hb-ref")
    a=ap.parse_args()
    evidence=json.loads(a.evidence_json)
    root=ledger_root(); receipts=root/"receipts"; receipts.mkdir(parents=True,exist_ok=True)
    head=root/"HEAD.json"; previous=None
    if head.exists():
        previous=json.loads(head.read_text()).get("receipt_sha256")
    body={
      "schema":"stegverse.repo-transition-receipt/v1",
      "repository":CONTRACT["repository"],
      "transition_id":a.transition_id,
      "transition_class":a.transition_class,
      "predecessor_state_sha256":a.predecessor_state_sha256,
      "successor_state_sha256":a.successor_state_sha256,
      "evidence":evidence,
      "authority_effect":a.authority_effect,
      "hb_reference":a.hb_ref,
      "observed_at":datetime.now(timezone.utc).isoformat(),
      "previous_receipt_sha256":previous
    }
    digest=sha(body)
    record={**body,"receipt_sha256":digest}
    path=receipts/(digest.split(":",1)[1]+".json")
    if path.exists() and json.loads(path.read_text())!=record: raise SystemExit("receipt collision")
    if not path.exists(): path.write_text(json.dumps(record,indent=2,sort_keys=True)+"\n")
    head.write_text(json.dumps({"repository":CONTRACT["repository"],"receipt_sha256":digest,"receipt_path":str(path)},indent=2,sort_keys=True)+"\n")
    print(json.dumps(record,sort_keys=True))
if __name__=="__main__": main()
