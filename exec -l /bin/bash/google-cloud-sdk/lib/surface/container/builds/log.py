# Copyright 2016 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Stream-logs command."""


from googlecloudsdk.api_lib.cloudbuild import logs as cb_logs
from googlecloudsdk.calliope import base
from googlecloudsdk.core import apis as core_apis


@base.ReleaseTracks(base.ReleaseTrack.BETA)
class Log(base.Command):
  """Stream the logs for a build."""

  @staticmethod
  def Args(parser):
    """Register flags for this command.

    Args:
      parser: An argparse.ArgumentParser-like object. It is mocked out in order
          to capture some information, but behaves like an ArgumentParser.
    """
    parser.add_argument(
        'build',
        help=('The build whose logs shall be printed. The ID of the build is '
              'printed at the end of the build submission process, or in the '
              'ID column when listing builds.'),
    )
    parser.add_argument(
        '--stream',
        help=('If a build is ongoing, stream the logs to stdout until '
              'termination.'),
        action='store_true')

  def Run(self, args):
    """This is what gets called when the user runs this command.

    Args:
      args: an argparse namespace. All the arguments that were provided to this
        command invocation.

    Returns:
      Some value that we want to have printed later.
    """

    client = core_apis.GetClientInstance('cloudbuild', 'v1')
    messages = core_apis.GetMessagesModule('cloudbuild', 'v1')
    registry = self.context['registry']

    build_ref = registry.Parse(
        args.build, collection='cloudbuild.projects.builds')

    logger = cb_logs.CloudBuildClient(client, messages)
    if args.stream:
      logger.Stream(build_ref)
      return

    # Just print out what's available now.
    logger.PrintLog(build_ref)
