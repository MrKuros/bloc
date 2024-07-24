Blender S3 Integration Add-on
Overview

Blender S3 Integration is a Blender add-on that allows users to seamlessly upload, download, and manage Blender files directly from AWS S3. This add-on enhances the workflow for 3D artists and developers by providing an easy-to-use interface within Blender to interact with AWS S3.
Features

    Upload to S3: Easily upload your Blender files to an S3 bucket.
    Download from S3: Download files from your S3 bucket directly into Blender.
    List Files: View a list of files in your S3 bucket and manage them.
    Delete and Update Files: Delete or update files in your S3 bucket directly from Blender. (feature is yet to be added)

Installation

To install the Blender S3 Integration add-on, follow these steps:

    Download the Add-on
        `git clone https://github.com/MrKuros/bloc.git`
  
    Install the Add-on in Blender
        Open Blender.
        Go to Edit > Preferences > Add-ons.
        Click on Install at the top of the preferences window.
		![2024-07-24-150222_1920x1080_scrot](https://github.com/user-attachments/assets/e973f4f7-2a49-4724-ba95-5fa0c672cdc0)

        Select the downloaded ZIP file.
        Enable the add-on by checking the box next to "Blender S3 Integration".

  		


Setup

Before using the add-on, you need to configure your AWS credentials:

    Open Blender Preferences
        Go to Edit > Preferences > Add-ons > Blender S3 Integration.

    Enter AWS Credentials
        In the add-on preferences, enter your AWS Access Key, Secret Key, and the region where your S3 bucket is located.

    Set Your S3 Bucket Name
        Enter the name of your S3 bucket in the preferences.

  		![2024-07-24-150233_1920x1080_scrot](https://github.com/user-attachments/assets/19e5737d-565f-43b4-8200-78bfd6684eb3)

Usage

Once installed and configured, you can use the add-on from the Blender interface:

    Open the S3 Integration Panel
        Go to the View3D > Tool Shelf > S3 Integration panel.

    ![2024-07-24-150241_1920x1080_scrot](https://github.com/user-attachments/assets/8d236350-ae7c-4dcc-8ddf-feb25df9e78d)


Contributing

If you want to contribute to this project, please fork the repository and create a pull request with your changes.
License

This project is licensed under the GNU General Public License v3.0 - see the LICENSE file for details.
