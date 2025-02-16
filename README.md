# YOLO Pre-annotation Tool

This tool uses a pretrained YOLO model to generate pre-annotated images in LabelMe format. It simplifies the labeling process by annotating images containing specific objects of interest. You can then manually adjust the annotations as needed.

## Installation

To get started, install the required dependencies:

1. **PyTorch and related libraries:**
    ```bash
    pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu126
    ```

2. **Ultralytics YOLO (for object detection):**
    ```bash
    pip install ultralytics
    ```

## Overview

This script performs the following tasks:

- Given a folder with subfolders containing raw images, it will automatically generate a `LabelMe`-compatible folder structure (`./3_AI_label`).
- It will pre-annotate images with objects of interest, filtering out images that don't contain any objects.
- Afterward, you can start manual labeling adjustments.

## How it Works

1. **Input:**
   - A folder containing raw images (and subfolders).

2. **Process:**
   - The tool processes the images and pre-annotates them using a YOLO model.
   - It filters out any images that don't contain objects of interest.

3. **Output:**
   - The script creates a `LabelMe` folder structure (`./3_AI_label`), with annotations already applied for images containing the interested objects.

## Preparation

1. Open the `config.yaml` file.
2. Replace the necessary values (e.g., object labels, folder paths) to match your dataset.

## Usage

- Run the `START.bat` file to initiate the process.

```bash
START.bat
