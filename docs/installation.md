# Installation Guide

Complete installation instructions for PentestAI framework.

## System Requirements

### Minimum Requirements
- **OS:** Windows 10/11, Ubuntu 20.04+, macOS 11+
- **RAM:** 4GB (8GB recommended)
- **Disk:** 10GB free space (20GB for Docker)
- **Python:** 3.9 or higher
- **Docker:** 20.10+ (optional but recommended)
- **Docker Compose:** 2.0+ (optional but recommended)

### Recommended Requirements
- **RAM:** 16GB
- **Disk:** 50GB SSD
- **CPU:** 4+ cores
- **Network:** Broadband (for LLM API calls)

## Installation Methods

### Method 1: Docker (Recommended)

Fastest and easiest way to get started.

#### Step 1: Install Docker

**Windows:**
1. Download Docker Desktop: https://www.docker.com/products/docker-desktop
2. Run installer
3. Restart computer
4. Verify: `docker --version`

**Linux (Ubuntu):**
```bash
# Update packages
sudo apt-get update

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Add user to docker group
sudo usermod -aG docker $USER

# Start Docker
sudo systemctl start docker
sudo systemctl enable docker

# Verify
docker --version
```

**macOS:**
1. Download Docker Desktop: https://www.docker.com/products/docker-desktop
2. Drag to Applications folder
3. Run Docker Desktop
4. Verify: `docker --version`

#### Step 2: Clone Repository

```bash
# Clone
git clone https://github.com/pentestai/pentestai.git
cd pentestai

# Or download ZIP and extract
```

#### Step 3: Configure Environment

```bash
# Copy template
cp .env.example .env

# Edit .env
nano .env  # Linux/Mac
notepad .env  # Windows

# Add your API key:
OPENAI_API_KEY=sk-your-key-here
```

#### Step 4: Start Services

```bash
# Start all services
docker-compose up -d --build

# Wait for services to start (30-60 seconds)

# Check status
docker-compose ps

# You should see 3 services running:
# - kali-mcp-server
# - pentestai-api  
# - pentestai-react-ui
```

#### Step 5: Access Interfaces

- **React UI:** http://localhost:3000
- **API Server:** http://localhost:8000
- **API Docs:** http://localhost:8000/docs
- **Documentation:** Run `.\start_docs.ps1` then http://localhost:3001

### Method 2: Python Virtual Environment

For development or if you prefer not to use Docker.

#### Step 1: Install Python

**Windows:**
1. Download Python 3.11: https://www.python.org/downloads/
2. Run installer (✓ Add to PATH)
3. Verify: `python --version`

**Linux (Ubuntu):**
```bash
sudo apt-get update
sudo apt-get install python3.11 python3.11-venv python3-pip
python3.11 --version
```

**macOS:**
```bash
# Using Homebrew
brew install python@3.11
python3.11 --version
```

#### Step 2: Clone Repository

```bash
git clone https://github.com/pentestai/pentestai.git
cd pentestai
```

#### Step 3: Create Virtual Environment

```bash
# Create venv
python -m venv venv

# Activate
# Windows:
venv\Scripts\activate

# Linux/Mac:
source venv/bin/activate

# Verify
which python  # Should show venv/bin/python
```

#### Step 4: Install Dependencies

```bash
# Upgrade pip
pip install --upgrade pip

# Install requirements
pip install -r requirements.txt

# Install in development mode
pip install -e .

# Verify installation
python -c "from pentestai import PentestAIController; print('✅ Import successful')"
```

#### Step 5: Configure API Key

```bash
# Set environment variable
# Windows:
set OPENAI_API_KEY=sk-your-key-here

# Linux/Mac:
export OPENAI_API_KEY=sk-your-key-here

# Or create .env file
echo "OPENAI_API_KEY=sk-your-key-here" > .env
```

#### Step 6: Test Installation

```bash
# Run interactive CLI
python pentestai_interactive.py

# Or run example
python quickstart.py
```

### Method 3: pip Install (Future)

Coming soon! Will support:
```bash
pip install pentestai
```

## Configuration

### Get OpenAI API Key

1. Visit: https://platform.openai.com/api-keys
2. Create account or log in
3. Click "Create new secret key"
4. Copy key (starts with `sk-`)
5. Add to `.env` file

**Free Tier Limits:**
- 3 requests/minute
- $5 free credit for new accounts
- Enough for testing!

### Get ArvanCloud API Key (Iranian Users)

1. Visit: https://arvancloud.ir
2. Create account
3. Navigate to AI Gateway
4. Copy API token
5. Add to `.env`:
```bash
ARVANCLOUD_API_KEY=your-token
OPENAI_BASE_URL=https://api.arvancloud.ir/llm/v1
```

## Verification

### Quick Health Check

```bash
# Docker installation
curl http://localhost:8000/api/health

# Expected response:
# {"status":"ok","llm_connected":true,"llm_model":"gpt-4"}
```

```python
# Python installation
from pentestai import PentestAIController, PentestAIConfig

config = PentestAIConfig(
    target="test",
    openai_api_key="sk-...",
    sandbox_mode=True
)

controller = PentestAIController(config)
print("✅ Installation verified!")
```

### Run Test Pentest

```python
#!/usr/bin/env python3
"""Quick test to verify installation."""

from pentestai import PentestAIController, PentestAIConfig

# Configure (sandbox mode is safe)
config = PentestAIConfig(
    target="192.168.1.100",
    openai_api_key="sk-your-key",  # Replace!
    sandbox_mode=True,  # Safe simulation
    max_iterations=3,  # Quick test
)

# Run pentest
controller = PentestAIController(config)
result = controller.run_pentest_only()

# Check results
print(f"✅ Test complete!")
print(f"Found {len(result.vulnerabilities)} vulnerabilities")
```

## Troubleshooting Installation

### Issue: Docker won't start

**Windows:**
```powershell
# Enable WSL2
wsl --install

# Enable Hyper-V (if needed)
# Run as Administrator:
Enable-WindowsOptionalFeature -Online -FeatureName Microsoft-Hyper-V -All
```

**Linux:**
```bash
# Check Docker service
sudo systemctl status docker

# Start if stopped
sudo systemctl start docker
```

### Issue: Python module not found

```bash
# Reinstall in development mode
pip install -e .

# Or install specific package
pip install openai pydantic python-dotenv
```

### Issue: Permission denied (Linux)

```bash
# Add user to docker group
sudo usermod -aG docker $USER

# Log out and back in
```

### Issue: Port already in use

```bash
# Change ports in docker-compose.yml
ports:
  - "3001:3000"  # React UI
  - "8001:8000"  # API
```

## Next Steps

After successful installation:

1. **Read Getting Started:** [docs/getting-started.md](getting-started.md)
2. **Review Configuration:** [docs/core/configuration.md](core/configuration.md)
3. **Run First Pentest:** [docs/examples/full-assessment.md](examples/full-assessment.md)
4. **Explore Architecture:** [docs/architecture.md](architecture.md)

## Uninstallation

### Docker Installation

```bash
# Stop and remove containers
docker-compose down

# Remove volumes
docker-compose down -v

# Remove images
docker rmi $(docker images | grep pentestai | awk '{print $3}')

# Remove project directory
cd ..
rm -rf pentestai
```

### Python Installation

```bash
# Deactivate venv
deactivate

# Remove project directory
cd ..
rm -rf pentestai

# Uninstall packages (if needed)
pip uninstall pentestai -y
```

## Update/Upgrade

### Docker Installation

```bash
# Pull latest changes
git pull origin main

# Rebuild and restart
docker-compose down
docker-compose up -d --build
```

### Python Installation

```bash
# Pull latest changes
git pull origin main

# Update dependencies
pip install --upgrade -r requirements.txt

# Reinstall package
pip install -e .
```

---

**Installation complete!** Continue to [Getting Started →](getting-started.md)
