import cv2
import numpy as np
from gameLogic import *
import time


top, right, bottom, left = 10, 100, 300, 400

def calibrateWithNewImages():
    rock = False
    paper = False
    scissor = False
    rockPrinted = False
    paperPrinted = False
    scissorsPrinted = False
    rockCount = 0
    scissorCount = 0
    paperCount = 0

    time.sleep(1)

    cap = cv2.VideoCapture(0)

    while (cap.isOpened()):

        ret, img = cap.read()


        cv2.rectangle(img, (left, top), (right, bottom), (0, 255, 0), 2)
        cv2.imshow('input', img)

        roi = img[top:bottom, right:left]
        

        k = cv2.waitKey(10)

        if (rock and paper and scissor):
            cap.release()

        elif (not rock and not rockPrinted):
            print ("press c key to take a picture of rock!")
            rockPrinted = True

        elif (rock and not paper and not paperPrinted):
            print ("press c key to take a picture of paper!")
            paperPrinted = True

        elif (rock and paper and not scissor and not scissorsPrinted):
            print ("press c key to take a picture of scissors!")
            scissorsPrinted = True


       

        if k == 99:

            if (not rock and rockCount != 5):
                cv2.imwrite("./rock/" + str(rockCount) +".jpg", roi)
                rockCount += 1
                
                if rockCount == 5:
                    rock = True
            
            elif (not paper and paperCount != 5):
                cv2.imwrite("./paper/" + str(paperCount) + ".jpg", roi)
                paperCount += 1

                if paperCount == 5:
                    paper = 5

            elif (not scissor and scissorsPrinted != 5):
                cv2.imwrite("./scissors/" + str(scissorCount) + ".jpg", roi)
                scissorCount += 1

                if scissorCount == 5:
                    scissor = True



        elif k == 27:
            break

def getTotalConfidence(src, imageDir):
    
    totalImages = []
    totalMatches = []
    totalConfidence = 0

    for i in range(5):
        tempImg = cv2.imread(imageDir + str(i) +".jpg")
        totalImages.append(tempImg)

    '''cv2.imshow('fuck',totalImages[1])

    k = cv2.waitKey(0)
    if k == 27:
        cv2.destroyAllWindows()'''

    
    for image in totalImages:
        tempMatch = cv2.matchTemplate(src, image, cv2.TM_CCOEFF_NORMED)
        totalMatches.append(tempMatch)

    for match in totalMatches:
        _, tempConfidence, _, _ = cv2.minMaxLoc(match)
        totalConfidence += tempConfidence

    return totalConfidence


def templateMatch(gray, scissorGray, rockGray, paperGray, ambientGray):
    #ret, thresh1 = cv2.threshold(blur, 70, 255, cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)

    paperMatch = cv2.matchTemplate(gray, paperGray, cv2.TM_CCOEFF_NORMED)
    rockMatch = cv2.matchTemplate(gray, rockGray, cv2.TM_CCOEFF_NORMED)
    scissorsMatch = cv2.matchTemplate(gray, scissorGray, cv2.TM_CCOEFF_NORMED)
    ambientMatch = cv2.matchTemplate(gray, ambientGray, cv2.TM_CCOEFF_NORMED)

    _, paperConfidence, _, _ = cv2.minMaxLoc(paperMatch)
    _, rockConfidence, _, _ = cv2.minMaxLoc(rockMatch)
    _, scissorsConfidence, _, _ = cv2.minMaxLoc(scissorsMatch)
    _, ambientConfidence, _, _ = cv2.minMaxLoc(ambientMatch)

    #print ("paper: " + str(paperConfidence) + " rock: " + str(rockConfidence) + " scissors: " + str(scissorsConfidence))

    if (paperConfidence > rockConfidence and paperConfidence > scissorsConfidence and paperConfidence > ambientConfidence):
        #print ("Paper!")
        return "paper"

    elif (rockConfidence > paperConfidence and rockConfidence > scissorsConfidence and rockConfidence > ambientConfidence):
        #print ("Rock!")
        return "rock"

    elif (scissorsConfidence > rockConfidence and scissorsConfidence > paperConfidence and scissorsConfidence > ambientConfidence):
        #print ("Scissors!")
        return "scissors"

    else:
        #print ("Nothing there!")
        return ""

def determineMaxConfidence(rockConfidence, paperConfidence, scissorsConfidence):
    if (paperConfidence > rockConfidence and paperConfidence > scissorsConfidence):
        #print ("Paper!")
        return "paper"

    elif (rockConfidence > paperConfidence and rockConfidence > scissorsConfidence):
        #print ("Rock!")
        return "rock"

    elif (scissorsConfidence > rockConfidence and scissorsConfidence > paperConfidence):
        #print ("Scissors!")
        return "scissors"

    else:
        #print ("Nothing there!")
        return ""

def main():

    rock = False
    paper = False
    scissor = False

    cap = cv2.VideoCapture(0)

    rockImg = cv2.imread("./rock/0.jpg")
    paperImg = cv2.imread("./paper/0.jpg")
    scissorImg = cv2.imread("./scissors/0.jpg")
    ambientImg = cv2.imread("./ambient/0.jpg")

    rockGray = cv2.cvtColor(rockImg, cv2.COLOR_BGR2GRAY)
    paperGray = cv2.cvtColor(paperImg, cv2.COLOR_BGR2GRAY)
    scissorGray = cv2.cvtColor(scissorImg, cv2.COLOR_BGR2GRAY)
    ambientGray = cv2.cvtColor(ambientImg, cv2.COLOR_BGR2GRAY)

    ret1, rockThresh = cv2.threshold(
        rockGray, 70, 255, cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)
    ret2, paperThresh = cv2.threshold(
        paperGray, 70, 255, cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)
    ret3, scissorThresh = cv2.threshold(
        scissorGray, 70, 255, cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)
    ret4, ambientThresh = cv2.threshold(
        ambientGray, 70, 255, cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)

    print("Press 'c' to calibrate with new images, 'e' to play the game and 'esc' to quit")

    while (cap.isOpened()):
        ret, img = cap.read()
        #top, right, bottom, left = 10, 100, 450, 400

        roi = img[top:bottom, right:left]

        gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (5, 5), 0)

        

        ret, imgThresh = cv2.threshold(
            blur, 70, 255, cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)

        k = cv2.waitKey(10)
        if k == 27:
            break

        elif k == 99:
            cap.release()
            cv2.destroyAllWindows()
            print("Calibrate with new images")
            calibrateWithNewImages()
            cap = cv2.VideoCapture(0)


        elif k == 101:
            print("")
            result = templateMatch(
                blur, scissorGray, rockGray, paperGray, ambientGray)
            computerChoice = runGame()
            print("Player chooses: " + result)
            print("Computer chooses: " + computerChoice)
            winner = handleWinner(result, computerChoice)
            print(winner)


        cv2.rectangle(img, (left, top), (right, bottom), (0, 255, 0), 2)
        cv2.imshow("Input", img)
        cv2.imshow("Actual hand input", imgThresh)

        


def testMain():
    cap = cv2.VideoCapture(0)

    while (cap.isOpened()):

        ret, img = cap.read()

        cv2.rectangle(img, (left, top), (right, bottom), (0, 255, 0), 2)
        cv2.imshow("input", img)

        k = cv2.waitKey(10)

        if k == 27:
            break

        elif k == 99:
            cap.release()
            cv2.destroyAllWindows()
            print("Calibrate with new images")
            calibrateWithNewImages()
            cap = cv2.VideoCapture(0)

        elif k == 101:
            x = getTotalConfidence(img, "./rock/")
            y = getTotalConfidence(img, "./paper/")
            z = getTotalConfidence(img, "./scissors/")

            result = determineMaxConfidence(x, y, z)

            computerChoice = runGame()
            print("Player chooses: " + result)
            print("Computer chooses: " + computerChoice)
            winner = handleWinner(result, computerChoice)
            print(winner)


    

testMain()

#main()
