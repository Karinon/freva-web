from pathlib import Path
import os
import logging
import sys
import pymysql
import ldap
import django_auth_ldap.config as ldap_cfg
from django_auth_ldap.config import LDAPSearch, NestedGroupOfNamesType
import configparser
import toml
from django.urls import reverse_lazy
from evaluation_system.misc import config

freva_share_path = Path(os.environ["EVALUATION_SYSTEM_CONFIG_FILE"]).parent
web_config_path = freva_share_path / "web" / "freva_web_conf.toml"
pymysql.version_info = (1, 4, 2, "final", 0)
pymysql.install_as_MySQLdb()


def _get_conf_key(config, key, alternative, is_file=True):
    """Check config of freva_web config."""
    if not is_file:
        return config.get(key, alternative)
    value = Path(config.get(key, alternative))
    if value.exists():
        return value
    return Path(alternative)


try:
    with open(web_config_path) as f:
        web_config = toml.load(f)
except FileNotFoundError:
    web_config = {}
# Is this a development instance? Set this to True on development/master
# instances and False on stage/prod.
DEV = bool(int(os.environ.get("DEV_MODE", 0)))
PROJECT_ROOT = os.environ.get("PROJECT_ROOT", None) or str(
    Path(__file__).absolute().parents[2]
)
STATIC_URL = "/static/"
if not DEV:
    STATIC_ROOT = str(Path(PROJECT_ROOT) / "static")
_logo = _get_conf_key(
    web_config,
    "INSTITUTION_LOGO",
    Path(PROJECT_ROOT) / "static" / "img/thumb-placeholder.png",
)
INSTITUTION_LOGO = f"{STATIC_URL}/img/{_logo.name}"
FREVA_LOGO = f"{STATIC_URL}/img/by_freva_transparent.png"
MAIN_COLOR = _get_conf_key(web_config, "MAIN_COLOR", "Tomato", False)
BORDER_COLOR = _get_conf_key(web_config, "BORDER_COLOR", "#6c2e1f", False)
HOVER_COLOR = _get_conf_key(web_config, "HOVER_COLOR", "#d0513a", False)
HOMEPAGE_TEXT = web_config.get(
    "HOMEPAGE_TEXT",
    (
        "Lorem ipsum dolor sit amet"
        ", consectetur adipiscing elit"
        ", sed do eiusmod tempor incididunt ut"
        "labore et dolore magna aliqua. Ut enim"
        "ad minim veniam, quis nostrud exercitation"
        "ullamco laboris nisi ut aliquip ex ea commodo"
        "consequat. Duis aute irure dolor in reprehenderit"
        "in voluptate velit esse cillum dolore eu fugiat"
        "nulla pariatur. Excepteur sint occaecat cupidatat"
        "non proident, sunt in culpa qui officia deserunt"
        "mollit anim id est laborum."
    ),
)
IMPRINT = web_config.get(
    "IMPRINT",
    [
        "ANAIS - RegIKlim",
        "German Climate Computing Center (DKRZ)",
        "Bundesstr. 45a",
        "20146 Hamburg",
        "Germany",
    ],
)
HOMEPAGE_HEADING = web_config.get("HOMEPATE_HEADING", "Lorem ipsum dolor.")
ABOUT_US_TEXT = web_config.get("ABOUT_US_TEXT", "Hello world, this is freva.")
CONTACTS = web_config.get("CONTACTS", ["help@freva.org"])
if isinstance(CONTACTS, str):
    CONTACTS = [CONTACTS]
##########
# Here you can customize the footer and texts on the startpage
##########
INSTITUTION_NAME = web_config.get("INSTITUTION_NAME", "Freva")
##################################################
##################################################
# SETTING FOR LDAP
# http://pythonhosted.org//django-auth-ldap/
##################################################
##################################################
# The server for LDAP configuration
AUTH_LDAP_SERVER_URI = web_config.get(
    "AUTH_LDAP_SERVER_URI", "ldap://mldap0.hpc.dkrz.de, ldap://mldap1.hpc.dkrz.de"
)
AUTH_LDAP_START_TLS = web_config.get("AUTH_LDAP_START_TLS", True)
# The directory with SSL certificates
CA_CERT_DIR = str(web_config_path.parent)
# the only allowd group
ALLOWED_GROUP = web_config.get("ALLOWED_GROUP", "ch1187")
# Require a ca certificate
AUTH_LDAP_GLOBAL_OPTIONS = {
    ldap.OPT_X_TLS_REQUIRE_CERT: ldap.OPT_X_TLS_DEMAND,  # TPYE OF CERTIFICATION
    ldap.OPT_X_TLS_CACERTDIR: CA_CERT_DIR,  # PATH OF CERTIFICATION
}
# this is not used by django directly, but we use it for
# python-ldap access, as well.
LDAP_USER_BASE = web_config.get("LDAP_USER_BASE", "cn=users,cn=accounts,dc=dkrz,dc=de")
LDAP_GROUP_BASE = web_config.get(
    "LDAP_GROUP_BASE", "cn=groups,cn=accounts,dc=dkrz,dc=de"
)
# Verify the user by bind to LDAP
AUTH_LDAP_USER_DN_TEMPLATE = "uid=%%(user)s, %s" % LDAP_USER_BASE
# keep the authenticated user for group search
AUTH_LDAP_BIND_AS_AUTHENTICATING_USER = True
# ALLOWED_GROUP_MEMBER user only
AUTH_LDAP_REQUIRE_GROUP = "cn=%s,cn=groups,cn=accounts,dc=dkrz,dc=de" % ALLOWED_GROUP
AUTH_LDAP_USER_ATTR_MAP = {
    "email": "mail",
    "last_name": "sn",
    "first_name": "givenname",
}
AUTH_LDAP_GROUP_SEARCH = LDAPSearch(
    LDAP_GROUP_BASE, ldap.SCOPE_SUBTREE, "(objectClass=groupOfNames)"  # USE SUB
)
AUTH_LDAP_GROUP_TYPE = NestedGroupOfNamesType()
AUTH_LDAP_MIRROR_GROUPS = True
# agent user for LDAP
LDAP_USER_DN = web_config.get(
    "LDAP_USER_DN", "uid=dkrzagent,cn=sysaccounts,cn=etc,dc=dkrz,dc=de"
)
LDAP_USER_PW = web_config.get("LDAP_USER_PW", "dkrzprox")
LDAP_MIKLIP_GROUP_FILTER = f"(cn={ALLOWED_GROUP})"
LDAP_MODEL = "django_evaluation.ldaptools.MiklipUserInformation"
##################################################
##################################################
# END SETTING FOR LDAP
##################################################
##################################################
# the host to start the scheduler
SCHEDULER_HOSTS = web_config.get("SCHEDULER_HOST", ["mistral.dkrz.de"])
if isinstance(SCHEDULER_HOSTS, str):
    SCHEDULER_HOSTS = [SCHEDULER_HOSTS]
# temporary directory for tailed scheduler files
TAIL_TMP_DIR = "/tmp/tail/"
# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    os.path.join(PROJECT_ROOT, "static_root"),
    ("assets/bundles", os.path.join(PROJECT_ROOT, "assets", "bundles")),
)
if not DEV:
    config.reloadConfiguration()
    STATICFILES_DIRS += (("preview", config.get("preview_path")),)
# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
    "django.contrib.staticfiles.finders.DefaultStorageFinder",
)
config.reloadConfiguration()
db_name = config.get("db.db")
db_user = config.get("db.user")
db_password = config.get("db.passwd")
db_host = config.get("db.host")
db_port = config.get("db.port")
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": db_name,
        "USER": db_user,
        "PASSWORD": db_password,  #'miklip',
        "HOST": db_host,  #'wwwdev-miklip',
        "PORT": db_port,
        "OPTIONS": {"charset": "utf8mb4"},
    },
}
# register the LDAP authentication backend
AUTHENTICATION_BACKENDS = (
    "django.contrib.auth.backends.ModelBackend",
    "django_auth_ldap.backend.LDAPBackend",
)

REDIS_HOST = web_config.get("REDIS_HOST", "127.0.0.1")
REDIS_PORT = web_config.get("REDIS_PORT", 6379)

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.redis.RedisCache",
        "LOCATION": f"redis://{REDIS_HOST}:{REDIS_PORT}",
    },
}

HOME_DIRS_AVAILABLE = web_config.get("HOME_DIRS_AVAILABLE", False)

# SECURITY WARNING: don't run with debug turned on in production!
# Debugging displays nice error messages, but leaks memory. Set this to False
# on all server instances and True only for development.
DEBUG = TEMPLATE_DEBUG = True
# Hosts/domain names that are valid for this site; required if DEBUG is False
# See https://docs.djangoproject.com/en/1.5/ref/settings/#allowed-hosts
ALLOWED_HOSTS = web_config.get("ALLOWED_HOSTS", ["localhost", "127.0.0.1"])
if isinstance(ALLOWED_HOSTS, str):
    ALLOWED_HOSTS = [ALLOWED_HOSTS]

# Provide a full list of all valid hosts (including the http(s):// prefix) which are expected
CSRF_TRUSTED_ORIGINS = web_config.get("CSRF_TRUSTED_ORIGINS", ["http://localhost"])

# path to the site packages used:
VENV_PYTHON_DIR = "/usr/bin/python3"
# Path to miklip-logo
MIKLIP_LOGO = STATIC_URL + "img/miklip-logo.png"
LOAD_MODULE = " "
FREVA_BIN = web_config.get("FREVA_BIN", os.path.join(sys.exec_prefix, "bin"))
NCDUMP_BINARY = os.path.join(FREVA_BIN, "metadata-inspector") + " --html"
# result to show at guest tour
GUEST_TOUR_RESULT = int(web_config.get("GUEST_TOUR_RESULT", 105))
SHELL_IN_A_BOX = "/shell/"
WEBPACK_LOADER = {
    "DEFAULT": {
        "BUNDLE_DIR_NAME": "assets/bundles",
        "STATS_FILE": PROJECT_ROOT + "/webpack-stats.json",
    }
}
RESULT_BROWSER_FACETS = [
    "plugin",
    "project",
    "product",
    "institute",
    "model",
    "experiment",
    "time_frequency",
    "variable",
]
MENU_ENTRIES = []
_MENU_ENTRIES = [
    ["Plugins", "plugins:home", "plugin_menu"],
    ["Data-Browser", "solr:data_browser", "browser_menu"],
    ["Result-Browser", "history:result_browser", "result_browser_menu"],
    ["History", "history:history", "history_menu"],
]

for title, url, html_id in web_config.get("MENU_ENTRIES", _MENU_ENTRIES):
    MENU_ENTRIES.append({"name": title, "url": reverse_lazy(url), "html_id": html_id})
