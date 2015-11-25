# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from charms.reactive import RelationBase
from charms.reactive import hook
from charms.reactive import scopes


class HadoopPluginProvides(RelationBase):
    scope = scopes.GLOBAL

    def yarn_ready(self):
        return self.get_remote('yarn-ready', 'false').lower() == 'true'

    def hdfs_ready(self):
        return self.get_remote('hdfs-ready', 'false').lower() == 'true'

    @hook('{provides:hadoop-plugin}-relation-joined')
    def joined(self):
        conv = self.conversation()
        conv.set_state('{relation_name}.connected')

    @hook('{provides:hadoop-plugin}-relation-changed')
    def changed(self):
        if self.yarn_ready():
            self.set_state('{relation_name}.yarn.ready')
        if self.hdfs_ready():
            self.set_state('{relation_name}.hdfs.ready')
        if self.yarn_ready() and self.hdfs_ready():
            self.set_state('{relation_name}.ready')

    @hook('{provides:hadoop-plugin}-relation-departed')
    def departed(self):
        conv = self.conversation()
        conv.remove_state('{relation_name}.connected')
        conv.remove_state('{relation_name}.ready')
        conv.remove_state('{relation_name}.yarn.ready')
        conv.remove_state('{relation_name}.hdfs.ready')
