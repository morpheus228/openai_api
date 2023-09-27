import openai

from utils import get_token
openai.api_key = get_token()


response = openai.Image.create(
  prompt="Star Wars and the Lion King",
  n=1,
  size="1024x1024"
)

image_url = response['data'][0]['url']
print(image_url)