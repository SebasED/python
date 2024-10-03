import datetime
from pydantic import BaseModel, Field


class Movie(BaseModel):
    id: int
    title: str
    overview: str
    year: int
    rating: float
    category: str


class MovieCreate(BaseModel):
    id: int
    title: str = Field(min_length=5, max_length=15)
    overview: str = Field(min_length=15, max_length=50)
    year: int = Field(le=datetime.date.today().year, ge=1900)
    rating: float = Field(ge=0, le=10, default=10)
    category: str = Field(min_length=5, max_length=20)

    model_config = {
        'json_schema_extra': {
            'example':{
                'id': 1,
                'title': 'My movie',
                'overview': 'This movie is about ...',
                'year': 2022,
                'rating': 5,
                'category' : 'Action'
            }
        }
    }

    # @validator('title')
    # def validate_title(cls, value):
    #     if len(value) < 5:
    #         raise ValueError('Title field hava a minimun length of 5 characters')
    #     if len(value) > 15:
    #         raise ValueError('Title field hava a maximun length of 5 characters')
    #     return value


class MovieUpdate(BaseModel):
    title: str
    overview: str
    year: int
    rating: float
    category: str