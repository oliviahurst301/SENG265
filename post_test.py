import unittest
from blogging.post import Post

class PostTest(unittest.TestCase):

    def test_equality(self):
        """
        Unittest for __eq__ for Post class
        """
        post1 = Post(1, "Hello", "World")
        post2 = Post(1, "Hello", "World")
        post3 = Post(2, "Bye", "World")

        self.assertTrue(post1 == post2, "these posts are equal")

        self.assertFalse(post1 == post3, "these posts are not equal")

        self.assertTrue(post1 != post3, "these posts are indeed not equal")


    def test_str(self):
        """
        Unittest for __str__ for Post class
        """
        post = Post(1, "Hello", "World")
        result = str(post)
        
        self.assertIn("Hello", result)

        self.assertIn("World", result)

        self.assertIn("1", result)

    
    def test_repr(self):
        """
        Unittest for __repr__ for Post class
        """
        post = Post(1, "Hello", "World")
        result = repr(post)

        self.assertIn("Post", result)

        self.assertIn("1", result)

        self.assertIn("Hello", result)


if __name__ == '__main__':
    unittest.main()