from file_watcher import FileWatcher


class Products:

    @staticmethod
    def get_product(product_id):
        return FileWatcher.get_product_reference().get(product_id, None)

    @staticmethod
    def get_products():
        return FileWatcher.get_product_reference()