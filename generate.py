import numpy as np
import cv2
import os

lines = True  # Lines
stb = True  # Starburst
tlstb = True  # Top Left Starburst
rad = True  # Radial
tlrad = True  # Top Left Radial

workingDirectory = os.getcwd()
csvDirectory = os.path.join(workingDirectory, "csvs")
outputDirectory = os.path.join(workingDirectory, "output")
directories = ["mononoke"]
filenames = ["average.csv", "kmeans.csv", "trimmedAverage.csv"]
# filenames += 'average.csv'
# filenames += 'kmeans.csv'
# filenames += 'trimmedAverage.csv'

def writeLines(file, skip, width, height, outputName):
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
        # if currentHeight > height:
        #     currentHeight = 0

    cv2.imwrite(
        outputName + "-lines.jpg", image
    )

def writeStarburst(file, skip, width, height, outputName):
    file.seek(0)
    image = np.zeros((height, width, 3), np.uint8)
    r = 0
    for line in file:
        values = np.array(line.split(", ")).astype(float)
        cv2.line(
            image,
            (250, 250),
            (
                250 + int(500 * np.sin(2 * np.pi * r / numLines)),
                250 + int(500 * np.cos(2 * np.pi * r / numLines)),
            ),
            values,
            1,
        )
        r += 1

    cv2.imwrite(
        outputName + "-centeredStarburst.jpg",
        image,
    )
    image = np.zeros((height, width, 3), np.uint8)

def writeTopLeftStarburst(file, skip, width, height, outputName):
    file.seek(0)
    image = np.zeros((height, width, 3), np.uint8)
    r = 0
    for line in file:
        values = np.array(line.split(", ")).astype(float)
        cv2.line(
            image,
            (0, 0),
            (
                int(1000 * np.sin(0.5 * np.pi * r / numLines)),
                int(1000 * np.cos(0.5 * np.pi * r / numLines)),
            ),
            values,
            1,
        )
        r += 1

    cv2.imwrite(
        outputName + "-topLeftStarburst.jpg",
        image,
    )
    image = np.zeros((height, width, 3), np.uint8)

def writeRadial(file, skip, width, height, outputName):
    file.seek(0)
    image = np.zeros((height, width, 3), np.uint8)
    r = 0
    radius = np.sqrt(height**2 + width**2) / 2
    for line in file:
        values = np.array(line.split(", ")).astype(float)
        cv2.circle(
            image,
            (250, 250),
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

def writeTopLeftRadial(file, skip, width, height, outputName):
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

for directory in directories:
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

        image = np.zeros((height, width, 3), np.uint8)

        with open(filePath) as file:
            if lines:
                writeLines(file, skip, width, height, outputName)
            if stb:
                writeStarburst(file, skip, width, height, outputName)
            if tlstb:
                writeTopLeftStarburst(file, skip, width, height, outputName)
            if rad:
                writeRadial(file, skip, width, height, outputName)
            if tlrad:
                writeTopLeftRadial(file, skip, width, height, outputName)

        # cv2.imshow('out', image)
        # cv2.waitKey()
        cv2.destroyAllWindows()
