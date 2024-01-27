# OCR for Siemens AI Rad Companion

![Alt text](./ocr-siemens_ai_rad_companion.svg)

[![forthebadge](https://forthebadge.com/images/badges/made-with-python.svg)](https://www.python.org/)
[![forthebadge](https://forthebadge.com/images/badges/uses-badges.svg)](https://forthebadge.com)

[![Maintenance](https://img.shields.io/badge/Maintained%3F-no-red.svg)]( https://github.com/nsourlos/ocr-siemens_ai_rad_companion)


> This tool can be used to automatically identify the nodule id, as this is returned by the AI. Since AI returns a maximum of 10 nodules, possible values of that id are L01-L10. To optimize/fine-tune our OCR, we keep only characters that are of that value. 

It should be noted that in the above implementation it was assumed that AI detects 10 nodules. This was because only one scan was available to us and we couldn�t fine-tune the OCR method for cases with less than 10 nodules. For such cases the above implementation might not actually work. The code to do the above can be found [here](/ocr_red_color.py)


In addition to the above, a tool is also provided which can be used to select a specific color/hue, like the red contours in an DICOM slice, or the yellow letters of the nodule id (which can be used to OCR them). Another application is to extract the contour of the nodule. This tool can be found [here](/hsv_interface.py)

Two AI slices with nodules to be used to demonstrate that code actually works can be found in the [ocr folder](/ocr)

## Documentation (by *Chat GPT*)

The documentation below was created by using the prompt 
> Write documentation for the following code

### [hsv_interface.py](/hsv_interface.py)


**Description**

This code is a Python script that uses the OpenCV library to track the yellow color object in an image. It loads an image in the DICOM format, converts the image to the HSV color format, and performs color thresholding to extract the yellow color object. The script allows the user to adjust the HSV min and max values to track the yellow color object by creating trackbars in a named window.

Libraries used
The following libraries are used in this code:
```bash
cv2: OpenCV library for computer vision and image processing.
numpy: Numerical Python library for array manipulation and mathematical operations.
pydicom: DICOM library for reading, modifying, and writing DICOM files.
```

**Main steps**

Load an image in the DICOM format using the pydicom library.
Create a named window using the `cv2.namedWindow` function.
Create trackbars for the minimum and maximum values of hue, saturation, and value in the HSV color format using the `cv2.createTrackbar` function. The trackbars allow the user to adjust the HSV values.
Set the default value for the maximum values of hue, saturation, and value.
Continuously get the current positions of all trackbars using the `cv2.getTrackbarPos` function.
Convert the image to the HSV format using the `cv2.cvtColor` function.
Perform color thresholding to extract the yellow color object by using the `cv2.inRange` function and the `cv2.bitwise_and` function.
Display the result image in the named window using the `cv2.imshow` function. The result image is the yellow color object in the original image.
Continuously display the result image until the user presses the 'q' key.
Destroy all windows when the user presses the 'q' key.

**Conclusion**

This code demonstrates how to use the OpenCV library to track the yellow color object in an image. The script is interactive, allowing the user to adjust the HSV values to extract the desired color object. The result image shows the yellow color object in the original image.



### [ocr_red_color.py](/ocr_red_color.py)

The code performs OCR on DICOM slices to extract nodule ID information. It starts by importing necessary libraries including `pytesseract, cv2, numpy, os, pydicom, time, and warnings`. The path to the Tesseract OCR executable is then set.

The code defines the path to the DICOM slices and the path to save the line with the nodule ID. If the path to save the line with the nodule ID does not exist, the code creates the folder.

The code then sets the settings and characters that can be used to recognize the nodule ID and initializes empty lists to be filled with nodules and slices with errors.

The code loops through all DICOM slices in the path and reads each slice into memory as a DICOM object. It then converts the pixel data of each slice into grayscale, performs thresholding to get an image with only nodules, and selects the first 30 lines/rows of the image with the nodule ID number.

If the selected part of the image contains a nodule ID (it is not empty), the code prints the file name/slice that contains the nodule ID, saves the yellow mask, and performs OCR using pytesseract. The code also extracts part of the image with the characters, resizes it, converts it to grayscale, and performs OCR using pytesseract.

The OCR output is then compared to a list of possible nodule ID prefixes ('L01', 'L02', etc.), and if a match is found, the nodule ID is added to the final_class dictionary. If no match is found, the code adds the slice to the errors list.

Finally, the code displays the time elapsed for the entire process to complete.

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.