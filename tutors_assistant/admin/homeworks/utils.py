def get_directory_path(instance, filename: str) -> str:
    """
    Директория файла
    """
    from admin.homeworks.models import ResourceMaterials, HomeworkAnswer, HomeworkFiles

    if isinstance(instance, HomeworkFiles):
        return "homework/files/{0}/{1}".format(instance.homework.id, filename)
    elif isinstance(instance, HomeworkAnswer):
        return "homework/files/{0}/answer/{1}".format(instance.homework.id, filename)
    elif isinstance(instance, ResourceMaterials):
        return "resourses/students/{0}/{1}".format(instance.student.full_name, filename)

    return "homework/other/files/{}".format(filename)
