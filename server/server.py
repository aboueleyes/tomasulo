from flask import Flask, request, jsonify
from flask_cors import CORS
import json


from src.instructions_parser import InstructionParser
from src.buffer import BufferAreas
from src.reservation import ReservationAreas
from src.tomasulo import Tomasulo
from src.components import Memory, RegisterFile

app = Flask(__name__)
CORS(app)


json_out = lambda current_cycle: {
    "buffer": BufferAreas.get_instance().to_json(),
    "reservation": ReservationAreas.get_instance().to_json(),
    "memory": Memory.get_instance().to_json(),
    "registers": RegisterFile.get_instance().to_json(),
    "cycle": current_cycle,
}


@app.route("/api/v1/run", methods=["POST"])
def run():
    payload = request.get_json()
    instructions = payload["instructions"].split("\n")
    latencies = payload["latencies"]

    instructions_parser = InstructionParser(latencies=latencies)

    with open("./instructions.txt", "w") as file:
        file.write(payload["instructions"])

    instructions_parser.read_file(file_name="./instructions.txt")
    instructions = instructions_parser.get_instructions()

    tomo = Tomasulo(instructions=instructions)
    current_cycle = 1
    out = []

    while tomo.is_running():
        out.append(json_out(current_cycle))
        tomo.tick()
        current_cycle += 1

    out.append(json_out(current_cycle))
    tomo.reset()
    return json.dumps(out)


app.run(
    port=5000,
    debug=True,
)
