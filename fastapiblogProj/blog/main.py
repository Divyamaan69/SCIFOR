# from fastapi import FastAPI, Form
# from pydantic import BaseModel
# from typing import List

# app = FastAPI()

# # Data model for a blog post
# class BlogPost(BaseModel):
#     title: str
#     content: str

# # In-memory storage for blog posts
# blog_posts = []

# # Route to get all blog posts
# @app.get("/posts", response_model=List[BlogPost])
# def get_posts():
#     return blog_posts

# # Route to create a new blog post
# @app.post("/posts")
# def create_post(title: str = Form(...), content: str = Form(...)):
#     new_post = BlogPost(title=title, content=content)
#     blog_posts.append(new_post)
#     return {"message": "Blog post created successfully"}

from fastapi import FastAPI, Form, Request
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from typing import List

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# Data model for a blog post
class BlogPost(BaseModel):
    title: str
    content: str

# In-memory storage for blog posts
blog_posts = []

# Display all blog posts on the homepage
@app.get("/")
def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "posts": blog_posts})

# Add a new blog post
@app.post("/posts")
def create_post(title: str = Form(...), content: str = Form(...)):
    new_post = BlogPost(title=title, content=content)
    blog_posts.append(new_post)
    return {"message": "Blog post created successfully"}
