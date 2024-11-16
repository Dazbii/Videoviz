import numpy as np
import cv2
import os

workingDirectory = os.getcwd()
csvDirectory = os.path.join(workingDirectory, "csvs")
outputDirectory = os.path.join(workingDirectory, "output")
filenames = ["average.csv", "kmeans.csv", "trimmedAverage.csv"]

def _writeLines(file, skip, width, height, outputName):
    file.seek(0)
    image = np.zeros((height, width, 3), np.uint8)
    currentHeight = 0
    i = 0

    for line in file:
        if i < skip:
            i += 1
            continue
        i = 0
        values = np.array(line.split(", ")).astype(float)
        cv2.line(
            image, (0, currentHeight), (width, currentHeight), values, 1
        )
        currentHeight += 1

    cv2.imwrite(
        outputName + "-lines.jpg", image
    )

def _writeStarburst(file, numLines, width, height, outputName):
    file.seek(0)
    image = np.zeros((height, width, 3), np.uint8)
    r = numLines
    center = (int(width / 2), int(height / 2))
    cornerDistance = np.sqrt((width/2) ** 2 +(height/2) ** 2)
    for line in file:
        values = np.array(line.split(", ")).astype(float)
        cv2.line(
            image,
            center,
            (
                center[0] + int(cornerDistance * np.sin(np.pi + 2 * np.pi * r / numLines)),
                center[1] + int(cornerDistance * np.cos(np.pi + 2 * np.pi * r / numLines)),
            ),
            values,
            1,
        )
        r -= 1

    cv2.imwrite(
        outputName + "-centeredStarburst.jpg",
        image,
    )
    image = np.zeros((height, width, 3), np.uint8)

def _writeTopLeftStarburst(file, numLines, width, height, outputName):
    file.seek(0)
    image = np.zeros((height, width, 3), np.uint8)
    r = numLines
    cornerDistance = np.sqrt(width ** 2 + height ** 2)
    for line in file:
        values = np.array(line.split(", ")).astype(float)
        cv2.line(
            image,
            (0, 0),
            (
                int(cornerDistance * np.sin(0.5 * np.pi * r / numLines)),
                int(cornerDistance * np.cos(0.5 * np.pi * r / numLines)),
            ),
            values,
            1,
        )
        r -= 1

    cv2.imwrite(
        outputName + "-topLeftStarburst.jpg",
        image,
    )
    image = np.zeros((height, width, 3), np.uint8)

def _writeRadial(file, numLines, width, height, outputName):
    file.seek(0)
    image = np.zeros((height, width, 3), np.uint8)
    r = 0
    radius = np.sqrt(height**2 + width**2) / 2
    center = (int(width / 2), int(height / 2))
    for line in file:
        values = np.array(line.split(", ")).astype(float)
        cv2.circle(
            image,
            center,
            int(radius * r / numLines),
            values,
            2,
            lineType=cv2.LINE_AA,
        )
        r += 1

    cv2.imwrite(
        outputName + "-centeredRadial.jpg",
        image,
    )
    image = np.zeros((height, width, 3), np.uint8)

def _writeTopLeftRadial(file, numLines, width, height, outputName):
    file.seek(0)
    image = np.zeros((height, width, 3), np.uint8)
    r = 0
    radius = np.sqrt(height**2 + width**2)
    for line in file:
        values = np.array(line.split(", ")).astype(float)
        cv2.circle(
            image,
            (0, 0),
            int(radius * r / numLines),
            values,
            2,
            lineType=cv2.LINE_AA,
        )
        r += 1

    cv2.imwrite(
        outputName + "-topLeftRadial.jpg",
        image,
    )

def generate(targetFile = "", imageType = ""):
    if targetFile:
        print("only generating for file: " + targetFile)

    lines = True  # Lines
    stb = True  # Starburst
    tlstb = True  # Top Left Starburst
    rad = True  # Radial
    tlrad = True  # Top Left Radial
    if imageType and imageType in ["lines", "starburst", "TLstarburst", "radial", "TLradial"]:
        lines = False
        stb = False
        tlstb = False
        rad = False
        tlrad = False
        if imageType == "lines":
            print("only generating lines images")
            lines = True
        if imageType == "starburst":
            print("only generating starburst images")
            stb = True
        if imageType == "TLstarburst":
            print("only generating top left starburst images")
            tlstb = True
        if imageType == "radial":
            print("only generating radial images")
            rad = True
        if imageType == "TLradial":
            print("only generating top left radial images")
            tlrad = True
            
    directories = [
        f for f in os.listdir(csvDirectory) if os.path.isdir(os.path.join(csvDirectory, f))
    ]

    for directory in directories:
        if targetFile and directory != os.path.splitext(targetFile)[0]:
            continue 

        readingDirectory = os.path.join(csvDirectory, directory)
        writingDirectory = os.path.join(outputDirectory, directory)
        if not os.path.exists(writingDirectory):
            os.makedirs(writingDirectory)

        for filename in filenames:
            filePath = os.path.join(readingDirectory, filename)
            outputName = os.path.join(writingDirectory, os.path.splitext(filename)[0])

            factor = 1
            tempWidth = int(5440 * factor)
            tempHeight = int(8480 * factor)

            numLines = sum(1 for line in open(filePath))
            skip = int(numLines / tempHeight - 1)

            height = int(numLines / (skip + 1))
            width = int((height / tempHeight) * tempWidth)

            with open(filePath) as file:
                if lines:
                    print("generating lines for " + os.path.splitext(filename)[0] + " of " + directory + "...")
                    _writeLines(file, skip, width, height, outputName)
                if stb:
                    print("generating starburst for " + os.path.splitext(filename)[0] + " of " + directory + "...")
                    _writeStarburst(file, numLines, width, height, outputName)
                if tlstb:
                    print("generating top left starburst for " + os.path.splitext(filename)[0] + " of " + directory + "...")
                    _writeTopLeftStarburst(file, numLines, width, height, outputName)
                if rad:
                    print("generating radial for " + os.path.splitext(filename)[0] + " of " + directory + "...")
                    _writeRadial(file, numLines, width, height, outputName)
                if tlrad:
                    print("generating top left radial for " + os.path.splitext(filename)[0] + " of " + directory + "...")
                    _writeTopLeftRadial(file, numLines, width, height, outputName)

            cv2.destroyAllWindows()
    
    print("Successfully completed generating images!")
