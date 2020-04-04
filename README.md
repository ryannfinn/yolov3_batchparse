# Batch Detecting and Parsing YOLOv3 with Python (Mac & Linux)

This is a Python (3.x) script I wrote for processing and parsing the results for YOLOv3. 

The original YOLOv3 does not provide a convenient way for processing the data in batch. Its default way to handle multiple images is: 

* to input each image path by interacting with the terminal after training the weights 
* feeding a text file with image paths for batch input, without retaining the image outputs

I wrote this script with the python module [pexpect](https://pexpect.readthedocs.io/en/stable/) to interact with the terminal, output a csv file indicating the unique objects detected on an image, and generate a summary for all images processed in that session. 

You may also want to check [alexgong7's project](https://darknet.gong.im). It is probably a more robust way to batch detect the objects on the images, as the author altered the source code in C to add the batch processing functions to the original YOLO (it doesn't come with parsing and summarising though)

**Note: The script is meant to be work under OS systems which use bash like Linux and MacOS only, as the command on the script   is in bash.**

## Setup

Please follow the [official setup guide](https://pjreddie.com/darknet/yolo/), as to `git clone` the darknet repository, compile by `make`, and `wget` the `yolov3.weights` file. Then put this script onto the root depository called `darknet`. 

As the script used [pexpect](https://pexpect.readthedocs.io/en/stable/) to interact with the terminal, please also `pip install pexpect	` before running the script. 

## Usage

Set the working directory, as the original darknet program seems to be only working when the working directory is on `darknet`:

```
$ cd darknet
```

Run the following command on terminal, where the `"testing_foto"` is the folder for the input photos and `"summary.csv"` is the name of the output file. Please put the input folder inside the `darknet` directory. 

```
python3 yolo_batch_parse.py "testing_foto" summary.csv 
```

## Output

The prediction images would be put under a new folder called `output` under the directory for input photo.

After all the photos have been processed in the session, a summary will be printed in the end:

```
The number of pictures processed is: 3
Occurence of objects:
Counter({'person': 2})
```

The script currently targets the use for detecing unique objects only. Therefore both the output file and output summary on the terminal only shows the unique occurence of an object in one photo, i.e. if three people appear in one photo, person would be counted as one. The confidence interval is not taken into account as well. 

The output file looks like this:


## Works to do

* Adding options to parse also the number of objects in one photo, and their respective confidence interval, in the format of a dataframe
* Adding options to use other weights other than the official `yolov3.weights`, as it is now hardcoded that with that. 

 