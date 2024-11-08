import numpy as np
import cv2
from datetime import datetime

lines = True # Lines
stb = False # Starburst
tlstb = False # Top Left Starburst
rad = False # Radial
tlrad = False # Top Left Radial

rootDirectory = 'TODO'
directories = ['foo/', 'bar/']
filenames = ['average.csv', 'kmeans.csv', 'trimmedAverage.csv']
# filenames += 'average.csv'
# filenames += 'kmeans.csv'
# filenames += 'trimmedAverage.csv'

for directory in directories:
    workingDirectory = rootDirectory + directory

    for filename in filenames:
        factor = 1
        tempWidth = int(5440 * factor)
        tempHeight = int(8480 * factor)

        numLines = sum(1 for line in open(workingDirectory + filename))
        skip = int(numLines / tempHeight - 1)

        height = int(numLines / (skip + 1))
        width = int((height / tempHeight) * tempWidth)

        image = np.zeros((height, width, 3), np.uint8)

        with open(workingDirectory + filename) as file:
            #### Vertical
            if lines:
                currentHeight = 0
                i = 0
                for line in file:
                    if i < skip:
                        i += 1
                        continue
                    i = 0
                    values = np.array(line.split(', ')).astype(float)
                    cv2.line(image, (0, currentHeight), (width, currentHeight), values, 1)
                    currentHeight += 1
                    # if currentHeight > height:
                    #     currentHeight = 0
                cv2.imwrite(workingDirectory + filename.split('.')[0] + '-lines.jpg', image)
                image = np.zeros((height, width, 3), np.uint8)

            ##### Centered starburst
            if stb:
                r = 0
                for line in file:
                    values = np.array(line.split(', ')).astype(float)
                    cv2.line(image, (250, 250), (250 + int(500 * np.sin(2 * np.pi * r/numLines)), 250 + int(500 * np.cos(2 * np.pi * r/numLines))), values, 1)
                    r += 1
                cv2.imwrite(workingDirectory + filename.split('.')[0] + '-centeredStarburst.jpg', image)
                image = np.zeros((height, width, 3), np.uint8)

            ##### Top Left starburst
            if tlstb:
                r = 0
                for line in file:
                    values = np.array(line.split(', ')).astype(float)
                    cv2.line(image, (0, 0), (int(1000 * np.sin(0.5 * np.pi * r/numLines)), int(1000 * np.cos(0.5 * np.pi * r/numLines))), values, 1)
                    r += 1
                cv2.imwrite(workingDirectory + filename.split('.')[0] + '-topLeftStarburst.jpg', image)
                image = np.zeros((height, width, 3), np.uint8)

            ##### Centered radial
            if rad:
                r = 0
                radius = np.sqrt(height**2 + width**2)/2
                for line in file:
                    values = np.array(line.split(', ')).astype(float)
                    cv2.circle(image, (250, 250), int(radius * r/numLines), values, 2, lineType=cv2.LINE_AA)
                    r += 1
                cv2.imwrite(workingDirectory + filename.split('.')[0] + '-centeredRadial.jpg', image)
                image = np.zeros((height, width, 3), np.uint8)

            #### Top left radial
            if tlrad:
                r = 0
                radius = np.sqrt(height**2 + width**2)
                for line in file:
                    values = np.array(line.split(', ')).astype(float)
                    cv2.circle(image, (0, 0), int(radius * r/numLines), values, 2, lineType=cv2.LINE_AA)
                    r += 1
                cv2.imwrite(workingDirectory + filename.split('.')[0] + '-topLeftRadial.jpg', image)
                image = np.zeros((height, width, 3), np.uint8)

        # cv2.imshow('out', image)
        # cv2.waitKey()
        cv2.destroyAllWindows()