""" Contains hidden functions to handle fixed file type """


from avro_to_python.classes.file import File


def _fixed_file(file: File, item: dict) -> None:
    """ Function to format enum field object

    Parameters
    ----------
        file: File
            file object containing information on enum file

    """
    # add symbol and default information
    file.size = item['size']
    file.default = item.get('default', None)
