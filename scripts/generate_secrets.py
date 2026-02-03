#!/usr/bin/env python3
"""
ALCIS Secret Generation Script
Generates secure keys for production deployment
"""
import secrets
import base64
import os
from cryptography.fernet import Fernet


def generate_secret_key(length: int = 32) -> str:
    """Generate a secure secret key"""
    return secrets.token_urlsafe(length)


def generate_encryption_key() -> str:
    """Generate a Fernet encryption key"""
    return Fernet.generate_key().decode()


def generate_jwt_secret() -> str:
    """Generate JWT secret key"""
    return secrets.token_urlsafe(64)


def main():
    """Generate all required secrets"""
    print("🔐 ALCIS Secret Generation")
    print("=" * 50)
    
    # Generate secrets
    secret_key = generate_secret_key()
    encryption_key = generate_encryption_key()
    jwt_secret = generate_jwt_secret()
    
    print("\n📋 GitHub Secrets Configuration")
    print("Add these to your GitHub repository secrets:")
    print("Repository Settings > Secrets and variables > Actions\n")
    
    print("🔑 Required Secrets:")
    print(f"SECRET_KEY={secret_key}")
    print(f"ENCRYPTION_KEY={encryption_key}")
    print(f"JWT_SECRET={jwt_secret}")
    
    print("\n🐳 Docker Secrets (Optional - for Docker Hub):")
    print("DOCKER_USERNAME=your-docker-username")
    print("DOCKER_PASSWORD=your-docker-password")
    
    print("\n📦 PyPI Secrets (Optional - for package publishing):")
    print("PYPI_API_TOKEN=your-pypi-token")
    
    print("\n🔧 External Service Secrets (Optional):")
    print("TWILIO_ACCOUNT_SID=your-twilio-sid")
    print("TWILIO_AUTH_TOKEN=your-twilio-token")
    print("AWS_ACCESS_KEY_ID=your-aws-key")
    print("AWS_SECRET_ACCESS_KEY=your-aws-secret")
    
    print("\n💾 Local Development (.env file):")
    env_content = f"""# ALCIS Local Development Environment
# Generated secrets - DO NOT COMMIT TO GIT

# Core Security
SECRET_KEY={secret_key}
ENCRYPTION_KEY={encryption_key}
JWT_SECRET={jwt_secret}

# Environment
ENVIRONMENT=development
DEBUG=true

# Database (Update with your local settings)
DATABASE_URL=postgresql://alcis:alcis@localhost/alcis
REDIS_URL=redis://localhost:6379/0

# External Services (Add your credentials)
TWILIO_ACCOUNT_SID=
TWILIO_AUTH_TOKEN=
TWILIO_PHONE_NUMBER=

AWS_ACCESS_KEY_ID=
AWS_SECRET_ACCESS_KEY=
AWS_REGION=us-east-1

SMTP_HOST=
SMTP_PORT=587
SMTP_USERNAME=
SMTP_PASSWORD=
SMTP_USE_TLS=true
"""
    
    # Write to .env file
    with open('.env', 'w') as f:
        f.write(env_content)
    
    print(f"\n✅ Local .env file created with secure secrets!")
    print("⚠️  Remember: Never commit .env to git!")
    
    print("\n🚀 Next Steps:")
    print("1. Create GitHub repository")
    print("2. Add secrets to GitHub repository settings")
    print("3. Push code: git push origin main")
    print("4. Watch CI/CD pipeline run automatically!")


if __name__ == "__main__":
    main()