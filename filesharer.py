from filestack import Client
class FileSharer:

    def __init__(self, filepath, api_key):
        """
               Khởi tạo một đối tượng FileSharer với đường dẫn tập tin và khóa API.

               Tham số:
               - filepath (str): Đường dẫn đến tập tin cần chia sẻ.
               - api_key (str): Khóa API được sử dụng để tương tác với dịch vụ chia sẻ tập tin.
        """

        self.filepath = filepath
        self.api_key = api_key

    def share(self):
        """
                Thực hiện việc chia sẻ tập tin bằng cách tải lên tập tin và trả về liên kết đến tập tin đã chia sẻ.

                Trả về:
                - url (str): Liên kết đến tập tin đã chia sẻ.
        """

        client = Client(self.api_key)

        new_filelink = client.upload(filepath=self.filepath)
        return new_filelink.url
