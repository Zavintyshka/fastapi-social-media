from fastapi import HTTPException, status

__all__ = ["UserNotFoundLoginException", "UserNotFoundException", "WrongPasswordException",
           "EmptyListOfPostsException", "EmptyListOfUsersException", "PostNotFoundException",
           "DeletePostException", "UpdatePostException", "UserAlreadyVotedException",
           "LikeNotExistingPostException", "UserAlreadyExistsException"]


class UserNotFoundLoginException(HTTPException):
    def __init__(self, user_email: str):
        super().__init__(status_code=status.HTTP_403_FORBIDDEN, detail=f"User with email {user_email} not found")


class UserNotFoundException(HTTPException):
    def __init__(self, user_id: int):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id: {user_id} not found")


class WrongPasswordException(HTTPException):
    def __init__(self):
        super().__init__(status_code=status.HTTP_403_FORBIDDEN, detail="Wrong password")


class EmptyListOfPostsException(HTTPException):
    def __init__(self):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail="Empty list of posts")


class EmptyListOfUsersException(HTTPException):
    def __init__(self):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail="Empty list of users")


class PostNotFoundException(HTTPException):
    def __init__(self, post_id: int):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {post_id} was not found")


class DeletePostException(HTTPException):
    def __init__(self):
        super().__init__(status_code=status.HTTP_403_FORBIDDEN, detail="You can't delete someone's post")


class UpdatePostException(HTTPException):
    def __init__(self):
        super().__init__(status_code=status.HTTP_403_FORBIDDEN, detail=F"You can't update someone's post")


class UserAlreadyVotedException(HTTPException):
    def __init__(self, user_id: int, post_id: int):
        super().__init__(status_code=status.HTTP_409_CONFLICT,
                         detail=f"User with id: {user_id} already vote on post with id: {post_id}")


class LikeNotExistingPostException(HTTPException):
    def __init__(self, user_id: int, post_id: int):
        super().__init__(status_code=status.HTTP_409_CONFLICT,
                         detail=f"User with id: {user_id} can't vote on post with id: {post_id} because it already"
                                f"has like")


class UserAlreadyExistsException(HTTPException):
    def __init__(self, user_email):
        super().__init__(status_code=status.HTTP_409_CONFLICT, detail=f"User with email: {user_email} already exists")
