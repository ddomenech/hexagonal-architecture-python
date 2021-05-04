from datetime import datetime
from typing import List

import inject
from fastapi import APIRouter, Response
from fastapi_camelcase import CamelModel
from pydantic import BaseModel

from hex.domain.actions.get_post import GetPost
from hex.domain.actions.search_posts import SearchPosts


class PostSchema(CamelModel):
    id: int
    author_name: str
    title: str
    body: str
    created_at: datetime
    updated_at: datetime


class ListPostSchema(BaseModel):
    results: List[PostSchema]
    count: int


@inject.autoparams()
def create_post_routers(search_posts: SearchPosts,
                        get_post: GetPost) -> APIRouter:
    post_router = APIRouter()

    @post_router.get('', response_model=ListPostSchema, status_code=200)
    def post_list(start_after: int = 0, end_before: int = 999999) -> Response:
        posts, count = search_posts.execute(start_after=start_after,
                                            end_before=end_before)

        post_schemas = [PostSchema(
            id=post.id, author_name=post.author_name,
            title=post.title, body=post.body,
            created_at=post.created_at, updated_at=post.updated_at
        ) for post in posts]

        return ListPostSchema(results=post_schemas, count=count).dict()

    @post_router.get('/{post_id}', response_model=PostSchema, status_code=200)
    def post_detail(post_id: int) -> Response:
        post = get_post.execute(post_id=post_id)
        serialize_post = PostSchema(
            id=post.id, author_name=post.author_name,
            title=post.title, body=post.body,
            created_at=post.created_at, updated_at=post.updated_at
        ).dict()
        return serialize_post

    return post_router
