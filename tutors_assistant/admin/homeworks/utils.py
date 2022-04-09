def get_directory_path(instance, filename) -> str:
    """
    Директория файла домашнего задания
    """
    return "homework/files/{0}/{1}".format(instance.homework.id, filename)
