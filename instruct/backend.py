import argparse
import io
from random import *
import pandas as pd
import os
os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="/Users/dakshidnani/Documents/doce/LAHacks-a323047fd484.json"


# FACE API WRAPPER

from google.cloud import vision
from google.cloud.vision import types
from PIL import Image, ImageDraw

def detect_face(face_file, max_results=4):
    """Uses the Vision API to detect faces in the given file.

    Args:
        face_file: A file-like object containing an image with faces.

    Returns:
        An array of Face objects with information about the picture.
    """
    client = vision.ImageAnnotatorClient()

    content = face_file.read()
    image = types.Image(content=content)

    global fa 
    fa = client.face_detection(image=image);
    return client.face_detection(image=image).face_annotations

def highlight_faces(image, faces, output_filename):
    """Draws a polygon around the faces, then saves to output_filename.

    Args:
      image: a file containing the image with the faces.
      faces: a list of faces found in the file. This should be in the format
          returned by the Vision API.
      output_filename: the name of the image file to be created, where the
          faces have polygons drawn around them.
    """
    im = Image.open(image)
    draw = ImageDraw.Draw(im)

    for face in faces:
        box = [(vertex.x, vertex.y)
               for vertex in face.bounding_poly.vertices]
        draw.line(box + [box[0]], width=5, fill='#00ff00')

    im.save(output_filename)

def markFaces(input_filename, output_filename, max_results):
    with open(input_filename, 'rb') as image:
        faces = detect_face(image, max_results)
        # print('Found {} face{}'.format(
        #     len(faces), '' if len(faces) == 1 else 's'))

        # print('Writing to file {}'.format(output_filename))
        # Reset the file pointer, so we can read the file again
        image.seek(0)
        highlight_faces(image, faces, output_filename)

def getAverageAttentiveness(input_filepath, currentSecond):
    markFaces('{}'.format(input_filepath), 'public/annotatedFrames/{}.jpg'.format(currentSecond), 100)
    return attentivenessHelper(fa)

def attentivenessHelper(photoData):
    annotations = photoData.face_annotations
    
    joyL = []
    sorrowL = []
    angerL = []
    surpriseL = []
    
    for annotation in annotations:
        joy = annotation.joy_likelihood
        sorrow = annotation.sorrow_likelihood
        anger = annotation.anger_likelihood
        surprise = annotation.surprise_likelihood
        joyL.append(joy)
        sorrowL.append(sorrow)
        angerL.append(anger)
        surpriseL.append(surprise)
    
    numFaces = len(joyL)
    
    if numFaces == 0:
        return 0

    # Calculate mode emotions
    joyMode = max(set(joyL), key=joyL.count)
    sorrowMode = max(set(sorrowL), key=sorrowL.count)
    angerMode = max(set(angerL), key=angerL.count)
    surpriseMode = max(set(surpriseL), key=surpriseL.count)

    difference = []
    attentive = []
    numAttentive = 0.0

    # Calculate deflection from the mode
    for i in range(numFaces):
        # joydiff, sorrowdiff, angerdiff, surprisediff
        joydiff = abs(joyMode - joyL[i])
        sorrowdiff = abs(sorrowMode - joyL[i])
        angerdiff = abs(angerMode - joyL[i])
        surprisediff = abs(surpriseMode - joyL[i])

        if joydiff > 1 or sorrowdiff > 1 or angerdiff > 1 or surprisediff > 1:
            attentive.append(False)
        else:
            attentive.append(True)

        if(attentive[i]):
            numAttentive += 1.0
            #print('Person {} is attentive'.format(i))
        
        difference.append(joydiff + sorrowdiff + angerdiff + surprisediff)
    
    attentiveness = numAttentive / numFaces

    if attentiveness == 1:      # Clip full attentiveness to reasonable amount, otherwise loss is infinite
        x = randint(1, 100) / 500.0 
        attentiveness -= x
        if x < .98:
            x += randint(1, 2) / 100.0


    return attentiveness * 100


# END OF FACE API

# SPEECH API things

fileN = 'uploads/file.mp4'
videoForAudio = 'uploads/audio.mp4'
fileL = 30

def transcribe_file_with_word_time_offsets(speech_file):
    """Transcribe the given audio file synchronously and output the word time
    offsets."""
    from google.cloud import speech
    from google.cloud.speech import enums
    from google.cloud.speech import types
    client = speech.SpeechClient()

    with io.open(speech_file, 'rb') as audio_file:
        content = audio_file.read()

    audio = types.RecognitionAudio(content=content)
    config = types.RecognitionConfig(
        encoding=enums.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code='en-US',
        enable_word_time_offsets=True)

    response = client.recognize(config, audio)

    return response
    # for result in response.results:
    #     alternative = result.alternatives[0]
    #     print('Transcript: {}'.format(alternative.transcript))

    #     for word_info in alternative.words:
    #         word = word_info.word
    #         start_time = word_info.start_time
    #         end_time = word_info.end_time
    #         print('Word: {}, start_time: {}, end_time: {}'.format(
    #             word,
    #             start_time.seconds + start_time.nanos * 1e-9,
    #             end_time.seconds + end_time.nanos * 1e-9))


# [START def_transcribe_gcs]
def transcribe_gcs_with_word_time_offsets(gcs_uri):
    """Transcribe the given audio file asynchronously and output the word time
    offsets."""
    from google.cloud import speech
    from google.cloud.speech import enums
    from google.cloud.speech import types
    client = speech.SpeechClient()

    audio = types.RecognitionAudio(uri=gcs_uri)
    config = types.RecognitionConfig(
        encoding=enums.RecognitionConfig.AudioEncoding.FLAC,
        sample_rate_hertz=16000,
        language_code='en-US',
        enable_word_time_offsets=True)

    operation = client.long_running_recognize(config, audio)

    print('Waiting for operation to complete...')
    result = operation.result(timeout=90)

    return result.results
    # for result in result.results:
    #     alternative = result.alternatives[0]
    #     print('Transcript: {}'.format(alternative.transcript))
    #     print('Confidence: {}'.format(alternative.confidence))

    #     for word_info in alternative.words:
    #         word = word_info.word
    #         start_time = word_info.start_time
    #         end_time = word_info.end_time
    #         print('Word: {}, start_time: {}, end_time: {}'.format(
    #             word,
    #             start_time.seconds + start_time.nanos * 1e-9,
    #             end_time.seconds + end_time.nanos * 1e-9))
# [END def_transcribe_gcs]

def mp4towav(filePath, lengthOfAudio):
    import subprocess
    command = "ffmpeg -y -i {} -ss 0 -t {} -ab 160k -acodec pcm_s16le -ac 1 -ar 16000 -vn output.wav".format(filePath, lengthOfAudio)
    subprocess.call(command, shell=True)

def cropVideo(filePath, newLength):
    import subprocess
    command = "ffmpeg -y -i {} -ss 0 -t {} cropped.mp4".format(filePath, newLength)
    subprocess.call(command, shell=True)

def makeFramesForVideo(videoPath):
    import cv2
    import numpy as np
    import os
    import math

    # Playing video from file:
    cap = cv2.VideoCapture('{}'.format(videoPath))

    try:
        if not os.path.exists('data'):
            os.makedirs('data')
    except OSError:
        print ('Error: Creating directory of data')

    frameRate = cap.get(5)
    currentFrame = 0
    currentSecond = 1
    while(cap.isOpened()):
        # Capture frame-by-frame
        ret, frame = cap.read()
        frameId = cap.get(1)
        if ret != True:
            print("wtf")
            break
        # Saves image of the current frame in jpg file
        if (frameId % (math.ceil(frameRate)) == 0):
            name = 'public/frames/second' + str(currentSecond) + '.jpg'
            print ('Creating...' + name)
            cv2.imwrite(name, frame)
            currentSecond += 1

        # To stop duplicate images
        currentFrame += 1

    # When everything done, release the capture
    cap.release()
    cv2.destroyAllWindows()


def transcriptSegmenter(transcriptOutput):
    for result in transcriptOutput.results:
        alternative = result.alternatives[0]

        endtimesList = []

        # Create list of active seconds
        for word_info in alternative.words:
            word = word_info.word
            #start_time = word_info.start_time
            end_time = word_info.end_time.seconds

            # word is a word, end time is in seconds
            if end_time not in endtimesList:
                endtimesList.append(end_time)

        segmentedWords = []
        i = 0
        for et in endtimesList:
            segmentedWords.append([])
            for word_info in alternative.words:
                word = word_info.word
                end_time = word_info.end_time.seconds
                if end_time == et:
                    segmentedWords[i].append(word)
            i += 1

        size = i
        segmentSentences = []
        for wordList in segmentedWords:
            s = ""
            for w in wordList:
                s += w
                s += " "
            segmentSentences.append(s)
        
        segmentImagePaths = []
        segmentAttentiveness = []
        for et in endtimesList:
            segmentAttentiveness.append(getAverageAttentiveness('public/frames/second{}.jpg'.format(et + 1), et))
            #ipath = "annotatedFrames/{}.jpg".format(et)
            segmentImagePaths.append('second{}'.format(et + 1))

            #print('Word: {}  End time: {}'.format(word, end_time))
            # print('Word: {}, start_time: {}, end_time: {}'.format(
            #     word,
            #     start_time.seconds + start_time.nanos * 1e-9,
            #     end_time.seconds + end_time.nanos * 1e-9))

    for x in range(len(segmentAttentiveness)):
            print('{}: et: {}, words: {}, at: {}, imagepath: {}'.format(x, endtimesList[x], segmentSentences[x], segmentAttentiveness[x], segmentImagePaths[x]))

    df = pd.DataFrame()
    df['segmentText'] = segmentSentences
    df['attentiveness'] = segmentAttentiveness
    df['imagePath'] = segmentImagePaths
    return df


# Creates cropped.mp4, a video file of the demo analysis length
cropVideo(fileN, fileL)

# Split cropped.mp4 into 1 frame per second
makeFramesForVideo('cropped.mp4')

# Get audio file for video
mp4towav(videoForAudio, fileL)
# Get the list of segments along with the text for each segment
df = transcriptSegmenter(transcribe_file_with_word_time_offsets("output.wav"))
df.to_csv('uploads/output.csv', index=False)
print(df)

