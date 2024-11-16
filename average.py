import numpy as np
import cv2
import scipy.spatial.distance
from datetime import datetime
import os
import sys

fileExtensions = [
    ".webm",
    ".mkv",
    ".flv",
    ".vob",
    ".ogv",
    ".ogg",
    ".rrc",
    ".gifv",
    ".mng",
    ".mov",
    ".avi",
    ".qt",
    ".wmv",
    ".yuv",
    ".rm",
    ".asf",
    ".amv",
    ".mp4",
    ".m4p",
    ".m4v",
    ".mpg",
    ".mp2",
    ".mpeg",
    ".mpe",
    ".mpv",
    ".m4v",
    ".svi",
    ".3gp",
    ".3g2",
    ".mxf",
    ".roq",
    ".nsv",
    ".flv",
    ".f4v",
    ".f4p",
    ".f4a",
    ".f4b",
    ".mod",
]
workingDirectory = os.getcwd()
videoDirectory = os.path.join(workingDirectory, "videos")
allFiles = [
    f
    for f in os.listdir(videoDirectory)
    if os.path.isfile(os.path.join(videoDirectory, f))
]
allVideoFiles = [f for f in allFiles if os.path.splitext(f)[1] in fileExtensions]
longestFilename = max(allVideoFiles, key=len)

def _handleAlgorithm(algorithm):
    averageCalc = True
    trimmedAverageCalc = True
    kmeansCalc = True

    if algorithm:
        if algorithm == "average":
            print("calculating only average")
            trimmedAverageCalc = False
            kmeansCalc = False
        if algorithm == "trimmedAverage":
            print("calculating only trimmed average")
            averageCalc = False
            kmeansCalc = False
        if algorithm == "kmeans":
            print("calculating only kmeans")
            averageCalc = False
            trimmedAverageCalc = False
        if algorithm == "noaverage":
            print("skipping average calculation")
            averageCalc = False
        if algorithm == "notrimmedAverage":
            print("skipping trimmed average calculation")
            trimmedAverageCalc = False
        if algorithm == "nokmeans":
            print("skipping kmeans calculation")
            kmeansCalc = False

    return averageCalc, trimmedAverageCalc, kmeansCalc

    

def average(targetFile = "", showVideo = True, skip = 8, algorithm = "", kmeansParameters = [5, 5, 0.1, 3]):
    if targetFile:
        print("only processing file: " + targetFile)
    if skip != 8:
        print("skipping every " + str(skip) + " frames")
    if kmeansParameters != [5, 5, 0.1, 3]:
        print("calculating kmeans with " + str(kmeansParameters[0]) + " colors, "
              + str(kmeansParameters[1]) + " iterations, "
              + str(kmeansParameters[3]) + " attempts, and a threshold of "
              + str(kmeansParameters[2]))

    averageCalc, trimmedAverageCalc, kmeansCalc = _handleAlgorithm(algorithm)
    kmeansColors, kmeansIterations, kmeansThreshold, kmeansAttempts = kmeansParameters

    for fileName in allVideoFiles:
        if targetFile and fileName != targetFile:
            pass 

        videoPath = os.path.join(videoDirectory, fileName)
        outputPath = os.path.join(workingDirectory, "csvs", os.path.splitext(fileName)[0])
                
        cap = cv2.VideoCapture(videoPath)
        prevTime = datetime.now()
        if not os.path.exists(outputPath):
            os.makedirs(outputPath)

        fps = cap.get(cv2.CAP_PROP_FPS)  # OpenCV2 version 2 used "CV_CAP_PROP_FPS"
        frameCount = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        duration = frameCount / fps
        currentFrame = 0

        i = 0
        with open(os.path.join(outputPath, "average.csv"), "a") as averageFile:
            with open(
                os.path.join(outputPath, "trimmedAverage.csv"), "a"
            ) as trimmedAverageFile:
                with open(os.path.join(outputPath, "kmeans.csv"), "a") as kmeansFile:
                    while cap.isOpened():
                        ret = cap.grab()
                        if not ret:
                            break
                        currentFrame += 1
                        if i < skip:
                            i += 1
                            continue
                        i = 0
                        _, frame = cap.retrieve()

                        ### Average Calculation
                        if averageCalc or trimmedAverageCalc:
                            average = frame.mean(axis=0).mean(axis=0)

                        ### Trimmed Average Calculation
                        if trimmedAverageCalc:
                            pixels = frame.reshape(-1, 3)
                            dist = scipy.spatial.distance.cdist(pixels, [average])
                            averageDist = dist.mean()

                            pixelsWithDist = np.concatenate((pixels, dist), axis=1)
                            # average2 = pixelsWithDist[pixelsWithDist[:,3].argsort()][:int(pixels.size/30),:3].mean(axis=0)
                            trimmedAverage = pixelsWithDist[
                                pixelsWithDist[:, 3] < averageDist
                            ][:, :3].mean(axis=0)

                            # average2 = trimmedPixels.mean()

                        ### Kmeans Calculation
                        if kmeansCalc:
                            pixels = np.float32(frame.reshape(-1, 3))
                            criteria = (
                                cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER,
                                kmeansIterations,
                                kmeansThreshold,
                            )
                            flags = cv2.KMEANS_RANDOM_CENTERS

                            _, labels, palette = cv2.kmeans(
                                pixels, kmeansColors, None, criteria, kmeansAttempts, flags
                            )
                            _, counts = np.unique(labels, return_counts=True)

                            dominant = palette[np.argmax(counts)]

                        if showVideo:
                            cv2.imshow("frame", frame)
                            blank = np.zeros((300, 300, 3), np.uint8)
                            if averageCalc:
                                cv2.rectangle(blank, (0, 0), (300, 300), average, -1)
                            if trimmedAverageCalc:
                                cv2.rectangle(
                                    blank,
                                    (150, 150),
                                    (300, 300),
                                    np.float64(trimmedAverage),
                                    -1,
                                )
                            if kmeansCalc:
                                cv2.rectangle(
                                    blank, (0, 150), (150, 300), np.float64(dominant), -1
                                )
                            cv2.imshow("average", blank)

                        if averageCalc and not np.isnan(average).any():
                            averageFile.write(
                                str(average[0])
                                + ", "
                                + str(average[1])
                                + ", "
                                + str(average[2])
                                + "\n"
                            )
                        if trimmedAverageCalc and not np.isnan(trimmedAverage).any():
                            trimmedAverageFile.write(
                                str(trimmedAverage[0])
                                + ", "
                                + str(trimmedAverage[1])
                                + ", "
                                + str(trimmedAverage[2])
                                + "\n"
                            )
                        if kmeansCalc and not np.isnan(dominant).any():
                            kmeansFile.write(
                                str(dominant[0])
                                + ", "
                                + str(dominant[1])
                                + ", "
                                + str(dominant[2])
                                + "\n"
                            )

                        newTime = datetime.now()
                        timeDiff = newTime - prevTime
                        prevTime = newTime
                        sys.stdout.write("\r")
                        progress = (
                            "Progress: "
                            + str(round(100 * currentFrame / frameCount, 3))
                            + "%"
                        )
                        sys.stdout.write(progress)
                        spacing = ""
                        for i in range(20 - len(progress)):
                            spacing += " "
                        consoleFps = (
                            spacing
                            + "fps: "
                            + str(round((skip + 1) * 1000000 / timeDiff.microseconds, 3))
                        )
                        sys.stdout.write(consoleFps)
                        spacing = ""
                        for i in range(20 - len(consoleFps)):
                            spacing += " "
                        sys.stdout.write(spacing + "file: " + fileName)
                        spacing = ""
                        for i in range(len(longestFilename) - len(fileName)):
                            spacing += " "
                        sys.stdout.write(spacing)
                        sys.stdout.flush()

                        if showVideo:
                            if cv2.waitKey(1) & 0xFF == ord("q"):
                                break

        cap.release()
        cv2.destroyAllWindows()
    
    print("")
    print("Successfully completed averaging!")
