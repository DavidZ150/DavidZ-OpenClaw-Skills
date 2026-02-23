#!/usr/bin/env python3
import argparse, json, os, re
from pathlib import Path

PATTERNS = [
    ("HIGH", "openai_like_key", re.compile(r"\bsk-[A-Za-z0-9_-]{20,}\b")),
    ("HIGH", "github_pat", re.compile(r"\bgh[pousr]_[A-Za-z0-9]{20,}\b")),
    ("HIGH", "slack_token", re.compile(r"\bxox[baprs]-[A-Za-z0-9-]{20,}\b")),
    ("HIGH", "aws_access_key", re.compile(r"\bAKIA[0-9A-Z]{16}\b")),
    ("HIGH", "bearer_token", re.compile(r"Bearer\s+[A-Za-z0-9._-]{20,}", re.I)),
    ("HIGH", "private_key", re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH |DSA )?PRIVATE KEY-----")),
    ("HIGH", "password_assignment", re.compile(r"\b(pass(word)?|passwd|pwd)\b\s*[:=]\s*['\"]?[^\s'\"]{6,}", re.I)),

    ("MEDIUM", "mac_path", re.compile(r"/Users/[A-Za-z0-9._-]+(?:/[\w .@%+-]+)+")),
    ("MEDIUM", "linux_path", re.compile(r"/home/[A-Za-z0-9._-]+(?:/[\w .@%+-]+)+")),
    ("MEDIUM", "windows_path", re.compile(r"[A-Za-z]:\\\\Users\\\\[^\\\s]+(?:\\\\[^\\\n\r]+)+")),
    ("MEDIUM", "email", re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b")),
    ("MEDIUM", "hostname_local", re.compile(r"\b[A-Za-z0-9._-]+\.local\b")),
    ("MEDIUM", "telegram_bot_token", re.compile(r"\b\d{8,10}:[A-Za-z0-9_-]{30,}\b")),

    ("LOW", "secret_keyword", re.compile(r"\b(secret|token|credential|api[_-]?key)\b", re.I)),
]

TEXT_EXTS = {".md", ".txt", ".json", ".yaml", ".yml", ".toml", ".env", ".ini", ".cfg", ".conf", ".py", ".sh", ".js", ".ts", ".tsx", ".jsx", ".html", ".css", ".xml"}
SKIP_DIRS = {".git", "node_modules", "dist", "build", "__pycache__"}


def is_text_file(path: Path) -> bool:
    if path.suffix.lower() in TEXT_EXTS:
        return True
    try:
        with path.open("rb") as f:
            chunk = f.read(2048)
        return b"\0" not in chunk
    except Exception:
        return False


def scan_file(path: Path):
    findings = []
    try:
        text = path.read_text(encoding="utf-8", errors="ignore")
    except Exception:
        return findings
    lines = text.splitlines()
    for idx, line in enumerate(lines, start=1):
        for sev, name, rx in PATTERNS:
            for m in rx.finditer(line):
                snippet = line[max(0, m.start()-20):min(len(line), m.end()+20)]
                findings.append({
                    "severity": sev,
                    "type": name,
                    "path": str(path),
                    "line": idx,
                    "match": m.group(0)[:200],
                    "snippet": snippet,
                })
    return findings


def walk(target: Path):
    all_findings = []
    for root, dirs, files in os.walk(target):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        for fn in files:
            p = Path(root) / fn
            if is_text_file(p):
                all_findings.extend(scan_file(p))
    return all_findings


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("target")
    ap.add_argument("--json-out", default="")
    args = ap.parse_args()

    target = Path(args.target).expanduser().resolve()
    findings = walk(target)

    counts = {"HIGH": 0, "MEDIUM": 0, "LOW": 0}
    for f in findings:
        counts[f["severity"]] += 1

    print(f"Target: {target}")
    print(f"Findings: HIGH={counts['HIGH']} MEDIUM={counts['MEDIUM']} LOW={counts['LOW']}")
    for sev in ("HIGH", "MEDIUM", "LOW"):
        subset = [x for x in findings if x["severity"] == sev]
        if not subset:
            continue
        print(f"\n[{sev}] {len(subset)} findings")
        for f in subset[:20]:
            print(f"- {f['type']} :: {f['path']}:{f['line']} :: {f['match']}")

    if args.json_out:
        Path(args.json_out).write_text(json.dumps({"target": str(target), "counts": counts, "findings": findings}, ensure_ascii=False, indent=2))
        print(f"\nJSON report: {args.json_out}")


if __name__ == "__main__":
    main()
