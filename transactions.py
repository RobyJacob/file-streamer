from file_watcher import FileWatcher


class Transactions:

    @staticmethod
    def get_transaction(transaction_id):
        return FileWatcher.get_transactions().get(transaction_id, None)

    @staticmethod
    def get_transactions():
        return FileWatcher.get_transactions()

    @staticmethod
    def get_summary_by_products(last_n_days):
        import datetime

        last_nth_day = datetime.datetime.now() - datetime.timedelta(days=int(last_n_days))
        summary = dict()

        for id, data in Transactions.get_transactions().items():
            if data.get("transactionDatetime") >= last_nth_day:
                agg_key = data.get("productId")

                if agg_key not in summary:
                    summary[agg_key] = data.get("transactionAmount")
                else:
                    summary[agg_key] += data.get("transactionAmount")

        return summary

    @staticmethod
    def get_summary_by_city(last_n_days):
        import datetime

        from products import Products

        last_nth_day = datetime.datetime.now() - datetime.timedelta(days=int(last_n_days))
        summary, product_city_map = dict(), dict()

        for id, data in Transactions.get_transactions().items():
            if data.get("transactionDatetime") >= last_nth_day:
                product_id = data.get("productId")

                agg_key = Products.get_product(product_id).get("productManufacturingCity")

                product_city_map[product_id] = agg_key

                if agg_key not in summary:
                    summary[agg_key] = data.get("transactionAmount")
                else:
                    summary[agg_key] += data.get("transactionAmount")

        return summary
