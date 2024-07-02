import logging
import uvicorn
from . import app

FORMAT = '%(asctime)s - %(levelname)s - %(message)s'
logging.basicConfig(level=logging.DEBUG, format=FORMAT, encoding='utf-8', handlers=[logging.FileHandler("url_uuid.log"),logging.StreamHandler()])



if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
