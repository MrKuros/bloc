bl_info = {
    "name": "Blender S3 Integration",
    "author": "Kashish aka MrKuros",
    "version": (1, 1),
    "blender": (4, 1, 0),
    "location": "View3D > Tool Shelf > S3 Integration",
    "description": "Upload and download Blender files to/from AWS S3",
    "category": "Development",
}

import bpy
import os
import boto3
from botocore.exceptions import NoCredentialsError

s3_client = None  # Global S3 client

class S3IntegrationPreferences(bpy.types.AddonPreferences):
    bl_idname = __name__

    access_key: bpy.props.StringProperty(
        name="Access Key",
        description="AWS Access Key",
        default="",
        subtype='PASSWORD'
    )
    secret_key: bpy.props.StringProperty(
        name="Secret Key",
        description="AWS Secret Key",
        default="",
        subtype='PASSWORD'
    )
    region_name: bpy.props.StringProperty(
        name="Region Name",
        description="AWS Region Name",
        default="us-west-2"
    )
    bucket_name: bpy.props.StringProperty(
        name="Bucket Name",
        description="S3 Bucket Name",
        default=""
    )

    def draw(self, context):
        """Draw the preferences UI."""
        layout = self.layout
        layout.prop(self, "access_key")
        layout.prop(self, "secret_key")
        layout.prop(self, "region_name")
        layout.prop(self, "bucket_name")

def initialize_s3_client():
    """Initialize the S3 client."""
    global s3_client
    prefs = bpy.context.preferences.addons[__name__].preferences
    s3_client = boto3.client(
        's3',
        aws_access_key_id=prefs.access_key,
        aws_secret_access_key=prefs.secret_key,
        region_name=prefs.region_name
    )

def upload_to_aws(local_file, bucket, s3_file):
    """Upload a file to AWS S3."""
    try:
        s3_client.upload_file(local_file, bucket, s3_file)
        print("Upload Successful")
        return True
    except FileNotFoundError:
        print("The file was not found")
        return False
    except NoCredentialsError:
        print("Credentials not available")
        return False
    except Exception as e:
        print(f"An error occurred: {e}")
        return False

def list_files_in_bucket(bucket):
    """List all files in an S3 bucket."""
    files = []
    try:
        s3_resource = boto3.resource('s3')
        my_bucket = s3_resource.Bucket(bucket)
        files = [obj.key for obj in my_bucket.objects.all()]
    except Exception as e:
        print(e)
    return files

def load_s3_file_into_blender(file_name):
    """Download and load an S3 file into Blender."""
    try:
        s3_file_path = f'/tmp/{file_name}'
        s3_client.download_file(bpy.context.preferences.addons[__name__].preferences.bucket_name, file_name, s3_file_path)
        bpy.ops.wm.open_mainfile(filepath=s3_file_path)
        os.remove(s3_file_path)
        print("File Loaded Successfully")
    except NoCredentialsError:
        print("Credentials not available")
    except Exception as e:
        print(f"An error occurred: {e}")

def delete_file_from_s3(bucket, s3_file):
    """Delete a file from AWS S3."""
    try:
        s3_client.delete_object(Bucket=bucket, Key=s3_file)
        print(f"Deleted {s3_file} from {bucket}")
        return True
    except Exception as e:
        print(f"Failed to delete {s3_file}: {e}")
        return False

class S3IntegrationPanel(bpy.types.Panel):
    bl_label = "S3 Integration"
    bl_idname = "OBJECT_PT_s3integration"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "S3 Integration"

    def draw(self, context):
        """Draw the panel UI."""
        layout = self.layout
        scene = context.scene
        col = layout.column()

        # List all files in the scene's custom list
        for item in scene.my_list:
            row = col.row()
            row.label(text=item.name)
            row.operator("s3integration.load_file", text="Load").file_name = item.name
            row.operator("s3integration.delete_file", text="Delete").file_name = item.name

        layout.operator("scene.update_list", text="Update List")
        layout.operator("s3integration.upload", text="Upload to S3")

class MyPropGroup(bpy.types.PropertyGroup):
    name: bpy.props.StringProperty()

class UpdateFileListOperator(bpy.types.Operator):
    bl_idname = "scene.update_list"
    bl_label = "Update List"

    def execute(self, context):
        """Update the scene's list of files from S3."""
        initialize_s3_client()  # Ensure S3 client is initialized
        scene = context.scene
        items_to_add = list_files_in_bucket(bpy.context.preferences.addons[__name__].preferences.bucket_name)
        scene.my_list.clear()
        for item_name in items_to_add:
            new_item = scene.my_list.add()
            new_item.name = item_name
        return {'FINISHED'}

class UploadOperator(bpy.types.Operator):
    bl_idname = "s3integration.upload"
    bl_label = "Upload to S3"

    def execute(self, context):
        """Upload the current Blender file to S3."""
        initialize_s3_client()  # Ensure S3 client is initialized
        local_file_path = bpy.context.blend_data.filepath
        s3_file_name = bpy.path.basename(local_file_path)
        upload_to_aws(local_file_path, bpy.context.preferences.addons[__name__].preferences.bucket_name, s3_file_name)
        
        # Update the list of files in the panel after upload
        bpy.ops.scene.update_list()

        return {'FINISHED'}

class LoadFileOperator(bpy.types.Operator):
    bl_idname = "s3integration.load_file"
    bl_label = "Load File from S3"

    file_name: bpy.props.StringProperty()

    def execute(self, context):
        """Load a selected file from S3 into Blender."""
        initialize_s3_client()  # Ensure S3 client is initialized
        load_s3_file_into_blender(self.file_name)
        return {'FINISHED'}

class DeleteFileOperator(bpy.types.Operator):
    bl_idname = "s3integration.delete_file"
    bl_label = "Delete File from S3"

    file_name: bpy.props.StringProperty()

    def execute(self, context):
        """Delete a file from S3."""
        initialize_s3_client()  # Ensure S3 client is initialized
        success = delete_file_from_s3(
            bpy.context.preferences.addons[__name__].preferences.bucket_name,
            self.file_name
        )
        if success:
            # Update the file list after deletion if successful
            bpy.ops.scene.update_list()
        return {'FINISHED'}

classes = [
    S3IntegrationPreferences,
    S3IntegrationPanel,
    UploadOperator,
    LoadFileOperator,
    DeleteFileOperator,
    UpdateFileListOperator,
    MyPropGroup,
]

def register():
    """Register classes and properties."""
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.Scene.my_list = bpy.props.CollectionProperty(type=MyPropGroup)
    bpy.app.handlers.load_post.append(initialize_addon)
    initialize_s3_client()  # Initialize the S3 client

def unregister():
    """Unregister classes and properties."""
    bpy.app.handlers.load_post.remove(initialize_addon)
    for cls in classes:
        bpy.utils.unregister_class(cls)
    del bpy.types.Scene.my_list

def initialize_addon(dummy):
    """Initialize the add-on, e.g., populate the list of files."""
    scene = bpy.context.scene
    items_to_add = list_files_in_bucket(bpy.context.preferences.addons[__name__].preferences.bucket_name)
    scene.my_list.clear()
    for item_name in items_to_add:
        new_item = scene.my_list.add()
        new_item.name = item_name

if __name__ == "__main__":
    register()
