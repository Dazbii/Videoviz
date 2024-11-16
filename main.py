import fire
from generate import generate
from average import average

def run(specifiedFilename=None, showVideo=None, skip=None, algorithm=None, kmeansParameters=None, imageType=None):
    notNoneParams = {k:v for k, v in locals().items() if v is not None}
    averageParams = {k:v for k, v in notNoneParams.items() if k != "imageType"}
    generateParams = {k:v for k, v in notNoneParams.items() if k in ["specifiedFilename", "imageType"]}
    average(**averageParams)
    generate(**generateParams)

if __name__ == "__main__":
    fire.Fire({
        "run": run,
        "generate": generate,
        "average": average
    })
