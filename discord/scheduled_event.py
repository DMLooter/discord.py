"""
The MIT License (MIT)

Copyright (c) 2015-present DMLooter

Permission is hereby granted, free of charge, to any person obtaining a
copy of this software and associated documentation files (the "Software"),
to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense,
and/or sell copies of the Software, and to permit persons to whom the
Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
DEALINGS IN THE SOFTWARE.
"""

from __future__ import annotations
from typing import Any, Iterator, List, Optional, TYPE_CHECKING, Tuple

from . import utils
from .utils import MISSING
from .asset import Asset, AssetMixin
from .utils import SnowflakeList, snowflake_time, MISSING
from .enums import ScheduledEventStatus, ScheduledEventEntityType, try_enum
from .user import User

__all__ = (
    'ScheduledEvent',
)

if TYPE_CHECKING:
    from .types.scheduled_event import ScheduledEvent as ScheduledEventPayload
    from .guild import Guild
    from .state import ConnectionState
    from .abc import Snowflake
    from .role import Role
    from datetime import datetime


class ScheduledEvent(AssetMixin):
    """Represents a custom scheduled event.

    Depending on the way this object was created, some of the attributes can
    have a value of ``None``.

    .. container:: operations

        .. describe:: x == y

            Checks if two scheduled events are the same.

        .. describe:: x != y

            Checks if two scheduled events are not the same.

        .. describe:: hash(x)

            Return the scheduled event's hash.

        .. describe:: iter(x)

            Returns an iterator of ``(field, value)`` pairs. This allows this class
            to be used as an iterable in list/dict/etc constructions.

        .. describe:: str(x)

            Returns the scheduled event rendered for discord.

    Attributes
    -----------
    name: :class:`str`
        The name of the scheduled event. (100)
    id: :class:`int`
        The scheduled event's ID.
    guild_id: :class:`int`
        The guild ID the scheduled event belongs to.
    channel_id: Optional[:class:`int`]
        The channel ID that this event will be hosted in. (bust be null if :attr:`entity_type` is EXTERNAL)
    creator_id: Optional[:class:`int`]
        The ID of the user that created this event
    description: :class:`str`
        The description of the Scheduled Event. (1000)
    scheduled_start_time: :class:`datetime.datetime`
        An aware datetime object that specifies the date and time in UTC that the event will start at.
    scheduled_end_time: Optional[:class:`datetime.datetime`]
        An aware datetime object that specifies the date and time in UTC that the event will end at.
        Required if :attr:`entity_type` is EXTERNAL.
    privacy_level: :class:`int`
        The privacy level of the event
    status: :class:`ScheduledEventStatus`
        The status of the event
    entity_type: :class:`ScheduledEventEntityType`
        The type of the event
    location: :class:`Optional[:class:`str`]`
        The location of the event if external
    user_count: :class:`int`
        The number of users who have RSVPed to the event
    image: :class:`str`
        The hash of the event's cover image
    creator: Optional[:class:`User`]
        The user that created the scheduled event. This can only be retrieved using :meth:`Guild.fetch_scheduled_event` and
        having the :attr:`~Permissions.manage_scheduled_events` permission.
    """

    __slots__: Tuple[str, ...] = (
        'id',
        'name',
        'guild_id',
        '_state',
        'channel_id',
        'creator_id',
        'description',
        'scheduled_start_time',
        'scheduled_end_time',
        'privacy_level',
        'status',
        'entity_type',
        'location',
        'user_count',
        'image',
        'creator',
    )

    def __init__(self, *, guild: Guild, state: ConnectionState, data: ScheduledEventPayload):
        self.guild_id: int = guild.id
        self._state: ConnectionState = state
        self._from_data(data)

    def _from_data(self, scheduled_event: ScheduledEventPayload):
        self.id: int = int(scheduled_event['id'])  # type: ignore
        self.name: str = scheduled_event['name']  # type: ignore
        self.guild_id: int = int(scheduled_event['guild_id'])

        channel = scheduled_event['channel_id']
        self.channel_id: int = int(channel) if channel else None

        self.creator_id: int = scheduled_event.get('creator_id', 0)
        self.description: str = scheduled_event['description']
        self.scheduled_start_time: datetime.datetime = utils.parse_time(scheduled_event['scheduled_start_time'])
        self.scheduled_end_time: datetime.datetime = utils.parse_time(scheduled_event['scheduled_end_time'])
        self.privacy_level: int = int(scheduled_event['privacy_level'])
        self.status: ScheduledEventStatus = try_enum(ScheduledEventStatus, scheduled_event['status'])
        self.entity_type: ScheduledEventEntityType = try_enum(ScheduledEventEntityType, scheduled_event['entity_type'])

        metadata = scheduled_event['entity_metadata']
        self.location: Optional[str] = metadata.get('location', None) if metadata else None
        self.user_count: int = int(scheduled_event.get('user_count', 0))
        self.image: str = scheduled_event['image']
        user = scheduled_event.get('creator')
        self.creator: Optional[User] = User(state=self._state, data=user) if user else None

    def _to_partial(self) -> PartialScheduledEvent:
        return PartialScheduledEvent(name=self.name, id=self.id)

    def __iter__(self) -> Iterator[Tuple[str, Any]]:
        for attr in self.__slots__:
            if attr[0] != '_':
                value = getattr(self, attr, None)
                if value is not None:
                    yield (attr, value)

    def __str__(self) -> str:
        return f'<:{self.name}:{self.id}:{self.description}:{self.location}/{self.channel_id}>'

    def __repr__(self) -> str:
        return f'<ScheduledEvent id={self.id} name={self.name!r}>'

    def __eq__(self, other: Any) -> bool:
        return isinstance(other, _ScheduledEventTag) and self.id == other.id

    def __ne__(self, other: Any) -> bool:
        return not self.__eq__(other)

    def __hash__(self) -> int:
        return self.id >> 22

    @property
    def created_at(self) -> datetime:
        """:class:`datetime.datetime`: Returns the scheduled_event's creation time in UTC."""
        return snowflake_time(self.id)

    @property
    def guild(self) -> Guild:
        """:class:`Guild`: The guild this scheduled event belongs to."""
        return self._state._get_guild(self.guild_id)

    async def delete(self, *, reason: Optional[str] = None) -> None:
        """|coro|

        Deletes the scheduled event.

        You must have :attr:`~Permissions.manage_scheduled_events` permission to
        do this.

        Parameters
        -----------
        reason: Optional[:class:`str`]
            The reason for deleting this scheduled_event. Shows up on the audit log.

        Raises
        -------
        Forbidden
            You are not allowed to delete scheduled_events.
        HTTPException
            An error occurred deleting the schedueld_event.
        """

        await self._state.http.delete_scheduled_event(self.guild.id, self.id, reason=reason)

    async def edit(self, *, name: str = MISSING, roles: List[Snowflake] = MISSING, reason: Optional[str] = None) -> Emoji:
        r"""|coro|

        Edits the custom emoji.

        You must have :attr:`~Permissions.manage_emojis` permission to
        do this.

        .. versionchanged:: 2.0
            The newly updated emoji is returned.

        Parameters
        -----------
        name: :class:`str`
            The new emoji name.
        roles: Optional[List[:class:`~discord.abc.Snowflake`]]
            A list of roles that can use this emoji. An empty list can be passed to make it available to everyone.
        reason: Optional[:class:`str`]
            The reason for editing this emoji. Shows up on the audit log.

        Raises
        -------
        Forbidden
            You are not allowed to edit emojis.
        HTTPException
            An error occurred editing the emoji.

        Returns
        --------
        :class:`Emoji`
            The newly updated emoji.
        """

        payload = {}
        if name is not MISSING:
            payload['name'] = name
        if roles is not MISSING:
            payload['roles'] = [role.id for role in roles]

        data = await self._state.http.edit_custom_emoji(self.guild.id, self.id, payload=payload, reason=reason)
        return Emoji(guild=self.guild, data=data, state=self._state)
