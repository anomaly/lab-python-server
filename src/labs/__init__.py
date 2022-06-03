"""Python project template for Anomaly
"""

__title__ = "Labs"
__version__ = "0.1.0"

from fluent import sender

from .config import config

# Configures a Fluentd sender that should be made available
# in the Docker-compose or K8s constructed environment.
logger = sender.FluentSender(__title__, 
    host=config.FLUENTD_HOST, 
    port=config.FLUENTD_PORT)

