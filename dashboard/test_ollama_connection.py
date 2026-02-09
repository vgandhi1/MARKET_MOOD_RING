import requests
import sys

def test_connection():
    # Try connecting to the IP of the Windows host directly if host.docker.internal fails
    # This is a common workaround for WSL2
    url = "http://host.docker.internal:11434/api/tags"
    
    # Check if we are in WSL environment (by checking /proc/version)
    in_wsl = False
    try:
        with open('/proc/version', 'r') as f:
            if 'microsoft' in f.read().lower():
                in_wsl = True
    except:
        pass

    print(f"🚀 Testing connection to: {url}")

    
    try:
        response = requests.get(url, timeout=5)
        print(f"✅ Status Code: {response.status_code}")
        if response.status_code == 200:
            print("🎉 SUCCESS! Container can reach Ollama on Windows Host.")
            print(f"Response: {response.text[:100]}...")
        else:
            print(f"⚠️  Connected, but received error code: {response.status_code}")
            
    except requests.exceptions.ConnectionError:
        print("❌ CONNECTION FAILED to host.docker.internal")
        
        # Fallback: Try to guess the host IP (Gateway IP)
        print("🔄 Attempting fallback: Trying default gateway IP...")
        try:
            # Alternative method to find host IP if ip/route command is missing
            # Typically 172.17.0.1 is the docker bridge gateway
            common_gateways = ["172.17.0.1", "192.168.65.2"] # 192.168.65.2 is common for Docker Desktop on Windows
            
            for ip in common_gateways:
                try:
                    fallback_url = f"http://{ip}:11434/api/tags"
                    print(f"🚀 Testing connection to IP: {fallback_url}")
                    response = requests.get(fallback_url, timeout=2)
                    if response.status_code == 200:
                        print(f"🎉 SUCCESS! Found Ollama at {ip}")
                        print(f"👉 ACTION REQUIRED: Update docker-compose 'extra_hosts' to point host.docker.internal to {ip}")
                        return
                except:
                    continue
        except Exception as e2:
            print(f"Fallback failed: {e2}")

        print("---------------------------------------------------")
        print("Reason: The container cannot reach the host.")
        print("Possible fixes:")
        print("1. Ensure Ollama is running on Windows.")
        print("2. Ensure OLLAMA_HOST=0.0.0.0:11434 environment variable is set on Windows.")
        print("3. Check Windows Firewall (Allow port 11434).")

    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_connection()
