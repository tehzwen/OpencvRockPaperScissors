import cv2
import numpy as np
from prediction import *
from gameLogic import *


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

    

def main():

    cap = cv2.VideoCapture(1)

    rockImg = cv2.imread("./rock/0.jpg")
    paperImg = cv2.imread("./paper/0.jpg")
    scissorImg = cv2.imread("./scissors/0.jpg")
    ambientImg = cv2.imread("./ambient/0.jpg")

    rockGray = cv2.cvtColor(rockImg, cv2.COLOR_BGR2GRAY)
    paperGray = cv2.cvtColor(paperImg, cv2.COLOR_BGR2GRAY)
    scissorGray = cv2.cvtColor(scissorImg, cv2.COLOR_BGR2GRAY)
    ambientGray = cv2.cvtColor(ambientImg, cv2.COLOR_BGR2GRAY)

    ret1, rockThresh = cv2.threshold(rockGray, 70, 255, cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)
    ret2, paperThresh = cv2.threshold(paperGray, 70, 255, cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)
    ret3, scissorThresh = cv2.threshold(scissorGray, 70, 255, cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)
    ret4, ambientThresh = cv2.threshold(ambientGray, 70, 255, cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)


    while (cap.isOpened()):
        ret, img = cap.read()
        
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (5,5), 0)

        ret, imgThresh = cv2.threshold(blur, 70, 255, cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)

        


        cv2.imshow("Input", imgThresh)
        k = cv2.waitKey(10)
        if k == 27:
            break

        elif k == 101:
            print("")
            result = templateMatch(blur, scissorGray, rockGray, paperGray, ambientGray)
            computerChoice = runGame()
            print ("Player chooses: " + result)
            print ("Computer chooses: " + computerChoice)
            winner = handleWinner(result, computerChoice)
            print (winner)
            #predict("image.jpg")

        
def predictMain():

    cap = cv2.VideoCapture(1)

    while (cap.isOpened()):

        ret, img = cap.read()

        cv2.imshow('input', img)

        #predict(img)

        k = cv2.waitKey(10)
            
        if k == 27:
            break

        elif k == 101:
            print("")
            cv2.imwrite("image.jpg", img)
            #predict("image.jpg")
            

main()

#predictMain()
