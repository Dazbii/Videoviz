import fire
from generate import generate
from average import average

def run():
    average()
    generate()

if __name__ == "__main__":
    fire.Fire({
        "run": run,
        "generate": generate,
        "average": average
    })
