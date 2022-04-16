def get_directory_path(instance, filename: str) -> str:
    """
    Директория файла
    """
    from admin.homeworks.models import ResourceMaterials, HomeworkAnswer

    if isinstance(instance, HomeworkAnswer):
        return "homework/files/{0}/{1}".format(instance.homework.id, filename)
    elif isinstance(instance, ResourceMaterials):
        return "resourses/students/{0}/{1}".format(instance.student.full_name, filename)

    return "/files/"
