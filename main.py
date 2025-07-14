"""
╔══════════════════════════════════════════════════════════════════════════════════════╗
║                                                                                      ║
║   ██████╗ ██╗████████╗███████╗████████╗██████╗ ███████╗ █████╗ ██╗  ██╗              ║
║  ██╔════╝ ██║╚══██╔══╝██╔════╝╚══██╔══╝██╔══██╗██╔════╝██╔══██╗██║ ██╔╝              ║
║  ██║  ███╗██║   ██║   ███████╗   ██║   ██████╔╝█████╗  ███████║█████╔╝               ║
║  ██║   ██║██║   ██║   ╚════██║   ██║   ██╔══██╗██╔══╝  ██╔══██║██╔═██╗               ║
║  ╚██████╔╝██║   ██║   ███████║   ██║   ██║  ██║███████╗██║  ██║██║  ██╗              ║
║   ╚═════╝ ╚═╝   ╚═╝   ╚══════╝   ╚═╝   ╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝              ║
║                                                                                      ║
║                          GitHub README Timestamp Updater                            ║
║                                                                                      ║
║                          Copyright (c) 2025 Vijay Vairagade                         ║
║                              All Rights Reserved                                     ║
║                                                                                      ║
║      ┌─────────────────────────────────────────────────────────────────────────┐    ║
║      │  🤖 Automatically updates README.md with timestamps via GitHub API      │    ║
║      │  ⏰ Random intervals (1 hour - 6 hours)                                  │    ║
║      │  🌐 Remote hosting capability                                            │    ║
║      │  🔐 Secure token-based authentication                                    │    ║
║      └─────────────────────────────────────────────────────────────────────────┘    ║
║                                                                                      ║
╚══════════════════════════════════════════════════════════════════════════════════════╝
"""

import time
import random
import re
import base64
import json
from datetime import datetime
import requests
import os
from typing import Optional
from pathlib import Path
from dotenv import load_dotenv

env_path = Path(__file__).parent / '.env'
load_dotenv(dotenv_path=env_path)

try:
    from dotenv import load_dotenv
    load_dotenv()
    DOTENV_AVAILABLE = True
except ImportError:
    DOTENV_AVAILABLE = False

class GitHubReadmeUpdater:
    def __init__(self, token: str, username: str, repo_name: str, readme_path: str = "README.md"):
        self.token = token
        self.username = username
        self.repo_name = repo_name
        self.readme_path = readme_path
        self.api_base = "https://api.github.com"
        self.headers = {
            "Authorization": f"token {token}",
            "Accept": "application/vnd.github.v3+json",
            "User-Agent": "README-Updater"
        }
        self.timestamp_pattern = r"Last Seen - \d{2}:\d{2}[AP]M \d{2}/\d{2}/\d{4} \w+"
        
    def get_current_timestamp(self) -> str:
        """Generate current timestamp in the required format"""
        now = datetime.now()
        formatted_time = now.strftime("%I:%M%p %d/%m/%Y %A")
        return f"Last Seen - {formatted_time}"
    
    def get_file_content(self) -> Optional[dict]:
        """Get current README.md content from GitHub"""
        url = f"{self.api_base}/repos/{self.username}/{self.repo_name}/contents/{self.readme_path}"
        
        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"❌ Error fetching README.md: {e}")
            return None
    
    def decode_content(self, content: str) -> str:
        """Decode base64 encoded content from GitHub API"""
        try:
            return base64.b64decode(content).decode('utf-8')
        except Exception as e:
            print(f"❌ Error decoding content: {e}")
            return ""
    
    def encode_content(self, content: str) -> str:
        """Encode content to base64 for GitHub API"""
        return base64.b64encode(content.encode('utf-8')).decode('utf-8')
    
    def update_timestamp_in_content(self, content: str) -> str:
        """Update or add timestamp to the content"""
        new_timestamp = self.get_current_timestamp()
        
        
        if re.search(self.timestamp_pattern, content):
            
            updated_content = re.sub(self.timestamp_pattern, new_timestamp, content)
        else:
            
            updated_content = content.rstrip() + "\n\n" + new_timestamp + "\n"
        
        return updated_content
    
    def update_file_on_github(self, new_content: str, sha: str) -> bool:
        """Update README.md on GitHub using the API"""
        url = f"{self.api_base}/repos/{self.username}/{self.repo_name}/contents/{self.readme_path}"
        
        commit_message = f"🤖 Auto-update timestamp: {self.get_current_timestamp()} | Copyright (c) Vijay Vairagade"
        
        data = {
            "message": commit_message,
            "content": self.encode_content(new_content),
            "sha": sha
        }
        
        try:
            response = requests.put(url, headers=self.headers, json=data)
            response.raise_for_status()
            print(f"✅ Successfully updated README.md on GitHub")
            print(f"📝 Commit: {commit_message}")
            return True
        except requests.exceptions.RequestException as e:
            print(f"❌ Error updating README.md on GitHub: {e}")
            if hasattr(e, 'response') and e.response is not None:
                print(f"Response: {e.response.text}")
            return False
    
    def test_github_connection(self) -> bool:
        """Test if GitHub API credentials and repository access work"""
        url = f"{self.api_base}/repos/{self.username}/{self.repo_name}"
        
        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            repo_info = response.json()
            print(f"✅ Connected to repository: {repo_info['full_name']}")
            print(f"🌐 Repository URL: {repo_info['html_url']}")
            return True
        except requests.exceptions.RequestException as e:
            print(f"❌ Error connecting to GitHub: {e}")
            print("Please check your token, username, and repository name")
            return False
    
    def update_readme_timestamp(self) -> bool:
        """Main function to update README with new timestamp"""
        
        file_data = self.get_file_content()
        if not file_data:
            return False
        
        current_content = self.decode_content(file_data['content'])
        updated_content = self.update_timestamp_in_content(current_content)
        
        if current_content == updated_content:
            print("⏭️  No changes needed - timestamp already current")
            return True
        return self.update_file_on_github(updated_content, file_data['sha'])
    
    def get_random_interval(self) -> int:
        """Get random interval between 1 hour and 6 hours (in seconds)"""
        min_seconds = 1 * 60 * 60  
        max_seconds = 6 * 60 * 60  
        return random.randint(min_seconds, max_seconds)
    
    def run_continuous(self):
        """Run the updater continuously with random intervals"""
        print("🚀 GitHub README Timestamp Updater started!")
        print(f"👨‍💻 Created by: Vijay Vairagade")
        print(f"📁 Repository: {self.username}/{self.repo_name}")
        print(f"📄 File: {self.readme_path}")
        print("⏰ Will update timestamp at random intervals (1 hour - 6 hours)")
        print("🛑 Press Ctrl+C to stop")
        print("-" * 50)
        
        if not self.test_github_connection():
            return
        
        try:
            while True:
                success = self.update_readme_timestamp()
                if success: 
                    interval = self.get_random_interval()
                    hours = interval // 3600
                    minutes = (interval % 3600) // 60
                    
                    print(f"⏳ Next update in: {hours}h {minutes}m")
                    print(f"⏰ Next update at: {datetime.now().strftime('%I:%M%p %d/%m/%Y')}")
                    print("-" * 50)
                    time.sleep(interval)
                else:
                    print("❌ Failed to update. Retrying in 10 minutes...")
                    time.sleep(600)  
                
        except KeyboardInterrupt:
            print("\n🛑 Updater stopped by user")
        except Exception as e:
            print(f"❌ Unexpected error: {e}")

def main():
    """Main function to run the script"""
    
    print(__doc__)
    print("🔧 GitHub README Timestamp Updater Setup")
    print("=" * 50)
    
    if DOTENV_AVAILABLE:
        print("✅ .env file support enabled")
        if os.path.exists('.env'):
            print("📄 Found .env file - loading configuration...")
        else:
            print("⚠️  No .env file found - will check environment variables")
    else:
        print("⚠️  python-dotenv not installed - install with: pip install python-dotenv")
        print("📝 Using environment variables and interactive input only")
    
    print("-" * 50)
    token = os.getenv('GITHUB_TOKEN')
    username = os.getenv('GITHUB_USERNAME')
    repo_name = os.getenv('GITHUB_REPO')
    readme_path = os.getenv('README_PATH', 'README.md')
    
    if not token:
        print("📝 GitHub Personal Access Token not found in environment")
        print("💡 Create one at: https://github.com/settings/tokens")
        print("🔐 Required permissions: Contents (read & write)")
        if DOTENV_AVAILABLE:
            print("🔧 You can also add it to your .env file as: GITHUB_TOKEN=your_token_here")
        token = input("Enter your GitHub token: ").strip()
    
    if not username:
        if DOTENV_AVAILABLE:
            print("🔧 You can add your username to .env file as: GITHUB_USERNAME=your_username")
        username = input("Enter your GitHub username: ").strip()
    
    if not repo_name:
        if DOTENV_AVAILABLE:
            print("🔧 You can add your repo to .env file as: GITHUB_REPO=your_repo_name")
        repo_name = input("Enter your repository name: ").strip()
    
    if not all([token, username, repo_name]):
        print("❌ Missing required information. Exiting...")
        return
        
    print(f"\n📊 Configuration:")
    print(f"👤 Username: {username}")
    print(f"📁 Repository: {repo_name}")
    print(f"📄 README Path: {readme_path}")
    print("=" * 50)
    
    
    updater = GitHubReadmeUpdater(token, username, repo_name, readme_path)
    updater.run_continuous()

if __name__ == "__main__":
    main()
