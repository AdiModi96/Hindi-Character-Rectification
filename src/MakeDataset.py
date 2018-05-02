import numpy as np, glob, os, cv2
import scipy.io as sio
import random as rand
import tqdm
import ProjectParameters as pp

trainInputImagesDirectoryPath = os.path.join(pp.corruptedDatasetDirectoryPath, 'train')
trainOutputImagesDirectoryPath = os.path.join(pp.untouchedDatasetDirectoryPath, 'train')
testInputImagesDirectoryPath = os.path.join(pp.corruptedDatasetDirectoryPath, 'test')
testOutputImagesDirectoryPath = os.path.join(pp.untouchedDatasetDirectoryPath, 'test')

datasetFilePath = os.path.join('D:\\', 'Codes', 'Python', 'Hindi Character Completion', 'generated', 'dataset.mat')

imageDimension = 32

corruptImageFileNamePrefixes = ['EEH_', 'EG_', 'ERH_', 'ID_', 'LB_', 'S&P_']

def recursivelyGatherImages(inputImagesDirectoryPath='', outputImagesDirectoryPath=''):

    print("Currently Processing:")
    print("\tInput Directory:", inputImagesDirectoryPath, sep=' ')
    print("\tOutput Directory:", outputImagesDirectoryPath, sep=' ')

    imagePaths = glob.glob(os.path.join(outputImagesDirectoryPath, '*.png'))

    progressBar = tqdm.tqdm(total=len(imagePaths), dynamic_ncols=True, unit=' Images', initial=0, ncols=80)

    inputImages = np.ndarray(shape=(0, imageDimension, imageDimension), dtype=np.uint8)
    outputImages = np.ndarray(shape=(0, imageDimension, imageDimension), dtype=np.uint8)

    for imagePath in imagePaths:
        imageName = imagePath[imagePath.rindex(os.sep) + 1:]
        # Reading Output Image Once and Adding it len(corruptImageFileNamePrefixes) times
        image = cv2.imread(imagePath, cv2.IMREAD_GRAYSCALE)
        for i in range(len(corruptImageFileNamePrefixes)):
            np.concatenate((outputImages, np.expand_dims(image, axis=0)), axis=0)

        #Respectively readin Input Images and adding it accordingly
        for i in range(len(corruptImageFileNamePrefixes)):
            image = cv2.imread(os.path.join(inputImagesDirectoryPath, corruptImageFileNamePrefixes[i] + str(imageName)), cv2.IMREAD_GRAYSCALE)
            np.concatenate((inputImages, np.expand_dims(image, axis=0)), axis=0)

        progressBar.update(1)

    progressBar.close()

    for item in os.listdir(outputImagesDirectoryPath):
        if os.path.isdir(os.path.join(outputImagesDirectoryPath, item)):
            tempInputImages, tempOutputImages = recursivelyGatherImages(os.path.join(inputImagesDirectoryPath, item), os.path.join(outputImagesDirectoryPath, item))
            np.concatenate((inputImages, tempInputImages), axis=0)
            np.concatenate((outputImages, tempOutputImages), axis=0)

    return inputImages, outputImages

print("Gathering Train Dataset: ")
trainInputImages, trainOutputImages = recursivelyGatherImages(trainInputImagesDirectoryPath, trainOutputImagesDirectoryPath)
print("Gathering Test Dataset: ")
testInputImages, testOutputImages = recursivelyGatherImages(testInputImagesDirectoryPath, testOutputImagesDirectoryPath)
print(trainInputImages.shape)
cv2.imshow("Sample of trainInputImages", rand.randint(0, len(trainInputImages)))
print(trainOutputImages.shape)
cv2.imshow("Sample of trainOutputImages", rand.randint(0, len(trainOutputImages)))
print(testInputImages.shape)
cv2.imshow("Sample of testInputImages", rand.randint(0, len(testInputImages)))
print(testOutputImages.shape)
cv2.imshow("Sample of testOutputImages", rand.randint(0, len(testOutputImages)))
sio.savemat(datasetFilePath, {
    "trainInputImages": trainInputImages,
    "trainOutputImages": trainOutputImages,
    "testInputImages": testInputImages,
    "testOutputImages": testOutputImages
})