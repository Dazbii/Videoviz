# Videoviz 
Creates art from video files.

Inspired by companies such as [MoviePalette](https://moviepalette.com/), [The Colors of Motion](https://thecolorsofmotion.com/), and [Frome](https://www.frome.co/)

## Requirements 🛒
- Python 3.12

## Usage ▶️
1. Clone the repository
2. Place the video files you would like to convert into the `Videoviz/videos/` folder that came with the repository
3. Open a console window in the root folder of this repository
4. Create a python virtual environment by running `python -m venv venv` (or replace `python` with the appropiate version if you have multiple)
5. Activate this virtual environment by running the appropiate command for your system
   - Windows (CMD): `venv\Scripts\activate.bat`
   - Windows (Powershell): `venv\Scripts\Activate.ps1`
   - Mac/Linux: `source venv/bin/activate`
6. Install the python requirements for this project by running `pip install -r requirements.txt`
7. Run the program by running `python main.py run`
8. Sit back and wait, this will take a while. You should see a window pop up displaying the video as the program calculates the averages for the video. The terminal should also display the progress on the current file and the framerate at which it is processing the file.
9. Check in the `Videoviz/output/` folder for the resulting images from the software

## Examples 🖼️
Some examples of this program being run on Studio Ghibli's Princess Mononoke:

<img src=./examples/trimmedAverage-lines.jpg alt="Lines generated from trimmed average" width=360> <img src=./examples/average-topLeftRadial.jpg alt="Top left radial generated from average" width=360>

## Advanced Usage 🔧
While running `python main.py run` should be all that is needed for most cases, there are additional controls accessible through the CLI.

You can choose to run the two parts of this program seperately if you wish. This can be done by calling `python main.py average` or `python main.py generate`. Both of these have their own sets of options, however any of these options can also be given to the regular `python main.py run` command and they will be passed to their appropiate part.

### Average
The first step of the program. It will go through the video files given to it in the `Videoviz/videos/` directory and take average colors of the frames of the video, storing them in a .csv in the `Videoviz/csvs/` directory for now. There are several algorithms that is uses for this:
- **average**: Simply takes an average of all pixels of the frame. Tends to produce more muted colors
- **trimmed average**: Averages all pixels on the frame, then throws away pixels that are far from the average and recalculates the average without them. Produces more vibrant colors than the regular average
- **k means**: Uses a [k-means clustering algorithm](https://en.wikipedia.org/wiki/K-means_clustering) to determine the 3 dominant colors of the frame, and saves the most prevalent of the three. Tends to produce even more vibrant colors than trimmed average, but dominant colors can flip rapidly, leading to images that appear less smooth than the averages

#### Options:
`--targetFile`
- Can be specified to only process a single file in `Videoviz/videos/`

`--noshowVideo`
- Can be specified to hide the video previews that are normally shown

`--skip`
- Can be specified to change the number of frames Videoviz will skip between frames that it processes

`--algorithm`
- Can be specified to turn on or off specific any of the three algorithms

`--kmeansParameters`
- Can be specified to tweak the internal parameters of the k-means clustering algorithm

### Generate
The second step of the program. It reads the .csv files from `Videoviz/csvs/` that were produced by the average step, and produces images from them, saving them in `Videoviz/output/`. There are several types of images it produces:
- **Lines**: Horizontal lines, from the start of the movie at the top to the end at the bottom
   - <img src=./examples/linesExample.jpg width=128> 
- **Starburst**: Straight lines radiating out from the center, the movie starts at 12 o clock and proceeds clockwise in a circle
   - <img src=./examples/starburstExample.jpg width=128> 
- **Top Left Starburst**: Straight lines radiating out from the top left, the movie starts at the top and proceeds in a 90 degree arc to end at the left side of the image
   - <img src=./examples/TLstarburstExample.jpg width=128> 
- **Radial**: Circles expanding out from the center, the movie starts in a dot in the center and ends in the corners of the image
   - <img src=./examples/radialExample.jpg width=128> 
- **Top Left Radial**: Circles exanding out from the top left, the movie starts in a dot in the top left in the image and proceeds outwards in a 90 degree arc, ending in the bottom right corner of the image
   - <img src=./examples/TLradialExample.jpg width=128> 

#### Options:
`--targetFile`
- Can be specified to only process csvs that were produced from a specific file in `Videoviz/videos/`

`--imageType`
- Can be specified to only produce images in one of the six form factors
