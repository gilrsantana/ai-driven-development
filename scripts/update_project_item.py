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

def update_item_field(token, project_id, item_id, field_id, option_id):
    mutation = """
    mutation($projectId: ID!, $itemId: ID!, $fieldId: ID!, $optionId: String!) {
      updateProjectV2ItemFieldValue(
        input: {
          projectId: $projectId
          itemId: $itemId
          fieldId: $fieldId
          value: {
            singleSelectOptionId: $optionId
          }
        }
      ) {
        projectV2Item {
          id
        }
      }
    }
    """
    
    variables = {
        "projectId": project_id,
        "itemId": item_id,
        "fieldId": field_id,
        "optionId": option_id
    }
    
    url = "https://api.github.com/graphql"
    headers = {
        "Authorization": f"Bearer {token}",
        "User-Agent": "Antigravity-Agent",
        "Content-Type": "application/json"
    }
    
    req_data = json.dumps({"query": mutation, "variables": variables}).encode("utf-8")
    req = urllib.request.Request(url, data=req_data, headers=headers, method="POST")
    
    try:
        with urllib.request.urlopen(req) as response:
            res_data = response.read().decode("utf-8")
            res_json = json.loads(res_data)
            if "errors" in res_json:
                return False, json.dumps(res_json["errors"])
            return True, None
    except urllib.error.HTTPError as e:
        err_msg = f"HTTP Error {e.code}: {e.reason}"
        try:
            err_msg += f" - {e.read().decode('utf-8')}"
        except Exception:
            pass
        return False, err_msg
    except Exception as e:
        return False, str(e)

def main():
    if len(sys.argv) < 6:
        print("Usage: update_project_item.py <projectId> <itemId> <fieldId> <optionId> <base_code_path>")
        sys.exit(1)
        
    project_id = sys.argv[1]
    item_id = sys.argv[2]
    field_id = sys.argv[3]
    option_id = sys.argv[4]
    base_code_path = sys.argv[5]
    
    token = load_token(base_code_path)
    if not token:
        print("ERROR: GitHub Token not found.", file=sys.stderr)
        sys.exit(1)
        
    print(f"Updating item {item_id} field {field_id} to option {option_id}...")
    success, error = update_item_field(token, project_id, item_id, field_id, option_id)
    if success:
        print("SUCCESS: Project item status updated.")
        sys.exit(0)
    else:
        print(f"ERROR: Failed to update project item: {error}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
