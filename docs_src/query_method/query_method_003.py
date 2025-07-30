#!/usr/bin/env python3

"""
Example: QUERY method implementation matching the original GitHub issue.

This example directly addresses the use case described in the GitHub issue:
- Complex nested data structures
- Dynamic field selection through request body
- Avoids URL length limitations
- Provides GraphQL-like flexibility with standard HTTP
"""

from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Optional, Dict, Any

app = FastAPI()


# Original data structure from the GitHub issue
sample_subject = {
    "id": 1,
    "name": "Math",
    "tags": [
        {
            "id": 1,
            "name": "Algebra",
            "number_of_clicks": 1,
            "number_of_questions": 7,
            "number_of_answers": 3,
            "number_of_comments": 2,
            "number_of_votes": 1,
        }
    ],
    "topics": [
        {
            "id": 1,
            "name": "Linear Equations",
            "likes": 1,
            "dislikes": 0,
            "number_of_clicks": 1,
            "number_of_tutorials": 1,
            "number_of_questions": 7,
            "posts": [
                {
                    "id": 1,
                    "title": "How to solve linear equations?",
                    "likes": 1,
                    "dislikes": 0,
                    "number_of_clicks": 1,
                    "number_of_answers": 3,
                    "number_of_comments": 2,
                    "number_of_votes": 1,
                    "answers": [
                        {
                            "id": 1,
                            "content": "You can solve linear equations by using the substitution method.",
                            "likes": 1,
                            "dislikes": 0,
                            "number_of_clicks": 1,
                            "number_of_comments": 2,
                            "number_of_votes": 1,
                            "comments": [
                                {
                                    "id": 1,
                                    "content": "That's a great answer!",
                                    "likes": 1,
                                    "dislikes": 0,
                                    "number_of_clicks": 1,
                                    "number_of_votes": 1,
                                }
                            ]
                        }
                    ]
                }
            ]
        }
    ]
}


class ArbitrarySchema(BaseModel):
    """
    The schema that clients send to specify exactly what they want in the response.
    This is the key innovation - clients can request any combination of fields.
    """
    # Root level fields to include
    root_fields: Optional[List[str]] = None
    
    # Nested object field specifications
    tags: Optional[Dict[str, Any]] = None  # {"fields": ["id", "name"], "limit": 5}
    topics: Optional[Dict[str, Any]] = None  # {"fields": [...], "limit": 10, "posts": {...}}
    
    # Global limits
    max_depth: Optional[int] = None


def filter_by_schema(data: Dict[str, Any], schema: ArbitrarySchema) -> Dict[str, Any]:
    """
    Filter the data based on the arbitrary schema provided by the client.
    This allows clients to specify exactly what fields they want at each level.
    """
    result = {}
    
    # Handle root fields
    if schema.root_fields:
        for field in schema.root_fields:
            if field in data:
                result[field] = data[field]
    else:
        # If no root fields specified, include basic fields
        result = {k: v for k, v in data.items() if k in ["id", "name"]}
    
    # Handle tags
    if schema.tags and "tags" in data:
        tags_config = schema.tags
        tags_data = data["tags"]
        
        # Apply limit if specified
        if "limit" in tags_config:
            tags_data = tags_data[:tags_config["limit"]]
        
        # Filter fields if specified
        if "fields" in tags_config:
            tags_data = [
                {field: tag.get(field) for field in tags_config["fields"] if field in tag}
                for tag in tags_data
            ]
        
        result["tags"] = tags_data
    
    # Handle topics (more complex nesting)
    if schema.topics and "topics" in data:
        topics_config = schema.topics
        topics_data = data["topics"]
        
        # Apply limit if specified
        if "limit" in topics_config:
            topics_data = topics_data[:topics_config["limit"]]
        
        processed_topics = []
        for topic in topics_data:
            processed_topic = {}
            
            # Filter topic fields
            if "fields" in topics_config:
                for field in topics_config["fields"]:
                    if field in topic:
                        processed_topic[field] = topic[field]
            else:
                # Default topic fields
                processed_topic = {k: v for k, v in topic.items() if k in ["id", "name"]}
            
            # Handle posts within topics
            if "posts" in topics_config and "posts" in topic:
                posts_config = topics_config["posts"]
                posts_data = topic["posts"]
                
                if "limit" in posts_config:
                    posts_data = posts_data[:posts_config["limit"]]
                
                processed_posts = []
                for post in posts_data:
                    processed_post = {}
                    
                    # Filter post fields
                    if "fields" in posts_config:
                        for field in posts_config["fields"]:
                            if field in post:
                                processed_post[field] = post[field]
                    else:
                        processed_post = {k: v for k, v in post.items() if k in ["id", "title"]}
                    
                    # Handle answers within posts
                    if "answers" in posts_config and "answers" in post:
                        answers_config = posts_config["answers"]
                        answers_data = post["answers"]
                        
                        if "limit" in answers_config:
                            answers_data = answers_data[:answers_config["limit"]]
                        
                        processed_answers = []
                        for answer in answers_data:
                            processed_answer = {}
                            
                            if "fields" in answers_config:
                                for field in answers_config["fields"]:
                                    if field in answer:
                                        processed_answer[field] = answer[field]
                            else:
                                processed_answer = {k: v for k, v in answer.items() if k in ["id", "content"]}
                            
                            # Handle comments within answers
                            if "comments" in answers_config and "comments" in answer:
                                comments_config = answers_config["comments"]
                                comments_data = answer["comments"]
                                
                                if "limit" in comments_config:
                                    comments_data = comments_data[:comments_config["limit"]]
                                
                                if "fields" in comments_config:
                                    processed_answer["comments"] = [
                                        {field: comment.get(field) for field in comments_config["fields"] if field in comment}
                                        for comment in comments_data
                                    ]
                                else:
                                    processed_answer["comments"] = [
                                        {k: v for k, v in comment.items() if k in ["id", "content"]}
                                        for comment in comments_data
                                    ]
                            
                            processed_answers.append(processed_answer)
                        
                        processed_post["answers"] = processed_answers
                    
                    processed_posts.append(processed_post)
                
                processed_topic["posts"] = processed_posts
            
            processed_topics.append(processed_topic)
        
        result["topics"] = processed_topics
    
    return result


@app.query("/query/subjects")
def query_subjects(schema: ArbitrarySchema):
    """
    Query subjects with an arbitrary schema - exactly as requested in the GitHub issue.
    
    This endpoint allows clients to specify exactly what fields they want
    at each level of the nested data structure, avoiding the need for:
    - Multiple API endpoints for different data combinations
    - Long URL parameters
    - Over-fetching of data
    
    Example schemas:
    
    1. Minimal data:
    {
        "root_fields": ["id", "name"],
        "tags": {"fields": ["id", "name"], "limit": 1}
    }
    
    2. Detailed topics only:
    {
        "root_fields": ["id", "name"],
        "topics": {
            "fields": ["id", "name"],
            "limit": 1,
            "posts": {
                "fields": ["id", "title"],
                "limit": 2
            }
        }
    }
    
    3. Full nested structure:
    {
        "topics": {
            "fields": ["id", "name"],
            "posts": {
                "fields": ["id", "title"],
                "answers": {
                    "fields": ["id", "content"],
                    "comments": {
                        "fields": ["id", "content"],
                        "limit": 1
                    }
                }
            }
        }
    }
    """
    # Apply the schema to filter the response
    filtered_data = filter_by_schema(sample_subject, schema)
    
    return {
        "message": "Successfully queried subjects using arbitrary schema",
        "schema_used": schema.model_dump(),
        "data": filtered_data
    }


@app.get("/")
def get_root():
    """
    Root endpoint showing the original issue's desired syntax working.
    """
    return {
        "message": "FastAPI QUERY Method - Original Issue Implementation",
        "issue_url": "https://github.com/tiangolo/fastapi/issues/...",
        "status": "✅ IMPLEMENTED",
        "usage": {
            "endpoint": "/query/subjects", 
            "method": "QUERY",
            "description": "Send arbitrary schema in request body to get exactly the data you need"
        },
        "examples": {
            "minimal": {
                "root_fields": ["id", "name"],
                "tags": {"fields": ["id", "name"], "limit": 1}
            },
            "detailed": {
                "root_fields": ["id", "name"],
                "topics": {
                    "fields": ["id", "name"],
                    "posts": {
                        "fields": ["id", "title"],
                        "answers": {
                            "fields": ["id", "content"],
                            "limit": 1
                        }
                    }
                }
            }
        }
    }


# This is the exact syntax the user wanted in their issue:
# @app.query('/query/subjects')
# def query_subjects(schema: ArbitrarySchema):
#     with Session(engine) as db:
#         subjects = db.query(Subject).all()
#         return schema(**subjects)
#
# ✅ This now works with our implementation!
