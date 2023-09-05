""" Contains hidden functions to handle fixed file type """


from avro_to_rust_etp.classes.file import File


def _meta_file(file: File, item: dict, keys: dict) -> None:
    """ Function to format meta field object

    Parameters
    ----------
        file: File
            file object containing information on enum file
        item: dict
            object to be turned into a file
        keys: dict
            array of keys to be processed
        queue: list
            array of file objects to be processed

    """

    for k in keys:


        #shoud be a  primitive type ?
        field = _primitive_type(item[k])

        #file.meta_fields[].append((k, item[k]))
