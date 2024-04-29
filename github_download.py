import jwt
import time
from pathlib import Path
import sys
import os
from pathlib import Path
import requests
import argparse
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def generate_jwt(app_id, pem_file):
    # Expands the ~ to the user's home directory
    pem_path = Path(os.path.expanduser(pem_file))
    if not pem_path.exists():
        raise FileNotFoundError(f"The private key file was not found: {pem_file}")
    with open(pem_path, 'r') as file:
        private_key = file.read()
    payload = {
        'iat': int(time.time()),
        'exp': int(time.time()) + (10 * 60),  # Token valid for 10 minutes
        'iss': app_id
    }
    return jwt.encode(payload, private_key, algorithm='RS256')

def make_request(url, headers, method='GET', stream=False):
    with requests.request(method, url, headers=headers, stream=stream) as r:
        r.raise_for_status()
        return r if stream else r.json()

def download_file(url, token, output_filename, output_dir):
    headers = {"Authorization": f"token {token}", "Accept": "application/vnd.github.v3+json"}
    destination = Path(output_dir) / output_filename
    response = make_request(url, headers, method='GET', stream=True)
    with open(destination, 'wb') as f:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)
    print(f"Downloaded file to {destination}")

def get_installations(jwt):
    headers = {"Authorization": f"Bearer {jwt}", "Accept": "application/vnd.github.v3+json"}
    url = "https://api.github.com/app/installations"
    return make_request(url, headers)

def get_installation_access_token(jwt, installation_id):
    headers = {"Authorization": f"Bearer {jwt}", "Accept": "application/vnd.github.v3+json"}
    url = f"https://api.github.com/app/installations/{installation_id}/access_tokens"
    return make_request(url, headers, 'POST')['token']

def parse_arguments():
    parser = argparse.ArgumentParser(description='Download GitHub repository code for a specific tag or branch.')
    
    # Default values from environment variables
    default_app_id = os.getenv('GITHUB_APP_ID')
    default_pem_file = os.getenv('GITHUB_PRIVATE_KEY_PATH')

    parser.add_argument('--app_id', type=str, required=not default_app_id, default=default_app_id,
                        help='GitHub App ID')
    parser.add_argument('--pem_file', type=str, required=not default_pem_file, default=default_pem_file,
                        help='Path to GitHub App private key file')
    parser.add_argument('--repo', type=str, required=True, help='GitHub repository in the format "username/repository"')
    parser.add_argument('--target', type=str, required=True, help='Specific tag, branch, or release to download')
    parser.add_argument('--mode', type=str, default="branch", choices=['release', 'tag', 'branch'],
                        help='Download mode: release, tag, or branch')
    parser.add_argument('--output-dir', type=str, default=".", help='Output directory for downloaded files')

    return parser.parse_args()

if __name__ == "__main__":
    args = parse_arguments()
    jwt_token = generate_jwt(args.app_id, args.pem_file)
    installations = get_installations(jwt_token)
    if not installations:
        print("No installations found for this GitHub App.")
        sys.exit(1)
    installation_id = installations[0]['id']
    access_token = get_installation_access_token(jwt_token, installation_id)
    download_url = f"https://api.github.com/repos/{args.repo}/tarball/{args.target}"
    repo_name = args.repo.split('/')[-1]
    output_filename = f"{repo_name}-{args.target}.tar.gz"
    download_file(download_url, access_token, output_filename, args.output_dir)
