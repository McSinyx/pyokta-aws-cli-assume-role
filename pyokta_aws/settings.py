from pyokta_aws import utils


class Settings(object):
    """Object that manages the configuration for pyokta_aws.

    This object can only be instantiated with keyword arguments.

    For example,

    .. code-block:: python

        Settings('myprofile', username='fakeusername')

    Will raise a :class:`TypeError`. Instead, you would want

    .. code-block:: python

        Settings(profile='myprofile', username='fakeusername')
    """

    @utils.no_positional(allow_self=True)
    def __init__(self,
                 profile=None,
                 username=None, password=None,
                 okta_org=None,
                 okta_aws_app_url=None,
                 sts_duration=None,
                 config_file='~/.pyokta_aws/config',
                 verbose=False,
                 interactive=True,
                 **ignored_kwargs
                 ):
        """Initialize our settings instance.

        :param str profile:
            AWS cli profile to use.

            This defaults to ``default``.
        :param str username:
            The username used to authenticate to Okta.
        :param str password:
            The password used to authenticate to Okta.
        :param str okta_org:
            The Okta Org base url.
        :param str config_file:
            The path to the configuration file to use.

            This defaults to ``~/.pyokta_aws/config``.
        :param bool verbose:
            Show verbose output.
        """
        self.profile = profile
        self.username = username
        self.password = password
        self.okta_org = okta_org
        self.okta_aws_app_url = okta_aws_app_url
        self.sts_duration = sts_duration
        self.config_file = config_file
        self.verbose = verbose

    @staticmethod
    def register_argparse_arguments(parser):
        """Register the arguments for argparse."""
        parser.add_argument(
            "-p", "--profile",
            action=utils.EnvironmentDefault,
            env="OKTA_AWS_PROFILE",
            required=False,
            help="AWS profile to use for authentication. "
                 "Example: myorg.okta.com "
                 "(Can also be set via %(env)s environment variable.)",
        )
        parser.add_argument(
            "-o", "--okta-org",
            action=utils.EnvironmentDefault,
            env="OKTA_ORG",
            required=False,
            help="Your Okta Org base URL. "
                 "Example: myorg.okta.com "
                 "(Can also be set via %(env)s environment variable.)",
        )
        parser.add_argument(
            "-a", "--okta-aws-app-url",
            action=utils.EnvironmentDefault,
            env="OKTA_AWS_APP_URL",
            required=False,
            help="The url for the Okta AWS app url. "
                 "Example: https://myorg.okta.com/home/amazon_aws/1a2b3c4d5e "
                 "(Can also be set via %(env)s environment variable.)",
        )
        parser.add_argument(
            "-r", "--aws-role-to-assume",
            action=utils.EnvironmentDefault,
            env="OKTA_AWS_ROLE_TO_ASSUME",
            required=False,
            help="The AWS role to assume. "
                 "Consists of aws account id, role, and okta user "
                 "(username or email depending on okta app setup). "
                 "Example: <aws_accnt_id>/AWSAdmin/<okta_user> "
                 "(Can also be set via %(env)s environment variable.)",
        )
        parser.add_argument(
            "-u", "--username",
            action=utils.EnvironmentDefault,
            env="OKTA_USERNAME",
            required=False,
            help="The username to authenticate to the repository "
                 "(package index) as. (Can also be set via "
                 "%(env)s environment variable.)",
        )
        parser.add_argument(
            "-pw", "--password",
            action=utils.EnvironmentDefault,
            env="OKTA_PASSWORD",
            required=False,
            help="The password to authenticate to the repository "
                 "(package index) with. (Can also be set via "
                 "%(env)s environment variable.)",
        )
        parser.add_argument(
            "-s", "--sts-duration",
            action=utils.EnvironmentDefault,
            env="OKTA_STS_DURATION",
            default=3600,
            help="The AWS session duration. "
                 "(Can also be set via %(env)s environment variable.)",
        )
        parser.add_argument(
            "-c", "--config-file",
            action=utils.EnvironmentDefault,
            env="PYOKTA_AWS_CONFIG",
            default="~/.pyokta_aws/config",
            help="The pyokta_aws config file to use. "
                 "This is not referring to awscli config. "
                 "(Can also be set via %(env)s environment variable.)",
        )
        parser.add_argument(
            "--non-interactive",
            default=False,
            required=False,
            action="store_true",
            help="Run command non-interactively. "
                 "Requires that all settings are set "
                 "via cli, env vars, or config file.",
        )
        parser.add_argument(
            "--verbose",
            default=False,
            required=False,
            action="store_true",
            help="Show verbose output.",
        )

    @classmethod
    def from_argparse(cls, args):
        """Generate the Settings from parsed arguments."""
        settings = vars(args)
        settings['interactive'] = not settings.pop('non_interactive')
        if settings['verbose']:
            print("\nUsing the following settings...")
            for x, y in settings.items():
                print('{:.<19s}: {}'.format(x, str(y) if x is not 'password' else '<redacted>'))
        return cls(**settings)