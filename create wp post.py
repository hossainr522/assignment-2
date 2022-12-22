import requests
import base64

def oai_answer(prompt):
    import openai
    import os
    from dotenv import load_dotenv
    load_dotenv()
    openai.api_key = os.getenv('API_KEY')
    response = openai.Completion.create(
      model="text-davinci-003",
      prompt=prompt,
      temperature=0.7,
      max_tokens=256,
      top_p=1,
      frequency_penalty=0,
      presence_penalty=0
    )
    output = response.get('choices')[0].get('text')
    return output

def wp_p(text):
    code = f'<!-- wp:paragraph --><p>{text}</p><!-- /wp:paragraph -->'
    return code

def wp_h2(text):
    code = f'<!-- wp:heading --><h2>{text}</h2><!-- /wp:heading -->'
    return code

with open('keyword.txt', 'r') as file:
    main_keyword = file.readline()
    seed_keyword = main_keyword.replace('best ', '')

intro = oai_answer(f'write an 150 words intro about {main_keyword}')
wp_intro = wp_p(intro).strip()
important_title = f'Important of {seed_keyword}'
important_para = oai_answer(important_title)
buying_title = f'What to look for before buying a {seed_keyword}?'
buying_guide = oai_answer(buying_title)
buying_para = wp_p(buying_guide)
conclusion_heading = f'Conclusion'
conclusion_para = oai_answer(f'write {conclusion_heading} about {main_keyword}')

wp_url = 'https://rayhan.local/wp-json/wp/v2/posts'
user = 'Rayhan'
password = 'Dr77 kD2h sW2t NegZ rALd 2yZ3'
credential = f'{user}:{password}'
token = base64.b64encode(credential.encode())
headers = {'Authorization': f'Basic {token.decode("utf-8")}'}

title = f'{seed_keyword} Buying Guide'
content = f'{wp_intro}{wp_h2(important_title)}{wp_p(important_para)}{wp_h2(buying_title)}{wp_p(buying_para)}{wp_h2(conclusion_heading)}{wp_p(conclusion_para)}'

data = {
    'title': title.title(),
    'content':content,
    'slug': main_keyword.strip().lower().replace(' ','-')
}

r = requests.post(wp_url, data=data, headers=headers, verify=False)
print('Post already done')