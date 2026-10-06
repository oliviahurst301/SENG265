import unittest
from blogging.blog import Blog
from blogging.post import Post

class BlogTest(unittest.TestCase):
    
    def setUp(self):
        self.blog = Blog(111, 'My Blog', 'my_blog', 'me@google.com')

    # posts created in a blog should have auto-incremented codes
    def test_create_post_auto_increment_codes(self):
        p1 = self.blog.create_post("First", "Body1")
        p2 = self.blog.create_post("Second", "Body2")
        self.assertIsInstance(p1, Post)
        self.assertIsInstance(p2, Post)
        self.assertEqual(1, p1.code)
        self.assertEqual(2, p2.code)

    # each blog has its own code
    def test_codes_are_per_blog_not_global(self):
        other = Blog(222, "Other", "other", "o@example.com")
        a = self.blog.create_post("A", "x")
        b = other.create_post("B", "y")
        self.assertEqual(1, a.code)
        self.assertEqual(1, b.code)

    # searching posts should match title or text, case-sensitive
    def test_search_posts_matches_title_or_text(self):
        self.blog.create_post("Hello World", "alpha")
        self.blog.create_post("Update", "WORLD news")
        hits = self.blog.search_posts("world")
        titles = [p.title for p in hits]
        self.assertEqual(["Hello World", "Update"], titles)

        self.assertEqual([], self.blog.search_posts("nope"))

    # updating an existing post should modify its fields and return True
    def test_update_post_changes_title_text(self):
        p = self.blog.create_post("T", "X")
        ok = self.blog.update_post(p.code, "T2", "Y")
        self.assertTrue(ok)
        self.assertEqual("T2", self.blog.posts[p.code].title)
        self.assertEqual("Y", self.blog.posts[p.code].text)
        # updating a non-existent code
        self.assertFalse(self.blog.update_post(999, "no", "no"))

    # deleting a post should remove it and return True
    def test_delete_post(self):
        p = self.blog.create_post("T", "X")
        self.assertTrue(self.blog.delete_post(p.code))
        self.assertFalse(self.blog.delete_post(p.code))  # already gone
        self.assertIsNone(self.blog.posts.get(p.code))

    # list of posts should return posts in order of creation (oldest to newest)
    def test_list_posts_returns_newest_first(self):
        self.blog.create_post("1", "a")
        self.blog.create_post("2", "b")
        self.blog.create_post("3", "c")
        lst = self.blog.list_posts()
        self.assertEqual(["3", "2", "1"], [p.title for p in lst])

if __name__ == "__main__":
    unittest.main()