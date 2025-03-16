"""
    Main file
"""
from cli.cli_argument_parser import *
from parse.apache_log_parser import ApacheLogParser, InvalidFormatApacheLogException
from analysis.apache_log_analyser import ApacheLogAnalyser
from analysis.apache_log_filter import ApacheLogFilter
from export.exporter import Exporter, ExportationException

if __name__ == "__main__":
    try:
        #Arguments
        argument_parser = CliArgumentParser("Analyse Apache access log.")
        # Get arguments
        args = argument_parser.parse()
        # Verbose mode
        if (args.verbose):
            print("Mode verbeux activé.")
            print(f'File : {args.file_path}')
            print("Start of the analyse...")
        # Analyse the file
        # Parse Apache log file
        apache_log_parser = ApacheLogParser(args.file_path)
        apache_log_file = apache_log_parser.get_file_parsed()
        if (args.verbose):
            print(f"{len(apache_log_file.entries)} lines analysed.")
        # Filter for the analysis
        filter = ApacheLogFilter(args.status, args.date, args.ip, args.method)
        # Analyse the Apache log file parsed
        analyser = ApacheLogAnalyser(apache_log_file, filter)
        analysis = analyser.get_complete_analysis(args.details)
        # Export the analysis (if --nooverride is given, disable override)
        exporter = Exporter(args.output, not args.nooverride)
        exporter.export_to_json(analysis)
    # Error management
    except CliArgumentException as ex:
        print("/!\\ Error with the arguments given. /!\\")
        print(ex)
    except InvalidFormatApacheLogException as ex:
        print("/!\\ Error with the Apache log file. /!\\")
        print(ex)
    except ExportationException as ex:
        print("/!\\ Error in the analysis exportation /!\\")
        print(ex)
    except Exception as ex:
        print("/!\\ A fatal error occured. /!\\")
        print(ex)