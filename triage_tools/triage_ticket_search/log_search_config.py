class LogSearchConfigItem:
    def __init__(self, path_regex:str, content_regex:str, label:str):
        self.path_regex = path_regex
        self.content_regex = content_regex
        self.label = label

class LogSearchConfig:

    def __init__(self):
        self.items = []

    def add_item(self, path_regex:str, content_regex:str, label:str):
        self.items += [LogSearchConfigItem(path_regex, content_regex, label)]

class ConfigParser:

    @staticmethod
    def get_jira_queries(config_json) -> list[str]:
        queries = []

        for value in config_json['jira_query_items']:
            queries += [value]
        return queries

    @staticmethod
    def get_log_search_config(config_json) -> "LogSearchConfig":
        logSearchConfig = LogSearchConfig()
        for log_search_item in config_json['logs_search_items']:
            logSearchConfig.add_item(
                log_search_item['path_regex'],
                log_search_item['content_regex'],
                log_search_item['label']
            )
        return logSearchConfig
