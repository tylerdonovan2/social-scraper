import requests, json
from lxml import etree

class profile:
    def __init__(self, user_id: str):
        pass

class post:
    def __init__(self, video_id: str):
        response = requests.get(f'https://www.tiktok.com/@hellofellowcoder/video/{video_id}')
        self.cookies = response.cookies.get_dict()

        tree = etree.HTML(response.text)
        page_data = tree.xpath("/html/body/script[1]")[0]
        
        j = json.loads(page_data.text)
        video_data = j["__DEFAULT_SCOPE__"]["webapp.video-detail"]["itemInfo"]["itemStruct"]
        self.json_post_data = video_data

        # useful video data
        self.video_id = video_id
        self.video_url = video_data["video"]["playAddr"]
        print(self.video_url)
        self.thumbnail = video_data["video"]["cover"]
        
        self.username = video_data["author"]["uniqueId"]
        
        self.caption = video_data["desc"]

        self.music_title = video_data["music"]["title"]
        self.music_id = video_data["music"]["id"]
        
        # video stat collection
        self.like_count = video_data["stats"]["diggCount"]
        self.comment_count = video_data["stats"]["commentCount"]
        self.view_count = video_data["stats"]["playCount"]
        self.favorite_count = video_data["stats"]["collectCount"]
        self.share_count = video_data["stats"]["shareCount"]

    def save_video(self, outfile: str):
        headers = {
            'Accept': '*/*',
            'Accept-Language': 'en-US,en;q=0.9',
            'Connection': 'keep-alive',
            # 'Cookie': 'tt_csrf_token=rciongDQ-hkljIa22xqixKidWsZupx0sxZno; tt_chain_token=zcXqUl9z/v7sMbOuqnOzYA==; odin_tt=8a1e0f504017234e493df022bd40396ebb7aeceaa27edaf3edf05c4ba8df1073ec9db932c5d11703a68864d383eda75436a892d91d1e5d86e7213cdbaee3bc5a2b12382a4723ec934c473d63ee392242; ak_bmsc=510A18424F9FAE85142E4B47A7BB0F55~000000000000000000000000000000~YAAQDw08Fye8ojaNAQAATOdDQxbFZj1cHZWAK8Owo2qrLMZ93VZPROb+SL3cevmA4S431o1b/k0FvKhxicnEQ8P7LMNn0Z/XfOePg70ZQFNIFyJpqbjNMf1ONOMgZ4mmnAI1Y8QQDKWKtNekM3sleuWwpZdiHiyJjkeL5PX4eh1sLaJ+orjlkablWWXLGDGWKc21Vg5cHvv3SvoGm6rzarAtFMiWkNlG9e7eEAJilCIq3qcHzyUUljfsRoHUyMjnFWTY66H3+1bIXQZgCFGdSCjUpsnK0C5JOpKs/Y2rzNrK9yqWtiemGJ3M000XbgVovM0SBHWeoQis1f1bi26ueGjZkK1wmb/0DV+wowpX7X9aWFKY5hxf2v0SZ0SfDgY8cNBcG+sjw9YDl4v3xTtdjYi8a4MDVCBZLjy+rMc+AWhWPF28HiwB/3dPTfJIW/f3rOxTsLFOS6RIv3nL+bJkub13+H8RnXJ5ThaqHs7DQ6pp2JOSweX8yXVPEbUGzA==; msToken=DNyEPQcI_I3l9PllAKU-Lp16vVpXhgsqXdLFt_MzgS4V3_ZfXNJdtCEE57Fadoa00zFcuDeRxen1PRfLSDTyZZJ_oS1lCtSpYo-QBhhnEhQjFnOd7EcqhQyc2Kn4R4BvWlIgtRayIeCczMY=; bm_sv=C5EBAED5D385AB108740700210948FC4~YAAQLi4nF1u4mD2NAQAA+3ltQxZdOOCTrSvBJMpvAFFbOn3OmgXtoBqK+gSs1JgY/T5pIrI672B0YKmCn9I5In1vWMUcChqprK64cDqc2F/yMirh8keKO5Bv9+MP9NqfvSGbi01BfIsio5jHq1n2A7k5Nla6HzJ1HiyJ1yAycz2d0ltC7P40js/4DFVkKcBGV6EAiw0ZjMqI2DWQCF90eydo232q2FwYevAbwKQJaGN1oDnmEuhsAhj7mYWSuiZV~1; ttwid=1%7CFLNDyNP3J86UXM0_we-G9N65omnTH4dBIVrRLG8i-vA%7C1706233265%7C8582cd8367cf564aef7c01722de10ba4b9cb0f830a39007b1aa41b5906eb61e4',
            'Origin': 'https://www.tiktok.com',
            'Range': 'bytes=0-',
            'Referer': 'https://www.tiktok.com/',
            'Sec-Fetch-Dest': 'video',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-site',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'sec-ch-ua': '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
        }

        response = requests.get(
            self.video_url,
            headers=headers,
            cookies=self.cookies,
        )

        with open(f'{outfile}.mp4','wb') as f:
            for chunk in response.iter_content(chunk_size=100000000000):
                f.write(chunk)
