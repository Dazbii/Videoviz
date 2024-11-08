import numpy as np
import cv2
import scipy.spatial.distance
from datetime import datetime
import os
import sys

fileNames = ['foo.mp4', 'bar.mp4']

for fileName in fileNames:

  workingDirectory = 'TODO'
  # fileName = 'mononoke.mkv'
  skip = 8
  showVideo = True
  averageCalc = True
  trimmedAverageCalc = True
  kmeansCalc = True
  kmeansColors = 5
  kmeansIterations = 5
  kmeansThreshold = 0.1
  kmeansAttempts = 3

  cap = cv2.VideoCapture(workingDirectory + fileName)
  prevTime = datetime.now()
  directoryName = fileName.split('.')[0]
  if not os.path.exists(workingDirectory + directoryName):
    os.makedirs(workingDirectory + directoryName)

  fps = cap.get(cv2.CAP_PROP_FPS)      # OpenCV2 version 2 used "CV_CAP_PROP_FPS"
  frameCount = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
  duration = frameCount/fps
  currentFrame = 0
  print(fps)

  i = 0
  with open(workingDirectory + directoryName + '/average.csv', 'a') as averageFile:
    with open(workingDirectory + directoryName + '/trimmedAverage.csv', 'a') as trimmedAverageFile:
      with open(workingDirectory + directoryName + '/kmeans.csv', 'a') as kmeansFile:
        while(cap.isOpened()):
          ret, frame = cap.read()
          if not ret:
            break
          currentFrame += 1
          if i < skip:
            i += 1
            continue
          i = 0

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
            trimmedAverage = pixelsWithDist[pixelsWithDist[:,3] < averageDist][:,:3].mean(axis=0)

            # average2 = trimmedPixels.mean()

          ### Kmeans Calculation
          if kmeansCalc:
            pixels = np.float32(frame.reshape(-1, 3))
            criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, kmeansIterations, kmeansThreshold)
            flags = cv2.KMEANS_RANDOM_CENTERS

            _, labels, palette = cv2.kmeans(pixels, kmeansColors, None, criteria, kmeansAttempts, flags)
            _, counts = np.unique(labels, return_counts=True)

            dominant = palette[np.argmax(counts)]

          if showVideo:
            cv2.imshow('frame',frame)
            blank = np.zeros((300, 300, 3), np.uint8)
            if averageCalc: cv2.rectangle(blank, (0, 0), (300, 300), average, -1)
            if trimmedAverageCalc: cv2.rectangle(blank, (150, 150), (300, 300), np.float64(trimmedAverage), -1)
            if kmeansCalc: cv2.rectangle(blank, (0, 150), (150, 300), np.float64(dominant), -1)
            cv2.imshow('average', blank)

          if averageCalc and not np.isnan(average).any(): 
            averageFile.write(str(average[0]) + ', ' + str(average[1]) + ', ' + str(average[2]) + '\n')
          if trimmedAverageCalc and not np.isnan(trimmedAverage).any(): 
            trimmedAverageFile.write(str(trimmedAverage[0]) + ', ' + str(trimmedAverage[1]) + ', ' + str(trimmedAverage[2]) + '\n')
          if kmeansCalc and not np.isnan(dominant).any(): 
            kmeansFile.write(str(dominant[0]) + ', ' + str(dominant[1]) + ', ' + str(dominant[2]) + '\n')

          newTime = datetime.now()
          timeDiff = newTime - prevTime
          prevTime = newTime
          sys.stdout.write('\r')
          progress = 'Progress: ' + str(round(100 * currentFrame / frameCount, 3)) + '%'
          sys.stdout.write(progress)
          spacing = ''
          for i in range(20 - len(progress)): 
            spacing += ' '
          sys.stdout.write(spacing + "fps: " + str(round((skip + 1) * 1000000 / timeDiff.microseconds, 3)))
          sys.stdout.flush()

          if showVideo:
            if cv2.waitKey(1) & 0xFF == ord('q'):
              break

  cap.release()
  cv2.destroyAllWindows()