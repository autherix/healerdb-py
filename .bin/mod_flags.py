import os, sys
from absl import app
from absl import flags
from absl.testing import absltest

# function ArgParser to parse the arguments passed to the script
def ArgParser(argv):
    ## Flags
    FLAGS = flags.FLAGS
    flags.DEFINE_string(name="config", default="config/config.yaml", help="The path to the config file for the connection to DB, logging, etc", short_name="c")
    flags.DEFINE_enum(name="function", enum_values=["ping", "list", "add", "remove", "update", "search", "export", "import"], default="ping", help="The functionality to run", short_name="f", case_sensitive=False)
    # flags.DEFINE_string(name="function", default="ping", help="The functionality to run", short_name="f")
    flags.DEFINE_enum(name="type", enum_values=["db", "target", "domain", "subdomain", "directory", "file", "parameter", "ip"], default="db", help="The type of the data to run the function on", short_name="t", case_sensitive=False)
    # flags.DEFINE_enum_class(name="type", enum_class=myutils.DataType, default=myutils.DataType.db, help="The type of the data to run the function on", short_name="t", case_sensitive=False, multiple=False, allow_override=False)
    flags.DEFINE_string(name="database", default="", help="The database to run the function on")
    flags.DEFINE_string(name="target", default="", help="The target (collection_name) to run the function on")
    flags.DEFINE_string(name="domain", default="", help="The domain to run the function on")
    flags.DEFINE_string(name="subdomain", default="", help="The subdomain to run the function on")
    flags.DEFINE_string(name="directory", default="", help="The directory to run the function on")
    flags.DEFINE_string(name="file", default="", help="The file to run the function on")
    flags.DEFINE_string(name="parameter", default="", help="The parameter to run the function on")
    flags.DEFINE_string(name="ip", default="", help="The ip to run the function on")

    # Parse the flags
    try:
        FLAGS(argv)
    except flags.Error as e:
        print('%s Usage: %s ARGS\\n%s' % (e, argv[0], FLAGS))
        sys.exit(1)

    # Return the flags
    return FLAGS