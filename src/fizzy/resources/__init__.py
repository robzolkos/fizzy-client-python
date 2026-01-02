"""Resource classes for the Fizzy API."""

from fizzy.resources.boards import AsyncBoardsResource, BoardsResource
from fizzy.resources.cards import AsyncCardsResource, CardsResource
from fizzy.resources.columns import AsyncColumnsResource, ColumnsResource
from fizzy.resources.comments import AsyncCommentsResource, CommentsResource
from fizzy.resources.identity import AsyncIdentityResource, IdentityResource
from fizzy.resources.notifications import AsyncNotificationsResource, NotificationsResource
from fizzy.resources.reactions import AsyncReactionsResource, ReactionsResource
from fizzy.resources.steps import AsyncStepsResource, StepsResource
from fizzy.resources.tags import AsyncTagsResource, TagsResource
from fizzy.resources.uploads import AsyncUploadsResource, UploadsResource
from fizzy.resources.users import AsyncUsersResource, UsersResource

__all__ = [
    "AsyncBoardsResource",
    "AsyncCardsResource",
    "AsyncColumnsResource",
    "AsyncCommentsResource",
    "AsyncIdentityResource",
    "AsyncNotificationsResource",
    "AsyncReactionsResource",
    "AsyncStepsResource",
    "AsyncTagsResource",
    "AsyncUploadsResource",
    "AsyncUsersResource",
    "BoardsResource",
    "CardsResource",
    "ColumnsResource",
    "CommentsResource",
    "IdentityResource",
    "NotificationsResource",
    "ReactionsResource",
    "StepsResource",
    "TagsResource",
    "UploadsResource",
    "UsersResource",
]
