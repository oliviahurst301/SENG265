from blogging.post import Post
from blogging.dao.post_dao_pickle import PostDAOPickle

class Blog:

    def __init__(self, id: int, name: str, url: str, email: str):
        self.id = id  
        self.name = name
        self.url = url 
        self.email = email
        self.next_post_code = 1
        self.posts_dao = PostDAOPickle(self)


    def __repr__(self):
        return f"Blog({self.id}, {self.name}, {self.url}, {self.email})"

    def __str__(self):
        return f"id: {self.id}\nName: {self.name}\nurl: {self.url}\nEmail: {self.email}"

    def __eq__(self, other) -> bool:
        return self.id == other.id and self.name == other.name and \
                self.url == other.url and self.email == other.email


    def get_id(self) -> int:
        return self.id
    
    def get_name(self) -> str:
        return self.name

    def get_url(self) -> str:
        return self.url

    def get_email(self) -> str:
        return self.email


    def set_id(self, new_id):
        self.id = new_id

    def set_name(self, new_name):
        self.name = new_name

    def set_url(self, new_url):
        self.url = new_url

    def set_email(self, new_email):
        self.email = new_email


    def update(self, new_id, new_name, new_url, new_email):
        """
        Update blog
        """
        self.id = new_id
        self.name = new_name
        self.url = new_url
        self.email = new_email


    def create_post(self, title, text):
        """
        Creates a new Post in this blog using the blog's
        auto-incrementing code.
        Returns the created post
        """
        code = self.next_post_code
        post = Post(code, title, text)
        self.next_post_code += 1

        return self.posts_dao.create_post(post)


    def search_posts(self, search):
        """
        Searches through a blog to find posts whose title
        or text contain the given search string
        Returns: a list of Post objects matching the criteria
        """

        return self.posts_dao.retrieve_posts(search)


    def update_post(self, code, new_title, new_text):
        """
        Updates a post identified by code in current blog.
        Returns: True if updated, False otherwise
        """

        return self.posts_dao.update_post(code, new_title, new_text)


    def delete_post(self, code):
        """
        Deletes the post identified by the code.
        Returns: True if deleted, False otherwise
        """
        """
        if code in self.posts:
            del self.posts[code]
            return True

        return False
        """
        return self.posts_dao.delete_post(code)


    def list_posts(self):
        """
        Lists all posts in this blog in order of creation 
        (last to first)
        Returns: A list of all posts in this blog
        """

        return self.posts_dao.list_posts()


    def search_post(self, code):
        """
        Return a single post by its code, or None if not found.
        """
        return self.posts_dao.search_post(code)