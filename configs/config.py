import os
import configparser


class AppConfig:
    def __init__(self):
        self.config_file = os.path.join(os.path.dirname(__file__), "config.ini")
        self.config = configparser.ConfigParser()

    def load_config(self):
        try:
            self.config.read(self.config_file)
        except configparser.Error as e:
            raise Exception(f"Error reading configuration file: {str(e)}")

    def __getattr__(self, name):
        self.load_config()
        if name in self.config:
            return ConfigSection(self.config[name])
        else:
            raise AttributeError(f"'AppConfig' object has no attribute '{name}'")


class ConfigSection:
    def __init__(self, section):
        self.section = section

    def __getattr__(self, name):
        if name in self.section:
            return self.section[name]
        else:
            raise AttributeError(f"'ConfigSection' object has no attribute '{name}'")


# Пример использования
if __name__ == "__main__":
    app_config = AppConfig()

    try:
        # Обращение к конфигурационным данным
        print("Database Host:", app_config.psql.host)
        print("Database Port:", app_config.psql.port)
        print("billing_documents custom_address:", app_config.billing_documents.custom_address)

    except AttributeError as e:
        print(f"Attribute Error: {str(e)}")
