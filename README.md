Allows a variety data to be pulled from various social media platforms.
Current Working Sites:
- Instagram
- TikTok


Example of scraping a post:
```
# To get the link, click share -> copy link
# the video id can be found in the link

# https://www.instagram.com/p/C2d1yC_Mmga/?utm_source=ig_web_copy_link
instagram_post = instagram.post('C2d1yC_Mmga')
link_instagram_post = instagram.post('https://www.instagram.com/p/C2d1yC_Mmga/?utm_source=ig_web_copy_link') # (this works too)

# https://www.tiktok.com/@jim59186/video/7316727623550340398?is_from_webapp=1&sender_device=pc
tiktokt_post = tiktok.post('7316727623550340398')
```


Example of scraping a profile:
```
# input the username of the profile
instagram_profile = instagram.profile('tyler_donovan2')
```

Instagram Profile Attributes:
```
# the following can be accessed by instagram.profile.attribute
json_user_data   # (dict) the direct json from the instagram api
username         # (str) profile username
full_name        # (str) profile display name
bio              # (str) user biography
profile_picture  # (str) profile picture url
is_buisness      # (bool) True/False value if account is a buisness acount
following        # (int) number of people the account is following 
followers        # (int) number of people following the account
highlight_count  # (int) number of highlights
post_count       # (int) number of posts
posts            # [(dict)] {"shortcode":"post shortcode","caption": "post caption","likes": "like count","comments": "comment count","url": "post url"}
```
