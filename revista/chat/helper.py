'''
front-end send json:
{
    "command" : "fetch_messages"
}
or
{
    "command" : "new_message",
    "message_type" : "text",
    "text" : "hello there.."
}
or
{
    "command" : "new_message",
    "message_type" : "image",
    "image" : "...."
}
'''

import re
from channels.db import database_sync_to_async
from accounts.models import CustomUser

# user object
def get_user_from_scope(scope):
        # get id from headers
        id_string = scope['headers'][4][1]
        s = id_string.decode('utf-8')
        match = re.search(r'\d+',s)
        id = int(match.group())
        
        # get the user object
        user = CustomUser.objects.filter(id=id).first()
        return user
    
# json
async def json_list(queryset):
        result = []
        async for message in queryset:
            result.append(await database_sync_to_async(message_to_json)(message))
        return result

def message_to_json(message):
    voice_record_url = None
    if message.voice_record and message.voice_record.url:
        voice_record_url = message.voice_record.url
    
    image_url = None
    if message.image:
        image_url = message.image.url
        
    return{
        "id": message.id,
        "author_id": message.author.id,
        "text": message.text,
        "reaction": message.reaction,
        "image": image_url,
        "voice_record": voice_record_url,
        "created_at": str(message.created_at),
        "updated_at": str(message.updated_at),
        "chat": message.chat.id
    }