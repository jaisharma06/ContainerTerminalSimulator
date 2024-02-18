class Container:
    """
    An Entity class that represents a container. contains the basic information of a container like container id.
    """

    def __init__(self, container_id: int, is_last_container: bool = False):
        """
        A constructor for the container class. it initialises the container_id of the container.
        @conainer_id: the id to be assigned to the container
        @is_last_containe: True if the container is loaded in the vessel at last else False.
        """
        self.container_id = container_id
        self.is_last_container = is_last_container

    def __str__(self) -> str:
        """
        An overload method that returns the name of the container in the format container_<container_id>.
        """
        return f'container_{self.container_id}'

    def get_name(self) -> str:
        """
        A method that returns the name of the container in the format container_<container_id>.
        """
        return f'container_{self.container_id}'
