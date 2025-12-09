"""
Quick test script to verify Azure OpenAI connection.
Uses Azure AD (Entra ID) authentication since key-based auth is disabled.
"""
import os
import time
from dotenv import load_dotenv
from openai import AzureOpenAI
from azure.identity import DefaultAzureCredential, get_bearer_token_provider

# Load environment variables from .env file
load_dotenv()

def test_aoai_connection():
    """Test the connection to Azure OpenAI by making a simple API call."""
    
    # Get configuration from environment
    endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
    model = os.getenv("AI_MODEL")
    api_version = os.getenv("API_VERSION")
    
    print(f"Testing connection to: {endpoint}")
    print(f"Using model: {model}")
    print(f"API Version: {api_version}")
    print("Authentication: Azure AD (DefaultAzureCredential)")
    print("-" * 50)
    
    # Set up Azure AD authentication
    credential = DefaultAzureCredential()
    token_provider = get_bearer_token_provider(
        credential,
        "https://cognitiveservices.azure.com/.default"
    )
    
    # Create the Azure OpenAI client with Azure AD auth
    client = AzureOpenAI(
        azure_endpoint=endpoint,
        azure_ad_token_provider=token_provider,
        api_version=api_version
    )
    
    # Define prompts for each style
    styles = {
        "small": {
            "system": "You are an ASCII artist. Create art using ONLY basic ASCII characters and ANSI color codes. ALWAYS include color codes. Format: \\033[32m for green, \\033[33m for yellow, \\033[31m for red, \\033[34m for blue, \\033[0m to reset. CONSTRAINTS: Max 40 characters wide, 8-12 lines tall. NO unicode. NO code blocks. Output raw art only.",
            "user": "Christmas tree: yellow * star on top, green tree body using / \\ and *, brown || trunk, and 2-3 small red/blue gift boxes [] at the bottom. Keep it compact, max 40 chars wide."
        },
        "banner": {
            "system": "You are an ASCII artist. RULES: 1) Use ONLY: * / \\ | _ - + [ ] ( ) o O @ # = ~ ^ . space and letters. 2) Use ANSI colors: \\033[32m=green \\033[33m=yellow \\033[31m=red \\033[34m=blue \\033[0m=reset. 3) NO unicode, NO box-drawing, NO emojis, NO markdown, NO code blocks. 4) Max 60 chars wide, 12 lines. 5) Output ONLY the raw ASCII art, nothing else.",
            "user": "Large Christmas tree: yellow * star at top, green tree body using / \\ and *, red o ornaments scattered on tree, brown || trunk, and 3 colorful gift boxes [] at bottom."
        },
        "simple": {
            "system": "You are a greeting card writer. Output a single line greeting with Christmas emojis and ANSI color codes. Format: \\033[32m for green, \\033[33m for yellow, \\033[31m for red, \\033[0m to reset. NO code blocks. Output raw text only.",
            "user": "Write a simple one-line Christmas greeting with a tree emoji, star, and gift. Include colors for key words."
        }
    }
    
    for style_name, prompts in styles.items():
        print(f"\n{'='*50}")
        print(f"STYLE: {style_name.upper()}")
        print('='*50)
        
        try:
            start_time = time.time()
            response = client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": prompts["system"]},
                    {"role": "user", "content": prompts["user"]}
                ]
            )
            elapsed_time = time.time() - start_time
            
            # Print the response
            print("✅ Success!")
            art = response.choices[0].message.content
            art = art.replace('\\033[', '\033[')
            print(f"Response:\n{art}")
            print("-" * 50)
            print(f"Tokens: {response.usage.total_tokens} | Time: {elapsed_time:.2f}s")
            
        except Exception as e:
            print(f"❌ Failed: {type(e).__name__}: {e}")
    
    return True

if __name__ == "__main__":
    test_aoai_connection()
