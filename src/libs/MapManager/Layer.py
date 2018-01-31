class Layer:

    name = None
    width = None
    height = None
    encoding = None
    data = list()

    def __init__(self, xml):
        self.name = xml.get('name')
        self.width = xml.get('width')
        self.height = xml.get('height')

        # Init data if exist
        data = xml.find('data')
        self.encoding = data.get('encoding')
        self.__extract_data(data.text)

    def __extract_data(self, text):
        """
        Extract the data of the layout
        :param text: The layout's data
        :return: None
        """
        if self.encoding == 'csv':
            self.data = self.__extract_data_from_csv(text)

    @staticmethod
    def __extract_data_from_csv(csv):
        """
        Extract all the layout's data encoded in CSV
        :return:
        """
        data = list()
        text = csv.strip()

        for line in text.split('\n'):
            buffer = list()
            for tile_id in line.split(','):
                try:
                    buffer.append(int(tile_id))
                except ValueError:
                    pass

            data.append(buffer)

        return data
