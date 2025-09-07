import requests

IPINFO_TOKEN = '6e211e3b5a889c'

def get_ip_location(ip):
    url = f"https://ipinfo.io/{ip}?token={IPINFO_TOKEN}"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            return {
                "ip": data.get("ip"),
                "city": data.get("city"),
                "region": data.get("region"),
                "country": data.get("country"),
                "loc": data.get("loc"), 
                "org": data.get("org"),  
                "timezone": data.get("timezone")
            }
        else:
            return {"error": f"Failed to fetch IP info: {response.status_code}"}
    except Exception as e:
        return {"error": str(e)}
