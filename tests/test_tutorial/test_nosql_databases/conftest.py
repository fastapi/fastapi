# Mock cassandra module to avoid Python 3.14+ import issues
# (asyncore removed in 3.12, cassandra-driver needs event loop)
import sys
from types import ModuleType
from unittest.mock import MagicMock

mock_cassandra = ModuleType('cassandra')
mock_cassandra_cluster = ModuleType('cassandra.cluster')
mock_cassandra_cluster.Cluster = MagicMock

# Set cluster attribute on cassandra module
mock_cassandra.cluster = mock_cassandra_cluster

sys.modules['cassandra'] = mock_cassandra
sys.modules['cassandra.cluster'] = mock_cassandra_cluster
