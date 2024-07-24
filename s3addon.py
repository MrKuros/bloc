bl_info = {
    "name": "Blender S3 Integration",
    "author": "Kashish aka MrKuros",
    "version": (1, 0),
    "blender": (4, 1, 0),
    "location": "View3D > Tool Shelf > S3 Integration",
    "description": "Upload and download Blender files to/from AWS S3",
    "category": "Development",
}

import bpy
import os
import boto3
from botocore.exceptions import NoCredentialsError

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
        layout = self.layout
        layout.prop(self, "access_key")
        layout.prop(self, "secret_key")
        layout.prop(self, "region_name")
        layout.prop(self, "bucket_name")

def get_s3_client():
    prefs = bpy.context.preferences.addons[__name__].preferences
    return boto3.client(
        's3',
        aws_access_key_id=prefs.access_key,
        aws_secret_access_key=prefs.secret_key,
        region_name=prefs.region_name
    )

def upload_to_aws(local_file, bucket, s3_file):
    s3 = get_s3_client()
    try:
        s3.upload_file(local_file, bucket, s3_file)
        print("Upload Successful")
        return True
    except FileNotFoundError:
        print("The file was not found")
        return False
    except NoCredentialsError:
        print("Credentials not available")
        return False

def list_files_in_bucket(bucket):
    s3 = get_s3_client()
    send_list = []
    try:
        s3_resource = boto3.resource('s3')
        my_bucket = s3_resource.Bucket(bucket)
        for obj in my_bucket.objects.all():
            send_list.append(obj.key)
    except Exception as e:
        print(e)
    return send_list

def download_from_s3(bucket, s3_file, local_file):
    s3 = get_s3_client()
    try:
        s3.download_file(bucket, s3_file, local_file)
        print("Download Successful")
    except Exception as e:
        print(e)

def load_s3_file_into_blender(file_name):
    prefs = bpy.context.preferences.addons[__name__].preferences
    try:
        s3_file_path = f'/tmp/{file_name}'
        download_from_s3(prefs.bucket_name, file_name, s3_file_path)
        bpy.ops.wm.open_mainfile(filepath=s3_file_path)
        os.remove(s3_file_path)
    except NoCredentialsError:
        print("Credentials not available")
    except Exception as e:
        print(f"An error occurred: {e}")

class S3IntegrationPanel(bpy.types.Panel):
    bl_label = "S3 Integration"
    bl_idname = "OBJECT_PT_s3integration"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "S3 Integration"

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        col = layout.column()
        
        for item in scene.my_list:
            row = col.row()
            row.label(text=item.name)
            row.operator("s3integration.load_file", text="Load").file_name = item.name
        
        layout.operator("scene.update_list", text="Update List")
        layout.operator("s3integration.upload", text="Upload to S3")

class MyPropGroup(bpy.types.PropertyGroup):
    name: bpy.props.StringProperty()

class UpdateFileListOperator(bpy.types.Operator):
    bl_idname = "scene.update_list"
    bl_label = "Update List"

    def execute(self, context):
        scene = context.scene
        prefs = bpy.context.preferences.addons[__name__].preferences
        items_to_add = list_files_in_bucket(prefs.bucket_name)
        scene.my_list.clear()
        
        for item_name in items_to_add:
            new_item = scene.my_list.add()
            new_item.name = item_name
        return {'FINISHED'}

class UploadOperator(bpy.types.Operator):
    bl_idname = "s3integration.upload"
    bl_label = "Upload to S3"   
    
    def execute(self, context):
        prefs = bpy.context.preferences.addons[__name__].preferences
        local_file_path = bpy.context.blend_data.filepath
        s3_file_name = bpy.path.basename(local_file_path)
        upload_to_aws(local_file_path, prefs.bucket_name, s3_file_name)
        return {'FINISHED'}

class LoadFileOperator(bpy.types.Operator):
    bl_idname = "s3integration.load_file"
    bl_label = "Load File from S3"

    file_name: bpy.props.StringProperty()

    def execute(self, context):
        load_s3_file_into_blender(self.file_name)
        return {'FINISHED'}

classes = [
    S3IntegrationPreferences,
    S3IntegrationPanel,
    UploadOperator,
    LoadFileOperator,
    UpdateFileListOperator,
    MyPropGroup,
]

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.Scene.my_list = bpy.props.CollectionProperty(type=MyPropGroup)
    bpy.app.handlers.load_post.append(initialize_addon)

def unregister():
    bpy.app.handlers.load_post.remove(initialize_addon)
    for cls in classes:
        bpy.utils.unregister_class(cls)
    del bpy.types.Scene.my_list

def initialize_addon(dummy):
    scene = bpy.context.scene
    prefs = bpy.context.preferences.addons[__name__].preferences
    items_to_add = list_files_in_bucket(prefs.bucket_name)
    scene.my_list.clear()
    for item_name in items_to_add:
        new_item = scene.my_list.add()
        new_item.name = item_name

if __name__ == "__main__":
    register()

