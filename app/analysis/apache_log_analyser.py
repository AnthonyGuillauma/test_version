
from collections import Counter
from parse.apache_log_file import ApacheLogFile
from analysis.apache_log_filter import ApacheLogFilter

class ApacheLogAnalyser:
    """
    Class for calculating statistics of an Apache log file.

    Attributes:
        file (ApacheLogFile): The Apache log file.
    """

    def __init__(self, 
                 apache_log_file: ApacheLogFile, 
                 apache_log_filter: ApacheLogFilter):
        self.file = apache_log_file
        self.filter = apache_log_filter
        self.valid_entries = self.__get_entries_pass_filter()

    def __get_entries_pass_filter(self) -> list:
        valid_entries = []
        for entry in self.file.entries:
            if self.filter.pass_filter(entry):
                valid_entries.append(entry)
        return valid_entries
    
    def __get_items_rate(self, list_items: list, items_name: str) -> list:
        items_count = Counter(list_items)
        items_total = len(list_items)
        return [
            {items_name: item, "total": count, "percent": count / items_total * 100}
            for item, count in items_count.items()
        ]
    
    def __get_top_items(self, list_items: list, items_name: str, top_n: int) -> list:
        items_count = Counter(list_items)
        items_total = len(list_items)
        top_items = items_count.most_common(top_n)
        return [
            {items_name: item, "total": count, "percent": count / items_total * 100}
            for item, count in top_items
        ]

    def get_complete_analysis(self, show_detail: bool) -> dict:
        analysis = {}
        # Information of the file
        analysis["path"] = self.file.path
        # Detail of the analysis if asked
        if show_detail:
            analysis["analysis"] = {"filter": self.filter.to_dict()}
        analysis["stats"] = {}
        analysis["total_requests"] = self.get_total_requests()
        # Analysis of the file
        # Statistics related to clients
        clients_stats = {}
        clients_stats["total_unique_ip"] = self.get_total_unique_ip()
        clients_stats["top_ips"] = self.get_top_ips(3)
        analysis["stats"]["clients"] = clients_stats
        # Statistics related to requests
        requests_stats = {}
        requests_stats["http_method_rate"] = self.get_http_method_rate()
        requests_stats["top_urls"] = self.get_top_urls(3)
        analysis["stats"]["requests"] = requests_stats
        # Statistics related to responses 
        responses_stats = {}
        responses_stats["status_code_rate"] = self.get_status_code_rate()
        responses_stats["status_code_classes_rate"] = self.get_status_code_classes_rate()
        analysis["stats"]["responses"] = responses_stats
        # Statistics related to metadatas
        metadatas_stats = {}
        metadatas_stats["os_rate"] = self.get_os_rate()
        metadatas_stats["browser_rate"] = self.get_browser_rate()
        metadatas_stats["type_device_rate"] = self.get_type_device_rate()
        metadatas_stats["bot_rate"] = self.get_bot_rate()
        analysis["stats"]["metadatas"] = metadatas_stats
        # Return the analysis
        return analysis

    def get_total_requests(self) -> int:
        """
        Returns the total number of requests in the log file.

        Returns:
            int: The total number of requests.
        """
        #Return the number of entries in the file
        return len(self.valid_entries)

    def get_total_unique_ip(self) -> int:

        unique_ip_count = Counter(entry.client_info.client_ip for entry in self.valid_entries)
        return len(unique_ip_count.keys())
    
    def get_top_ips(self, top_n: int) -> dict:
        """
        Returns the top 'n' IPs with the most requests.

        Args:
            top_n (int): The number of top IPs to return.

        Returns:
            list: A sorted list of tuples, each containing an IP and the number of requests.
        """
        ips = [entry.client_info.client_ip for entry in self.valid_entries]
        return self.__get_top_items(ips, "ip", top_n)

    def get_http_method_rate(self) -> dict:
        http_methods = [entry.request_info.method for entry in self.valid_entries]
        http_methods_rate = self.__get_items_rate(http_methods, "method")
        return http_methods_rate

    def get_top_urls(self, top_n: int) -> dict:
        urls = [entry.request_info.url for entry in self.valid_entries]
        return self.__get_top_items(urls, "url", top_n)

    def get_status_code_rate(self) -> list:
        """
        Returns the number of requests for each HTTP status code.

        Returns:
            list: A sorted list of dict containing the status code and its request count.
        """
        status_code = [entry.response_info.status_code for entry in self.valid_entries]
        status_code_rate = self.__get_items_rate(status_code, "code")
        return sorted(status_code_rate, key=lambda x: x["code"])

    def get_status_code_classes_rate(self) -> dict:
        """
        Returns the number of requests with the percent for each status code classes.

        Returns:
            dict: A dict containing the request count and the percent for each classes.
        """
        classes = [entry.response_info.get_status_code_class() for entry in self.valid_entries]
        classes_rate = self.__get_items_rate(classes, "class")
        return sorted(classes_rate, key= lambda x: x["class"], reverse=True)

    def get_browser_rate(self) -> dict:
        browsers = [entry.metadata_info.get_browser() for entry in self.valid_entries]
        return self.__get_items_rate(browsers, "browser")
    
    def get_os_rate(self) -> dict:
        os = [entry.metadata_info.get_os() for entry in self.valid_entries]
        return self.__get_items_rate(os, "os")
    
    def get_type_device_rate(self) -> dict:
        devices = [entry.metadata_info.get_type_device() for entry in self.valid_entries]
        return self.__get_items_rate(devices, "type_device")
    
    def get_bot_rate(self) -> dict:
        total_requests = self.get_total_requests()
        bots_count = 0
        for entry in self.valid_entries:
            if entry.metadata_info.is_bot():
                bots_count += 1
        return {"total": bots_count, "percent": bots_count / total_requests * 100}