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

from typing import Optional, TypedDict
from .snowflake import Snowflake, SnowflakeList
from .user import User

class ScheduledEventEntity(TypedDict, total=False):
    location: str

"""
channel_id 	?snowflake	the channel id in which the scheduled event will be hosted, or null if scheduled entity type is EXTERNAL
creator_id?	?snowflake	the id of the user that created the scheduled event
scheduled_end_time 	?ISO8601 timestamp	the time the scheduled event will end, required if entity_type is EXTERNAL
entity_id	?snowflake	the id of an entity associated with a guild scheduled event
entity_metadata **	?entity metadata	additional metadata for the guild scheduled event
image	?string	the cover image hash of the scheduled event

"""
#This class contains the optional parts
class PartialScheduledEvent(TypedDict):
    channel_id: Optional[Snowflake]
    creator_id: Optional[Snowflake]
    scheduled_end_time: Optional[str]
    entity_id: Optional[Snowflake]
    entity_metadata: Optional[ScheduledEventEntity]
    image: Optional[str]
    """id: Optional[Snowflake]
    name: Optional[str]"""

PrivacyLevel = Literal[2]
EventStatus = [1,2,3,4]
ScheduledEventEntityType = [1,2,3]

"""
id	             snowflake	the id of the scheduled event
guild_id	   snowflake	the guild id which the scheduled event belongs to
name	       string	the name of the scheduled event (1-100 characters)
description?	string	the description of the scheduled event (1-1000 characters)
scheduled_start_time	ISO8601 timestamp	the time the scheduled event will start
privacy_level	privacy level	the privacy level of the scheduled event
status	         event status	the status of the scheduled event
entity_type	    scheduled entity type	the type of the scheduled event
creator?	   user object	the user that created the scheduled event
user_count?	    integer	the number of users subscribed to the scheduled event
"""
#This class contains only the required parts
class ScheduledEvent(PartialEmoji, total=False):
    id: Snowflake
    guild_id: Snowflake
    name: str
    description: str
    scheduled_start_time: ISO8601 timestamp
    privacy_level: PrivacyLevel
    status: EventStatus
    entity_type: ScheduledEventEntityType
    creator: User
    user_count: int
    """
    roles: SnowflakeList
    user: User
    require_colons: bool
    managed: bool
    animated: bool
    available: bool"""

"""channel_id? *	?snowflake	the channel id of the scheduled event, set to null if changing entity type to EXTERNAL
entity_metadata?	entity metadata	the entity metadata of the scheduled event
name?	string	the name of the scheduled event
privacy_level?	privacy level	the privacy level of the scheduled event
scheduled_start_time?	ISO8601 timestamp	the time to schedule the scheduled event
scheduled_end_time? *	ISO8601 timestamp	the time when the scheduled event is scheduled to end
description?	string	the description of the scheduled event
entity_type? *	event entity type	the entity type of the scheduled event
status?	event status	the status of the scheduled event
image?	image data	the cover image of the scheduled event
"""
#This contains the fields needed to edit the event
class EditScheduledEvent(TypedDict):
    channel_id: Optional[Snowflake]
    name: str
    privacy_level: PrivacyLevel
    scheduled_start_time: str
    scheduled_end_time: str
    description: str
    entity_type: ScheduledEventEntityType
    status: EventStatus
    image: bytes
    """name: str
    roles: Optional[SnowflakeList]"""
