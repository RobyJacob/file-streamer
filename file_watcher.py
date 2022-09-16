import os, csv, datetime


class FileWatcher:
    _files_processed = set()
    _transactions = dict()
    _product_reference = dict()

    @classmethod
    def _load_files(cls, base_path):
        with open(os.path.join(base_path, "ProductReference.csv")) as file_:
            rows = csv.DictReader(file_)

            cls._product_reference = {row["productId"]: {
                "productName": row["productName"],
                "productManufacturingCity": row["productManufacturingCity"]
            } for row in rows}

        for file in os.listdir(os.path.join(base_path, "transactions")):
            with open(os.path.join(base_path, "transactions", file)) as file_:
                rows = csv.DictReader(file_)

                cls._transactions.update({row["transactionId"]: {
                    "productId": row["productId"],
                    "transactionAmount": float(row["transactionAmount"]),
                    "transactionDatetime": datetime.datetime.strptime(row["transactionDatetime"],
                                                                      "%d/%m/%Y %H:%M")
                } for row in rows})

            cls._files_processed.add(file)

    @classmethod
    def _add_latest_file(cls, base_path, prefix=""):
        files = set(os.listdir(os.path.join(base_path, prefix)))

        latest_file_set = files - cls._files_processed

        if len(latest_file_set) == 0:
            return

        latest_file = latest_file_set.pop()

        with open(os.path.join(base_path, prefix, latest_file)) as file_:
            rows = csv.DictReader(file_)

            cls._transactions.update({row["transactionId"]: {
                "productId": row["productId"],
                "transactionAmount": float(row["transactionAmount"]),
                "transactionDatetime": datetime.datetime.strptime(row["transactionDatetime"],
                                                                  "%d/%m/%Y %H:%M")
            } for row in rows})

        cls._files_processed.add(latest_file)

    @classmethod
    def get_files_processed(cls):
        return cls._files_processed

    @classmethod
    def get_transactions(cls):
        return cls._transactions

    @classmethod
    def get_product_reference(cls):
        return cls._product_reference

    @classmethod
    def start(cls, base_path):
        import time

        if len(cls._files_processed) == 0:
            cls._load_files(base_path)
            last_processed_time = datetime.datetime.now()

        while True:
            while (datetime.datetime.now() - last_processed_time).seconds < 30:
                pass

            cls._add_latest_file(base_path, prefix="transactions")

            last_processed_time = datetime.datetime.now()
