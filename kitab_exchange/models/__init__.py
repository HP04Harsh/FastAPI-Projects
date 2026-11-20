from models.user import User
from models.book import Book

# Resolve string annotations & back-references
User.model_rebuild()
Book.model_rebuild()