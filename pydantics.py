from pydantic import BaseModel, ValidationError, field_validator
from content_safety import analyser

class UserModel(BaseModel):
    user_query: str
    @field_validator("user_query")
    def validate_user_query(cls, query: str) -> str:
        if not query.strip():
            return '100'
        if query.isdigit():
            return '101'
        
        allowed_chars = set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 .,!?;'\"[]%&*|\\/`–—_-")
        invalid_chars = set(query) - allowed_chars
        
        if invalid_chars:
            return '102'
        flag = None
        for c in query:
            if c.isalpha():
                flag =1
                break
        if not flag:
            return '103'
        
        analyse_object=analyser(query)
        if analyse_object['categoriesAnalysis'][0]['severity']>2 and analyse_object['categoriesAnalysis'][0]['severity']<5:
            return '200'
        if analyse_object['categoriesAnalysis'][0]['severity']>4:
            return '201'
        if analyse_object['categoriesAnalysis'][1]['severity']>2 and analyse_object['categoriesAnalysis'][1]['severity']<5:
            return '300'
        if analyse_object['categoriesAnalysis'][1]['severity']>4:
            return '301'
        if analyse_object['categoriesAnalysis'][2]['severity']>2 and analyse_object['categoriesAnalysis'][2]['severity']<5:
            return '400'
        if analyse_object['categoriesAnalysis'][2]['severity']>4:
            return '401'
        if analyse_object['categoriesAnalysis'][3]['severity']>2 and analyse_object['categoriesAnalysis'][3]['severity']<5:
            return '500'
        if analyse_object['categoriesAnalysis'][3]['severity']>4:
            return '501'
        
        return '000'

