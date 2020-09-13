import requests
import random
from environs import Env

env = Env()
env.read_env()

url = env('URL', default='http://127.0.0.1:8000/')
posts_url = url + 'api/blog/posts/'
bloggers_url = url + 'api/blog/bloggers/'

num_users = env.int('NUMBER_OF_USERS', default=5)
max_num_posts = env.int('MAX_POSTS_PER_USER', default=5)
max_num_likes = env.int('MAX_LIKES_PER_USER', default=10)

word_site = "http://svnweb.freebsd.org/csrg/share/dict/words?view=co&content-type=text/plain"

response = requests.get(word_site)
words = response.text.splitlines()

class User:
    def __init__(self, url, username, password, email):
        self.email = email
        self.username = username
        self.password = password

        self._url = url
        self._pk = None
        self.session = requests.Session()
        self.created = False
        
    def create_user(self):
        data = {'email': self.email, 'username': self.username, 'password': self.password}
        re = self.session.post(f'{self._url}auth/users/', data=data)
        if re.status_code == 201:
            self.created = True
            self._pk = re.json()['id']
        
        else:
            print(re.text)
        
    def _auth(self):
        data = {'username': self.username, 'password': self.password}
        return self.session.post(f'{url}auth/jwt/create/', data=data).json()

    def login(self):
        tokens = self._auth()
        headers = {
            'Accept': 'application/json',
            'Authorization': f'Bearer {tokens["access"]}'
        }
        self.session.headers.update(headers)

        if not self._pk:
            data = self.session.get(f'{url}auth/users/me/')
            if data.status_code == 200:
                self._pk = data.json()['id']
        
        self.session.close()

    def create_post(self, title, text):
        data = {'title': title, 'text': text}
        self.session.post(posts_url, data=data)
        self.session.close()
    
    def like_post(self, post_pk):
        if type(post_pk) is int:
            post_pk = [post_pk]
        like_url = f'{bloggers_url}{self._pk}'

        res = self.session.get(like_url)

        likes = res.json()['likes']
        likes += post_pk
        res = self.session.patch(like_url, data={'likes': likes})
        if res.status_code == 200:
            print(f'User {self.username} liked posts: {post_pk}')
        else:
            print(res.text)
        self.session.close()
        

if __name__ == '__main__':
    users = []
    for i in range(num_users):
        user = User(url, f'bot_user{i}', '123zaq!@#', f'user{i}@email.com')
        user.create_user()
        user.login()
        users.append(user)
        for _ in range(random.randint(1, max_num_posts)):
            title = " ".join(random.sample(words, random.randint(1, 5)))
            text = " ".join(random.sample(words, random.randint(5, 20)))
            user.create_post(title, text)
    
    usernames = [user.username for user in users]

    while True:
        if len(users) == 0:
            break
        max_posts = 0
        for i,user in enumerate(users):
            data = user.session.get(f'{bloggers_url}{user._pk}').json()
            posts = data["posts"]
            print(f'User #{user._pk} {user.username} has {len(posts)} posts. Current record is {max_posts}')
            if len(posts) > max_posts:
                active_user = i
                max_posts = len(posts)
                liked_posts = data["likes"]

        
        print(f'Biggest poster is {user.username} with {max_posts} posts')
        user = users[active_user]
        likes = 0
        while likes < max_num_likes:
            all_posts = user.session.get(posts_url).json()
            unliked_posts = [post for post in all_posts if len(post['likes']) == 0]
            if not unliked_posts:
                print('No unliked posts found, exiting.')
                exit()
            eligable_users = set()
            for post in unliked_posts:
                if post['author'] not in eligable_users and post['author'] != user.username:
                    eligable_users.add(post['author'])
                if len(eligable_users) == num_users - 1:
                    break
            if not eligable_users:
                break
            eligable_posts = [post for post in all_posts if post['author'] in eligable_users
                                                            and post['id'] not in liked_posts]

            post_to_like = random.choice(eligable_posts)['id']                                                        
            user.like_post(post_to_like)
            liked_posts.append(post_to_like)
            likes += 1
        users.pop(active_user)

