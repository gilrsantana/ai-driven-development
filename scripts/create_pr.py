#!/usr/bin/env python3
import os
import sys
import json
import urllib.request
import urllib.error

def load_token(workspace_path):
    token = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
    if token:
        return token
    if workspace_path:
        env_path = os.path.join(workspace_path, ".env")
        if os.path.exists(env_path):
            try:
                with open(env_path, "r") as f:
                    for line in f:
                        if line.strip().startswith("GITHUB_TOKEN="):
                            return line.strip().split("=", 1)[1].strip().strip('"').strip("'")
                        if line.strip().startswith("GH_TOKEN="):
                            return line.strip().split("=", 1)[1].strip().strip('"').strip("'")
            except Exception:
                pass
    return None

def create_pull_request(token, owner, repo, title, head, base="main", body=""):
    url = f"https://api.github.com/repos/{owner}/{repo}/pulls"
    headers = {
        "Authorization": f"Bearer {token}",
        "User-Agent": "Antigravity-Agent",
        "Accept": "application/vnd.github+json",
        "Content-Type": "application/json"
    }
    
    data = {
        "title": title,
        "head": head,
        "base": base,
        "body": body
    }
    
    req_data = json.dumps(data).encode("utf-8")
    req = urllib.request.Request(url, data=req_data, headers=headers, method="POST")
    
    try:
        with urllib.request.urlopen(req) as response:
            res_data = response.read().decode("utf-8")
            res_json = json.loads(res_data)
            return True, res_json.get("html_url")
    except urllib.error.HTTPError as e:
        err_msg = f"HTTP Error {e.code}: {e.reason}"
        try:
            err_details = json.loads(e.read().decode("utf-8"))
            err_msg += f" - {err_details.get('message')}"
            if 'errors' in err_details:
                err_msg += f" ({json.dumps(err_details['errors'])})"
        except Exception:
            pass
        return False, err_msg
    except Exception as e:
        return False, str(e)

def main():
    if len(sys.argv) < 6:
        print("Usage: create_pr.py <owner> <repo> <title> <head_branch> <base_code_path> [base_branch] [body]")
        sys.exit(1)
        
    owner = sys.argv[1]
    repo = sys.argv[2]
    title = sys.argv[3]
    head = sys.argv[4]
    base_code_path = sys.argv[5]
    base = sys.argv[6] if len(sys.argv) > 6 else "main"
    body = sys.argv[7] if len(sys.argv) > 7 else ""
    
    token = load_token(base_code_path)
    if not token:
        print("ERROR: GitHub Token not found.", file=sys.stderr)
        sys.exit(1)
        
    print(f"Creating pull request in {owner}/{repo}: {head} -> {base}...")
    success, result = create_pull_request(token, owner, repo, title, head, base, body)
    if success:
        print(f"SUCCESS: Pull request created successfully: {result}")
        sys.exit(0)
    else:
        print(f"ERROR: Failed to create pull request: {result}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
