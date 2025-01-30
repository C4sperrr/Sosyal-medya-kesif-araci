import requests
import matplotlib.pyplot as plt

def twitter_api_request(username, access_token):
    """
    Twitter API'ye istek gönderir ve kullanıcı bilgilerini döner.
    
    Zorunlu Parametreler:
    - username (str): Twitter kullanıcı adı
    - access_token (str): Twitter API erişim anahtarı
    
    Çıktı Formatı:
    {
        "sonuç": {
            "durum": "başarılı/başarısız",
            "veri": {
                "id": <user_id>,
                "username": <username>,
                "followers_count": <followers_count>,
                "following_count": <following_count>,
                "tweet_count": <tweet_count>
            },
            "hata_mesajı": <error_message> 
        }
    }
    """
    url = f"https://api.twitter.com/2/users/by/username/{username}?user.fields=public_metrics"
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(url, headers=headers)
    data = response.json()

    if response.status_code != 200:
        return {
            "sonuç": {
                "durum": "başarısız",
                "veri": {},
                "hata_mesajı": data.get("detail", "Bilinmeyen hata")
            }
        }

    return {
        "sonuç": {
            "durum": "başarılı",
            "veri": {
                "id": data.get("data", {}).get("id"),
                "username": data.get("data", {}).get("username"),
                "followers_count": data.get("data", {}).get("public_metrics", {}).get("followers_count"),
                "following_count": data.get("data", {}).get("public_metrics", {}).get("following_count"),
                "tweet_count": data.get("data", {}).get("public_metrics", {}).get("tweet_count")
            },
            "hata_mesajı": None
        }
    }

def instagram_api_request(access_token):
    """
    Instagram API'ye istek gönderir ve kullanıcı bilgilerini döner.
    
    Zorunlu Parametreler:
    - access_token (str): Instagram API erişim anahtarı
    
    Çıktı Formatı:
    {
        "sonuç": {
            "durum": "başarılı/başarısız",
            "veri": {
                "id": <user_id>,
                "username": <username>,
                "account_type": <account_type>,
                "followers_count": <followers_count>,
                "following_count": <following_count>
            },
            "hata_mesajı": <error_message> 
        }
    }
    """
    url = f"https://graph.instagram.com/me?fields=id,username,account_type,media_count,followers_count,follows_count&access_token={access_token}"
    response = requests.get(url)
    data = response.json()

    if response.status_code != 200:
        return {
            "sonuç": {
                "durum": "başarısız",
                "veri": {},
                "hata_mesajı": data.get("error", {}).get("message", "Bilinmeyen hata")
            }
        }

    return {
        "sonuç": {
            "durum": "başarılı",
            "veri": {
                "id": data.get("id"),
                "username": data.get("username"),
                "account_type": data.get("account_type"),
                "media_count": data.get("media_count"),
                "followers_count": data.get("followers_count"),
                "following_count": data.get("follows_count")
            },
            "hata_mesajı": None
        }
    }

def facebook_api_request(access_token):
    """
    Facebook API'ye istek gönderir ve kullanıcı bilgilerini döner.
    
    Zorunlu Parametreler:
    - access_token (str): Facebook API erişim anahtarı
    
    Çıktı Formatı:
    {
        "sonuç": {
            "durum": "başarılı/başarısız",
            "veri": {
                "id": <user_id>,
                "name": <user_name>,
                "friends_count": <friends_count>,
                "friends_list": [<friend_1>, <friend_2>, ...]
            },
            "hata_mesajı": <error_message>
        }
    }
    """
    url = f"https://graph.facebook.com/v18.0/me?fields=id,name,friends.limit(100)&access_token={access_token}"
    response = requests.get(url)
    data = response.json()

    if response.status_code != 200:
        return {
            "sonuç": {
                "durum": "başarısız",
                "veri": {},
                "hata_mesajı": data.get("error", {}).get("message", "Bilinmeyen hata")
            }
        }

    friends = data.get("friends", {}).get("data", [])
    return {
        "sonuç": {
            "durum": "başarılı",
            "veri": {
                "id": data.get("id"),
                "name": data.get("name"),
                "friends_count": len(friends),
                "friends_list": [friend.get("name") for friend in friends]
            },
            "hata_mesajı": None
        }
    }

def generate_report(username, twitter_token, instagram_token, facebook_token):
    """
    Tüm platformlardan veriyi çekip rapor oluşturur.
    """
    twitter_data = twitter_api_request(username, twitter_token)
    instagram_data = instagram_api_request(instagram_token)
    facebook_data = facebook_api_request(facebook_token)

    report = {
        "Twitter": twitter_data,
        "Instagram": instagram_data,
        "Facebook": facebook_data
    }
    return report

def visualize_data(report):
    """
    Çekilen veriyi görselleştirir.
    """
    platforms = ["Twitter", "Instagram", "Facebook"]
    followers = [
        report["Twitter"].get("sonuç", {}).get("veri", {}).get("followers_count", 0),
        report["Instagram"].get("sonuç", {}).get("veri", {}).get("followers_count", 0),
        report["Facebook"].get("sonuç", {}).get("veri", {}).get("friends_count", 0)
    ]
    
    plt.figure(figsize=(8, 5))
    plt.bar(platforms, followers, color=['blue', 'purple', 'green'])
    plt.xlabel("Platforms")
    plt.ylabel("Followers/Friends Count")
    plt.title("Social Media Audience Comparison")
    plt.show()

if __name__ == "__main__":
    # Zorunlu parametreler:
    twitter_username = "example_username"  # Twitter kullanıcı adı
    twitter_token = "YOUR_TWITTER_ACCESS_TOKEN"
    instagram_token = "YOUR_INSTAGRAM_ACCESS_TOKEN"
    facebook_token = "YOUR_FACEBOOK_ACCESS_TOKEN"
    
    report = generate_report(twitter_username, twitter_token, instagram_token, facebook_token)
    print("Social Media Report:", report)
    visualize_data(report)
