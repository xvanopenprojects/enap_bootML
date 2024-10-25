import os
from dataclasses import dataclass

from dotenv import load_dotenv


@dataclass
class Storage:
    """
    Uma forma simplificada de acessar os dados ou localmente ou na azure.
    para isso precisa estar preenchido no .env a variável LOCAL_RUN
    com o valor "local" ou "azure".

    LOCAL_RUN="local"
    LOCAL_RUN="azure"

    Se Azure precisará de mais duas variável

    AZURE_ACCOUNT_NAME="stomgiprd"
    AZURE_DEFAULT_CONTAINER_NAME="bronze"

    ou setar isso logo a após a construção da classe
    """

    account_name: str = ""
    container_name: str = ""
    directory_name: str = ""
    directory_path: str = ""
    local: str = ""

    # Sobrescrevendo o comportamento padrão do getter e setter
    def get_directory_name(self):
        """
            Sobrescrevendo o comportamento padrão do get
        :return: str
        """
        return f"{self.directory_path}{self.directory_name}"

    def get_local(self):
        """
            Se vazio pega o local do .env
        :return: str
        """
        if self.local == "":
            self.local = os.getenv("LOCAL_RUN")
        return self.local

    def get_account_name(self):
        """
            Se vazio pega o local do .env
        :return: str
        """
        if self.local != "azure":
            raise SystemError("Ambiente não azure")
        if self.account_name == "":
            self.account_name = os.getenv("AZURE_ACCOUNT_NAME")
        return self.account_name

    def get_container_name(self):
        """
            Se vazio pega o local do .env
        :return: str
        """
        if self.local != "azure":
            raise SystemError("Ambiente não azure")
        if self.container_name == "":
            self.container_name = os.getenv("AZURE_DEFAULT_CONTAINER_NAME")
        return self.container_name

    def set_directory_name(self, directory_name):
        """
            Pega o path / directory_name
        :param directory_name: str
        :return: str
        """
        self.directory_name = directory_name
        local = self.get_local()
        path = os.getenv("ROOT_PATH")
        if local == "azure":
            account_name = self.get_account_name()
            container_name = self.get_container_name()
            data = {
                "account_name": account_name,
                "container_name": container_name,
            }
            path = f"{path.format_map(data)}/"
        # if local == "local": não faça nada
        self.directory_path = path
        return self.get_directory_name()

    # Construtor
    def __init__(self, directory_name: str = "", container_name: str = ""):
        """
            Para iniciar instanciar essa classe vc passa o nome do arquivo...
            Se for localmente não é necessário container_name...
            Caso contrário, ele é obrigatório
        :param directory_name: str, default = ""
        :param container_name: nome do container: "bronze", "prata", "ouro" ou "outros"
        """
        load_dotenv()
        self.container_name = container_name
        self.set_directory_name(directory_name)

    def get_path(self, file: str):
        """
            retorna o arquivo com o caminho completo de acesso
        :param file: str
        :return:
        """
        return f"{self.get_directory_name()}/{file}"
