# Videoviz 
Creates art from video files.

Inspired by companies such as [MoviePalette](https://moviepalette.com/), [The Colors of Motion](https://thecolorsofmotion.com/), and [Frome](https://www.frome.co/)

## Requirements 🛒
- Python 3.12

## Usage ▶️
1. Clone the repository
2. Place the video files you would like to convert into the "videos" directory that came with the repository
3. Open a console window in the root directory of this repository
4. Create a python virtual environment by running `python -m venv venv` (or replace `python` with the appropiate version if you have multiple)
5. Activate this virtual environment by running the appropiate command for your system
   - Windows (CMD): `venv\Scripts\activate.bat`
   - Windows (Powershell): `venv\Scripts\Activate.ps1`
   - Mac/Linux: `source venv/bin/activate`
6. Install the python requirements for this project by running `pip install -r requirements.txt`
7. Run the program by running `python main.py run`
8. Sit back and wait, this will take a while. You should see a window pop up displaying the video as the program calculates the averages for the video. The terminal should also display the progress on the current file and the framerate at which it is processing the file.
9. Check in the "output" folder for the resulting images from the software

## Examples 🖼️
Some examples of this program being run on Studio Ghibli's Princess Mononoke:

<img src=./examples/trimmedAverage-lines.jpg alt="Lines generated from trimmed average" width=360> <img src=./examples/average-topLeftRadial.jpg alt="Top left radial generated from average" width=360>
