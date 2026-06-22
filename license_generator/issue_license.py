import sys
import argparse
import json
import base64
from pathlib import Path
from datetime import datetime, timedelta

# Add project root to path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT / "Project") not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT / "Project"))
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from license_generator.generator import generate_key, generate_signed_license

def _read_req(file_path):
    p = Path(file_path)
    if not p.exists():
        print(f"[ERROR] Request file not found: {file_path}")
        sys.exit(1)
    content = p.read_text(encoding="utf-8").strip()
    try:
        data = json.loads(content)
        return data
    except Exception:
        try:
            decoded = base64.b64decode(content).decode('utf-8')
            return json.loads(decoded)
        except Exception as e:
            print(f"[ERROR] Failed to parse .licreq file: {e}")
            sys.exit(1)

def _save_license(name, signed_lic, suffix):
    out_dir = PROJECT_ROOT / "exports" / "licenses"
    out_dir.mkdir(parents=True, exist_ok=True)
    safe_name = name.replace(" ", "_").replace("/", "-")
    path = out_dir / f"{safe_name}_{suffix}.lic"
    path.write_text(json.dumps(signed_lic, indent=2), encoding="utf-8")
    print(f"\n[SUKSES] License saved to: {path}")

def main():
    parser = argparse.ArgumentParser(description="CafePulse License Generator")
    parser.add_argument("name", help="Customer Name")
    parser.add_argument("--founder", action="store_true", help="Generate Founder License")
    parser.add_argument("--beta", action="store_true", help="Generate Beta License")
    parser.add_argument("--commercial", action="store_true", help="Generate Commercial License")
    parser.add_argument("--req", help="Path to .licreq file (Required for Founder/Commercial)")
    parser.add_argument("--days", type=int, default=30, help="Validity in days for Beta")
    parser.add_argument("--founder-id", help="Founder ID (Required for Founder)")
    parser.add_argument("--email", default="", help="Customer Email")
    parser.add_argument("--cohort", default="RC", help="Beta Cohort")
    parser.add_argument("--notes", default="", help="Additional Notes")

    args = parser.parse_args()

    # LEGACY FALLBACK
    if not any([args.founder, args.beta, args.commercial]):
        print(f"[INFO] Generating legacy serial key for {args.name}...")
        key = generate_key(args.name)
        print(f"\n[SUKSES] Kunci Lisensi Legacy Terbit!")
        print(f"Pemilik:    {args.name}")
        print(f"Serial Key: {key}")
        print("-" * 50)
        return

    now = datetime.now()
    issue_date = now.isoformat()
    
    # Process requests
    hwid = None
    if args.req:
        req_data = _read_req(args.req)
        hwid = req_data.get("hwid")
        if not hwid:
            print("[ERROR] HWID not found in request file.")
            sys.exit(1)
        if not args.email:
            args.email = req_data.get("email", "")

    if args.beta:
        print(f"Generating BETA license for: {args.name}")
        expiry_dt = now + timedelta(days=args.days)
        signed_lic = generate_signed_license(
            owner_name=args.name,
            edition="PROFESSIONAL",
            license_type="BETA",
            issue_date=issue_date,
            expiry_date=expiry_dt.isoformat(),
            hardware_id="ANY",
            email=args.email,
            beta_cohort=args.cohort,
            notes=args.notes
        )
        _save_license(args.name, signed_lic, "beta")

    elif args.founder:
        if not args.req:
            print("[ERROR] --req is required for Founder license.")
            sys.exit(1)
        if not args.founder_id:
            print("[ERROR] --founder-id is required for Founder license.")
            sys.exit(1)
            
        print(f"Generating FOUNDER license for: {args.name}")
        try:
            expiry_dt = now.replace(year=now.year + 5)
        except ValueError:
            expiry_dt = now.replace(year=now.year + 5, day=28)
            
        signed_lic = generate_signed_license(
            owner_name=args.name,
            edition="PROFESSIONAL",
            license_type="FOUNDER",
            issue_date=issue_date,
            expiry_date=expiry_dt.isoformat(),
            hardware_id=hwid,
            email=args.email,
            founder_id=args.founder_id,
            notes=args.notes
        )
        _save_license(args.name, signed_lic, "founder")

    elif args.commercial:
        if not args.req:
            print("[ERROR] --req is required for Commercial license.")
            sys.exit(1)
            
        print(f"Generating COMMERCIAL license for: {args.name}")
        try:
            expiry_dt = now.replace(year=now.year + 5)
        except ValueError:
            expiry_dt = now.replace(year=now.year + 5, day=28)
            
        signed_lic = generate_signed_license(
            owner_name=args.name,
            edition="PROFESSIONAL",
            license_type="COMMERCIAL",
            issue_date=issue_date,
            expiry_date=expiry_dt.isoformat(),
            hardware_id=hwid,
            email=args.email,
            notes=args.notes
        )
        _save_license(args.name, signed_lic, "commercial")

if __name__ == "__main__":
    main()
