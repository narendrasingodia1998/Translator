from app.manager.translator import Google,Lacto,Rapid

class AutoSelectManager():
    @classmethod
    async def findserver(cls,request):
        '''
         Translate the text
         Args:
            request : dict 
         Return : dict
         '''
        google_success_rate = Google.success / Google.failure
        rapid_success_rate = Rapid.success / Rapid.failure
        lacto_success_rate = Lacto.success / Lacto.failure
        if google_success_rate >= rapid_success_rate and google_success_rate >= lacto_success_rate:
            #print("Google is selected")
            manager = Google
        elif rapid_success_rate >= google_success_rate  and rapid_success_rate >=lacto_success_rate:
            #print("Rapid is selected")
            manager = Rapid
        else:
            #print("Lacto is selected")
            manager = Lacto
        response  = await manager.translate(request)
        return response