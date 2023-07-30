'''
front-end send json:
{
    "command" : "fetch_messages"
}
or
{
    "command" : "new_message",
    "message_type" : "text",
    "text" : "hello there..",
    "reply_id" : 1 (if it's not a reply send 0)
}
or
{
    "command" : "new_message",
    "message_type" : "image",
    "image" : "....",
    "reply_id" : 1
}
or
{
    "command" : "new_message",
    "message_type" : "voice_record",
    "voice_record" : "....",
    "reply_id" : 1
}
or
{
    "command" : "add_reaction",
    "message_id" : "1",
    "reaction_id" : "1"
}
'''

import re
from channels.db import database_sync_to_async
from accounts.models import CustomUser

# user object
def get_user_from_scope(scope):
    # get id from headers
    id_string = scope['headers'][6][1]
    s = id_string.decode('utf-8')
    match = re.search(r'\d+',s)
    id = int(match.group())
    print('id: ', id)
    
    # get the user object
    user = CustomUser.objects.filter(id=id).first()
    if user is None:
        print('Wrong user id')
    return user
    
def get_url_from_scope(scope):
    server = scope['server']
    domain = server[0]
    port = server[1]
    url = f'http://{domain}:{port}'
    return url

# json
async def json_list(queryset, url):
    result = []
    async for message in queryset:
        result.append(await database_sync_to_async(message_to_json)(message, url))
    return result


def message_to_json(message, url):
    voice_record_url = None
    if message.voice_record and message.voice_record.url:
        voice_record_url = message.voice_record.url
    
    image_url = None
    if message.image:
        image_url = url + message.image.url
        
    return{
        "id": message.id,
        "author_id": message.author.id,
        "text": message.text,
        "image": image_url,
        "voice_record": voice_record_url,
        "reaction": message.reaction,
        "reply_id": message.reply_id,
        "created_at": str(message.created_at),
        "updated_at": str(message.updated_at),
        "chat": message.chat.id
    }
