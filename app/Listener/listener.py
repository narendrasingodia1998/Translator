import aiofiles
from app.manager.translator import Google,Rapid,Lacto

async def read_file():
    async with aiofiles.open('performance_log.txt', mode='r') as f:
        contents = await f.read()
        contents = contents.split('/n')
        Google.success,Google.failure = eval(contents[0])
        Rapid.success,Rapid.failure = eval(contents[1])
        Lacto.success,Lacto.failure = eval(contents[2])

async def write_file():
    async with aiofiles.open('performance_log.txt', mode='w') as f:
        await f.write(str((Google.success,Google.failure))+'/n')
        await f.write(str((Rapid.success,Rapid.failure))+'/n')
        await f.write(str((Lacto.success,Lacto.failure))+'/n')