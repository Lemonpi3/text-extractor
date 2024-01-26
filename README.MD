# Universal Text Extractor

WIP - 
This project is to create a text extractor that can extract the text content from diferent types of files such as pdfs, pptx, html, txt, docx, etc and returns a clean string with the document's content.

## The overall plan 

<img src="/assets/pipelineOverview.png" alt="Pipeline overview"/>

**1. First we check which type of file is**:
   - If is a file that I can extract the text straight forward It will go to the text extraction pipeline
   - If it's a pptx/image it will go to the ocr pipeline (I can extract pptx text with python pptx but layout information is important for this type of file)
   - If it is an ambiguous like a pdf file where it could be a scanned document (images) or a digital text I do a check to determine which one to use
  
**2. The text is extracted by the corresponding pipeline**:
- For the ocr pipeline I try to extract the important parts of the file while ignoring things like watermarks, footers, etc.

**3. Tries to clean the text from typos/weird parsing imperfections**

## Components

### TextPipeline
WIP

### OCRPipeline
WIP

### Layout classifier
WIP- I'm going to try to build my own from scratch by using some sample files and a labeling tool to create the labels for the training data.

The output of the layout classifier would be a json with boundary box coordinates and a label that indicates what type of text is (if it's a title subtitle paragraph footer etc) so then I can feed the OCR pipeline the coordinates of the desired ones.

This component might include a rotation detection in case the file is flipped in a different direction.

### PostProcessing
WIP 

# Dependencies

```
python >= 3.12
```
```
pip install -r requirements.txt
```