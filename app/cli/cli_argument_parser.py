"""
    CLI manage.
"""

from argparse import ArgumentParser, Namespace
from re import match
from datetime import datetime

class CliArgumentException(Exception):

    def __init__(self, *args):
        super().__init__(*args)


class CliArgumentParser(ArgumentParser):

    def __init__(self, description: str):
        super().__init__(description=description, allow_abbrev=False)
        self.__set_arguments()

    def __set_arguments(self):
        """Defines all command-line arguments."""
        # Required arguments
        self.add_argument('file_path', help='Path of the Apache access.log')
        # Optional arguments
        self.add_argument("-o", "--output", type=str, default="./apache_stats.json", help="Output file")
        self.add_argument("-f", "--format", choices=["json"], default="json", help="Output format")
        self.add_argument("-v", "--verbose", action="store_true", help="Enable verbose mode")
        self.add_argument("-n", "--nooverride", action="store_true", help="Force the creation of the output file.")
        self.add_argument("--details", action="store_true", help="Put the detail of analysis in the output file.")
        # Filter arguments
        self.add_argument("-s", "--status", type=int, help="")
        self.add_argument("-d", "--date", type=str, help="DD/MM/YYYY")
        self.add_argument("-i", "--ip", type=str, help="")
        self.add_argument("-m", "--method", choices=["GET", "POST", "PUT", "DELETE"], type=str, help="")

    def parse(self) -> Namespace :
        """Parses arguments and performs basic validation if needed."""
        # Parse arguments
        try:
            args = self.parse_args()
        except Exception as ex:
            raise CliArgumentException(str(ex))
        # Parse date filter if given
        if args.date:
            try:
                args.date = datetime.strptime(args.date, "%d/%m/%Y")
            except ValueError:
                raise CliArgumentException("The format of the date filter isn't valid.")
        # Check logic between file and format
        if not args.output.endswith(f".{args.format}"):
            raise CliArgumentException(f"The output file {args.output} isn't a {args.format} file.")
        # Check logic for the status code if given
        if args.status:
            if not 100 <= args.status <= 599:
                raise CliArgumentException(f"The status code {args.status} isn't valid.")
        # Check logic for the IP if given (only IPv4 are acceptable)
        if args.ip:
            if not bool(match(r"^((25[0-5]|(2[0-4]|1\d|[1-9]|)\d)\.?\b){4}$", args.ip)):
                raise CliArgumentException(f"Only IPv4 can be used to filter.")
        return args