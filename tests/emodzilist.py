import json
import utils.work_with_json_BETA as wwjb
EMODZI = ['😄', '😃', '😁', '😆', '😊', '☺️',
          '🤗', '👋', '✌️', '🤝', '👍', '👌',
          '💖', '😌', '😏', '😎', '🥰', '🤩',
          '🧘‍♂️', '🌿', '☕', '🐱‍👤']
for emo in EMODZI:
    print(emo)

print(wwjb.save_as_json(EMODZI,filename='emodzi.json'))
