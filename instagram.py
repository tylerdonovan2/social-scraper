import requests, json, re

class profile:
    def __init__(self, username: str):
        # if link is inputted parse then username
        if 'https' in username or 'http' in username:
            username = re.findall("(?<=www.instagram.com/)(.*)(?=/)",username)[0]

        headers = {
            'authority': 'www.instagram.com',
            'accept': '*/*',
            'accept-language': 'en-US,en;q=0.9',
            'dpr': '1',
            'sec-ch-prefers-color-scheme': 'dark',
            'sec-ch-ua': '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
            'sec-ch-ua-full-version-list': '"Not_A Brand";v="8.0.0.0", "Chromium";v="120.0.6099.225", "Google Chrome";v="120.0.6099.225"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-model': '""',
            'sec-ch-ua-platform': '"Windows"',
            'sec-ch-ua-platform-version': '"10.0.0"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'x-asbd-id': '129477',
            'x-csrftoken': '0OuEofPI73rhodypQeXTuZ',
            'x-ig-app-id': '936619743392459',
            'x-ig-www-claim': '0',
            'x-requested-with': 'XMLHttpRequest',
        }

        params = {
            'username': username,
        }

        response = requests.get(
            'https://www.instagram.com/api/v1/users/web_profile_info/',
            params=params,
            headers=headers,
        )

        j = json.loads(response.text)

        user_data = j["data"]["user"]
        self.json_user_data = user_data

        self.username = username
        self.full_name = user_data["full_name"] if user_data["full_name"] else username
        self.bio = user_data["biography"]
        self.profile_picture = user_data["profile_pic_url_hd"]
        self.is_buisness = user_data["is_business_account"]

        # profile stats
        self.following = user_data["edge_follow"]["count"]
        self.followers = user_data["edge_followed_by"]["count"]
        self.highlight_count = user_data["highlight_reel_count"]
        self.post_count = user_data["edge_owner_to_timeline_media"]["count"]

        self.posts = []
        for edge in user_data["edge_owner_to_timeline_media"]["edges"]:
            post_data = {
                "shortcode": edge["node"]["shortcode"], 
                "caption": edge["node"]["edge_media_to_caption"]["edges"][0]["node"]["text"],
                "likes": edge["node"]["edge_liked_by"]['count'],
                "comments": edge["node"]["edge_media_to_comment"]['count'],
                "url": f'https://www.instagram.com/{username}/p/{edge["node"]["shortcode"]}/',
                "images": [image_data["node"]["display_url"].replace(r'\u0026',"&") for image_data in edge["node"]["edge_sidecar_to_children"]["edges"]]
            }

            self.posts.append(post_data)

    def __repr__(self):
        return f"{self.full_name} ({self.username})"

class post:
    def __init__(self, shortcode: str):

        # if link is inputted then parse shortcode
        if 'https' in shortcode or 'http' in shortcode:
            shortcode = re.findall("(?<=www.instagram.com/p/)(.*)(?=/)",shortcode)[0]

        headers = {
            'authority': 'www.instagram.com',
            'accept': '*/*',
            'accept-language': 'en-US,en;q=0.9',
            'content-type': 'application/x-www-form-urlencoded',
            'dpr': '1',
            'origin': 'https://www.instagram.com',
            'referer': 'https://www.instagram.com/tyler_donovan2/p/CzXMF1mPEd4/?img_index=1',
            'sec-ch-prefers-color-scheme': 'dark',
            'sec-ch-ua': '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
            'sec-ch-ua-full-version-list': '"Not_A Brand";v="8.0.0.0", "Chromium";v="120.0.6099.225", "Google Chrome";v="120.0.6099.225"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-model': '""',
            'sec-ch-ua-platform': '"Windows"',
            'sec-ch-ua-platform-version': '"10.0.0"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'viewport-width': '1069',
            'x-asbd-id': '129477',
            'x-csrftoken': '0OuEofPI73rhodypQeXTuZ',
            'x-fb-friendly-name': 'PolarisPostActionLoadPostQueryQuery',
            'x-fb-lsd': 'AVoX-PGNFn0',
            'x-ig-app-id': '936619743392459',
        }

        data = {
            'av': '0',
            '__d': 'www',
            '__user': '0',
            '__a': '1',
            '__req': '4',
            '__hs': '19748.HYP:instagram_web_pkg.2.1..0.0',
            'dpr': '1',
            '__ccg': 'UNKNOWN',
            '__rev': '1011024574',
            '__s': 'h2zto8:xct2qq:uyfmbo',
            '__hsi': '7328190870083555436',
            '__dyn': '7xeUjG1mxu1syUbFp60DU98nwgU29zEdEc8co2qwJw5ux609vCwjE1xoswIwuo2awlU-cw5Mx62G3i1ywOwv89k2C1Fwc60AEC7U2czXwae4UaEW2G1NwwwNwKwHw8Xxm16wUwtEvw4JwJCwLyES1Twoob82ZwrUdUbGwmk1xwmo6O1FwlE6PhA6bxy4UjK5V8',
            '__csr': 'gR17fBRql6j8iLVJqGpaExemRJtkqi9WyEyqeCiy8yqbgy699mviyqiKF8yhoiyaLG9GRJ7hpayppuiFGyO7CyG-HyrxbAUiyEO7oW5um4WxK00j3ahw6RU0bJE0qawg856yPw7wg0NS1Nw5hP0aS1awiUk80OU1LiwtE02Epw',
            '__comet_req': '7',
            'lsd': 'AVoX-PGNFn0',
            'jazoest': '2852',
            '__spin_r': '1011024574',
            '__spin_b': 'trunk',
            '__spin_t': '1706227397',
            'fb_api_caller_class': 'RelayModern',
            'fb_api_req_friendly_name': 'PolarisPostActionLoadPostQueryQuery',
            'variables': f'{{"shortcode":"{shortcode}","fetch_comment_count":50,"fetch_related_profile_media_count":0,"parent_comment_count":50,"child_comment_count":5,"fetch_like_count":10,"fetch_tagged_user_count":null,"fetch_preview_comment_count":0,"has_threaded_comments":true,"hoisted_comment_id":null,"hoisted_reply_id":null}}',
            'server_timestamps': 'true',
            'doc_id': '10015901848480474',
        }

        response = requests.post('https://www.instagram.com/api/graphql', headers=headers, data=data)

        # print(response.text)

        j = json.loads(response.text)


        post_data = j["data"]["xdt_shortcode_media"]
        self.json_post_data = post_data
        
        self.shortcode = shortcode
        self.is_reel = post_data["is_video"]
        self.username = post_data["owner"]["username"]
        self.thumbnail = post_data["thumbnail_src"]
        
        self.tagged_users = [{"full_name":edge["node"]["user"]["full_name"],"username":edge["node"]["user"]["username"],} for edge in post_data["edge_media_to_tagged_user"]["edges"]]
        self.comments = [{"text": edge["node"]["text"],"username":edge["node"]["owner"]["username"]} for edge in post_data["edge_media_to_parent_comment"]["edges"]]
        
        self.like_count = post_data["edge_media_preview_like"]["count"]
        self.comment_count = post_data["edge_media_to_parent_comment"]["count"]

        try:
            self.caption = post_data["edge_media_to_caption"]["edges"][0]["node"]["text"]
        except:
            self.caption = ""
        if self.is_reel:
            # get reel video link
            self.video_url = post_data["video_url"]
        else:
            try:
                # if multiple images
                self.image_urls = [edge["node"]["display_url"] for edge in post_data["edge_sidecar_to_children"]["edges"]]
            except:
                # single image
                self.image_urls = [post_data['display_url']]

    def get_profile(self):
        return profile(self.username)






print(re.findall("(?<=www.instagram.com/)(.*)(?=/)","https://www.instagram.com/tyler_donovan2/")[0])
