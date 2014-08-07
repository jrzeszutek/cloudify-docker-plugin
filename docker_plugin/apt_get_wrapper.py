# coding=utf-8
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.


import docker_plugin.subprocess_wrapper as subprocess_wrapper

from cloudify import exceptions


_DOCKER_INSTALLATION_CMD = ['install_docker.sh']
_MAX_WAITING_TIME = 10
_TIMEOUT_TERMINATE = 5


def install_docker(ctx):
    return_code, stdout, stderr = subprocess_wrapper.run_process(
        ctx,
        _DOCKER_INSTALLATION_CMD,
        waiting_for_output=_MAX_WAITING_TIME,
        timeout_terminate=_TIMEOUT_TERMINATE,
    )
    if stdout != '':
        ctx.logger.debug(
            'Docker installation\'s stdout:\n{}\n'.format(stdout)
        )
    if return_code != 0:
        if stderr != '':
            ctx.logger.error(
                'Docker installation\'s stderr:\n{}\n'.format(stderr)
            )
        raise exceptions.NonRecoverableError(
            'Error during docker installation'
        )
