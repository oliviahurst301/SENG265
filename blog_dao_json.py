from blogging.blog import Blog
from blogging.dao.blog_dao import BlogDAO
from blogging.exception.illegal_operation_exception import IllegalOperationException
from blogging.configuration import Configuration
from blogging.dao.blog_encoder import BlogEncoder
from blogging.dao.blog_decoder import BlogDecoder
import json

# concrete DAO for blogs
class BlogDAOJSON(BlogDAO):
    
    # constructor
    def __init__(self):
        self.autosave = Configuration.autosave

        # check persistence
        if self.autosave:
            self.blogs = self.load_blogs()

        else:
            self.blogs = {}

    
    def load_blogs(self):
        """
        Loads blogs from blogs_file in Configuration for the constructor.
        Stored as id for key and a Blog() object for the value pair.
        Returns the loaded blogs dictionary.
        """
        blogs = {}
        try:

            # open blogs_file in the Configuration class in "read" mode
            with open(Configuration.blogs_file, 'r') as file:

                # uses BlogDecoder which was implemented in blog_decoder.py
                blogs_json = json.load(file, cls=BlogDecoder)
                
                # loop through user blogs
                for current_blog in blogs_json:
                    blogs[current_blog.id] = current_blog
                return blogs

        # exception if the files is not found
        except FileNotFoundError:
            return blogs


    def save_blogs(self):
        """
        Saves blogs into blogs.json whenever any state change occurs.
        """
        if self.autosave:

            # open blogs_file in the Configuration class in "write" mode
            with open(Configuration.blogs_file, 'w') as file:

                # uses BlogEncoder which was implemented in blog_encoder.py
                json.dump(list(self.blogs.values()), file, cls=BlogEncoder)

    
    def create_blog(self, blog_id: int, name: str, url: str, email: str):
        '''
        Create a new blog from the given Blog class parameters.
        Raises:
            IllegalOperationException if blog with given ID already exists
        Returns:
            The created blog.
        '''
        if blog_id in self.blogs:
            raise IllegalOperationException()

        blog = Blog(blog_id, name, url, email)
        self.blogs[blog_id] = blog

        self.save_blogs()
        return blog


    def search_blog(self, blog_id: int):
        '''
        Search if the blog exist from the given id
        Returns:
            Blog if found, otherwise None
        '''
        return self.blogs.get(blog_id)


    def retrieve_blogs(self, search: str) -> list[Blog]:
        '''
        Returns a list of blogs whose names contain
        the search string
        '''
        result = []
        for blog in self.blogs.values():
            if search in blog.get_name():
                result.append(blog)

        return result


    def update_blog(self, blog_id: int, new_id: int, new_name: str, new_url: str, new_email: str) -> bool:
        '''
        Update blogs from the given requested changes.
        Raises:
            IllegalOperationException if
                - blog id does not exist
                - new id conflicts with another existing blog
        Returns:
            True upon a successful update.
        '''
        if blog_id not in self.blogs:
            raise IllegalOperationException()

        if new_id in self.blogs and new_id != blog_id:
            raise IllegalOperationException()

        blog = self.blogs[blog_id]
        blog.update(new_id, new_name, new_url, new_email)

        if new_id != blog_id:
            self.blogs[new_id] = blog
            del self.blogs[blog_id]

        self.save_blogs()
        return True


    def delete_blog(self, blog_id: int) -> bool:
        '''
        Delete the given blog from blog_id
        Raises:
            IllegalOperationException if:
                - blog id does not exist
        Returns: 
            True if deletion was successful.
        '''
        if not self.blogs:
            raise IllegalOperationException()

        if blog_id not in self.blogs:
            raise IllegalOperationException()

        del self.blogs[blog_id]
        
        self.save_blogs()
        return True


    def list_blogs(self) -> list[Blog]:
        '''
        List all blogs in the system
        Returns: 
            list[Blog] - a list of Blog objects
        '''
        return list(self.blogs.values())