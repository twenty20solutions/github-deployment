# GitHub Deployment Automation Project

This repository contains scripts and tools for automating deployment processes via GitHub Apps, focusing on tasks such as downloading specific releases, tags, or branches from private GitHub repositories.

## Getting Started

These instructions will guide you through setting up and running the project on your local machine for development and testing purposes.

### Prerequisites

- **Python**: Ensure Python 3.8 or newer is installed on your system. Verify by running `python --version` or `python3 --version` in your terminal.

### Installation

1. **Clone the Repository**

   Clone this repository to your local machine:

   ```bash
   git clone https://github.com/twenty20solutions/github-deployment.git
   ```

2. **Install Python Dependencies**

   Navigate to the project directory and install the necessary libraries:

   ```bash
   cd github-deployment
   python -m pip install -r requirements.txt
   ```

3. **Set Up a GitHub App**

   - Go to your GitHub organization or user settings.
   - Access **Developer settings** > **GitHub Apps** > **New GitHub App**.
   - Fill in the necessary details such as app name and permissions, ensuring at least `Contents: Read-only` is selected.
   - Generate and download a private key for your GitHub App.

### Configuration

1. **GitHub App Credentials**

   Set up the GitHub App ID and the private key path. You can use environment variables directly or specify them in a `.env` file:

   - **App ID**: Found on the GitHub App settings page.
   - **Private Key**: Ensure the `.pem` file is secure and accessible by the script.

2. **Environment Variables**

   For enhanced security and ease of use, particularly in automated environments, you can set the following environment variables directly or through a `.env` file located in the project root:

   ```bash
   export GITHUB_APP_ID="your_app_id_here"
   export GITHUB_PRIVATE_KEY_PATH="/path/to/your/private/key.pem"
   ```

   Alternatively, add these to a `.env` file:

   ```
   GITHUB_APP_ID=your_app_id_here
   GITHUB_PRIVATE_KEY_PATH=/path/to/your/private/key.pem
   ```

### Usage

Utilize the provided Python script to automate your GitHub deployment tasks, extending or modifying the scripts as necessary for your specific workflows.

- **Download Files**: The `github_download.py` script handles JWT generation and downloading specified content from a GitHub repository.

  ```bash
  python github_download.py --app_id [your_app_id] --pem_file /path/to/private_key.pem --repo [username/repository] --target [tag/branch/release] --output-dir [download_directory]
  ```

### Contributing

If you're interested in improving the GitHub Deployment Automation Project, please fork the repository and submit pull requests.

---

This version of the README now includes details on how to configure `.env` files for environment variables, providing flexibility and security for managing sensitive data.
