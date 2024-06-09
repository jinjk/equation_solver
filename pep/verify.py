import os
from img_ocr import read_img_by_index
import save_ocr_to_els as els

with els.create_client() as client:
    for i in range(1, 133):
        jsonFile = f"ocr_res/cropped_{i}.json"
        if not os.path.exists(jsonFile):
            read_img_by_index(i)
            els.save_json_to_els(client, i)

