#!/usr/bin/env python3

"""
Example: Advanced QUERY method usage with complex filtering.

This example demonstrates the power of the QUERY method for complex data filtering
and field selection, similar to GraphQL but using standard HTTP.
"""

from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Optional, Dict, Any

app = FastAPI()


# Sample data structure
sample_data = [
    {
        "id": 1,
        "name": "Math Course",
        "description": "Advanced mathematics",
        "instructor": {
            "id": 101,
            "name": "Dr. Smith",
            "email": "smith@university.edu",
            "bio": "Mathematics professor with 20 years experience"
        },
        "topics": [
            {
                "id": 1,
                "title": "Algebra",
                "difficulty": "intermediate",
                "lessons": 15,
                "exercises": [
                    {"id": 1, "title": "Linear Equations", "points": 10},
                    {"id": 2, "title": "Quadratic Equations", "points": 15}
                ]
            },
            {
                "id": 2,
                "title": "Calculus",
                "difficulty": "advanced",
                "lessons": 20,
                "exercises": [
                    {"id": 3, "title": "Derivatives", "points": 20},
                    {"id": 4, "title": "Integrals", "points": 25}
                ]
            }
        ],
        "tags": ["mathematics", "algebra", "calculus"],
        "rating": 4.8,
        "enrolled_students": 245
    },
    {
        "id": 2,
        "name": "Physics Course",
        "description": "Quantum physics fundamentals",
        "instructor": {
            "id": 102,
            "name": "Dr. Johnson",
            "email": "johnson@university.edu",
            "bio": "Physics professor specializing in quantum mechanics"
        },
        "topics": [
            {
                "id": 3,
                "title": "Quantum Mechanics",
                "difficulty": "advanced",
                "lessons": 25,
                "exercises": [
                    {"id": 5, "title": "Wave Functions", "points": 30},
                    {"id": 6, "title": "Uncertainty Principle", "points": 35}
                ]
            }
        ],
        "tags": ["physics", "quantum", "mechanics"],
        "rating": 4.9,
        "enrolled_students": 156
    }
]


class FieldSelector(BaseModel):
    """Define which fields to include in the response."""
    course_fields: Optional[List[str]] = None
    instructor_fields: Optional[List[str]] = None
    topic_fields: Optional[List[str]] = None
    exercise_fields: Optional[List[str]] = None


class QueryFilter(BaseModel):
    """Define filters for the query."""
    min_rating: Optional[float] = None
    max_rating: Optional[float] = None
    difficulty: Optional[str] = None
    tags: Optional[List[str]] = None
    instructor_name: Optional[str] = None


class CourseQuery(BaseModel):
    """Complete query schema for course data."""
    fields: Optional[FieldSelector] = None
    filters: Optional[QueryFilter] = None
    limit: Optional[int] = 10
    offset: Optional[int] = 0


def filter_object(obj: Dict[str, Any], allowed_fields: Optional[List[str]] = None) -> Dict[str, Any]:
    """Filter an object to only include specified fields."""
    if allowed_fields is None:
        return obj
    return {field: obj.get(field) for field in allowed_fields if field in obj}


def apply_filters(data: List[Dict], filters: Optional[QueryFilter]) -> List[Dict]:
    """Apply filters to the data."""
    if not filters:
        return data
    
    filtered_data = data.copy()
    
    if filters.min_rating is not None:
        filtered_data = [item for item in filtered_data if item.get("rating", 0) >= filters.min_rating]
    
    if filters.max_rating is not None:
        filtered_data = [item for item in filtered_data if item.get("rating", 0) <= filters.max_rating]
    
    if filters.difficulty:
        filtered_data = [
            item for item in filtered_data 
            if any(topic.get("difficulty") == filters.difficulty for topic in item.get("topics", []))
        ]
    
    if filters.tags:
        filtered_data = [
            item for item in filtered_data 
            if any(tag in item.get("tags", []) for tag in filters.tags)
        ]
    
    if filters.instructor_name:
        filtered_data = [
            item for item in filtered_data 
            if filters.instructor_name.lower() in item.get("instructor", {}).get("name", "").lower()
        ]
    
    return filtered_data


def apply_field_selection(data: List[Dict], fields: Optional[FieldSelector]) -> List[Dict]:
    """Apply field selection to shape the response."""
    if not fields:
        return data
    
    result = []
    for item in data:
        filtered_item = filter_object(item, fields.course_fields)
        
        # Filter instructor fields
        if "instructor" in item and fields.instructor_fields:
            filtered_item["instructor"] = filter_object(item["instructor"], fields.instructor_fields)
        
        # Filter topic fields
        if "topics" in item and fields.topic_fields:
            filtered_topics = []
            for topic in item["topics"]:
                filtered_topic = filter_object(topic, fields.topic_fields)
                
                # Filter exercise fields if requested
                if "exercises" in topic and fields.exercise_fields:
                    filtered_topic["exercises"] = [
                        filter_object(exercise, fields.exercise_fields)
                        for exercise in topic["exercises"]
                    ]
                
                filtered_topics.append(filtered_topic)
            filtered_item["topics"] = filtered_topics
        
        result.append(filtered_item)
    
    return result


@app.query("/courses/search")
def query_courses(query: CourseQuery):
    """
    Query courses with complex filtering and field selection.
    
    This endpoint demonstrates the power of the QUERY method:
    - Send complex query parameters in the request body
    - Filter data based on multiple criteria
    - Select only the fields you need (like GraphQL)
    - Avoid URL length limitations
    
    Example query:
    {
        "fields": {
            "course_fields": ["id", "name", "rating"],
            "instructor_fields": ["name", "email"],
            "topic_fields": ["title", "difficulty"]
        },
        "filters": {
            "min_rating": 4.5,
            "difficulty": "advanced",
            "tags": ["mathematics"]
        },
        "limit": 5
    }
    """
    # Start with all data
    filtered_data = sample_data.copy()
    
    # Apply filters
    if query.filters:
        filtered_data = apply_filters(filtered_data, query.filters)
    
    # Apply pagination
    offset = query.offset or 0
    limit = query.limit or 10
    paginated_data = filtered_data[offset:offset + limit]
    
    # Apply field selection
    if query.fields:
        paginated_data = apply_field_selection(paginated_data, query.fields)
    
    return {
        "query": query.model_dump(),
        "total_results": len(filtered_data),
        "returned_results": len(paginated_data),
        "offset": offset,
        "limit": limit,
        "data": paginated_data
    }


@app.get("/")
def read_root():
    """Instructions for using the QUERY endpoint."""
    return {
        "message": "Advanced QUERY Method Example",
        "query_endpoint": "/courses/search",
        "method": "QUERY",
        "description": "Use the QUERY method to send complex filtering and field selection parameters",
        "example_query": {
            "fields": {
                "course_fields": ["id", "name", "rating"],
                "instructor_fields": ["name"],
                "topic_fields": ["title", "difficulty"]
            },
            "filters": {
                "min_rating": 4.5,
                "tags": ["mathematics"]
            },
            "limit": 5
        }
    }
