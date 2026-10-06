from blogging.dao.blog_dao_json import BlogDAOJSON
from blogging.blog import Blog
from blogging.exception.duplicate_login_exception import DuplicateLoginException
from blogging.exception.illegal_access_exception import IllegalAccessException
from blogging.exception.illegal_operation_exception import IllegalOperationException
from blogging.exception.invalid_login_exception import InvalidLoginException
from blogging.exception.invalid_logout_exception import InvalidLogoutException
from blogging.exception.no_current_blog_exception import NoCurrentBlogException
from blogging.configuration import Configuration
import hashlib

class Controller:

    def __init__(self, autosave: bool = False):
        self.autosave = Configuration.autosave
        self.blog_dao = BlogDAOJSON()
        self.current_blog = None
        self.logged_in = False
        self.current_user = None

        if self.autosave:
            self.users = self.load_users()

        else:
            self.users = {
                "user": self.hash_password("123456"),
                "ali": self.hash_password("@G00dPassw0rd"),
            }
        

    def load_users(self):
        """
        Loads users from users_file in Configuration for the constructor.
        Stored as username for key and password for the value pair.
        Returns the loaded users dictionary.
        """
        users = {}
        try:
            with open(Configuration.users_file, 'r') as file:
                for user_line in file:
                    user_line = user_line.strip()
                    user_info = user_line.split(',')
                    name = user_info[0]
                    password = user_info[1]
                    users[name] = password
                return users
        
        except FileNotFoundError:
            return users

    def hash_password(self, plain: str) -> str:
        '''
        Changes given string to a hashed password
        Returns:
            str of a hashed password
        '''
        return hashlib.sha256(plain.encode("utf-8")).hexdigest()


    def ensure_logged_in(self):
        '''
        Checks if there is a user logged in
        Raises:
            IllegalAccessException if no user is logged in
        '''
        if not self.logged_in:
            raise IllegalAccessException()


    def ensure_current_blog(self):
        '''
        Checks is there is a current blog
        Raises:
            NoCurrentBlogException if no current blog
        '''
        if self.current_blog is None:
            raise NoCurrentBlogException()


    def login(self, given_username: str, given_password: str) -> bool:
        """
        Determines if the two given arguments of given_username and given_password 
        matches the actual username and password.
        Raises: 
            DuplicateLoginException if user already logged in
            InvalidLoginException if username/password are incorrect
        Returns:
            True on sucessful loging
        """
        if self.logged_in:
            raise DuplicateLoginException()

        # check if username is valid
        if given_username not in self.users:
            raise InvalidLoginException()

        # check if password hash is valid
        hashed_password = self.hash_password(given_password)
        if hashed_password != self.users[given_username]:
            raise InvalidLoginException()

        self.logged_in = True
        self.current_user = given_username

        return True


    def logout(self) -> bool:
        """
        Logout user if the user is logged in
        Raises:
            InvalidLogoutException if no user is logged in
        Returns:
            True if logout was successful
        """
        if not self.logged_in:
            raise InvalidLogoutException()
        
        self.logged_in = False
        self.current_user = None
        self.current_blog = None

        return True


    def search_blog(self, blog_id: int):
        """
        Search if the blog exist from the given id
        Raises:
            IllegalAccessException if not logged in
        Returns:
            Blog if found, otherwise None
        """
        self.ensure_logged_in()
        return self.blog_dao.search_blog(blog_id)


    def create_blog(self, blog_id: int, name: str, url: str, email: str):
        """
        Create a new blog from the given Blog class parameters.
        Raises:
            IllegalOperationException if blog with given ID already exists
        Returns:
         The created blog.
        """
        self.ensure_logged_in()

        return self.blog_dao.create_blog(blog_id, name, url, email)


    def retrieve_blogs(self, search: str):
        """
        Search filter from the given search name.
        Raises:
            IllegalAccessException if not logged in
        Returns:
            A list of blogs that have the given search in their names.
        """
        self.ensure_logged_in()

        return self.blog_dao.retrieve_blogs(search)


    def update_blog(self, blog_id: int, new_id: int, new_name: str, new_url: str, new_email: str) -> bool:
        """
        Update blogs from the given requested changes.
        Raises:
            IllegalAccessException if not logged in
            IllegalOperationException if:
                - blog id does not exist
                - the blog is the current blog
                - new id conflicts with another existing blog
        Returns:
            True upon a successful update.
        """

        #check if user is logged in
        self.ensure_logged_in()

        if self.current_blog is self.blog_dao.search_blog(blog_id):
            raise IllegalOperationException()

        return self.blog_dao.update_blog(blog_id, new_id, new_name, new_url, new_email)


    def delete_blog(self, blog_id: int) -> bool:
        """
        Delete the given blog from blog_id
        Raises:
            IllegalAccessException if not logged in
            IllegalOperationException if:
                - there are no blogs at all
                - blog id does not exist
                - blog id is the current blog
        Returns: 
            True if deletion was successful.
        """
        self.ensure_logged_in()
            
        if self.current_blog is self.blog_dao.search_blog(blog_id):
            raise IllegalOperationException()

        return self.blog_dao.delete_blog(blog_id)


    def list_blogs(self):
        """
        List all blogs in the system
        Raises:
            IllegalAccessException if not logged in
        Returns: 
            list[Blog] - a list of Blog objects
        """
        self.ensure_logged_in()
            
        return self.blog_dao.list_blogs()

    
    def set_current_blog(self, blog_id: int) -> bool:
        """
        Set the current blog by its ID
        Raises:
            IllegalAccessOperation if not logged in
            IllegalOperationException if blog does not exist
        Returns: 
            True if blog exists and was set as current, False otherwise
        """
        self.ensure_logged_in()

        blog = self.blog_dao.search_blog(blog_id)
        if blog is None:
            raise IllegalOperationException()

        self.current_blog = blog
        return True


    def unset_current_blog(self) -> bool:
        """
        Unset the blog that is currently selected
        Raises:
            IllegalAccessOperation if not logged in
        Returns: 
            True if a current blog was set and has been unset,
            False otherwise
        """
        self.ensure_logged_in()
        
        if self.current_blog is None:
            return False

        self.current_blog = None
        return True


    def get_current_blog(self):
        """
        Gets the current blog.
        Raises:
            IllegalAccessOperation if not logged in
        Returns: 
        Current blog, otherwise None if user is not logged in
        """

        self.ensure_logged_in()

        return self.current_blog


    def create_post(self, title: str, text: str):
        """
        Creates a new post in the current blog
        Raises:
            IllegalAccessOperation if not logged in
            NoCurrentBlogException if there is no current blog
        Returns: 
            Post if successful, None otherwise
        """
        self.ensure_logged_in()
        self.ensure_current_blog()

        return self.current_blog.create_post(title, text)


    def retrieve_posts(self, search: str):
        """
        Retrieves posts from current blog whose title or text
        contain search string.
        Raises:
            IllegalAccessOperation if not logged in
            NoCurrentBlogException if there is no current blog
        Returns: 
            A list of Post objects if successful, None 
            otherwise
        """
        self.ensure_logged_in()
        self.ensure_current_blog()

        return self.current_blog.search_posts(search)


    def update_post(self, code: int, new_title: str, new_text: str) -> bool:
        """
        Updates an existing Post by its code in the current blog
        Raises:
            IllegalAccessOperation if not logged in
            NoCurrentBlogException if there is no current blog
        Returns: 
            True if updated, False otherwise
        """
        self.ensure_logged_in()
        self.ensure_current_blog()

        return self.current_blog.update_post(code, new_title, new_text)


    def delete_post(self, code: int) -> bool:
        """
        Deletes an existing post by its code in the current blog.
        Raises:
            IllegalAccessOperation if not logged in
            NoCurrentBlogException if there is no current blog
        Returns: 
            True if deleted, False otherwise
        """
        self.ensure_logged_in()
        self.ensure_current_blog()

        return self.current_blog.delete_post(code)


    def search_post(self, code: int):
        """
        Searches for a post by code in the current blog.
        Raises:
            IllegalAccessException if not logged in
            NoCurrentBlogException if there is no current blog
        Returns: 
            Post if found, otherwise None
        """
        self.ensure_logged_in()
        self.ensure_current_blog()

        #return self.current_blog.posts.get(code)
        return self.current_blog.search_post(code)


    def list_posts(self):
        """
        Lists all posts from the current blog from
        last created to first created.
        Raises:
            IllegalAccessOperation if not logged in
            NoCurrentBlogException if there is no current blog
        Returns: 
            list[Post]
        """
        self.ensure_logged_in()
        self.ensure_current_blog()

        return self.current_blog.list_posts()