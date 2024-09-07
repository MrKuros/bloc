# Blender S3 Integration Add-on

## Overview

Bloc is a Blender add-on that integrates AWS S3 for seamless file management. It enhances the workflow for 3D artists and developers by allowing easy upload, download, and management of Blender files directly from within Blender.

## Features

- **Upload to S3**: Easily upload Blender files to an S3 bucket.
- **Download from S3**: Download files from your S3 bucket directly into Blender.
- **List Files**: View and manage files in your S3 bucket.
- **Delete and Update Files**: Delete or update files in your S3 bucket from Blender.

## Updated Features (v2.0)

- Upload Blender files with dependencies (textures, images, etc.) to S3.
- Download Blender files with dependencies (textures, images, etc.) from S3.

## Note

- Dependency paths should be relative to the blend file and located in the same folder as the blend file.

## Installation

To install the Blender S3 Integration add-on, follow these steps:

1. **Download the Add-on**
   - Clone the repository:
     ```bash
     git clone https://github.com/mrkuros/bloc.git
     ```
     
2. **Install the Add-on in Blender**
   - Open Blender.
   - Go to `Edit > Preferences > Add-ons`.
   - Click on `Install` at the top of the preferences window.
   - Select the downloaded ZIP file.
   - Enable the add-on by checking the box next to "Blender S3 Integration".

## Setup

Before using the add-on, configure your AWS credentials:

1. **Open Blender Preferences**
   - Go to `Edit > Preferences > Add-ons > Blender S3 Integration`.

   ![Blender Preferences](https://github.com/user-attachments/assets/8d102066-a5d6-43f3-a709-5e7d7c154160)

2. **Enter AWS Credentials**
   - In the add-on preferences, enter your AWS Access Key, Secret Key, and the region where your S3 bucket is located.

3. **Set Your S3 Bucket Name**
   - Enter the name of your S3 bucket in the preferences.

   ![Add-on Preferences](https://github.com/user-attachments/assets/8ee196da-2d21-4e26-9cda-f88564d79be9)

## Usage

Once installed and configured, use the add-on from the Blender interface:

1. **Open the S3 Integration Panel**
   - Go to `View3D > Tool Shelf > S3 Integration` panel to access the features.

   ![S3 Integration Panel](https://github.com/user-attachments/assets/9f5a15af-1199-4ca0-b5f4-57eba054384a)

## Contributing

To contribute, fork the repository and create a pull request with your changes.

## License

This project is licensed under the GNU General Public License v3.0. See the [LICENSE](LICENSE) file for details.

