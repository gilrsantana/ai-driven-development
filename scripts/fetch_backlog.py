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

def fetch_project_items(token, login, number):
    query = """
    query($login: String!, $number: Int!) {
      user(login: $login) {
        projectV2(number: $number) {
          id
          title
          fields(first: 20) {
            nodes {
              ... on ProjectV2FieldCommon {
                id
                name
              }
              ... on ProjectV2SingleSelectField {
                id
                name
                options {
                  id
                  name
                }
              }
            }
          }
          items(first: 100) {
            nodes {
              id
              fieldValues(first: 20) {
                nodes {
                  ... on ProjectV2ItemFieldSingleSelectValue {
                    name
                    field {
                      ... on ProjectV2FieldCommon {
                        name
                      }
                    }
                  }
                  ... on ProjectV2ItemFieldTextValue {
                    text
                    field {
                      ... on ProjectV2FieldCommon {
                        name
                      }
                    }
                  }
                }
              }
              content {
                ... on DraftIssue {
                  title
                  body
                }
                ... on Issue {
                  title
                  body
                  number
                  state
                  repository {
                    name
                    owner {
                      login
                    }
                  }
                }
                ... on PullRequest {
                  title
                  body
                  number
                  state
                }
              }
            }
          }
        }
      }
    }
    """
    
    variables = {
        "login": login,
        "number": number
    }
    
    url = "https://api.github.com/graphql"
    headers = {
        "Authorization": f"Bearer {token}",
        "User-Agent": "Antigravity-Agent",
        "Content-Type": "application/json"
    }
    
    req_data = json.dumps({"query": query, "variables": variables}).encode("utf-8")
    req = urllib.request.Request(url, data=req_data, headers=headers, method="POST")
    
    try:
        with urllib.request.urlopen(req) as response:
            res_data = response.read().decode("utf-8")
            return json.loads(res_data)
    except urllib.error.HTTPError as e:
        print(f"HTTP Error: {e.code} - {e.reason}", file=sys.stderr)
        try:
            print(e.read().decode("utf-8"), file=sys.stderr)
        except Exception:
            pass
        return None
    except Exception as e:
        print(f"Error connecting to GitHub: {e}", file=sys.stderr)
        return None

def main():
    if len(sys.argv) < 4:
        print("Usage: fetch_backlog.py <github_owner> <project_number> <base_code_path>", file=sys.stderr)
        sys.exit(1)
        
    login = sys.argv[1]
    try:
        number = int(sys.argv[2])
    except ValueError:
        print("ERROR: Project number must be an integer.", file=sys.stderr)
        sys.exit(1)
    base_code_path = sys.argv[3]
    
    token = load_token(base_code_path)
    if not token:
        print("ERROR: GitHub Token not found. Please set GITHUB_TOKEN environment variable or add it to a .env file in the specified workspace.", file=sys.stderr)
        sys.exit(1)
        
    print(f"Fetching items from GitHub Project v2 (Owner: {login}, Project: {number})...")
    result = fetch_project_items(token, login, number)
    if not result:
        sys.exit(1)
        
    if "errors" in result:
        print("GraphQL Errors:", file=sys.stderr)
        print(json.dumps(result["errors"], indent=2), file=sys.stderr)
        sys.exit(1)
        
    project = result.get("data", {}).get("user", {}).get("projectV2")
    if not project:
        print("ERROR: Project not found. Verify owner and project number.", file=sys.stderr)
        sys.exit(1)
        
    project_id = project.get("id")
    print(f"\nProject Title: {project.get('title')} (ID: {project_id})")
    
    # Parse Status field options
    fields = project.get("fields", {}).get("nodes", [])
    status_field_id = None
    status_options = {}
    for f in fields:
        if f.get("name") == "Status":
            status_field_id = f.get("id")
            for opt in f.get("options", []):
                status_options[opt.get("name")] = opt.get("id")
                
    print(f"Status Field ID: {status_field_id}")
    print("Status Options Mapping:")
    for name, opt_id in status_options.items():
        print(f"  - {name}: {opt_id}")
        
    items = project.get("items", {}).get("nodes", [])
    backlog_items = []
    
    for item in items:
        item_id = item.get("id")
        status = "None"
        title = "Untitled"
        body = ""
        number = None
        repo_name = None
        repo_owner = None
        
        # 1. Parse Field Values
        field_nodes = item.get("fieldValues", {}).get("nodes", [])
        for fn in field_nodes:
            field_info = fn.get("field", {})
            if field_info.get("name") == "Status":
                status = fn.get("name", "None")
        
        # 2. Parse Content
        content = item.get("content")
        if content:
            title = content.get("title", title)
            body = content.get("body", "")
            number = content.get("number")
            repo = content.get("repository")
            if repo:
                repo_name = repo.get("name")
                owner = repo.get("owner")
                if owner:
                    repo_owner = owner.get("login")
            
        backlog_items.append({
            "itemId": item_id,
            "title": title,
            "status": status,
            "body": body,
            "number": number,
            "repo_name": repo_name,
            "repo_owner": repo_owner
        })
        
    print("\n--- Project Board Items ---")
    for status_group in sorted(list(set(item["status"] for item in backlog_items))):
        print(f"\n[{status_group.upper()}]")
        group_items = [it for it in backlog_items if it["status"] == status_group]
        for it in group_items:
            num_str = f" #{it['number']}" if it['number'] else ""
            repo_str = f" ({it['repo_owner']}/{it['repo_name']})" if it['repo_name'] else ""
            print(f"- {it['title']}{num_str}{repo_str}")
            print(f"  Item ID: {it['itemId']}")
            if it['body']:
                body_preview = it['body'].split('\n')[0][:80]
                print(f"  Preview: {body_preview}...")
 
    backlog_or_todo = [it for it in backlog_items if it["status"].lower() in ["backlog", "todo", "todo / backlog"]]
    if backlog_or_todo:
        print("\n--- Next Recommended Item to Implement ---")
        next_item = backlog_or_todo[0]
        print(f"Title: {next_item['title']}")
        print(f"Status: {next_item['status']}")
        print(f"Requirements:\n{next_item['body']}")
    else:
        print("\nNo items found in 'Backlog' or 'Todo' status.")

if __name__ == "__main__":
    main()
