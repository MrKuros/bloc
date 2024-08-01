# Blender S3 Integration Add-on

## Overview

Bloc is a Blender add-on that allows users to seamlessly upload, download, and manage Blender files directly from AWS S3. This add-on enhances the workflow for 3D artists and developers by providing an easy-to-use interface within Blender to interact with AWS S3.

## Features

- **Upload to S3**: Easily upload your Blender files to an S3 bucket.
- **Download from S3**: Download files from your S3 bucket directly into Blender.
- **List Files**: View a list of files in your S3 bucket and manage them.
- **Delete and Update Files**: Delete or update files in your S3 bucket directly from Blender.

## New Release bug fixes
- Initialized S3 client globally.
- Combined download and load functions for code hygiene.
- Added file delete functionality.
- Improved error handling and user feedback."

## Installation

To install the Blender S3 Integration add-on, follow these steps:

1. **Download the Add-on**
   - Download the latest release of the add-on
     ```
     git clone https://github.com/mrkuros/bloc.git
      ```
     
1. **Install the Add-on in Blender**
   - Open Blender.
   - Go to `Edit > Preferences > Add-ons`.
   - Click on `Install` at the top of the preferences window.
   - Select the downloaded ZIP file.
   - Enable the add-on by checking the box next to "Blender S3 Integration".

## Setup

Before using the add-on, you need to configure your AWS credentials:

1. **Open Blender Preferences**
   - Go to `Edit > Preferences > Add-ons > Blender S3 Integration`.

![2024-07-24-150222_1920x1080_scrot](https://github.com/user-attachments/assets/8d102066-a5d6-43f3-a709-5e7d7c154160)


2. **Enter AWS Credentials**
   - In the add-on preferences, enter your AWS Access Key, Secret Key, and the region where your S3 bucket is located.

3. **Set Your S3 Bucket Name**
   - Enter the name of your S3 bucket in the preferences.
  
![2024-07-24-150233_1920x1080_scrot](https://github.com/user-attachments/assets/8ee196da-2d21-4e26-9cda-f88564d79be9)


## Usage

Once installed and configured, you can use the add-on from the Blender interface:

1. **Open the S3 Integration Panel**
   - Go to the `View3D > Tool Shelf > S3 Integration` panel and enjoy your life.

![2024-07-24-150241_1920x1080_scrot](https://github.com/user-attachments/assets/9f5a15af-1199-4ca0-b5f4-57eba054384a)

## Contributing

If you want to contribute to this project, please fork the repository and create a pull request with your changes.

## License

This project is licensed under the GNU General Public License v3.0 - see the [LICENSE](LICENSE) file for details.
