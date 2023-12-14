import os
from dotenv import load_dotenv
# import subprocess

from main import app 

load_dotenv()

# print("Generating requirements.txt...")
# subprocess.run("pip freeze > requirements.txt", shell=True)
# print("Requirements file generated.")

PORT = int(os.getenv("PORT", default=10010))

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=PORT) 
