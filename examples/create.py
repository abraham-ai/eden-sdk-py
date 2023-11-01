import os
import eden

import dotenv
dotenv.load_dotenv()

eden.api_url = os.environ['EDEN_API_URL'] or "https://api.eden.art"
eden.api_key = os.environ['EDEN_API_KEY']
eden.api_secret = os.environ['EDEN_API_SECRET']

generator_name = "create"

config = {
    "text_input": "a beautiful clearing in the forest with an alien glass orb floating in the air, high quality professional photography, nikon d850 50mm",
    "guidance_scale": 8,
    "width": 1024,
    "height": 1024,
    "n_samples": 1,
    "steps": 35,
    "upscale_f": 1.0,
}

creation = eden.tasks.run(generator_name, config)
print(creation)
eden.utils.save_creation(creation, config, "eden_creations")
