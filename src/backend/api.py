from communiko import CommunikoBookworm
from app import bookworm



class Api:
    def send(name, content):
        output = name + ":" + content

        output2 = output.encode()

        bookworm.write(bookworm, output2)
        
        

    
    
    
        